from datetime import datetime
from http import HTTPStatus
from io import BytesIO
from os import makedirs
from os.path import exists, join, splitext
from typing import Any, Dict, List, Optional, Tuple, Union

from flask import Blueprint, current_app, g, jsonify
from flask import make_response as make_flask_response
from flask import request
from flask.wrappers import Request, Response
from pandas import DataFrame, read_csv, to_datetime
from werkzeug.utils import secure_filename

import pollux.auth as pauth
import pollux.visualisations as vis
from pollux.cneg import make_plain_dict, make_plotly_dict
from pollux.datasource import DataSource

MAIN = Blueprint("", __name__)

TFlaskResponse = Union[Response, Tuple[Response, HTTPStatus]]

#: The media-type used for plotly output
PLOTLY_MT = "application/prs.plotlydict+json"


def make_response(
    df: DataFrame, genera: List[str], request: Request
) -> Response:
    accept = request.accept_mimetypes.best_match([PLOTLY_MT])
    if accept == PLOTLY_MT:
        data = make_plotly_dict(df, genera)
        content_type = PLOTLY_MT
    else:
        data = make_plain_dict(df)
        content_type = "application/json"
    auth_header = request.headers.get("Authorization", "")
    response = jsonify(
        pauth.with_refreshed_token(
            auth_header, current_app.config["JWT_SECRET"], data
        )
    )
    response.content_type = content_type
    return response


def allowed_file(filename: str) -> bool:
    _, ext = splitext(filename)
    return ext.lower() in {".csv"}


@MAIN.before_app_request
def globals() -> None:
    ds = getattr(g, "data_source", None)
    if not ds:
        ds = DataSource.default()
        g.data_source = ds


@MAIN.before_app_request
def authentication() -> Optional[TFlaskResponse]:
    auth_header = request.headers.get("Authorization", "")
    method, _, token = auth_header.partition(" ")
    g.auth_info = {}
    if method and method.lower() not in ("jwt", "bearer"):
        return (
            jsonify(
                pauth.with_refreshed_token(
                    auth_header,
                    current_app.config["JWT_SECRET"],
                    {"message": "Unrecognized auth header"},
                )
            ),
            HTTPStatus.UNAUTHORIZED,
        )
    elif method:
        auth_info = pauth.decode_jwt(token, current_app.config["JWT_SECRET"])
        if not auth_info:
            return (
                jsonify(
                    pauth.with_refreshed_token(
                        auth_header,
                        current_app.config["JWT_SECRET"],
                        {"message": "Unable to decode the token"},
                    )
                ),
                HTTPStatus.UNAUTHORIZED,
            )
        g.auth_info = auth_info
    return None


@MAIN.after_app_request
def cors(response: Response) -> Response:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type, Authorization"
    return response


@MAIN.route("/")
def index() -> Response:
    auth_header = request.headers.get("Authorization", "")
    return jsonify(
        pauth.with_refreshed_token(
            auth_header,
            current_app.config["JWT_SECRET"],
            {
                "_links": {
                    "recent": {
                        "href": "/recent",
                        "title": "Fetch data for the last <n> days",
                    }
                }
            },
        )
    )


@MAIN.route("/recent")
def recent() -> Response:
    num_days = int(request.args.get("num_days", 7))
    genera = request.args.getlist("genus")
    df = g.data_source.recent(num_days=num_days, genera=genera)
    return make_response(df, genera, request)


@MAIN.route("/between/<start>/<end>")
def between(start: str, end: str) -> Response:
    startDate = datetime.strptime(start, "%Y-%m-%d")
    endDate = datetime.strptime(end, "%Y-%m-%d")
    genera = request.args.getlist("genus")
    df = g.data_source.between(startDate, endDate, genera=genera)
    return make_response(df, genera, request)


@MAIN.route("/genera")
def genera() -> Response:
    data = g.data_source.genera()
    auth_header = request.headers.get("Authorization", "")
    return jsonify(
        pauth.with_refreshed_token(
            auth_header, current_app.config["JWT_SECRET"], data
        )
    )


@MAIN.route("/heatmap/<genus>")
def heatmap(genus: str) -> Response:
    data = g.data_source.heatmap(genus)
    auth_header = request.headers.get("Authorization", "")
    return jsonify(
        pauth.with_refreshed_token(
            auth_header, current_app.config["JWT_SECRET"], data
        )
    )


@MAIN.route("/upload", methods=["POST"])
def upload() -> TFlaskResponse:
    auth_header = request.headers.get("Authorization", "")
    if not g.auth_info:
        return (
            jsonify(
                pauth.with_refreshed_token(
                    auth_header,
                    current_app.config["JWT_SECRET"],
                    {"message": "Authorization required"},
                )
            ),
            HTTPStatus.UNAUTHORIZED,
        )
    if not auth.Permission.UPLOAD_DATA in g.auth_info["permissions"]:
        return (
            jsonify(
                pauth.with_refreshed_token(
                    auth_header,
                    current_app.config["JWT_SECRET"],
                    {"message": "Access denied"},
                )
            ),
            HTTPStatus.FORBIDDEN,
        )
    dest = current_app.config["UPLOAD_FOLDER"]
    if not exists(dest):
        makedirs(dest)
    if len(request.files) != 1:
        return jsonify(pauth.with_refreshed_token(auth_header, current_app.config["JWT_SECRET"], {"message": "Expecting exactly one file!"})), 400  # type: ignore

    filename, data = list(request.files.items())[0]

    if not allowed_file(filename):
        return jsonify(pauth.with_refreshed_token(auth_header, current_app.config["JWT_SECRET"], {"message": "Unsupported file-extension"})), 400  # type: ignore
    filename = join(dest, secure_filename(filename))  # type: ignore
    data.save(filename)

    return jsonify(
        pauth.with_refreshed_token(
            auth_header, current_app.config["JWT_SECRET"], {"status": "OK"}
        )
    )


@MAIN.route("/auth", methods=["POST"])
def auth() -> TFlaskResponse:
    auth_header = request.headers.get("Authorization", "")
    payload = request.json
    permissions = pauth.auth(
        payload["username"],
        payload["password"],
        current_app.config["AUTH_FILE"],
    )
    if not permissions:
        return (
            jsonify(
                pauth.with_refreshed_token(
                    auth_header,
                    current_app.config["JWT_SECRET"],
                    {"message": "Access Denied"},
                )
            ),
            HTTPStatus.UNAUTHORIZED,
        )

    jwt_body = {
        "username": payload["username"],
        "permissions": [perm.value for perm in permissions],
    }
    token = pauth.encode_jwt(jwt_body, current_app.config["JWT_SECRET"])
    return jsonify(
        pauth.with_refreshed_token(
            auth_header, current_app.config["JWT_SECRET"], {"token": token}
        )
    )


@MAIN.route("/graph/lineplot")
def lineplot():
    df = read_csv("data.csv")
    df["date"] = df["date"].apply(to_datetime)
    df = df.set_index("date")
    fig = vis.lineplot(df)
    output = BytesIO()
    fig.savefig(output, format="png")
    data = output.getvalue()
    response = make_flask_response(data)
    response.content_type = "image/png"
    return response

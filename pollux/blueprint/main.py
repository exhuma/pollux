# type: ignore
from datetime import datetime
from http import HTTPStatus
from os import makedirs
from os.path import exists, join
from typing import List, Optional, Tuple, Union

from flask import Blueprint, current_app, g, jsonify
from flask import make_response as make_flask_response
from flask import request
from flask.wrappers import Request, Response
from pandas import DataFrame
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import pollux.auth as pauth
from pollux.cneg import make_plain_dict, make_plotly_dict
from pollux.datasource import DataSource
from pollux.uploads import allowed_file

MAIN = Blueprint("", __name__)

TFlaskResponse = Union[Response, Tuple[Response, HTTPStatus]]

#: The media-type used for plotly output
PLOTLY_MT = "application/prs.plotlydict+json"


def _store_file(filename: str, object: FileStorage) -> None:
    """
    Store the Flask file-object into the given file-name

    This function exists to aid in unit-testing
    """
    filename = join(dest, secure_filename(filename))  # type: ignore
    file_storage.save(filename)


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


@MAIN.before_app_request
def globals() -> None:
    ds = getattr(g, "data_source", None)
    if not ds:
        ds = DataSource.default()
        g.data_source = ds


@MAIN.before_app_request
def authentication() -> Optional[TFlaskResponse]:
    auth_header = request.headers.get("Authorization", "")
    _, _, token = auth_header.partition(" ")
    g.auth_info = {}
    if not pauth.is_valid_request(
        auth_header, current_app.config["JWT_SECRET"]
    ):
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
        return None

    auth_info = pauth.decode_jwt(token, current_app.config["JWT_SECRET"])
    g.auth_info = auth_info


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

    if not pauth.is_allowed_to_upload(g.auth_info):
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

    filename, file_storage = list(request.files.items())[0]

    if not allowed_file(filename):
        return jsonify(pauth.with_refreshed_token(auth_header, current_app.config["JWT_SECRET"], {"message": "Unsupported file-extension"})), 400  # type: ignore

    _store_file(filename, file_storage)

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
    image_data, image_type = g.data_source.lineplot()
    response = make_flask_response(image_data)
    response.content_type = image_type
    return response

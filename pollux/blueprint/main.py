from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Tuple, Union

import jwt
import pollux.auth as pauth
from flask import Blueprint, current_app, g
from flask import jsonify as jsonify_orig
from flask import request
from flask.wrappers import Response
from pollux.datasource import DataSource

MAIN = Blueprint("", __name__)

TFlaskResponse = Union[
    Response,
    Tuple[Response, HTTPStatus]
]


def jsonify(data: Dict[str, Any]) -> Response:
    auth_header = request.headers.get("Authorization", "")
    _, _, token = auth_header.partition(" ")
    if token:
        refreshed_token = pauth.refresh_token(token, current_app.config["JWT_SECRET"])
        merged_data = {"refreshed_token": refreshed_token, **data}
    else:
        merged_data = data
    output = jsonify_orig(merged_data)
    return output  # type: ignore



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
            jsonify({"message": "Unrecognized auth header"}),
            HTTPStatus.UNAUTHORIZED
        )
    elif method:
        auth_info = pauth.decode_jwt(token, current_app.config["JWT_SECRET"])
        if not auth_info:
            return (
                jsonify({"message": "Unable to decode the token"}),
                HTTPStatus.UNAUTHORIZED
            )
        g.auth_info = auth_info
    return None


@MAIN.after_app_request
def cors(response: Response) -> Response:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@MAIN.route("/")
def index() -> Response:
    return jsonify(
        {
            "_links": {
                "recent": {
                    "href": "/recent",
                    "title": "Fetch data for the last <n> days",
                }
            }
        }
    )


@MAIN.route("/recent")
def recent() -> Response:
    num_days = int(request.args.get("num_days", 7))
    genera = request.args.getlist("genus")
    data = g.data_source.recent(num_days=num_days, genera=genera)
    return jsonify(data)


@MAIN.route("/between/<start>/<end>")
def between(start: str, end: str) -> Response:
    startDate = datetime.strptime(start, "%Y-%m-%d")
    endDate = datetime.strptime(end, "%Y-%m-%d")
    genera = request.args.getlist("genus")
    data = g.data_source.between(startDate, endDate, genera=genera)
    return jsonify(data)


@MAIN.route("/genera")
def genera() -> Response:
    data = g.data_source.genera()
    return jsonify(data)


@MAIN.route("/heatmap/<genus>")
def heatmap(genus: str) -> Response:
    data = g.data_source.heatmap(genus)
    return jsonify(data)


@MAIN.route("/upload")
def upload() -> TFlaskResponse:
    if not g.auth_info:
        return jsonify({"message": "Authorization required"}), HTTPStatus.UNAUTHORIZED
    return jsonify({"status": "OK"})


@MAIN.route("/auth", methods=["POST"])
def auth() -> TFlaskResponse:
    payload = request.json
    permissions = pauth.auth(
        payload["username"],
        payload["password"],
        current_app.config["AUTH_FILE"],
    )
    if not permissions:
        return jsonify({"message": "Access Denied"}), HTTPStatus.UNAUTHORIZED

    jwt_body = {
        "username": payload["username"],
        "permissions": [perm.value for perm in permissions],
    }
    token = pauth.encode_jwt(jwt_body, current_app.config["JWT_SECRET"])
    return jsonify({"token": token})

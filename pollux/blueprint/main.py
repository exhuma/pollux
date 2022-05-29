# type: ignore
from datetime import datetime
from http import HTTPStatus
from os import makedirs
from os.path import exists, join
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Header, Query, Response, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from pandas import DataFrame

import pollux.auth as pauth
from pollux.cneg import best_accept_match, make_plain_dict, make_plotly_dict
from pollux.datasource import DataSource
from pollux.dependencies import get_data_source, get_settings
from pollux.model import Credentials
from pollux.settings import Settings
from pollux.uploads import allowed_file

#: The media-type used for plotly output
PLOTLY_MT = "application/prs.plotlydict+json"
ROUTER = APIRouter()


def _store_file(filename: str, object: Any) -> None:
    """
    Store the Flask file-object into the given file-name

    This function exists to aid in unit-testing
    """
    filename = join(dest, secure_filename(filename))  # type: ignore
    file_storage.save(filename)


def make_response(
    df: DataFrame,
    genera: List[str],
    jwt_secret: str,
    accept_mimetype: str,
    authorization: str,
) -> Any:
    """
    Create a valid HTTP response from a Pandas Dataframe
    """
    accept = best_accept_match(accept_mimetype, ["application/json", PLOTLY_MT])
    if accept == PLOTLY_MT:
        data = make_plotly_dict(df, genera)
    else:
        data = make_plain_dict(df)
    response = JSONResponse(
        content=pauth.with_refreshed_token(authorization, jwt_secret, data),
        headers={"content_type": accept},
    )
    return response


@ROUTER.get("/")
async def index() -> Dict[str, Any]:
    """
    Main index
    """
    return RedirectResponse("/docs")


@ROUTER.get("/recent")
async def recent(
    num_days: int = Query(default=7),
    genus: Optional[List[str]] = Query(default=None),
    data_source: DataSource = Depends(get_data_source),
    settings: Settings = Depends(get_settings),
    authorization: str = Header(default=""),
    accept: str = Header(),
) -> Any:
    genus = genus or []
    dataframe = data_source.recent(num_days=num_days, genera=genus)
    return make_response(
        dataframe, genus, settings.jwt_secret, accept, authorization
    )


@ROUTER.get("/between/{start}/{end}")
async def between(
    start: str,
    end: str,
    genus: Optional[List[str]] = Query(default=None),
    authorization: str = Header(default=""),
    data_source: DataSource = Depends(get_data_source),
    settings: Settings = Depends(get_settings),
    accept: str = Header(),
) -> Any:
    """
    Return daily concentrations of pollen between two dates
    """
    genus = genus or []
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    dataframe = data_source.between(start_date, end_date, genera=genus)
    return make_response(
        dataframe, genus, settings.jwt_secret, accept, authorization
    )


@ROUTER.get("/genera")
async def genera(
    authorization: str = Header(default=""),
    data_source: DataSource = Depends(get_data_source),
    settings: Settings = Depends(get_settings),
) -> Any:
    """
    Return all available "genera" (type) of pollen.
    """
    data = data_source.genera()
    return pauth.with_refreshed_token(authorization, settings.jwt_secret, data)


@ROUTER.get("/heatmap/{genus}")
async def heatmap(
    genus: str,
    data_source: DataSource = Depends(get_data_source),
    authorization: str = Header(default=""),
    settings: Settings = Depends(get_settings),
) -> Any:
    """
    Return a heatmap of historical values of a specific pollen genus
    """
    data = data_source.heatmap(genus)
    return pauth.with_refreshed_token(authorization, settings.jwt_secret, data)


@ROUTER.post("/upload")
async def upload(
    file: UploadFile,
    authorization: str = Header(default=""),
    settings: Settings = Depends(get_settings),
) -> Any:
    auth_info = pauth.create_auth_info(authorization, settings.jwt_secret)
    if not pauth.is_allowed_to_upload(auth_info):
        return JSONResponse(
            content=pauth.with_refreshed_token(
                authorization,
                settings.jwt_secret,
                {"message": "Access denied"},
            ),
            status_code=HTTPStatus.FORBIDDEN,
        )
    dest = settings.upload_folder
    if not exists(dest):
        makedirs(dest)

    if not allowed_file(file.filename):
        return JSONResponse(
            content=pauth.with_refreshed_token(
                authorization,
                settings.jwt_secret,
                {"message": "Unsupported file-extension"},
            ),
            status_code=400,
        )

    _store_file(filename, file_storage)

    return jsonify(
        pauth.with_refreshed_token(
            authorization, current_app.config["JWT_SECRET"], {"status": "OK"}
        )
    )


@ROUTER.post("/auth")
async def auth(
    credentials: Credentials,
    authorization=Header(default=""),
    settings=Depends(get_settings),
) -> Any:
    """
    Login to the application
    """
    permissions = pauth.auth(
        credentials.username,
        credentials.password,
        settings.auth_file,
    )
    if not permissions:
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content=pauth.with_refreshed_token(
                authorization,
                settings.jwt_secret,
                {"message": "Access Denied"},
            ),
        )

    jwt_body = {
        "username": credentials.username,
        "permissions": [perm.value for perm in permissions],
    }
    token = pauth.encode_jwt(jwt_body, settings.jwt_secret)
    return pauth.with_refreshed_token(
        authorization, settings.jwt_secret, {"token": token}
    )


@ROUTER.get("/graph/lineplot/{genus}")
async def lineplot(
    genus: str,
    data_source: DataSource = Depends(get_data_source),
):
    image_data, image_type = data_source.lineplot(genus)
    response = Response(content=image_data, media_type=image_type)
    return response

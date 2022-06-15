from http import HTTPStatus

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.types import Receive, Scope, Send

import pollux.auth as pauth
from pollux.blueprint.main import ROUTER
from pollux.dependencies import get_settings
from pollux.settings import Settings

origins = ["*"]


def check_auth(
    authorization: str = Header(default=""),
    settings: Settings = Depends(get_settings),
):
    """
    Check if the request has a valid JWT token, if not raise a 401 error.
    """
    if not pauth.is_valid_request(authorization, settings.jwt_secret):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Unable to decode the token",
        )


def make_app() -> FastAPI:
    """
    Create an application object
    """
    app = FastAPI(dependencies=[Depends(check_auth)])
    app.include_router(ROUTER)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["Content-Type", "Authorization"],
    )
    return app

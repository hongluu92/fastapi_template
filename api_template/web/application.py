from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles

from api_template.logging import configure_logging
from api_template.web.api.router import api_router
from api_template.web.lifetime import register_shutdown_event, register_startup_event
from api_template.errors.http_res_err import HttpResException 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from uuid import uuid4

from starlette.types import ASGIApp, Receive, Scope, Send

from api_template.db.session import set_session_context, reset_session_context, session


class SQLAlchemyMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
        finally:
            await session.remove()
            reset_session_context(context=context)


class UnicornException(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
APP_ROOT = Path(__file__).parent.parent

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="api_template",
        version=metadata.version("api_template"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        debug=True
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        SQLAlchemyMiddleware 
    )

    # Adds startup and shutdown events.
    #register_startup_event(app)
    #register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=418,
            content={"message":  "{}".format(exc.__class__.__name__)},
        )
    @app.exception_handler(HttpResException)
    async def exception_handler(request: Request, exc: HttpResException):
        return JSONResponse(
            status_code=400,
            content={
                "msg":  exc.msg, 
                "msg_code": exc.code,
                "detail": "{}".format(repr(exc))
            },
        )

    return app

import uvicorn

from api_template.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "api_template.web.application:get_app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        debug=True
    )


if __name__ == "__main__":
    main()

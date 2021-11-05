from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from stream2fa.api.errors.http_error import http_error_handler
from stream2fa.api.errors.validation_error import validation_error_handler
from stream2fa.api.router import router

def get_application() -> FastAPI:
    application = FastAPI(debug=True, title="stream2fa", version="0.0.1")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, validation_error_handler)

    application.include_router(router, prefix="")
    
    application.mount("/static", StaticFiles(directory="static"), name="static")

    return application


app = get_application()

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from typing import Union


async def http422_error_handler(request: Request,
                exc: Union[RequestValidationError, ValidationError]) -> JSONResponse:
    
    return JSONResponse(
        {"errors": exc.errors(),
         "request_headers": request.headers},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )
    
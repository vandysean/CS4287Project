from fastapi import APIRouter

from stream2fa.api.routes import test_routes

router = APIRouter()

router.include_router(test_routes.router, tags=["test"], prefix="/test")

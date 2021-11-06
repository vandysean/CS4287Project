from fastapi import APIRouter

from stream2fa.api.routes import (
    base,
    test_routes,
    authorization,
    registration,
    downloads
)

router = APIRouter()

router.include_router(base.router, tags=["base"], prefix="")
router.include_router(test_routes.router, tags=["test"], prefix="/test")
router.include_router(authorization.router, tags=["auth"], prefix="/auth")
router.include_router(registration.router, tags=["register"], prefix="/register")
router.include_router(downloads.router, tags=["download"], prefix="/download")

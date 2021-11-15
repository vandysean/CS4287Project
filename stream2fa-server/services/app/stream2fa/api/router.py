from fastapi import APIRouter

from stream2fa.api.routes import (
    base,
    authorization,
    registration,
    downloads,
    redirect,
    deletion
)

router = APIRouter()

router.include_router(base.router, tags=["base"], prefix="")
router.include_router(authorization.router, tags=["auth"], prefix="/auth")
router.include_router(registration.router, tags=["register"], prefix="/register")
router.include_router(downloads.router, tags=["download"], prefix="/download")
router.include_router(redirect.router, tags=["redirect"], prefix="/redirect")
router.include_router(deletion.router, tags=["delete"], prefix="/delete")

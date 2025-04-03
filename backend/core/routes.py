from fastapi import APIRouter
from accounts.routes import router as account_router

router = APIRouter()
router.include_router(account_router, prefix="/user", tags=["User"])

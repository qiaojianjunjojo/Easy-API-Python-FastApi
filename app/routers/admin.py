from fastapi import APIRouter, Depends, HTTPException
from ..util.dependencies import get_query_token, get_token_header

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}


@router.get("/")
async def get_admin_info():
    return {"admin": "qiaojianjun"}

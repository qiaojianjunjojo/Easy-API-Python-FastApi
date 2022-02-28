from fastapi import APIRouter, Form
from typing import Optional
from pydantic import BaseModel

router = APIRouter()


@router.post('/login/')
async def login(username: str = Form(..., min_length=6, max_length=18), password: str = Form(..., min_length=6, max_length=18,regex='^(?=.*[a-zA-Z])(?=.*[0-9])[A-Za-z0-9]{8,18}$')):
    # 校验逻辑 balabala
    return {"username": username, "token": username[::-1]}


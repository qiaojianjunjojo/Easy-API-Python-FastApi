from fastapi import APIRouter, Form, Request, Response, Query
from typing import Optional
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


router = APIRouter()
limiter = Limiter(key_func=get_remote_address,
                  storage_uri="redis://10.189.127.62:40118/0")


@router.get('/limiterdata1/')
@limiter.limit("1/second")
async def get_limiter_data1(request: Request,
                            response: Response,
                            name: str = Query(...)):
    # 校验逻辑 balabala
    return {"username": name}


@router.post('/limiterdata2/')
@limiter.limit("1/day")
async def create_limiter_data2(request: Request,
                               response: Response,
                               username: str = Form(...),
                               password: str = Form(...)):
    # 逻辑 balabala
    return {"msg": "created success!", "username": username}


class Item(BaseModel):
    username: str
    age: int
    address: Optional[str] = None
    phone: Optional[str] = None


@router.put('/limiterdata3/')
@limiter.limit('2/day')
async def update_limiter_data3(request: Request,
                               response: Response,
                               item: Item):
    return item

# Default  limits  5/minute


@router.delete('/limiterdata4/')
async def delete_limiter_data4(request: Request,
                               response: Response,
                               item: Item):
    return item

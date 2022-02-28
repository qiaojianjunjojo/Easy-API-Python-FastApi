from typing import Optional
from fastapi import APIRouter, Path, Body, Cookie, Header
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@router.put('/data1/{item_id}')
async def update_material_data1(*, item_id: int = Path(..., title="the ID of the item to update", ge=0, le=1000),
                                q: Optional[str] = None,
                                item: Optional[Item] = None,
                                ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# 演示多個請求體參數(两个 Pydantic 模型参数),
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     }
# }


@router.put('/data2/{item_id}')
async def update_material_data2(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# cookie参数 声明 Cookie 参数的结构与声明 Query 参数和 Path 参数时相同。第一个值是参数的默认值，同时也可以传递所有验证参数或注释参数，来校验参数：
@router.delete('/data3/')
async def delete_material_data3(ads_id: Optional[str] = Cookie(None), age: Optional[int] = Cookie(None, ge=10, le=100)):
    return {"ads_id": ads_id, "age": age}


# header 参数 声明 header 参数的结构与声明 Query 参数和 Path 参数时相同。第一个值是参数的默认值，同时也可以传递所有验证参数或注释参数，来校验参数：
@router.get('/data4/')
async def get_material_data4(user: Optional[str] = Header(None), app: str = Header(..., regex='^inx.*$')):
    return {"user_agent": user, "app": app}

from fastapi import APIRouter, Query, Path
from typing import Optional
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# 演示 怎么获取post请求数据,数据的校验工作全由Pydantic 来完成，包括数据的自动转换


@router.post('/data1/')
async def create_machine_data1(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# 演示Query 參數字符串校驗


@router.get('/data2/')
async def get_machine_data2(
    name: Optional[str] = Query(None,
                                max_length=50,
                                min_length=3,
                                description="Query string for the items to search in the database that have a good match",
                                title="Query string",
                                )):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if name:
        results.update({"name": name})
    return results

# 演示 路径参数和数值校验


@router.get('/data3/{item_id}')
async def get_machine_data3(item_id: int = Path(...,
                                                title="The ID of the item to get",
                                                ge=1,
                                                le=10),
                            q: Optional[str] = Query(None, alias="item-query"),):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

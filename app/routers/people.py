from fastapi import APIRouter
from typing import Optional
from ..util.errorhandle import InternalException
from enum import Enum

router = APIRouter()


class UserlName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# 演示全局统一异常处理
@router.get('/data1')
async def get_people_data1():
    try:
        a = 1/0
    except Exception as e:
        raise InternalException(
            "500", str(e))
    return {"data": "people data1"}

# 演示使用预设值Enum
@router.get('/data2/{user_name}')
async def get_people_data2(user_name: UserlName):
    if user_name == UserlName.alexnet:
        return {"user_name": user_name, "message": "Deep Learning FTW!"}
    if user_name.value == "lenet":
        return {"user_name": user_name, "message": "LeCNN all the images"}
    return {"user_name": user_name, "message": "Have some residuals"}

# 演示使用"查询字符串"参数:URL 的 ？ 之后，并以 & 符号分隔
# http://127.0.0.1:8000/people/data3/2?age=22&token=jessica
@router.get('/data3/{user_id}')
async def get_people_data3(user_id: str, age: Optional[str] = None):
    if age:
        return {"user_id": user_id, "age": age}
    return {"user_id": user_id}
    

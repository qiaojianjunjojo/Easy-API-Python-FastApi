from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .util.dependencies import get_query_token, get_token_header
from .routers import items, users, people, machine, material, login, fileupload, limiters,admin
from .config.allow_origin import origins
from .util.errorhandle import InternalException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from .util.logger import logger
import time
import uvicorn

app = FastAPI()
# app = FastAPI(dependencies=Depends(get_query_token))

#region app 基础配置部分 一般不需要修改;
# logger 中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.client.host}  |   {request.url}  |  {round(process_time,3)}s  |  {response.status_code}")
    return response

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 自定义异常处理器; 暂时没有办法做到像node express那种 不需要写try catch就能捕获全局异常的功能
# 这里还是需要在可能发生异常的代码中加上 try ... except ... raise InternalException("5","msg")
@app.exception_handler(InternalException)
async def unicorn_exception_handler(request: Request, exc: InternalException):
    return JSONResponse(
        status_code=200,  # http response status 200 OK
        content={
            "code": exc.code,  # 自定义code 0 :正常, 1: get请求失败, 2:post 请求失败
            "message": exc.desc},
    )

# limiter:api 限流器
limiter = Limiter(key_func=get_remote_address, default_limits=[
                  "5/minute"], storage_uri="redis://10.189.127.62:40118/0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

#endregion


app.include_router(login.router,               # 登录注册
                    tags=['login'])            

app.include_router(fileupload.router,          # 文件上传
                    tags=['fileupload'])        

app.include_router(limiters.router,            # limiter使用演示
                   tags=['limiter'],
                   responses={429: {"description": "Too Many Requests!"}})

app.include_router(items.router)

app.include_router(people.router, 
                   prefix='/people',
                   tags=['people'],
                   dependencies=[Depends(get_token_header)],
                   responses={418: {"description": "I'm a teapot"}})

app.include_router(machine.router, prefix='/machine',
                   tags=['machine'],
                   #    dependencies=[Depends(get_token_header)],
                   responses={418: {"description": "I'm a teapot"}})

app.include_router(material.router, prefix='/material',
                   tags=['material'],
                   #    dependencies=[Depends(get_token_header)],
                   responses={418: {"description": "I'm a teapot"}})

# 在同一路由器上使用不同的前缀来多次使用 .include_router()，例如以不同的前缀公开同一个的 API，比方说 /api/v1 和 /api/latest。
# app.include_router(users.router, prefix='/api/v1')
# app.include_router(users.router, prefix='/api/latest')
app.include_router(admin.router,
                   prefix='/admin',
                   tags=['admin'],
                   dependencies=[Depends(get_token_header)],
                   responses={418: {"description": "I'm a teapot"}})


@app.get('/')
@limiter.exempt
def root(request: Request):
    return {"message": "Hello FASTAPI"}

if __name__ == "__main__":
    uvicorn.run(app = 'app.main:app',host='0.0.0.0',port = 8000,reload=True)

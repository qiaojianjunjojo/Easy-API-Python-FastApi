## API 开发框架(python-Fastapi版）

### 简介
Python世界最受欢迎的异步框架FastAPI.  
本demo演示了fastapi常用的一些功能,详情查阅 https://fastapi.tiangolo.com/zh/
  
功能包括：  
跨域  
restful API  
文件上传、下载、删除  
自定义异常处理器  
logger记录  
自动生成Swagger Ui  
中间件开发  
限流服务limiter(https://slowapi.readthedocs.io/en/latest/#slowapi)  
基本的Query,Body,Form,Cookie,Header,参数校验，数据类型自动转换等  

环境需求：
python3.7(python3.6以上支持类型注释皆可)

## Installation

clone:
```
$ git clone  http://fsrserver.cminl.oa/data_team/easy-api-python-fastapi.git
$ cd easy-api-python-fastapi
```
使用python自带的venv模块创建虚拟环境并在虚拟环境中安装项目依耐  
create & activate virtual env then install dependency:

with venv/virtualenv + pip:
```
1.创建虚拟环境 windows: python -m venv env || Python3 on Linux & macOS : python3 -m venv env
2.激活虚拟环境 windosw: env\Scripts\activate.bat || Python3 on Linux & macOS : source env/bin/activate 
3.安装项目依耐 pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

```
本地启动 开启热加载：
```
uvicorn app.main:app --reload

Running on http://127.0.0.1:8000/
```
 如需開啟斷點調試模式(Debug)  
 vscode下选择app/main.py 按F5  
 Pycharm下 


## 容器化 服务器部署
1.使用本目录下的dockerfile  新建 镜像images.
```
docker build -t  qjj/fastapi:1.0  . 
```
2.使用上一步新建的image创建并运行一个container
```
docker run -idt  --name qjj-FASTAPI -p 8001:8000 qjj/fastapi:1.0
```
访问 yourhost:8001 =>{"message": "Hello FASTAPI"}
## 日志 log
日志文件放在logs目录.  
日志记录规则如下:  
1.整个app运行的详细日志(*._log文件) 包括全部的明细信息,文件达到200M后,自动新建,这一类日志永久保存;  
2.路由访问的日志(*._info文件) 包括路由访问的信息(IP : request time),文件每天00:00新建,只保留最近15天;  
3.运行错误日志(*._error文件) app运行报错的信息,文件每天00:00新建,只保留最近15天;  
  
## License

This project is licensed under the MIT License 

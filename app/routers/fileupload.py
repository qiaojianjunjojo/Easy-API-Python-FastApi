import os
from typing import List
from fastapi import APIRouter, File, UploadFile, Form, Query, Body
from fastapi.responses import HTMLResponse, FileResponse


BASE_PATH = os.path.dirname(os.path.abspath(__package__))
dir = os.path.join(BASE_PATH, 'upload')
if not os.path.exists(dir):
    os.makedirs(dir)

router = APIRouter()

# 文件下载 
# ex : http://127.0.0.1:8000/getFile/?sysid=FSWMS&filename=API.xlsx
@router.get("/getFile/")
async def download_file(sysid: str = Query(...), filename: str = Query(...)):
    filepath = os.path.join(BASE_PATH, "upload", sysid,filename)
    if not os.path.exists(filepath):
        return {"issuccess": False, "msg": "file not found!"}
    return FileResponse(filepath)


# 文件删除 
# ex :
@router.delete("/deleteFile/")
async def delete_file(sysid: str = Body(...), filename: str = Body(...)):
    filepath = os.path.join(BASE_PATH, "upload", sysid,filename)
    if not os.path.exists(filepath):
        return {"issuccess": False, "msg": "file not found!"}
    os.remove(filepath)
    return {"issuccess": True}


# 文件上传
@router.post("/postFileBySystem/")
async def upload_files(sysid: str = Body(...), files: List[UploadFile] = File(...)):
    try:
        save_path = os.path.join(BASE_PATH, "upload", sysid)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        for file in files:
            contents = await file.read()
            with open(os.path.join(save_path, file.filename), 'wb') as f:
                f.write(contents)
    except Exception as e:
        # raise InternalException("5","文件上传失败！")
        return {"issuccess": False, "msg": str(e)}
    return {"issuccess": True, "filenames": [(file.filename, file.content_type) for file in files]}

# 获取 系統下 所有的file list
@router.get("/getFileListBySystem")
async def getFileListBySystem(sysid:str = Query(...)):
    path = os.path.join(BASE_PATH,'upload',sysid)
    return {"filelist" :os.listdir(path),"sysid" : sysid}
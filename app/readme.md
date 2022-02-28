1.当我想使用@limiter.exempt 去解除一支route的限制时,我不能使用async method
```python
@app.get('/')
@limiter.exempt
async def root(request: Request):
    return {"message": "2/minute"}
```
他总是报这个错误：
```
ValueError: [TypeError("'coroutine' object is not iterable"), TypeError('vars() argument must have __dict__ attribute')]
```
stackover上关于这个问题的回复：
https://github.com/tiangolo/fastapi/issues/679
  
所以,我将async 拿掉了 then everything goes well

2.有一个 不知道算不算Bug的Bug
```python
路由函数定义如下：
@router.get('/items/{item_id}')
当我试着访问
'http://127.0.0.1:8000/items/gun'  达到limiter 5次以后,我试着访问 'http://127.0.0.1:8000/items/gun2',又可以 访问5次,但我不希望这样.
```

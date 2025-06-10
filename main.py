from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
from auth import AuthHandler
from schemas import UserIn
from models import *

import uvicorn

app = FastAPI()
register_tortoise(
    app=app,
    config=TORTOISE_ORM
)

auth_handler = AuthHandler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/login")
async def login(user: UserIn):
    if not await User.filter(user_id=user.user_id):
        return {
            "status": False,
            "detail": "用户不存在"
        }
    if not await User.filter(password=user.password):
        return {
            "status": False,
            "detail": "账号或密码错误"
        }
    token = auth_handler.encode_token(user.user_id)
    return {
        "status": True,
        "token": token
    }


@app.get("/user")
async def see_user(user_id=Depends(auth_handler.auth_wrapper)):
    if type(user_id) is dict:
        return user_id
    user = await User.get(user_id=user_id).values("name")
    course = await Course.filter(scores1__user_id=user_id).values("name", "scores1__score")
    course = [
        {
            "course_name": item["name"],
            "score": item["scores1__score"]
        }
        for item in course
    ]
    course.insert(0, user)
    return {
        "status": True,
        "data": course
    }


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                reload=False, workers=16, http="httptools")

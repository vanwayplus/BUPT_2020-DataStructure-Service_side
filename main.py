from fastapi import FastAPI, Form, File, UploadFile
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
import models
import json
import re
from huffman import *
import os

app = FastAPI(
    title='Data_Structure Project API Docs',
    description='Data_Structure Project',
    version='1.0.0',
    docs_url='/docs',
)

with open("users.json", "r", encoding='utf-8') as f:
    users = json.load(f)

with open("superusers.json", "r", encoding='utf-8') as f:
    superusers = json.load(f)

with open("courses.json", "r", encoding='utf-8') as f:
    course = json.load(f)


@app.get("/")
async def root():
    return {"message": "Hello World"}


class UserIn(BaseModel):
    username: str
    password: str


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 用户登录
@app.post("/user/login/", response_model=models.User)
async def response_model(user: UserIn):
    print(user.password)
    return users[user.username]


# 获取课程表
@app.get("/user/courses/board/{user}")
async def get_courses(user: str):
    cur_user = users[user]
    cls = cur_user["clas"]
    keys = list(course.keys())
    print(keys)
    matched = []
    qw = "-" + str(cls)
    for k in keys:
        if re.search(qw, k):
            matched.append(k)
    board = []
    for key in matched:
        board.append(course[key])
    return board


# 创建活动
@app.post("/user/activities/create_activities/")
async def create_activities(
        user: str,
        name: str,
        address: str,
        start: str,
        end: str,
        mode: str,
        description: Optional[str] = None
):
    cur = users[user]
    act = models.User.activity(
        name=name,
        mode=mode,
        address=address,
        start=start,
        end=end,
        description=description
    )

    cur_user = models.User.construct(**cur)
    cur_user.activities.append(act)
    n = json.dumps(cur_user, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    n = json.loads(n)
    if n != users[user]:
        users[user] = n
        with open("users.json", "w", encoding='utf-8') as f:
            json.dump(None, f, ensure_ascii=False)
        with open("users.json", "w", encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    return cur_user.activities


# 读取活动
@app.get("/user/activities/get_activities/{user}")
async def get_activities(user: str):
    cur = users[user]
    cur_user = models.User.construct(**cur)
    act = cur_user.activities
    return act


# 上传作业
@app.put("/user/courses/upload_homework")
async def upload_homework(
        file_b: UploadFile = File(...),  # UploadFile转为文件对象，可以保存文件到本地
        user: str = Form(...),
        hm_id: int = Form(...),
        course_id=Form(...),
):
    # contents = await file_b.read()
    # models.Course.homework
    raw = course[course_id]
    cur = models.Course.construct(**raw)
    hm = cur.homework
    version = 0

    for file in hm.files:
        name = file.split('.')
        info = name.split('-')
        if info[-1] and info[0] is user:
            version = version + 1
    # def encode-file(input file, student_id, type, course, id=0, version=0):
    zip_name = encodefile(file_b, user, "homework", course_id, hm.id, version)

    # 更新当前文件属性
    hm.unsubmitted.remove(user)
    hm.submitted.append(user)
    hm.files.append(zip_name)

    cur.homeworks[hm_id] = hm
    n = json.dumps(cur, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    n = json.loads(n)
    course[course_id] = n
    with open("users.json", "w", encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    return ({
        'file_name': zip_name,
        'version': version,
        'homework_id': hm_id,
        'user': user,
        'time': datetime,
    })


# 查询课程作业
@app.post("/user/courses/query_homework")
async def query_homework(
        user: str,
        course_id: str,
        homework_id: Optional[str] = None,
):
    raw = course[course_id]
    cur = models.Course.construct(**raw)
    hm = cur.homework
    hms = []
    for file in hm.files:
        name = file.split('.')
        info = name.split('-')
        if info[0] is user:
            hms.append(
                {
                    "id": info[1],
                    "versions": info[-1],
                    "scores": -1
                }
            )
    return hms


# 上传资源
@app.put("/user/courses/upload_resources")
async def upload_resources(
        file: UploadFile = File(...),  # UploadFile转为文件对象，可以保存文件到本地
        user: str = Form(...),
        sc_id: str = Form(...),
        course_id: str = Form(...),
        description: Optional[str] = Form(0, ...)
):
    raw = course[course_id]
    cur = models.Course.construct(**raw)
    # def encodefile(inputfile, student_id, type, course, id=0, version=0):
    zip_name = encodefile(file, user, "homework", cur.name)
    new_sc = models.Course.resource(
        name=description,
        authors=[user],
        files=[zip_name]
    )
    new_sc.description.append(description)
    new_sc.time = datetime
    cur.resources.append(new_sc)
    n = json.dumps(cur, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    n = json.loads(n)
    # 更新
    course[course_id] = n
    with open("users.json", "w", encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    return ({
        'file_name': zip_name,
        'sc_name': description,
        'sc_id': len(cur.resources),
        'author': user,
        'time': datetime,
    })


# 更新资源
@app.put("/user/courses/update_resources")
async def update_resources(
        file: UploadFile = File(...),  # UploadFile转为文件对象，可以保存文件到本地
        user: str = Form(...),
        sc_id: int = Form(...),  # id
        course_id: str = Form(...),  # name
        description: str = Form(...)  # 描述
):
    raw = course[course_id]
    cur = models.Course.construct(**raw)
    # sc_list = cur.resources
    if sc_id > len(cur.resources):
        return "not exist, please create one"
    zip_name = encodefile(file, user, "homework", cur.name)
    # cur_sc = cur.resources[sc_id]
    cur.resources[sc_id].files.append(zip_name)
    cur.resources[sc_id].description.append(description)
    n = json.dumps(cur, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    n = json.loads(n)
    course[course_id] = n
    with open("users.json", "w", encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    return ({
        'file_name': zip_name,
        'name': cur.resources[sc_id],
        'details': description,
        'author': user,
    })
    pass


# TODO:管理员登录
@app.post("/user/login/", response_model=models.User)
async def response_model(user: UserIn):
    print(user.password)
    return users[user.username]


# TODO:添加课程
@app.put("/superuser/courses/create_courses")
async def create_courses(course: models.Course):
    pass


# TODO: 创建考试信息
@app.put("/superuser/courses/create_exams/{course}")
async def create_exams(exam: models.Course.exam):
    pass


# TODO: 发布作业
@app.put("/superuser/courses/create_homework/{hmwk}")
async def create_exams(exam: models.Course.exam):
    pass


# TODO:修改课程地点
@app.post("/superuser/courses/edit_address/{course}")
async def edit_course_address(addr: str):
    pass


# TODO:修改课程时间
@app.post("/superuser/courses/edit_time/{course}")
async def edit_course_address(start: date, end: date):
    pass

# TODO:下载作业
# TODO: 错误处理

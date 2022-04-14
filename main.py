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
        sc_id: Optional[str] = Form(...),
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


# 添加课程
@app.post("/superuser/courses/create_course")
async def create_courses(
        c_name: str = Form(...),
        c_clas: int = Form(...),
        c_date: list = Form(...),
        c_start: list = Form(...),
        c_end: list = Form(...),
        c_address: str = Form(...),
        c_contact_group: str = Form(...),  # id
):
    new_course = models.Course(
        name=c_name,
        clas=c_clas,
        date=c_date,
        start=c_start,
        end=c_end,
        address=c_address,
        contact_group=c_contact_group
    )
    formatting = json.dumps(new_course, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    formatted = json.loads(formatting)  # 格式化
    new_name_id = c_name + "-" + str(c_clas)
    course[new_name_id] = formatted
    with open("users.json", "w", encoding='utf-8') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)
    return ({
        "course_name": new_name_id,
        "course": formatted
    })


# 创建考试信息
@app.post("/superuser/courses/create_exams")
async def create_exams(
        superuser_id: str = Form(...),
        course_id: str = Form(...),
        exam_name: str = Form(...),
        start_time: str = Form(...),
        end_time: str = Form(...),
        members: list = Form(...),
        address: str = Form(...),
        cr_time: str = Form(...),
        description: Optional[str] = None
):
    new_exam = models.Course.exam(
        name=exam_name,
        start=start_time,
        end=end_time,
        members=members,
        address=address,
        description=description
    )
    new_exam.create_time = cr_time
    raw = course[course_id]
    cur = models.Course.construct(**raw)
    cur.exams.append(new_exam)
    formatting = json.dumps(cur, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    formatted = json.loads(formatting)
    course[course_id] = formatted
    with open("users.json", "w", encoding='utf-8') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)
    return ({
        "exams": formatted
    })


# 发布作业
@app.put("/superuser/courses/create_homework")
async def create_exams(
        name: str = Form(...),
        clas: Optional[list] = Form(...),
        start: str = Form(...),
        end: str = Form(...),
        file: Optional[UploadFile] = Form(...),
        description: str = Form(...),
):
    new_homework = models.Course.homework(
        name=name,
        start=start,
        end=end,
        description=description
    )
    members = []
    for group in clas:
        for _, usr in users:
            cur_user = models.User(**usr)
            if cur_user.clas is group:
                members.append(cur_user.student_id)
    new_homework.unsubmitted = members

    formatting = json.dumps(new_homework, default=lambda obj: obj.__dict__, indent=4, sort_keys=True,
                            ensure_ascii=False)
    formatted = json.loads(formatting)  # 格式化
    with open("users.json", "w", encoding='utf-8') as f:
        json.dump(formatted, f, indent=4, ensure_ascii=False)
    return ({
        "name": name,
        "course": formatted
    })


# 修改课程信息
@app.put("/superuser/courses/edit")
async def edit_course_address(
        course_id: str = Form(...),
        new_clas: Optional[list[int]] = Form(...),
        new_date: Optional[list] = Form(...),
        new_start: Optional[list] = Form(...),
        new_end: Optional[list] = Form(...),
        new_contact_group: Optional[str] = Form(...),  # id
        new_address: Optional[str] = Form(...)
):
    raw = course[course_id]
    cur = models.Course.construct(**raw)
    if new_clas:
        cur.clas = new_clas
    if new_address:
        cur.address = new_address
    if new_date:
        cur.date = new_date
    if new_start:
        cur.start = new_start
    if new_end:
        cur.end = new_end
    if new_contact_group:
        cur.contact_group = new_contact_group

    formatting = json.dumps(cur, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    formatted = json.loads(formatting)

    course[course_id] = formatted

    with open("courses.json", "w", encoding='utf-8') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)

    return ({
        "course": formatted
    })


# TODO:下载作业
@app.get("superuser/courses/download_homework")
async def download_homework(
        user_id: str = Form(...),
        course_id: str = Form(...),
        homework_id: int = Form(...)
):
    pass


# TODO: 批改作业
@app.put("superuser/courses/charge_homework")
async def download_homework(
        user_id: str = Form(...),
        course_id: str = Form(...),
        homework_id: int = Form(...)
):
    pass


# TODO: 下载资源
@app.get("user/courses/download_resource")
async def download_resource(
        course_id: str = Form(...),
        sc_id: int = Form(...)
):
    pass

# TODO: 错误处理

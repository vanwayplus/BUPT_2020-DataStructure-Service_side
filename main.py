from fastapi import FastAPI, Form, File, UploadFile
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

from starlette.background import BackgroundTask
import os
import hashlib
import models
import json
import re
from huffman import *
import os
from starlette.responses import FileResponse
from guide import *
from md_hash import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Data_Structure Project API Docs',
    description='Data_Structure Project',
    version='1.0.0',
    docs_url='/docs',
)

origins = ["*"]

# 3、配置 CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=False,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)

Pool = []


def logging(user, func, time, destination=None):
    new_log = {time: user + func + destination}
    with open("log.json", "a", encoding='utf-8') as f:
        json.dump(new_log, f, indent=4, ensure_ascii=False)


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
@app.get("/user/login/{user}")
async def response_model(user: str, pswd: str):
    if "2020211100" <= user <= "2020211110":
        if user == pswd:
            return "fine"
        else:
            return "password incorrect!"
    else:
        return "illegal username"


# 获取总日程
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


# 获取日程
@app.get("/user/schedule/{user}")
async def get_schedule(user: str, date_d: int):
    cur_user = users[user]
    cls = cur_user["clas"]
    keys = list(course.keys())

    schedule = []
    matched = []
    qw = "-" + str(cls)
    for k in keys:
        if re.search(qw, k):
            matched.append(k)
    board = []
    for key in matched:
        course_i = course[key]
        starts = course_i["start"]
        ends = course_i["end"]
        dates = course_i["date"]
        for i in range(len(starts)):
            name = course_i["name"]
            date = dates[i]
            start, st = transfer_course_time(starts[i])
            st, end = transfer_course_time(ends[i])
            for i in range(len(dates)):
                if dates[i] == date_d:
                    a = {"name": name,
                         "mode": "课程",
                         "start": start,
                         "end": end}
                    schedule.append(a)

    acts = cur_user["activities"]
    for i in range(len(acts)):
        act = acts[i]
        name = act["name"]
        date = int(act["date"])
        if date == date_d:
            start = act["start"].split(" ")[1]
            start = float(start.split(":")[0] + "." + start.split(":")[1])
            end = act["end"].split(" ")[1]
            end = float(end.split(":")[0] + "." + end.split(":")[1])
            a = {"name": name,
                 "mode": "活动",
                 "start": start,
                 "end": end}
            schedule.append(a)

    sorted_schedules = sorted(schedule, key=lambda r: r['start'])
    return sorted_schedules


# 获取课程表表格
@app.get("/user/courses/table/{user}")
async def get_table(user: str):
    cur_user = users[user]
    cls = cur_user["clas"]
    keys = list(course.keys())
    matched = []
    qw = "-" + str(cls)
    for k in keys:
        if re.search(qw, k):
            matched.append(k)
    board = []
    line_1 = {"name": "一"}
    line_2 = {"name": "二"}
    line_3 = {"name": "三"}
    line_4 = {"name": "四"}
    line_5 = {"name": "五"}
    line_6 = {"name": "六"}
    line_7 = {"name": "七"}
    line_8 = {"name": "八"}
    line_9 = {"name": "九"}
    line_10 = {"name": "十"}
    line_11 = {"name": "十一"}
    line_12 = {"name": "十二"}
    line_13 = {"name": "十三"}
    line_14 = {"name": "十四"}
    board.append(line_1)
    board.append(line_2)
    board.append(line_3)
    board.append(line_4)
    board.append(line_5)
    board.append(line_6)
    board.append(line_7)
    board.append(line_8)
    board.append(line_9)
    board.append(line_10)
    board.append(line_11)
    board.append(line_13)
    board.append(line_14)
    for key in matched:
        course_i = course[key]
        starts = course_i["start"]
        ends = course_i["end"]
        dates = course_i["date"]
        for i in range(len(starts)):
            name = course_i["name"]
            date = dates[i]
            n_d = ["mon", "tue", "wed", "thu", "fri"]
            date = n_d[date - 1]
            start = starts[i]
            end = ends[i]
            for time in range(start, end):
                board[time - 1][date] = name
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
        date: str,
        calendar: str,
        description: Optional[str] = None
):
    start_c = float(start.split(":")[0]+"."+ start.split(":")[1])
    end_c = float(end.split(":")[0] + "." + end.split(":")[1])
    if conflict_detection(user, date_d=date, start=start_c, end=end_c):
        cur = users[user]
        start = calendar + start
        end = calendar + end
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
    else:
        return "conflict!"


# 读取活动
@app.get("/user/activities/get_activities/{user}")
async def get_activities(user: str):
    cur = users[user]
    cur_user = models.User.construct(**cur)
    act = cur_user.activities
    return act


# 上传作业
@app.post("/user/courses/upload_homework")
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
    hm = cur.homeworks[hm_id]
    hm = models.Course.homework.construct(**hm)
    version = 0
    contents = await file_b.read()

    fname = "temp/" + file_b.filename

    with open(fname, "wb") as f:
        f.write(contents)

    for file in hm.files:
        for file_name in file:
            name = file_name.split('.')
            info = name[0].split('-')
            if info[0] is user:
                version = version + 1
    # def encode-file(input file, student_id, type, course, id=0, version=0):
    zip_name = encodefile(fname, user, "homework", course_id, hm.id, version)

    # 更新当前文件属性
    if user in hm.unsubmitted:
        hm.unsubmitted.remove(user)
        hm.submitted.append(user)
        hm.files.append(zip_name)

    cur.homeworks[hm_id] = hm
    md5 = generate_file_md5value(fname)
    if md5 in Pool:
        chongfu = 1
    else:
        chongfu = 0
        Pool.append(md5)
    n = json.dumps(cur, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    n = json.loads(n)

    course[course_id] = n

    with open("courses.json", "w", encoding='utf-8') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)
    return ({
        'file_name': zip_name,
        'version': version,
        'homework_id': hm_id,
        'user': user,
        'chongfu': chongfu
    })


# 查询课程作业
@app.post("/user/courses/query_homework")
async def query_homework(
        user: str,
        course_id: str,
        homework_id: str = None
):
    raw = course[course_id]
    cur = models.Course.construct(**raw)
    hm = cur.homeworks[homework_id]
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
        description: Optional[str] = Form(...)
):
    raw = course[course_id]
    cur = models.Course.construct(**raw)
    # def encodefile(inputfile, student_id, type, course, id=0, version=0):

    contents = await file.read()

    fname = "temp/" + file.filename
    with open(fname, "wb") as f:
        f.write(contents)

    zip_name = encodefile(fname, user, "source", course_id)
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
    mf5 = generate_file_md5value(fname)
    if md5 in Pool:
        chongfu = 1
    else:
        chongfu = 0
        Pool.append(md5)
    with open("courses.json", "w", encoding='utf-8') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)
    return ({
        'sc_name': description,
        'sc_id': len(cur.resources),
        'author': user,
        'chongfu': chongfu
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

    contents = await file.read()

    fname = "temp/" + file.filename
    with open(fname, "wb") as f:
        f.write(contents)

    zip_name = encodefile(file, user, "source", course_id)
    # cur_sc = cur.resources[sc_id]
    cur.resources[sc_id].files.append(zip_name)
    cur.resources[sc_id].description.append(description)

    n = json.dumps(cur, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    n = json.loads(n)
    course[course_id] = n

    with open("courses.json", "w", encoding='utf-8') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)
    return ({
        'name': cur.resources[sc_id],
        'details': description,
        'author': user,
    })


# 管理员登录
@app.post("/superuser/login/", response_model=models.User)
async def response_model(user: UserIn):
    print(user.password)
    return users[user.username]


# 添加课程
@app.post("/superuser/courses/create_course")  # fine
async def create_courses(
        c_name: str = Form(...),
        c_clas: int = Form(...),
        c_date: list = Form(...),
        c_start: list = Form(...),
        c_end: list = Form(...),
        c_address: str = Form(...),
        c_contact_group: str = Form(...),  # id
        c_teacher: str = Form(...)
):
    new_course = models.Course(
        name=c_name,
        clas=c_clas,
        date=c_date,
        teacher=c_teacher,
        start=c_start,
        end=c_end,
        address=c_address,
        contact_group=c_contact_group
    )
    formatting = json.dumps(new_course, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    formatted = json.loads(formatting)  # 格式化
    new_name_id = c_name + "-" + str(c_clas)
    course.update(new_name_id=formatted)
    with open("courses.json", "w", encoding='utf-8') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)
    return ({
        "course_name": new_name_id,
        "course": formatted
    })


# 创建考试信息
@app.post("/superuser/courses/create_exams")
async def create_exams(
        # superuser_id: str = Form(...),
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
    with open("courses.json", "w", encoding='utf-8') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)
    return ({
        "course": course[course_id]
    })


# 发布作业
@app.post("/superuser/courses/create_homework")
async def create_exams(
        course_id: str = Form(...),
        name: str = Form(...),
        clas: Optional[list] = Form(...),
        start: str = Form(...),
        end: str = Form(...),
        # file: Optional[UploadFile] = Form(...),
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
        for usr in users.values():
            cur_user = models.User(**usr)
            if cur_user.clas == int(group):
                members.append(cur_user.student_id)
    new_homework.unsubmitted = members

    raw = course[course_id]
    cur = models.Course.construct(**raw)
    cur.homeworks.append(new_homework)

    formatting = json.dumps(cur, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    formatted = json.loads(formatting)
    course[course_id] = formatted

    with open("courses.json", "w", encoding='utf-8') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)

    return ({
        "name": name,
        "course": formatted
    })


# 修改课程信息
@app.post("/superuser/courses/edit")
async def edit_course_address(
        course_id: str = Form(...),
        new_clas: list = None,
        new_date: list = None,
        new_start: list = None,
        new_end: list = None,
        new_contact_group: str = None,  # id
        new_address: str = None
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


@app.get("/map/guide")
async def guide(
        start: str = Form(...),
        end: str = Form(...),
        mode: str = Form(...)
):
    print(start, end, mode)
    activate_dij(start, end, mode)
    path = []
    distance, path = read_meta_file()
    if path:
        return ({
            "state": True,
            "distance": distance,
            "path": path
        })
    else:
        return ({
            "state": False,
            "distance": distance,
            "path": path
        })


#  下载资源
@app.get("/user/courses/download_resource")
async def download_resource(
        course_id: str = Form(...),
        sc_id: int = Form(...),
        version: int = Form(...)
):
    raw = course[course_id]
    cur = models.Course.construct(**raw)
    sc = cur.resources[sc_id]
    zip_name = sc.files[version]
    zip_path = "/files/" + course_id + "/source/" + zip_name + ".ys"
    temp_file_path = decodefile(zip_path)
    # 后台删除临时文件
    task = BackgroundTask(os.remove, path=temp_file_path)
    return FileResponse(
        path=temp_file_path,
        filename=temp_file_path,
        background=task
    )


# TODO:冲突
#1为没有，0为有
def conflict_detection(user_id, date_d, start, end):
    cur_user = users[user_id]
    cls = cur_user["clas"]
    keys = list(course.keys())

    schedule = []
    matched = []
    qw = "-" + str(cls)
    for k in keys:
        if re.search(qw, k):
            matched.append(k)
    board = []
    for key in matched:
        course_i = course[key]
        starts = course_i["start"]
        ends = course_i["end"]
        dates = course_i["date"]
        for i in range(len(starts)):
            name = course_i["name"]
            date = str(dates[i])
            start, st = transfer_course_time(starts[i])
            st, end = transfer_course_time(ends[i])
            for i in range(len(dates)):
                if dates[i] == date_d:
                    a = {"name": name,
                         "mode": "课程",
                         "start": start,
                         "end": end}
                    schedule.append(a)

    acts = cur_user["activities"]
    for i in range(len(acts)):
        act = acts[i]
        name = act["name"]
        date = str(act["date"])
        if date == date_d:
            start = act["start"].split(" ")[1]
            start = float(start.split(":")[0] + "." + start.split(":")[1])
            end = act["end"].split(" ")[1]
            end = float(end.split(":")[0] + "." + end.split(":")[1])
            a = {"name": name,
                 "mode": "活动",
                 "start": start,
                 "end": end}
            schedule.append(a)

    sorted_schedules = sorted(schedule, key=lambda r: r['start'])
    flag = 0

    for schedule in sorted_schedules:
        start_c = schedule["start"]
        end_c = schedule["end"]
        if start_c <= start <= end_c or start_c <= end <= end_c or start <= start_c and end >= end_c:
            flag = 1
    if flag == 0:
        return 1  # 无冲突
    else:
        return 0  # 有冲突


# TODO:闹钟
@app.post("/user/set_alarm")
async def set_alarm(
        user_id: str = Form(...),
        date: str = Form(...),
        time: str = Form(...)
):
    raw = users[user_id]
    cur = models.User.construct(**raw)
    cur.clocks.append((date, time))

    formatting = json.dumps(cur, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
    formatted = json.loads(formatting)

    users[user_id] = formatted

    with open("users.json", "w", encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

    return ({
        "clock": (date, time)
    })


"""@app.put("/user/set_alarm")
async def download_homework(
        user_id: str = Form(...),
        time: str = Form(...),
):

    pass"""


# TODO: 批改作业
@app.put("/superuser/courses/charge_homework")
async def download_homework(
        user_id: str = Form(...),
        course_id: str = Form(...),
        homework_id: int = Form(...)
):
    pass


def transfer_course_time(n):
    if n == 1:
        return (8.00, 8.45)
    elif n == 2:
        return 8.50, 9.35
    elif n == 3:
        return 9.50, 10.35
    elif n == 4:
        return 10.40, 11.25
    elif n == 5:
        return 11.30, 12.15
    elif n == 6:
        return 13.00, 13.45
    elif n == 7:
        return 13.50, 14.35
    elif n == 8:
        return 14.45, 15.30
    elif n == 9:
        return 15.40, 16.25
    elif n == 10:
        return 16.35, 17.20
    elif n == 11:
        return 17.25, 18.10
    elif n == 12:
        return 18.30, 19.15
    elif n == 13:
        return 19.20, 20.05
    elif n == 14:
        return 20.10, 20.55

# TODO: 日志处理


# TODO: 错误处理

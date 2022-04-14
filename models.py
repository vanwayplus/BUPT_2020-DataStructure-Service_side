from datetime import datetime, date
# from pathlib import Path
from typing import List
from typing import Optional

from pydantic import BaseModel


# from pydantic import constr


class User(BaseModel):
    class activity(BaseModel):
        name: str
        address: str
        start: str
        end: str
        mode: str
        description: Optional[str] = None
    clas: int
    student_id: str
    password: str
    name: str
    courses: Optional[list] = []
    activities: Optional[list] = []
    sign_up: Optional[datetime]



class Superuser(BaseModel):
    id: str
    name: str
    password: str


class Course(BaseModel):
    class exam(BaseModel):
        id: int
        name: str
        start: datetime
        end: datetime
        members: list
        address: str
        description: Optional[str] = None

    class homework(BaseModel):
        id: int
        name: str
        submitted: Optional[list] = []
        files: Optional[list] = []
        folder: Optional[str] = None
        unsubmitted: Optional[list] = []
        start: datetime
        ddl: datetime
        source: Optional[list] = None
        description: str
        name_rule: Optional[str] = None

    class resource(BaseModel):
        id: int
        name: str
        author: Optional[str] = None
        files: list[str]
        time: Optional[datetime]

    name: str
    clas: int
    teacher: str
    date: List[int] = []
    start: List[int] = []
    end: List[int] = []
    contact_group: str
    resources: Optional[list] = []
    exams: Optional[List[exam]] = []
    homeworks: Optional[List[homework]] = []
    create_time: Optional[datetime]
"""
14节课， 
"1
08:00-08:45"
"2
08:50-09:35"
"3
09:50-10:35"
"4
10:40-11:25"
"5
11:30-12:15"
"6
13:00-13:45"
"7
13:50-14:35"
"8
14:45-15:30"
"9
15:40-16:25"
"10
16:35-17:20"
"11
17:25-18:10"
"12
18:30-19:15"
"13
19:20-20:05"
"14
20:10-20:55"

"""
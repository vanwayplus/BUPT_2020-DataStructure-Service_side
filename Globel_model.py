from datetime import datetime, date
from pathlib import Path
from typing import List
from typing import Optional

from pydantic import BaseModel, ValidationError
from pydantic import constr


class bell(BaseModel):
    id: int
    type: str
    time: datetime
    is_compete: bool = False
    description: Optional[str] = None


class logger(BaseModel):
    id: int
    time: datetime
    type: str
    description: Optional[str] = None

    # def create(self, name, description):
    # self.description =

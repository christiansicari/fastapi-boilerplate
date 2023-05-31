import vyper
from datetime import datetime
from pydantic import BaseModel
from enum import Enum, IntEnum
import typing

class User(BaseModel):
    username: str
    name: str
    surname: str
    birthdate: datetime | typing.Any
    # needed for SQLAlchemy
    class Config:
        orm_mode = True

class Users(BaseModel):
    users: list[User]

class UserCreated(BaseModel):
    id: str

class Operations(str, Enum):
    avg = 'avg'
    min = 'min'


def read_config(config: vyper.Vyper, f="config.json"):
    config.set_config_type("json")
    config.set_config_file(f)
    config.automatic_env()
    config.read_in_config()

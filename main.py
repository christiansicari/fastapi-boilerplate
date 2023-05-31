import time
from os.path import realpath
from pathlib import Path
import uvicorn
from fastapi import FastAPI, Request, Response, status
from vyper import v as config
from bson.objectid import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import pydantic
from libs import utils
from libs import asyncmongo
from libs import sqldb
from libs.sqldb import models as sqlmodels

__here__ = str(Path(realpath(__file__)).parents[0])
utils.read_config(config, f="config.json")
nosqldb = asyncmongo.AsyncMongo(config.get("mongo"), config.get("nosqldb"))
sql = sqldb.DB(config.get("sqldb"), sqlmodels)
sqldb = sql.session
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/dosomething", status_code=200)
def root() -> str:
    return "Hellooo"


@app.get("/nosql/users/{usrid}", status_code=200)
async def root(usrid: str) -> utils.Users:
    users = (await nosqldb.find_all("users", {"_id": ObjectId(usrid)}))
    return utils.Users(users=users)


@app.get("/nosql/users", status_code=200)
async def root() -> utils.Users:
    users = (await nosqldb.find_all("users", {}))
    return utils.Users(users=users)


@app.post("/nosql/users", status_code=201)
async def new_user(user: utils.User, response: Response) -> utils.UserCreated:
    try:
        userid = await nosqldb.insert("users", user.dict())
        return utils.UserCreated(id=userid)
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.get("/nosql/users/{usrid}/stats", status_code=200)
async def new_user(usrid, op: utils.Operations, field: str, groupby: str):
    pipeline = [
        {"$match": {"_id": ObjectId(usrid)}},
        {"$group": {
            "_id": f"${groupby}",
            "stat": {f"${op.value}": f"${field}"}
        }}
    ]
    result = await nosqldb.aggregate("users", pipeline)
    return {"result": result}


@app.post("/sql/users")
def create_user(user: utils.User):
    dbuser = sqlmodels.User(**user.dict())
    sqldb.add(dbuser)
    sqldb.commit()
    sqldb.refresh(dbuser)
    return dbuser


@app.put("/sql/users/{usrid}")
def create_user(usrid: str, body: dict):
    dbuser = sqldb.query(sqlmodels.User).filter(sqlmodels.User.id == usrid).first()
    for k, v in body.items():
        if hasattr(dbuser, k):
            setattr(dbuser, k, v)
    sqldb.commit()
    sqldb.refresh(dbuser)
    return dbuser


@app.get("/sql/users/{usrid}")
def get_users(usrid: str) -> utils.User:
    user = sqldb.query(sqlmodels.User).filter(sqlmodels.User.id == usrid).first()
    return user


@app.get("/sql/users")
def get_users(skip: int = 0, limit: int = 100) -> utils.Users:
    users = sqldb.query(sqlmodels.User).offset(skip).limit(limit).all()
    return utils.Users(users=users)


if __name__ == '__main__':
    uvicorn.run(app, host=config.get('listeningHost'), port=config.get_int('listeningPort'))

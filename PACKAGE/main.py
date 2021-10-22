#!/usr/bin/env python
# coding: utf-8
# yc@2021/07/31

from importlib.metadata import version

from fastapi import FastAPI

from {PACKAGE} import utils
from {PACKAGE}.routers import users


app = FastAPI(title='{TITLE}', version=version('{PACKAGE}'))
db = utils.get_db()
utils.setup_logging()

app.include_router(users.router, tags=['User'])


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()

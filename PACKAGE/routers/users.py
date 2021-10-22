#!/usr/bin/env python
# coding: utf-8
# yc@2021/09/26

from fastapi import APIRouter
from sqlalchemy import select

from {PACKAGE} import utils, models
from {PACKAGE}.tables import User


router = APIRouter(prefix='/users')
db = utils.get_db()


@router.get('/{uid}', response_model=models.UserOut)
async def get_user(uid: int):
    '''
    Get user
    '''
    user = await db.fetch_one(select(User).where(User.c.id == uid))
    if not user:
        raise utils.HTTP400(detail=f'No such user: {uid}')
    return user

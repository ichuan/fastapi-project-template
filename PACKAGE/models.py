#!/usr/bin/env python
# coding: utf-8
# yc@2021/07/31

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    username: str
    email: Optional[EmailStr] = ''

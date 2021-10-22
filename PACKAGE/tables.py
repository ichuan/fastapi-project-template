#!/usr/bin/env python
# coding: utf-8
# yc@2021/7/31

import datetime

import sqlalchemy as sa

metadata = sa.MetaData()


User = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('username', sa.String(length=42), unique=True),
    sa.Column('email', sa.String(length=254), nullable=False, default=''),
    sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow),
)

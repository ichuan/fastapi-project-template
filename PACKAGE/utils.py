#!/usr/bin/env python
# coding: utf-8
# yc@2021/07/30

import os
import ssl
import time
import random
import base64
import asyncio
import logging
import logging.handlers
from datetime import datetime
from functools import partial
import urllib.request
import urllib.error
import urllib.parse

import databases
import aioredis
from fastapi import HTTPException

from {PACKAGE} import consts


database = databases.Database(consts.DATABASE_URL)
logger = logging.getLogger('{PACKAGE}')
redis = aioredis.from_url(consts.REDIS_URL, encoding='utf-8')

HTTP400 = partial(HTTPException, status_code=400)


def get_db():
    return database


def new_db():
    return databases.Database(consts.DATABASE_URL)


def now():
    return datetime.utcnow()


UAS = [
    # win10, edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like'
    ' Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    # Chromebook
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like'
    ' Gecko) Chrome/51.0.2704.64 Safari/537.36',
    # osx, safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 '
    '(KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    # win7, chrome
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like '
    'Gecko) Chrome/47.0.2526.111 Safari/537.36',
    # linux, firefox
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 ' 'Firefox/15.0.1',
]


def http_get(
    url,
    try_times=1,
    timeout=consts.HTTP_TIMEOUT,
    extra_headers=None,
    check_certificate=False,
):
    headers = {'User-Agent': random.choice(UAS), 'Cache-Control': 'max-age=0'}
    if extra_headers:
        headers.update(extra_headers)
    context = None if check_certificate else ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    for i in range(try_times, 0, -1):
        try:
            return urllib.request.urlopen(req, timeout=timeout, context=context).read()
        except urllib.error.URLError:
            if i == 1:
                raise
            time.sleep(random.random())


def http_post(
    url,
    data,
    extra_headers=None,
    timeout=consts.HTTP_TIMEOUT,
    alternative_method=None,
    check_certificate=False,
):
    '''
    data: utf-8 encoded dict OR string
    '''
    headers = {'User-Agent': random.choice(UAS), 'Cache-Control': 'max-age=0'}
    if extra_headers:
        headers.update(extra_headers)
    context = None if check_certificate else ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers, method=alternative_method)
    if type(data) is dict:
        data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    return urllib.request.urlopen(req, data, timeout=timeout, context=context).read()


def random_key(size=24):
    return base64.urlsafe_b64encode(os.urandom(size))[:size].decode('utf-8')


def setup_logging():
    logger.setLevel(getattr(logging, consts.LOG_LEVEL.upper()))
    # 100MB
    handler = logging.handlers.RotatingFileHandler(
        filename=consts.LOG_FILE,
        maxBytes=104857600,
        backupCount=5,
    )
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(message)s'))
    logger.addHandler(handler)


async def async_call(func, *args):
    return await asyncio.get_running_loop().run_in_executor(None, func, *args)

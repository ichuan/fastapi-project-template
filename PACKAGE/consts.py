#!/usr/bin/env python
# coding: utf-8
# yc@2021/07/30

import os
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv('DATA_DIR', './'))
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATA_DIR}/db.sqlite3')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost/3')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = DATA_DIR.joinpath('logs', 'web.log')
HTTP_TIMEOUT = 15

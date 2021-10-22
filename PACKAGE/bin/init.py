#!/usr/bin/env python
# coding: utf-8
# yc@2021/09/26

'''
Init a new config
'''
import sys

from {PACKAGE} import consts
from pathlib import Path


supervisord_example = consts.PACKAGE_DIR.joinpath('supervisord.example.ini')


def init(data_dir):
    data_dir = Path(data_dir)
    if data_dir.exists():
        print(f'Dir "{data_dir}" already exists')
        return 1
    data_dir.joinpath('run').mkdir(parents=True)
    data_dir.joinpath('logs', 'supervisord').mkdir(parents=True)
    data_dir.joinpath('config').mkdir(parents=True)
    supervisord_config = data_dir.joinpath('config', 'supervisord.ini')
    supervisord_config.write_text(
        supervisord_example.read_text().replace('PACKAGE', '{PACKAGE}')
    )
    print(f'Start with:\n    supervisord -c {supervisord_config.resolve()}')
    print('Or, without supervisord:')
    print(f'    DATA_DIR={data_dir.resolve()} python -m {PACKAGE}.bin.cmd')
    return 0


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.exit(init(sys.argv[1]))
    else:
        print('Usage: python -m {PACKAGE}.bin.init <new_data_dir>')

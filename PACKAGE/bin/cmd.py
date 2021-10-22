#!/usr/bin/env python
# coding: utf-8
# yc@2021/7/31

'''
Usage:
    cmd.py create tables
    cmd.py drop tables
    cmd.py upsert user <username> <email>
    cmd.py list users [--offset=OFFSET] [--limit=LIMIT]

Options:
    -h --help         Show this screen
    --offset=OFFSET   Query offset [default: 0]
    --limit=LIMIT     Query LIMIT [default: 20]
'''

from docopt import docopt
from sqlalchemy import select, insert, update


def get_db():
    import sqlalchemy
    from {PACKAGE}.consts import DATABASE_URL

    return sqlalchemy.create_engine(DATABASE_URL, future=True)


def main(args):
    if args['tables']:
        engine = get_db()
        from {PACKAGE}.tables import metadata

        if args['create']:
            print('Creating tables...')
            metadata.create_all(engine)
        elif input('Confirm to drop tables?[y/n] ') == 'y':
            print('Dropping tables...')
            metadata.drop_all(engine)
    elif args['upsert'] and args['user']:
        from {PACKAGE}.tables import User

        username = args['<username>'].lower()
        email = args['<email>'].lower()
        with get_db().connect() as conn:
            row = conn.execute(
                select(User).where(User.c.username == username).limit(1)
            ).first()
            if row:
                # update
                conn.execute(
                    update(User).where(User.c.username == username).values(email=email)
                )
                print(f'Updated user with email: {email}')
            else:
                # insert
                res = conn.execute(insert(User).values(username=username, email=email))
                print(f'Created user with uid: {res.inserted_primary_key[0]}')
            conn.commit()
    elif args['list'] and args['users']:
        from {PACKAGE}.tables import User

        offset = int(args['--offset'])
        limit = int(args['--limit'])

        print('Printing users from {} to {} ...'.format(offset, offset + limit))
        with get_db().connect() as conn:
            res = conn.execute(select(User).offset(offset).limit(limit))
            for i in res:
                for j, k in i._asdict().items():
                    print(f'{j}: {k}')
                print('')


if __name__ == '__main__':
    main(docopt(__doc__))

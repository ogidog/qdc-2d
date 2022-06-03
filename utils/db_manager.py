from psycopg2 import pool

db_pool = None


def init(**kwargs):
    db_pool = pool.SimpleConnectionPool(minconn=1, maxconn=20, **kwargs)

    if (db_pool):
        return db_pool
    else:
        print('Unable to create db connection pool')

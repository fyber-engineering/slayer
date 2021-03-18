import os

from database_info import DatabaseInfo


def load_environment_variables():
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_DATABASE_NAME = os.environ.get('POSTGRES_DATABASE_NAME')
    return (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE_NAME)


def create_database_info():
    (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT,
     POSTGRES_DATABASE_NAME) = load_environment_variables()
    return DatabaseInfo(user=POSTGRES_USER,
                        password=POSTGRES_PASSWORD,
                        port=POSTGRES_PORT,
                        host=POSTGRES_HOST,
                        database=POSTGRES_DATABASE_NAME)


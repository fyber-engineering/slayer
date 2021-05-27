import os

from database_info import DatabaseInfo

POSTGRES_DEFAULT_PORT = '5432'

def create_database_info():
    return DatabaseInfo(user=os.getenv('POSTGRES_USER'),
                        password=os.environ.get('POSTGRES_PASSWORD'),
                        port=os.environ.get('POSTGRES_PORT', POSTGRES_DEFAULT_PORT),
                        host=os.environ.get('POSTGRES_HOST'),
                        database= os.environ.get('POSTGRES_DATABASE_NAME'))
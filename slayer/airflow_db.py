import psycopg2

from sla_miss_query import SLA_MISS_QUERY
from ti import TI


def connect_to_db(database_info):
    try:
        connection = psycopg2.connect(user=database_info.user,
                                      password=database_info.password,
                                      host=database_info.host,
                                      port=database_info.port,
                                      database=database_info.database)

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        return (connection, cursor)
    except (Exception, psycopg2.Error) as error:
        raise Exception("Error while connecting to PostgreSQL", error)


def transform_dag_run_records_to_list(dags_run_record):
    dags_info_with_sla_miss = []
    for row in dags_run_record:
        dags_info_with_sla_miss.append(
            (
                row[TI.dag_id],
                row[TI.task_id],
                row[TI.execution_date]
            )
        )
    return dags_info_with_sla_miss


def get_dags_run_with_sla_miss_from_db(cursor):
    dags_run_with_sla_miss_query = SLA_MISS_QUERY
    cursor.execute(dags_run_with_sla_miss_query)
    dags_run_record = cursor.fetchall()
    dags_info_with_sla_miss = transform_dag_run_records_to_list(dags_run_record)
    return dags_info_with_sla_miss

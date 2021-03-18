import psycopg2
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
        print("Error while connecting to PostgreSQL", error)

def get_dags_run_with_sla_miss_from_db(cursor):
    dags_run_with_sla_miss_query = '''        
        SELECT dag_id, task_id, execution_date, state
        FROM (SELECT task_id, dag_id, execution_date, state 
            FROM task_instance
            INNER JOIN sla_miss USING(task_id, dag_id, execution_date)
            WHERE state IS NULL OR (state!='success' AND state!='skipped')) AS sla_task
        WHERE EXISTS (SELECT dag_id, execution_date 
                        FROM dag_run 
                        WHERE (dag_run.state!='success') AND 
                        sla_task.dag_id=dag_run.dag_id AND 
                        sla_task.execution_date=dag_run.execution_date);
        '''

    cursor.execute(dags_run_with_sla_miss_query)

    dags_run_record = cursor.fetchall()
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


def close_connection(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
    print("")

import airflow_db as db
import pandas


class DagWithSLAMissInfo():
    def __init__(self, dag_id, task_id, execution_date):
        self.dag_id = dag_id
        self.task_id = task_id
        self.execution_date = execution_date


class SLAMissesDetector:
    def __init__(self, database_info):
        self._cursor = db.connect_to_db(database_info)[1]
        print(self._cursor)

    def get_tasks_with_sla_miss(self):
        tasks_from_db_df = self._get_df_tasks_from_db()
        return tasks_from_db_df.values.tolist()

    def _get_df_tasks_from_db(self):
        tasks_from_db = db.get_dags_run_with_sla_miss_from_db(self._cursor)
        df = pandas.DataFrame(tasks_from_db, columns=['dag_id', 'task_id', 'execution_date'])
        return df

import time
from slayer.environment_var import create_database_info
import prometheus_client
from prometheus_client.core import GaugeMetricFamily
from slayer.sla_misses_detector import SLAMissesDetector
from slayer.ti import TI


class MetricsCollector(object):

    def __init__(self):
        airflow_database_info = create_database_info()
        self.sla_misses_detector = SLAMissesDetector(airflow_database_info)

    def describe(self):
        return []

    def collect(self):
        tasks_with_sla_miss = self._get_tasks_with_sla_miss()
        return self._add_tasks_instance_sla_metrics(tasks_with_sla_miss)

    def _get_tasks_with_sla_miss(self):
        return self.sla_misses_detector.get_tasks_with_sla_miss()

    def _add_tasks_instance_sla_metrics(self, tasks_with_sla_miss):
        for task_instance in tasks_with_sla_miss:
            dag_sla_miss_metric_family = self._define_metric_family()
            self._create_metric_from_task_instance(dag_sla_miss_metric_family,
                                                   task_instance)
            yield dag_sla_miss_metric_family

    def _define_metric_family(self):
        return GaugeMetricFamily(
            'airflow_sla_misses',
            'currently running dags with SLA misses',
            labels=['dag_id', 'task_id', 'execution_date']
        )

    def _create_metric_from_task_instance(self,
                                          dag_sla_miss_metric_family,
                                          task_instance):
        dag_sla_miss_metric_family.add_metric(
            [task_instance[TI.dag_id],
             task_instance[TI.task_id],
             task_instance[TI.execution_date].strftime("%Y-%m-%dT%H:%M")],
            1.0
        )


def run_slayer_prometheus_client():
    try:
        prometheus_client.start_http_server(8000)
        prometheus_client.REGISTRY.register(MetricsCollector())
        while True:
            time.sleep(1)
    except Exception as inst:
        print(inst)

if __name__ == '__main__':
    run_slayer_prometheus_client()

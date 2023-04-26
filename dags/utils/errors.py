from airflow.exceptions import AirflowException

class Error:
    def raise_airflow_exception(self, msg):
        raise AirflowException(msg)
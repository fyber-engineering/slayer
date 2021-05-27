SLA_MISS_QUERY = '''        
    SELECT 
        dag_id, task_id, execution_date, state
    FROM 
        (
            SELECT 
                task_id, dag_id, execution_date, state 
            FROM 
                task_instance
            INNER JOIN 
                sla_miss USING(task_id, dag_id, execution_date)
            WHERE  
                state IS NULL OR (state!='success' AND state!='skipped')
        ) AS sla_task
    WHERE EXISTS 
        (
            SELECT 
                dag_id 
            FROM 
                dag_run 
            WHERE 
                dag_run.state!='success' 
                    AND 
                sla_task.dag_id=dag_run.dag_id 
                    AND 
                sla_task.execution_date=dag_run.execution_date
        );
    '''
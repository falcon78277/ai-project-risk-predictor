import pandas as pd
import random
from datetime import datetime, timedelta

def generate_large_dataset(num_entries=200):
    statuses = ['On Track', 'Delayed', 'At Risk']
    workloads = ['Low', 'Medium', 'High']
    data = []

    for i in range(1, num_entries + 1):
        project_id = 100 + (i // 10)
        employee_id = 1000 + i
        status = random.choice(statuses)
        deadline = datetime(2025, 7, 20) + timedelta(days=random.randint(0, 30))
        progress = random.randint(30, 100)
        workload = random.choice(workloads)
        hours_logged = random.randint(20, 50)
        sentiment_score = round(random.uniform(-0.6, 0.8), 2)

        data.append([
            project_id, employee_id, status, deadline.strftime('%Y-%m-%d'),
            progress, workload, hours_logged, sentiment_score
        ])

    df = pd.DataFrame(data, columns=[
        'project_id', 'employee_id', 'status', 'deadline',
        'progress', 'workload', 'hours_logged', 'sentiment_score'
    ])
    df.to_csv('uploads/large_project_data.csv', index=False)

generate_large_dataset()

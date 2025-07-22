from celery import shared_task
import time
@shared_task
def process_task(task_id):
    print(f"任務 {task_id} 背景開始處理")
    time.sleep(5)
    print(f"任務 {task_id} 處理完成")

from celery import Celery
from datetime import datetime
import time

app = Celery('celery_tasks.mytask', broker='redis://127.0.0.1:6379/3')


@app.task
def dosomething():
    with open('temp.txt', 'a+') as f:
        f.write('我滴老家就住在这个屯儿。')
        time.sleep(5)
        f.write(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
        f.write('\r\n')
        f.flush()


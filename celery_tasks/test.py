from celery_tasks.mytask import dosomething


def func():
    print("#" * 20)
    print("worker working...")
    dosomething.delay()
    print('over  haha')


if __name__ == '__main__':
    func()


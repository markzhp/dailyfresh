from celery_tasks.mytask import dosomething


def func():
    print("#" * 20)
    print("worker working...")
    dosomething.delay()
    print('over  haha')


class A(object):
    @classmethod
    def do(cls):
        print('我是你的眼')


class B(object):
    @classmethod
    def do(cls):
        print(cls)
        super(B, cls).do()
        print("--" * 12)


class C(B, A):
    pass


if __name__ == '__main__':
    C.do()

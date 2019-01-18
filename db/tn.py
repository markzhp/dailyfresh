class A(object):
    def m1(self):
        print('m1')
        self.m2()

    def m2(self):
        print('m2')

a=A()
a.m1()
class A:
    def a(self):
        print('a')
    

class B:
    def a(self):
        print('b')
    

class C(B, A):
    def a(self):
        self.a()
    

o = C()
o.c()




























def doNothing():
    pass

anInt = 1
aString = 'Single'
bString = "Double"

class AClass:
    def __init__(self, param):
        self.content = param

    def makePublic(self):
        return self.content

    def doNothing(self, *args, **kwargs):
        doNothing()

    def __beDiscrete(self):
        self.content.extend('someSecret')

    def __str__(self):
        return 'Name'

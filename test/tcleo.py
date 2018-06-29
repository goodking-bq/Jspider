# coding:utf-8
from __future__ import absolute_import, unicode_literals

__author__ = "golden"
__date__ = '2018/6/21'

from cleo import Command


class GreetCommand(Command):
    """
    Greets someone

    greet
        {name? : Who do you want to greet?}
        {--y|yell : If set, the task will yell in uppercase letters}
    """

    def handle(self):
        name = self.argument('name')

        if name:
            text = 'Hello %s' % name
        else:
            text = 'Hello'

        if self.option('yell'):
            text = text.upper()

        self.line(text)


class GreetCommand1(Command):
    """
    Greets someone

    greet1
        {name? : Who do you want to greet?}
        {--y|yell : If set, the task will yell in uppercase letters}
    """

    def handle(self):
        name = self.argument('name')

        if name:
            text = 'Hello %s' % name
        else:
            text = 'Hello'

        if self.option('yell'):
            text = text.upper()

        self.line(text)



from cleo import Application

application = Application()
application.add(GreetCommand())
application.add(GreetCommand1())

if __name__ == '__main__':
    application.run()

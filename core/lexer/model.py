#!/usr/bin/env python
# encoding:utf-8

class Token:
    def __init__(self, description, value, line, column):
        self.description = description
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return "[%d:%d] <%s, %s>" % (self.line, self.column, self.description, self.value)

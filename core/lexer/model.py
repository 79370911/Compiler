#!/usr/bin/env python
# encoding:utf-8

class Token:
    def __init__(self, description, value):
        self.description = description
        self.value = value

    def __str__(self):
        return "<%s, %s>" % (self.description, self.value)

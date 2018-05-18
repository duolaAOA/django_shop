# -*-coding:utf-8 -*-

dsn = ""

from raven import Client

client = Client(dsn)

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()
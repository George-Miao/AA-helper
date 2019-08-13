"""
AutoHelper.util._logging
~~~~~~~~~~~~~~~~~~~

This module contains the logging class.
"""
from sys import exit


class Log(object):
    def __init__(self):
        pass

    def debug(self, msg):
        """
        Only use when debugging
        :param msg: Message to be logged
        :return:
        """
        pass

    def info(self, msg):
        """
        Log normal info onto console and log file
        :param msg: Message to be logged
        :return:
        """
        pass

    def warning(self, msg):
        """
        Log warning onto console and log file
        :param msg: Message to be logged
        :return:
        """
        pass

    def critical(self, msg):
        """
        Log critical info onto console and log file then exit the program.
        :param msg: Message to be logged
        :return:
        """
        print(msg)
        exit(1)
        pass

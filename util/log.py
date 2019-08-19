"""
AutoHelper.util._logging
~~~~~~~~~~~~~~~~~~~

This module contains the logging class.
"""
import traceback
import datetime
from sys import exit


class Log(object):  # TODO
    def __init__(self):
        pass

    def input(self, prompt=''):
        return input(f'[>] {prompt}>>> ')

    @staticmethod
    def get_time():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def debug(self, msg, error=None):
        """
        Only use when debugging
        :param msg: Message to be logged
        :param error: Error info
        :return:
        """
        print('[-] ' + msg)
        if error:
            print('    >>  ' + traceback.format_exc()[:-1].replace('\n', '\n    >>  '))

    def info(self, msg, error=None):
        """
        Log normal info onto console and log file
        :param msg: Message to be logged
        :param error: Error info
        :return:
        """
        print('[+] ' + msg)
        if error:
            print('    >>  ' + traceback.format_exc()[:-1].replace('\n', '\n    >>  '))

    def warning(self, msg, error=None):
        """
        Log warning onto console and log file
        :param msg: Message to be logged
        :param error: Error info
        :return:
        """
        print(f'[!] [{self.get_time()}] {msg}')
        if error:
            print('    >>  ' + traceback.format_exc()[:-1].replace('\n', '\n    >>  '))

    def critical(self, msg, error=None):
        """
        Log critical info onto console and log file then exit the program.
        :param msg: Message to be logged
        :return:
        """
        print('[X] ' + msg)
        if error:
            print('    >>  ' + traceback.format_exc()[:-2].replace('\n', '\n    >>  '))
        exit(1)
        quit(1)
        pass

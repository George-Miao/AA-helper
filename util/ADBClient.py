"""
AutoHelper.util.ADBClient
~~~~~~~~~~~~~~~~~~~

This module contains the ADBClient class which is a simple wrapper of ADB.
"""
from os import path
from subprocess import run, SubprocessError
from .exceptions import ADBConnectionError, ADBRunCommandError


class ADBClient(object):
    def __init__(self, host=[], adb_path: str = r""):
        """
        The main module of ADB client
        :type adb_path: raw str
        :param host: str The host of simulator
        """
        if host:
            self.host = host
        else:
            self.host = self.detect_hosts()
        self.path = path.normpath(adb_path)
        if not path.isabs(self.path):
            self.path = path.abspath(self.path)
        self.path = path.join(self.path, 'adb.exe')

    def detect_hosts(self):
        """
        Auto detect available adb host
        :return:
        """
        host_list = run(f"{self.path} devices", capture_output=True).stdout.decode('utf-8').split('\r\n')[1:-2]
        return [host.replace('\tdevice', '') for host in host_list]

    def run_command(self, args):
        """
        Run ADB command
        :param args:
        :return:
        """
        command = f"{self.path} -s {self.host} {args}"
        try:
            return run(command, capture_output=True).stdout
        except SubprocessError as e:
            raise ADBRunCommandError(f'Error Occurred when running {command}:\ne')

    def screen_shot(self, pic_name):
        self.run_command(f'screencap -p /pictures/{pic_name}')

    def test_connect(self):
        """
        Test the connection of adb when run the program
        :return: (bool) If the connect is available
        """
        return True

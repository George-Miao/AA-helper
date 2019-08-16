"""
AutoHelper.util.ADBClient
~~~~~~~~~~~~~~~~~~~

This module contains the ADBClient class which is a simple wrapper of ADB.
"""
from os import path
from subprocess import run, SubprocessError
from .exceptions import ADBRunCommandError, ADBDetectHostError, ADBScreenShotError


class ADBClient(object):
    def __init__(self, adb_path: str = r"", host=''):
        """
        The main module of ADB client
        :type adb_path: raw str
        :param host str The host of simulator
        """
        self.is_connected = False
        # Set the adb.exe path (if it's not abs path, change it to abs path)
        self.path = path.normpath(adb_path)
        if not path.isabs(self.path):
            self.path = path.abspath(self.path)
        if not path.basename(self.path) == 'adb.exe':
            self.path = path.join(self.path, 'adb.exe')

        # Set the host (If it's blank, auto detect)
        if host:
            self.host = host
        else:
            self.host = self.select_host(self.detect_host())
        self.is_connected = True

    def detect_host(self):
        """
        Auto detect available ADB host
        :return: A list of ADB hosts
        """
        try:
            host_list = run(f"{self.path} devices", capture_output=True).stdout.decode('utf-8').split('\r\n')[-3:0:-1]
        except Exception as e:
            raise ADBDetectHostError(f'Error when detect host with ADB_path {self.path}\n'
                                     f'{e}')
        host_list = [host.replace('\tdevice', '') for host in host_list]
        if not host_list:
            raise ADBDetectHostError(f'Cannot detect any running emulator')
        else:
            return host_list

    @staticmethod
    def select_host(host_list):
        """
        let user select one host from host lists
        :param host_list: a list of ADB hosts
        :return: host
        """
        if len(host_list) > 1:
            print('[+] Detected multiple hosts: (Port 62001 will be the first and default port for adb devices)')
            for host_id, host in enumerate(host_list):
                print(f" > ({host_id+1}) {host}")
            print('[+] Input the number of host you want to connect (1, 2....)')
            inp = input('>>> ')
            try:
                return [host_list[int(inp) - 1]]
            except Exception:
                raise ADBDetectHostError('Error input')
        else:
            return host_list[0]

    # Function for interacting with ADB
    def run_command(self, args):
        """
        Run ADB command
        :param args: ADB commands
        :return: stdout
        """
        command = f"{self.path} -s {self.host} {args}"
        try:
            return run(command, capture_output=True).stdout
        except SubprocessError as e:
            raise ADBRunCommandError(f'Error Occurred when running {command} >> {self.host}:\ne')

    def screen_shot(self, pic_path):
        """
        To capture a screen shot and save it to pic_path
        :param pic_path: The abs path of screen shot, pictures/ by default
        :return:
        """
        self.run_command(f'shell screencap -p /sdcard/screen.png')
        if not path.exists(pic_path):
            self.run_command(f'pull /sdcard/screen.png {pic_path}')
        else:
            raise ADBScreenShotError(f'{pic_path} already exist')
        self.run_command(f'shell rm /sdcard/screen.png')

    @property
    def window_size(self):
        x_y = self.run_command('shell wm size').replace(b'\r\r\n', b'')\
            .decode('utf-8').replace('Physical size: ', '').split('x')
        return [int(x) for x in x_y]

    def __str__(self):
        return f'ADBClient(host = {self.host}, path = {self.path}, is_connected = {self.is_connected})'

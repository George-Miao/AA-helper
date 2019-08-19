"""
AutoHelper.util.ADBClient
~~~~~~~~~~~~~~~~~~~

This module contains the ADBClient class which is a simple wrapper of ADB.
"""
from os import path, remove
from subprocess import run, SubprocessError
from contextlib import contextmanager
from .exceptions import ADBError


class ADBClient(object):
    def __init__(self, adb_path: str = r"", host=''):
        """
        The main module of ADB client
        :type adb_path: raw str
        :param host str The host of simulator
        """
        self.is_connected = False
        # Set the adb.exe path (if it's not abs path, convert it to abs path)
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

        # Detect the size of window
        self.size = self.get_window_size()

    def detect_host(self):
        """
        Auto detect available ADB host
        :return: A list of ADB hosts
        """
        try:
            host_list = run(f"{self.path} devices", capture_output=True).stdout.decode('utf-8').split('\r\n')[-3:0:-1]
        except Exception as e:
            raise ADBError(e)
        host_list = [host.replace('\tdevice', '') for host in host_list]
        if not host_list:
            raise ADBError(f'Cannot detect any running emulator')
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
                raise ADBError('Error input')
        else:
            return host_list[0]

    # Function for interacting with ADB
    def run_command(self, args):
        """
        basic function: Run ADB command
        :param args: ADB commands
        :return: stdout
        """
        command = f"{self.path} -s {self.host} {args}"
        try:
            return run(command, capture_output=True).stdout
        except SubprocessError as e:
            raise ADBError(f'Error occurred when running {command} >> {self.host}:\ne')
        except Exception as e:
            raise ADBError(f'Unknown error when running {command} >> {self.host}:\ne')

    @contextmanager
    def screen_shot(self, pic_path):
        """
        To capture a screen shot ,save it to pic_path and delete it after using
        Using context manager to guarantee the picture is well deleted
        :param pic_path: The abs path of screen shot, pictures/ by default
        :return: pic_path
        """
        self.run_command(f'shell screencap -p /sdcard/screen.png')
        if not path.exists(pic_path):
            self.run_command(f'pull /sdcard/screen.png {pic_path}')
        else:
            raise ADBError(f'{pic_path} already exist')
        self.run_command(f'shell rm /sdcard/screen.png')
        yield pic_path
        remove(pic_path)

    def get_window_size(self):
        """
        Detect window size and return
        :return: int[2] which is the width and height of the window
        """
        coordinate = self.run_command('shell wm size').replace(b'\r\r\n', b'')
        coordinate = coordinate.decode('utf-8').replace('Physical size: ', '').split('x')
        if len(coordinate) != 2:
            raise ADBError('Error when detecting window size')
        return [int(x) for x in coordinate]

    def click(self, location):
        if not type(location) is tuple:
            raise ADBError(f'Error input: {location}')
        self.run_command(f'shell input tap {location[0]} {location[1]}')

    def __str__(self):
        return f'ADBClient(' \
            f'host = {self.host}, ' \
            f'path = {self.path}, ' \
            f'is_connected = {self.is_connected}' \
            f')'

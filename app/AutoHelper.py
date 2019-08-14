import importlib
from os import path, getcwd
from util import Log, ADBClient, Ocr
from util.exceptions import *


class AutoHelper(object):
    def __init__(self, config_name='sample_config', *args):
        # Instantiate util.Log module
        self.log = Log()

        # Import config file
        try:
            self.config = importlib.import_module(config_name, package='AutoHelper')
            self.log.info(f'Import config success: {config_name}.py')
            if not self.verify_config():
                self.log.warning('Config file is not compliant.'
                                 'Missing args will be blank')
        except ImportError as e:
            self.log.critical(f'Import config error:\n{e}')

        # Instantiate util.ADB_client to interact with emulator
        try:
            self.adb = ADBClient(self.config.ADB_root, self.config.ADB_host)
        except ADBError as e:
            self.log.critical(f'ADB Error:\n{e}')

        # Instantiate util.Ocr to interact with Baidu-api
        try:
            self.ocr = Ocr(self.config.APP_ID, self.config.API_KEY, self.config.SECRET_KEY)
        except AIPError as e:
            self.log.critical(f'Connecting to Baidu-api error:'f'{e}')

    def init_coordinate(self):
        try:
            self.adb.screen_shot('homepage.png')
        except Exception as e:
            print(e)

    def verify_config(self):
        """
        To verify if the config file is compliant format.
        :return:(bool)
        """
        pass

    def battle_module(self):
        """
        The main module of battle
        :return: None
        """
        pass

    def single_mission(self, times=0):
        """
        A loop function to repeat a single mission.
        Start from the mission page(which has the '开始行动' button)
        :param times:  times the mission to be looped.
                If times == 0(By default), it will keep loop until strength(理智) is not enough.
        :return: None
        """
        pass

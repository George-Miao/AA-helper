import importlib
from util import Log, ADBClient, Ocr
from util.exceptions import *


class AutoHelper(object):
    def __init__(self, config_name='sample_config'):
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
            self.log.critical('Import config error')

        #  Instantiate util.ADB_client to interact with emulator
        self.adb = ADBClient(self.config.ADB_root, self.config.ADB_host)

        if not self.adb.test_connect():  # Test if the ADB host(s) are available
            self.log.critical('ADB host(s) are not available')
        else:
            self.log.info('ADB host(s) are available')

        #  Instantiate util.Ocr to interact with Baidu-api
        try:
            self.ocr = Ocr(self.config.APP_ID, self.config.API_KEY, self.config.SECRET_KEY)
        except AIPError as e:
            self.log.critical(f'Connecting to Baidu-api error:'
                                  f'{e}')

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

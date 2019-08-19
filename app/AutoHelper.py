"""
Main module - AutoHelper
````````

AutoHelper.app.AutoHelper
"""

import importlib
import json
from random import uniform
from json import JSONDecodeError
from os import path, getcwd
from util import Log, ADBClient, Ocr
from util.exceptions import *


class AutoHelper(object):
    def __init__(self, config_name='sample_config', *args):
        try:
            # Get the current abspath
            self.path = getcwd()

            # Instantiate util.Log module
            self.log = Log()

            # Import config file
            self.config = importlib.import_module(config_name, package='AutoHelper')
            self.log.info(f'Import config success: {config_name}.py.')
            if not self.__verify_config():
                self.log.warning('Config file is not compliant. Missing args will be blank.')

            # Instantiate util.ADB_client to interact with emulator
            self.adb = ADBClient(self.config.ADB_root, self.config.ADB_host)

            # Instantiate util.Ocr to interact with Baidu-api
            self.ocr = Ocr(self.config.APP_ID, self.config.API_KEY, self.config.SECRET_KEY)

            # Initialize
            with open('ingame.json', mode='r') as file:
                self.ingame = json.load(file)
            self.initialize()

        except ImportError as e:
            self.log.critical(f'Import config error:', e)
        except ADBError as e:
            self.log.critical(f'ADB Error:', e)
        except OCRError as e:
            self.log.critical(f'Connecting to Baidu-api error:', e)
        except Exception as e:
            self.log.warning('Unknown Error:', e)

    # Initializers
    def initialize(self):
        """
        Initialize in-game info (Includes window size, click positions etc.)
        And save into ingame.json
        :return: None
        """
        def homepage():
            self.log.info("Please go to home page, when finished, input anything below:")
            self.log.input()
            self.log.info("Start recognizing...")
            with self.adb.screen_shot(screenshot_path):
                pic_content = self.ocr.scan(screenshot_path)
            if pic_content['flag']['is_homepage'] == 'TRUE':
                self.ingame['location']['homepage_strength'] = pic_content['location']['strength']
                self.log.info('Done')
            else:
                raise AutoHelperError('Incorrect page')

        def mission_page():
            self.log.info("Please go to mission page (anyone with '开始行动' button), "
                          "when finished, input anything below:")
            self.log.input()
            self.log.info("Start recognizing...")
            with self.adb.screen_shot(screenshot_path):
                pic_content = self.ocr.scan(screenshot_path)
            if pic_content['flag']['is_mission_page']  == 'TRUE':
                self.ingame['location']['mission_page_strength'] = pic_content['location']['strength']
                self.ingame['location']['start_mission'] = pic_content['location']['start_mission']
                self.log.info('Done')
            else:
                raise AutoHelperError('Incorrect page')

        def preparation():
            self.log.info('The program will automatically go to preparation page(without actually start the mission)\n'
                          "Please don't disturbance the program")
            self.adb.click(self.confuse(self.ingame['location']['start_mission']))
            with self.adb.screen_shot(screenshot_path):
                pic_content = self.ocr.scan(screenshot_path)
            if pic_content['flag']['is_preparation_page'] == 'TRUE':
                self.ingame['location']['prepare_start'] = pic_content['location']['prepare_start']
                self.log.info('Done')
            else:
                raise AutoHelperError('Incorrect page')

        try:
            # Detect if it's first time
            if self.ingame['FIRST_TIME'] == "TRUE":
                self.log.info('First time using AA-Helper, Initializing, please follow the instruction.')  # TODO
                # Detect window size
                self.ingame['window_size'] = self.adb.get_window_size()

                # Set screenshot save path
                screenshot_path = path.join(self.path, 'pictures', 'Screenshot.png')

                # Detect homepage
                self.retry(homepage)

                # Detect mission page
                self.retry(mission_page)

                # Detect start button in preparation page
                self.retry(preparation)

                # Change the first-time status into false
                # self.ingame['FIRST_TIME'] = "FALSE" TODO: Uncomment

                # Writing into file
                with open('ingame.json', mode='w') as file:
                    file.write(json.dumps(self.ingame))
        except FileNotFoundError as e:
            self.log.warning('Cannot found ingame.json, creating...', e)
            with open('ingame.json', mode='w') as file:  # Create the file and set FIRST_TIME to TRUE
                self.ingame = dict()
                self.ingame['FIRST_TIME'] = "TRUE"
                file.write(json.dumps(self.ingame))
        except JSONDecodeError as e:
            self.log.warning('JSON decoder error:', e)
        except Exception as e:
            self.log.warning('Unknown error during initializing:', e)

    def retry(self, func, max_time=3):
        try:
            return func()
        except Exception as e:
            self.log.warning('Unknown error:', e)
            if max_time > 0:
                self.log.info(f"Error while running '{func.__name__}', retrying ({max_time} time(s) left).")
                return self.retry(func, max_time - 1)
            else:
                raise

    def __verify_config(self):  # TODO
        """
        To verify if the config file is compliant format.
        :return:(bool)
        """
        return True

    # Battle functions
    def battle(self):  # TODO
        """
        A overall battle module
        :return: None
        """
        try:
            self.__start_battle()
        except Exception as e:
            self.log.warning("Unknown Error:", e)

    def __start_battle(self, times=0):  # TODO
        """
        Simply click on '开始战斗' for times
        :param times: Times of clicking '开始战斗' button
        :return: None
        """
        try:
            self.adb.click(self.confuse(self.ingame['location']['start_mission']))
        except Exception as e:
            self.log.warning('Unknown error:', e)

    def confuse(self, loca):
        try:
            return loca['left'] + uniform(-0.49, 0.49) * loca['width'], \
                   loca['top'] + uniform(-0.49, 0.49) * loca['height'],
        except Exception as e:
            self.log.warning("Unknown error:", e)

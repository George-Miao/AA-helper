"""
AutoHelper.util.ocr
~~~~~~~~~~~~~~~~~~~

This module contains the ocr class which provides a simple wrapper of Baidu ocr api.
"""
from aip import AipOcr
from os import path
from util.exceptions import AIPError


class Ocr(object):
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        try:
            self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        except Exception as e:
            raise AIPError(f'Error occurred when initializing the ocr client\n{e}')





"""
AutoHelper.util.ocr
~~~~~~~~~~~~~~~~~~~

This module contains the ocr class which provides a simple wrapper of Baidu ocr api.
"""
from util.exceptions import OCRError

from aip import AipOcr
from PIL import Image


class Ocr(object):
    def __init__(self, APP_ID, API_KEY, SECRET_KEY, is_accurate=False):
        try:
            self.aip = AipOcr(APP_ID, API_KEY, SECRET_KEY)
            self.is_accurate = is_accurate
        except Exception as e:
            raise OCRError(f'Error occurred when initializing the ocr client\n{e}')

    def scan(self, file_path, **options):
        """
        Scan picture and return its content
        :param file_path: Path of picture
        :return: (str) Content of the picture(with index and other info)
        """
        try:
            with open(file_path, 'rb') as pic:
                if self.is_accurate:
                    return self.parse_wholepage_result(self.aip.accurate(pic.read(), options))
                else:
                    return self.parse_wholepage_result(self.aip.general(pic.read(), options))
        except Exception as e:
            raise OCRError(e)

    @staticmethod
    def cut_image(path, x1, x2, y1, y2):  # TODO
        try:
            img = Image.open(path)
            img = img.crop((x1, x2, y1, y2))
            img.save(path)
        except Exception as e:
            raise OCRError

    @staticmethod
    def parse_wholepage_result(aip_ret):
        if 'error_code' in aip_ret or 'error_msg' in aip_ret:
            raise OCRError(f"{aip_ret['error_code']}:"
                              f"(read https://cloud.baidu.com/doc/OCR/s/zjwvxzmhh for more information)\n"
                              f"{aip_ret['error_msg']}")
        ret = {
            'flag': {
                    'is_homepage': False,
                    'is_mission_page': False,
                    'is_preparation_page': False
                    },
            'location': dict(),
            'strength': '',
            'log_id': aip_ret['log_id'],
            'words_result': aip_ret['words_result']
            }
        for word in aip_ret['words_result']:
            ret['flag']['is_homepage'] |= '采购中心' in word['words']
            ret['flag']['is_mission_page'] |= '开始行动' in word['words']
            ret['flag']['is_preparation_page'] |= '本次行动配置不可更改' in word['words']
        if ret['flag']['is_mission_page']:
            ret['strength'] = aip_ret['words_result'][2]['words'].split('/')[0]
            ret['location']['strength'] = aip_ret['words_result'][2]['location']
            ret['location']['start_mission'] = [word['location']
                                                for word in aip_ret['words_result'] if '开始行动' in word['words']][0]
        elif ret['flag']['is_homepage']:
            ret['location']['strength'] = [word['location']
                                           for word in aip_ret['words_result'] if '作战' in word['words']][0]
        elif ret['flag']['is_preparation_page']:
            ret['location']['prepare_start'] = [word['location']
                                                for word in aip_ret['words_result'] if '开始' in word['words']][0]
        # Change flags into string
        ret['flag']['is_homepage'] = Ocr.upper_str(ret['flag']['is_homepage'])
        ret['flag']['is_mission_page'] = Ocr.upper_str(ret['flag']['is_mission_page'])
        ret['flag']['is_preparation_page'] = Ocr.upper_str(ret['flag']['is_preparation_page'])
        return ret

    @staticmethod
    def upper_str(in_bool):
        return str(in_bool).upper()

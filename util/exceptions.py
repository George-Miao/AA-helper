"""
AutoHelper.util.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Auto Helper exceptions.
"""


#  ADB Error
class ADBError(Exception):
    """
    An ADB base exception
    """
    pass


class ADBRunCommandError(ADBError):
    """
    An ADB error occurred when running command
    """
    pass


class ADBDetectHostError(ADBError):
    """
    An ADB error occurred when detecting host
    """
    pass


class ADBScreenShotError(ADBError):
    """
    An ADB error occurred when capturing screen
    """
    pass


# Logging Error
class LogError(Exception):
    """
    A Log base exception
    """
    pass


# OCR Error
class OCRError(Exception):
    """
    An OCR base exception
    """
    pass


class AIPError(OCRError):
    """
    An Baidu-Aip error
    """
    pass

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


class ADBConnectionError(ADBError):
    """
    An ADB connection Error occurred (Unable to find the host or the host is not exist)
    """
    pass


class ADBRunCommandError(ADBError):
    """
    An ADB error occurred when running command
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

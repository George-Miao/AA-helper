"""
AutoHelper.util.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Auto Helper exceptions.
"""


# Auto Helper Error
class AutoHelperError(Exception):
    """
    An AutoHelper error
    """
    pass


# ADB Error
class ADBError(Exception):
    """
    An ADB base exception
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

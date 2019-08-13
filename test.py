from util import ADBClient
from util import ADBDetectHostError
from subprocess import run

b = ADBClient('../../Program Files/Nox/bin/adb.exe')

print(b.host)

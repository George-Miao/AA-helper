from app import AutoHelper
from os import path, getcwd

a = AutoHelper()

a.adb.run_command(f'shell screencap -p /sdcard/screen.png')

a.adb.run_command(f"pull /sdcard/screen.png {path.join(getcwd(), 'pictures', 'Screenshot.png')}")
a.adb.run_command(f'shell rm /sdcard/screen.png')
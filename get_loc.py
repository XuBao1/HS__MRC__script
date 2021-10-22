'''
Author: xubao
Date: 2021-10-20 13:08:11
Description:  获取屏幕位置的坐标
'''

import os, time

from PIL.Image import new
import pyautogui as pag

last_pos = pag.position()
try:
    while True:
        new_pos = pag.position()
        if last_pos != new_pos:
            print(f'当前鼠标位置：{new_pos}')
            last_pos = new_pos
            #time.sleep(1)
except KeyboardInterrupt:
    print('\nExit.')
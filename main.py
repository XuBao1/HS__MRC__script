'''
Author: xubao
Date: 2021-10-20 18:24:24
Description:  炉石传说佣兵战纪H1-2坐牢脚本，在悬赏的关卡选择页面运行此程序。
version：1.0 未优化代码的可移植性，未优化问号刷在第三层中间时第二层的选路逻辑
'''

import time
from ctypes import FormatError

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
from PIL.ImageOps import grayscale

pyautogui.FAILSAFE = False

# 加载图像
pohuai = cv2.imread('./images/piece/pohuai.png')
cifu = cv2.imread('./images/piece/cifu.png')
msren = cv2.imread('./images/piece/msren.png')
zhandou = cv2.imread('./images/piece/zhandou.png')
yizhe = cv2.imread('./images/piece/yizhe.png')
secret = cv2.imread('./images/piece/secret.png')
secret_light = cv2.imread('./images/piece/secret_light.png')
frame = cv2.imread('./images/piece/frame.png')
zhayao = cv2.imread('./images/piece/zhayao.png')
treasure = cv2.imread('./images/piece/treasure.png')

# 记录神秘选项刷在中间的情况（需要改进）
flag = False

def moveClick(x, y, t=2):
    """ 移动到指定位置并点击，延时t秒 """
    pyautogui.moveTo(x, y)
    pyautogui.click()
    print(f'点击：({x}, {y})')
    time.sleep(t)


def prepare():
    """ 准备进入战斗界面 """
    moveClick(460, 370) 
    moveClick(1080, 760) # 进入H1-2
    moveClick(423, 341)
    moveClick(1000, 815)
    moveClick(500, 570, 5)


def battle():
    """ 战斗 """
    time.sleep(2)
    moveClick(1080, 765) # 开始战斗
    time.sleep(26) 

    # 佣兵上场
    pyautogui.moveTo(465, 907, 1)
    pyautogui.dragTo(850, 560, 0.5)
    pyautogui.moveTo(518, 910, 1)
    pyautogui.dragTo(850, 560, 0.5)
    pyautogui.moveTo(700, 913, 1)
    pyautogui.dragTo(850, 560, 0.5)
    time.sleep(2)
    moveClick(1120, 466) # 按下就绪按钮
    time.sleep(3)

    # 放技能
    moveClick(635, 458, 2) # 拉格纳罗斯
    moveClick(635, 458, 2) # 嘉顿
    moveClick(472, 458, 0.5)
    moveClick(660, 302, 2) # 安东尼
    moveClick(1120, 466, 30) # 按下就绪按钮,设置延迟的时间（即战斗所需时间）需要测量并更改

    # 选宝藏
    moveClick(1120, 466, 1.5) 
    moveClick(1129, 466, 7)
    moveClick(510, 468, 0.5)
    moveClick(758, 770)
    time.sleep(5)

def get_loc(target_img):
    """ 在当前屏幕中寻找目标图像，并返回其位置坐标 """
    screen_catch = ImageGrab.grab()
    screen_catch.save('./images/screen.png', 'png') # 获取屏幕截图

    img_rgb = cv2.imread('./images/screen.png') # 加载原始rgb图像
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) # 创建原始图像的灰度版本，所有操作在灰度版本中处理，最后在rgb图像中使用相同坐标还原
    template = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY) # 加载要搜索的图像模板, 转换成灰色版本

    w, h = template.shape[::-1] # 记录模板的尺寸

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED) # 使用matchTemplate对原始灰度图像和图像模板进行匹配

    threshold = 0.7 # 设置阈值
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        target_loc = (pt[0] + w/2, pt[1] +h/2)
        return target_loc # 返回目标的中心位置坐标


def select_path():
    """ 第一关打完之后，识别神秘选项，并选择第二层路线 """
    """ 有待优化，主要是如何判断神秘选项在中间的情况以及第二层关卡位置会变动 """
    loc_secret = get_loc(secret)
    print(f'神秘选项在({loc_secret[0]}，{loc_secret[1]})')
    if loc_secret == None:
        return
    if loc_secret[0] > 626 and loc_secret[0] < 750 and loc_secret[1] > 157 and loc_secret[1] < 276:
        moveClick(577, 480) # 走右边
        moveClick(662, 480)
        moveClick(754, 480)
    elif loc_secret[0] > 199 and loc_secret[0] < 323 and loc_secret[1] > 159 and loc_secret[1] < 281:
        moveClick(171, 480) # 走左边
        moveClick(264, 480)
        moveClick(387, 480)
    else: # 神秘选项在中间的情况（需要优化）
        global flag
        flag = True

def check_event():
    """ 识别随机事件的种类并做出响应 """
    cifu_loc = get_loc(cifu)
    yizhe_loc = get_loc(yizhe)
    zhandou_loc = get_loc(zhandou)
    if zhandou_loc:
        print('战斗')
        battle()
    else:
        moveClick(1080, 765, 6)
        moveClick(1080, 466, 5)
        print('赐福/灵魂医者')
    
def get_treasure():
    """ 获取神秘人的碎片 """
    secret_light_loc = get_loc(secret_light)
    print(f'神秘人在({secret_light_loc[0]},{secret_light_loc[1]})')
    moveClick(secret_light_loc[0], secret_light_loc[1], 4)
    msren_loc = get_loc(msren)
    if msren_loc:
        moveClick(1080, 765, 3)
        treasure_loc = get_loc(treasure)
        moveClick(treasure_loc[0], treasure_loc[1])
        moveClick(614, 684)
        moveClick(614, 684)
    else:
        moveClick(1080, 765, 6)
        moveClick(1080, 466) 


def end_game():
    """ 结束，点放弃 """
    moveClick(452, 900)
    moveClick(725, 725)
    moveClick(494, 570, 4)
    moveClick(494, 570, 4)
    moveClick(63, 497)

    global flag
    flag = False


if __name__ == '__main__':
    """ 主函数 """
    for cnt in range(10):
        prepare()

        battle() # 第一层战斗
        select_path()
        if flag:
            end_game()
        else:
            check_event()
            get_treasure()
            end_game()
        
        print(f'完成{cnt + 1}轮悬赏')
    






import os

import cv2
import numpy as np
import PIL.ImageGrab
import time
import pyautogui
import keyboard
import win32api, win32con
from pynput.mouse import Button, Controller

from gui import press_map, right, left, przod, tyl, turn_around, turn_right, turn_left, start_autobattle

IMAGE_WIDTH: int = 2560
IMAGE_HEIGHT: int = 1440
IMAGE_CHANNELS: int = 3
#RGB
hp_min = (214,253,255)
hp_max = (49,255,249)

lost_hp = (52,59,65)
lost_hp2 = (56,64,71)

class Cord:
    def __init__(self,x1, x2, y1, y2):
        if x1 is None or x2 is None or y1 is None or x2 is None:
            raise  Exception("wrong coordinates")
        else:
            self.x1 = int(x1)
            self.x2 = int(x2)
            self.y1 = int(y1)
            self.y2 = int(y2)

    def __repr__(self):
        return f"Cord( {self.x1} {self.x2} {self.y1} {self.y2})"


out_of_battle_cord_dict = {"hero1_hp": Cord(2211, 2351, 452, 456),
                           "hero2_hp": Cord(2211, 2351, 577, 581),
                           "hero3_hp": Cord(2211, 2351, 702, 705),
                           "hero4_hp": Cord(2211, 2351, 826, 830),
                           "open_map": [],
                           "skillpoint_1": [],
                           "skillpoint_2": [],
                           "skillpoint_3": [],
                           "skillpoint_4": [],
                           "skillpoint_5": [],
                           "icon1":Cord(1780,1781,80,81),
                           "icon2":Cord(1911,1912,70,71),
                           "icon3":Cord(2036,2037,75,76),
                           "icon4":Cord(2123,2124,75,76),
                           "icon5":Cord(2242,2243,84,85),
                           "icon6":Cord(2353,2354,40,41),
                           "icon7":Cord(2468,2469,40,41)}

in_battle_skillpoint_dict = {"skill1":Cord(1932, 1933, 1292, 1293),
                            "skill2":Cord(1955, 1956, 1292, 1293),
                            "skill3":Cord(1979, 1980, 1292, 1293),
                            "skill4":Cord(2004, 2005, 1292, 1293),
                            "skill5":Cord(2028, 2029, 1292, 1293)}

star_map_dict = {"Herta_Space_Station": Cord(475,476,710,711),
                 "Jarilo-VI": Cord(1350,1351,340,341),
                 "The_Xianzhou_Luofu": Cord(2030,2031,1120,1121)}

def crop(image, cord):
    cropped = image[cord.y1:cord.y2, cord.x1: cord.x2]
    return cropped

def check_number_of_skills(image):
    val = 0
    for i in range(5):
        cord = in_battle_skillpoint_dict[f"skill{i+1}"]
        cropped = crop(image, cord)
        r,g,b = cropped
        if r > 250 and g > 250 and b > 250:
            val += 1
    return val

def check_if_battle(image):
    rgbs = []
    for i in range(3):

        cord = in_battle_skillpoint_dict[f"skill{i+1}"]
        cropped = crop(image, cord)
        rgb = cropped
        rgbs.append(rgb)
    v = 0
    for rgb in rgbs:
        print(rgb)
        if (rgb > 250).all():
            v+=1

    if v == 3:
        return True
    else:
        return False


def check_if_endbattle(image):
    rgbs = []
    for i in range(3):

        cord = out_of_battle_cord_dict[f"icon{i+1}"]
        cropped = crop(image, cord)
        rgb = cropped
        rgbs.append(rgb)
    v = 0
    for rgb in rgbs:
        print(rgb)
        if (rgb > 200).all():
            v+=1

    if v == 3:
        return True
    else:
        return False


def get_image(convert = True):
   im = PIL.ImageGrab.grab()
   image = np.array(im)
   if convert:
       image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
   return image


def read_hero_hp(image, nr):
    cord = out_of_battle_cord_dict[f"hero{nr}_hp"]


    cropped = image[cord.y1:cord.y2, cord.x1: cord.x2]
    print(cropped.shape)
    # cv2.imshow("xDDDD",cv2.resize(cropped,(200,200)))
    # cv2.imshow("xDDDD", cropped)
    # cv2.waitKey(0)
    hp = 0
    for i in range(cord.x2 - cord.x1):
        b, g, r = cropped[2, i]
        # print(f"{i}: {b} {g} {r}")
        # print(g)
        # print(b)
        if g > 230 and b > 230:
            pass
        else:
            hp = i/(cord.x2-cord.x1)
            break
    else:
        hp=100
    print(hp," %")
    return hp


def show_img(img):
    cv2.imshow("shown image", img)
    cv2.waitKey(0)


def read_team_hp(image):
    hps = [read_hero_hp(image, i) for i in range(1,5,1)]
    for i, hp in enumerate(hps):
        print(f"hero nr {i+1} hp = {hp}%")


if __name__ == '__main__':
    time.sleep(1)

    x = 100
    y = 100
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(4)
    turn_around()
    out = True
    h = 0
    while out:
        time.sleep(0.5)
        image = get_image()
        battle = check_if_battle(image)
        if battle:
            out= False
            print("started battle")
            break
        else:
            print("not in battle")
            przod(0.5)
        h+=1
        if h == 100:
            out = False
            raise Exception("ERROR")


    start_autobattle()

    in_battle = True
    while in_battle:
        time.sleep(10)
        image = get_image()
        battle = check_if_endbattle(image)
        if battle:
            in_battle = False
            print("ended battle")
            break
        else:
            print("still in battle")
        h += 1
        if h == 100:
            out = False
            raise Exception("ERROR")

    print("END")

    # read_team_hp(image)
    # read_hero_hp(image, 1)
    image = get_image()
    path = f"{os.getcwd()}\\test_images"
    cv2.imwrite(f"{path}\\star_map_image.png", image)
    # time.sleep(3)
    # x_offset = 50
    # y_offset = 50


    # right()
    # left()
    # przod(2)
    # tyl()
    # time.sleep(1)
    # press_map()
    # print("move")
    # currentMouseX, currentMouseY = pyautogui.position()
    # print(currentMouseX, currentMouseY)
    # pyautogui.moveTo(100, 150)
    #
    # pyautogui.move(x_offset, y_offset)
    # pyautogui.move(x_offset, y_offset+50)
    # pyautogui.move(x_offset+50, y_offset+50, duration =1)
    # pyautogui.moveTo(x_offset+550, y_offset+550, duration =1)
    # pyautogui.moveRel(0, 150, duration=1)
    # pyautogui.dragRel(100, 0, duration=1)
    # currentMouseX, currentMouseY = pyautogui.position()
    # print(currentMouseX, currentMouseY)
    # print("stop moving")
    #
    #
    # print("with alt")
    #
    # # keyboard.press('alt')
    # # for _ in range(20):
    # #     pyautogui.dragRel(10, 0, duration=1)
    # #     time.sleep(0.1)
    # # keyboard.release('alt')
    #
    # for _ in range(10):
    #     przod()
    # przod()
    # tyl()
    # tyl()
    # przod()
    # currentMouseX, currentMouseY = pyautogui.position()
    # print(currentMouseX, currentMouseY)
    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1000, 505, 0, 0)
    # time.sleep(1)
    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 505, 1000, 1000)m

    # currentMouseX, currentMouseY = pyautogui.position()
    # print(currentMouseX, currentMouseY)
    # for i in range(20):
    #     turn_around()
    #     time.sleep(0.1)
    #
    # time.sleep(1)
    # turn_right()
    # time.sleep(1)
    # turn_left()
    # turn_around()
    # time.sleep(0.1)
    # turn_around()
    # time.sleep(0.1)
    # turn_around()
    # time.sleep(0.1)
    # turn_around()
    # time.sleep(0.1)
    # turn_around()
    # time.sleep(0.1)
    # turn_around()
    # time.sleep(0.1)
    # turn_around()
    # time.sleep(0.1)



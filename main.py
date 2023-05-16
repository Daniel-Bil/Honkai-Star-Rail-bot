import json
import os
from copy import deepcopy

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

def read_json(path):
    with open(f'{path}', 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

def save_json(path, dict):
    with open(f"{path}", "w") as outfile:
        json.dump(dict, outfile)

class Cord:
    def __init__(self,x1, x2, y1, y2):
        if x1 is None or x2 is None or y1 is None or x2 is None:
            raise Exception("wrong coordinates")
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

Herta_Space_Station_dict = {"parlor_car": Cord(2431,2432,309,310),
                            "master_control_zone": Cord(2443,2444,437,438),
                            "base_zone": Cord(2440,2441,570,571),
                            "storage_zone": Cord(2440,2441,690,691),
                            "supply_zone": Cord(2440,2441,820,821)}

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
    # jsonStr = json.dumps(Cord(1,2,3,4).__dict__)
    pass
    # image = get_image()
    image = cv2.imread(f"{os.getcwd()}\\test_images\\enemy_on_map_image.png")
    cord = Cord(60,315,75,330)
    cropped = crop(image, cord)
    cv2.imshow("name", cropped)
    cropped_gray = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(f"{os.getcwd()}\\test_images\\locked_enemy.png", image)
    # threshold = cv2.threshold()
    blue_cropped = deepcopy(cropped)

    # blue_cropped[np.all(blue_cropped == (0, 198, 255), axis=2)] = (255, 255, 255)
    # blue_cropped[np.all(blue_cropped == (255, 198, 0), axis=2)] = (255, 255, 255)
    # print((200 < blue_cropped[:, :, 0]) & (blue_cropped[:, :, 0] < 256) &
    #       (190 < blue_cropped[:, :, 1]) & (blue_cropped[:, :, 1] < 256) &
    #       (0 < blue_cropped[:, :, 2]) & (blue_cropped[:, :, 2] < 60))
    player_mask = ((200 < blue_cropped[:, :, 0]) & (blue_cropped[:, :, 0] <= 256) &
          (190 < blue_cropped[:, :, 1]) & (blue_cropped[:, :, 1] <= 256) &
          (0 <= blue_cropped[:, :, 2]) & (blue_cropped[:, :, 2] < 60))

    enemy_mask = ((85 < blue_cropped[:, :, 0]) & (blue_cropped[:, :, 0] <= 120) &
                   (80 < blue_cropped[:, :, 1]) & (blue_cropped[:, :, 1] <= 100) &
                   (190 <= blue_cropped[:, :, 2]) & (blue_cropped[:, :, 2] < 256))
    # maks = np.where(mask==True,255,0)
    binary_image = np.where(player_mask, 255, 0).astype(np.uint8)
    binary_image2 = np.where(enemy_mask, 255, 0).astype(np.uint8)
    print(player_mask)
    # blue_cropped = blue_cropped[blue_cropped[:,:,0]]
    # blue_cropped[~np.all(
    #     (blue_cropped[:, :, 0] > 230) & (150 < blue_cropped[:, :, 1]) & (blue_cropped[:, :, 1] < 250) & (
    #                 0 < blue_cropped[:, :, 2]) & (blue_cropped[:, :, 2] < 70), axis=1)] = (0, 0, 0)
    # w, h, _ = blue_cropped.shape
    # print(w, h)
    # print(blue_cropped[0,0])
    # for i in range(w):
    #     for j in range(h):
    #         print(f"{blue_cropped[j, i]} == (0, 198, 255)")
    #         if np.all(blue_cropped[j, i] == [255, 198, 0]):
    #             print(f"{blue_cropped[j, i]} == (0, 198, 255)")
    #             blue_cropped[j, i] = (0,0,0)
    #         else:
    #             blue_cropped[j, i] = (255, 255, 255)

    # blue_cropped = np.where(np.all(blue_cropped == (0, 198, 255), axis=2, keepdims=True), (255, 255, 255), blue_cropped)

    # blue_cropped[np.where(blue_cropped == (0, 198, 255), axis=2)] = (255, 255, 255)

    # for rgb in blue_cropped:
    #     if np.all(rgb == (0, 198, 255)):
    #         rgb = (255, 255, 255)
    #     else:
    #         rgb = (0, 0, 0)

    # blue_cropped = blue_cropped[np.where(blue_cropped==(0,198,255),255,0)]
    # print(blue_cropped)

    ret, thresh1 = cv2.threshold(cropped_gray, 150, 255, cv2.THRESH_BINARY)
    cv2.imshow("thresh", thresh1)
    cv2.imshow("blue", blue_cropped)
    cv2.imshow("binary", binary_image)
    cv2.imshow("binary2", binary_image2)
    cv2.waitKey(0)
    # time.sleep(1)
    #
    # x = 100
    # y = 100
    # pyautogui.moveTo(x, y)
    # pyautogui.click()
    # time.sleep(4)
    # turn_around()
    # out = True
    # h = 0
    # while out:
    #     time.sleep(0.5)
    #     image = get_image()
    #     battle = check_if_battle(image)
    #     if battle:
    #         out= False
    #         print("started battle")
    #         break
    #     else:
    #         print("not in battle")
    #         przod(0.5)
    #     h+=1
    #     if h == 100:
    #         out = False
    #         raise Exception("ERROR")
    #
    #
    # start_autobattle()
    #
    # in_battle = True
    # while in_battle:
    #     time.sleep(10)
    #     image = get_image()
    #     battle = check_if_endbattle(image)
    #     if battle:
    #         in_battle = False
    #         print("ended battle")
    #         break
    #     else:
    #         print("still in battle")
    #     h += 1
    #     if h == 100:
    #         out = False
    #         raise Exception("ERROR")
    #
    # print("END")
    #
    # # read_team_hp(image)
    # # read_hero_hp(image, 1)
    # image = get_image()
    # path = f"{os.getcwd()}\\test_images"
    # cv2.imwrite(f"{path}\\star_map_image.png", image)
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



import json
import math
import os
import random

from colorama import Fore
from copy import deepcopy
from typing import Union
from mss import mss
import cv2
import numpy as np
import PIL.ImageGrab
import time
import pyautogui
import keyboard
import torch
import win32api, win32con
from pynput.mouse import Button, Controller

from Class1.lvl_class import LVL
from dictionaries import in_battle_skillpoint_dict, out_of_battle_cord_dict, Cord, Herta_Space_Station_dict, \
    Storage_Zone_dict, Base_Zone_dict, Supply_Zone_dict
from gui import press_map, right, left, przod, tyl, turn_around, turn_right, turn_left, start_autobattle, turn, \
    press_map2, click_cords, attack
from utilities import show_images

colors = {0: (0,255,0),
          1: (46,139,87),
          2: (0,139,139),
          3: (0,255,255),
          4: (127,255,212),
          5: (255,0,255)}

IMAGE_WIDTH: int = 2560
IMAGE_HEIGHT: int = 1440
IMAGE_CHANNELS: int = 3
#RGB
hp_min = (214,253,255)
hp_max = (49,255,249)

lost_hp = (52,59,65)
lost_hp2 = (56,64,71)
GREEN = (0, 255, 0)

def load_model(planet):
    if planet == "Herta":
        model = torch.hub.load(f'ultralytics/yolov5', 'custom', path=f'E:/Honkai-Star-Rail-bot/model/herta_newest.pt')
    elif planet == "Jarilo4":
        model = torch.hub.load(f'ultralytics/yolov5', 'custom', path=f'E:/Honkai-Star-Rail-bot/model/jarilo6.pt')
    elif planet == "xianhou":
        # model = torch.hub.load(f'ultralytics/yolov5', 'custom',
        #                        path=f'E:/Honkai-Star-Rail-bot/model/hertaSpaceStation.pt')
        raise Exception("Not implemented model")
    else:
        raise Exception("wrong planet")
    return model

if __name__ == '__main__':
    time.sleep(1)
    model = load_model("Herta")
    # c_t_l = {0: "Automaton Spider",
    #          1: "Vagrant",
    #          2: "Automaton Beetle",
    #          3: "Automaton Hound",
    #          4: "Everwinter Shadewalker",
    #          5: "Flamespawn",
    #          6: "Frostspawn",
    #          7: "Imaginary Weaver",
    #          8: "Incineration Shadewalker",
    #          9: "Mask of No Thought",
    #          10: "Silvermane Cannoneer",
    #          11: "Silvermane Gunner",
    #          12: "Windspawn",
    #          13: "teleport",
    #          14: "ice statue"}

    c_t_l = {0:"eliminator",
             1:"disruptor",
             2:"reaver",
             3:"antibaryon",
             4: "trampler"}
sct = mss()
from PIL import Image
while True:
    # time.sleep(0.7)
    monitor = {'top': 0, 'left': 0, 'width': IMAGE_WIDTH, 'height': IMAGE_HEIGHT}
    img = Image.frombytes('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), sct.grab(monitor).rgb)
    # img = np.array(img)
    screen = np.array(img)
    # screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    screen = cv2.resize(screen, (640, 640))
    # print(screen)

    result = model(screen)
    print("result")
    # print(result)
    labels, cord = result.xyxyn[0][:, -1], result.xyxyn[0][:, :-1]
    print(labels)
    print(cord)
    n = len(labels)
    print(n)
    if n > 0:
        row = cord[0]
        if row[4] >= 0.5:
            x1, y1, x2, y2 = int(row[0] * 640), int(row[1] * 640), int(row[2] * 640), int(row[0] * 640)
            xc = (x1 + x2) / 2
            yc = (y1 + y2) / 2
            print(f"{Fore.GREEN} {xc} {yc} {(x2 - x1)} {Fore.RESET}")

            leb = labels[0].cpu()

    for i in range(n):
        row = cord[i]

        if row[4] >= 0.5:

            x1, y1, x2, y2 = int(row[0]*640), int(row[1]*640), int(row[2]*640), int(row[0]*640)
            cv2.rectangle(screen, (x1, y1), (x2, y2), colors[0] if i == 0 else colors[1], 2)
            # print(labels[i])
            leb = labels[i].cpu()
            cv2.putText(screen, f"{c_t_l[int(leb.item())]}", (x1, y1-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(screen, f"{row[4]:.2f}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    screen = cv2.resize(screen, (1920, 1080))
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    cv2.namedWindow("Screen")
    cv2.moveWindow("Screen", -2560, 0)
    cv2.imshow("Screen", screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
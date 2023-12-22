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
    Storage_Zone_dict, Base_Zone_dict, Supply_Zone_dict, star_map_dict, Jarilo_VI_dict, Outlying_Snow_Plains, templates
from gui import press_map, right, left, przod, tyl, turn_around, turn_right, turn_left, start_autobattle, turn, \
    press_map2, click_cords, attack, mouse_move, mouse_move2, press_keyboard
from main import locate_enemy_and_start_battle, w84endbattle, tp_parlor, load_model, read_json, combine1
from utilities import show_images
colors = {0: (0,255,0),
          1: (46,139,87),
          2: (0,139,139),
          3: (0,255,255),
          4: (127,255,212),
          5: (255,0,255)}
tp_cord = Cord(2341, 2342, 1299, 1300)
IMAGE_WIDTH: int = 2560
IMAGE_HEIGHT: int = 1440
IMAGE_CHANNELS: int = 3
#RGB
hp_min = (214,253,255)
hp_max = (49,255,249)

lost_hp = (52,59,65)
lost_hp2 = (56,64,71)
GREEN = (0, 255, 0)

def play():
    time.sleep(2)
    c = Cord(400, 400)
    c.move_and_click_cord()
    model = load_model("Herta")
    c_t_l = read_json(".//config//classes_herta.json")

    #Scroll map
    press_map2()
    time.sleep(1)
    print("scroll")
    for _ in range(10):
        pyautogui.scroll(-1)


    print("1")

    combine1(templates["supply_zone"])
    click_cords(Supply_Zone_dict["Spare Parts Warehouse"], slow=2)
    combine1(templates["teleport"])

    locate_enemy_and_start_battle(model)
    w84endbattle()

    print("10")
    press_map2()

    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["storage_zone"])
    click_cords(Storage_Zone_dict["Calyx (Crimson): Bud of Destruction"], slow=2)
    combine1(templates["teleport"])
    turn_around()
    przod(6)
    locate_enemy_and_start_battle(model)
    w84endbattle()

    print("2")


    press_map2()
    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["supply_zone"])
    click_cords(Supply_Zone_dict["Electrical Room"], slow=2)
    click_cords(Cord(1442, 1443, 999, 1000), slow=2)
    combine1(templates["teleport"])
    locate_enemy_and_start_battle(model)
    w84endbattle()

    print("11")
    press_map2()

    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["storage_zone"])
    click_cords(Storage_Zone_dict["Calyx (Crimson): Bud of Destruction"], slow=2)
    combine1(templates["teleport"])

    przod(4)
    turn(-30)
    przod(4)
    locate_enemy_and_start_battle(model)
    w84endbattle()

    print("3")

    press_map2()
    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["supply_zone"])
    click_cords(Supply_Zone_dict["Electrical Room"], slow=2)
    click_cords(Cord(1442, 1443, 999, 1000), slow=2)
    combine1(templates["teleport"])

    przod(10)

    locate_enemy_and_start_battle(model)
    w84endbattle()

    print("9")
    press_map2()
    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["storage_zone"])
    click_cords(Storage_Zone_dict["Outside_the_Control_Center"], slow=2)
    combine1(templates["teleport"])

    locate_enemy_and_start_battle(model)
    w84endbattle()

    print("4")

    press_map2()
    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["supply_zone"])
    Supply_Zone_dict["Calyx"].move_and_click_cord()
    combine1(templates["teleport"])

    turn(-162)
    przod(3.5)
    time.sleep(2)
    press_keyboard("f")
    time.sleep(2)
    przod(1)

    locate_enemy_and_start_battle(model, c_t_l)
    w84endbattle()

    print("8")
    press_map2()

    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["storage_zone"])
    click_cords(Storage_Zone_dict["Courtyard"], slow=2)
    click_cords(Cord(1570, 1571, 1007, 1008), slow=2)
    combine1(templates["teleport"])
    turn(-90)
    przod(0.5)
    locate_enemy_and_start_battle(model)
    w84endbattle()

    print("5")

    press_map2()

    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["supply_zone"])
    Supply_Zone_dict["Calyx"].move_and_click_cord()
    combine1(templates["teleport"])

    turn(-162)
    przod(3.5)
    time.sleep(2)
    press_keyboard("f")
    time.sleep(2)
    przod(1)
    turn(-90)
    przod(6)

    locate_enemy_and_start_battle(model, c_t_l)
    w84endbattle()


    print("6")

    press_map2()
    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["base_zone"])
    click_cords(Base_Zone_dict["Monitoring_Room"], slow=2)
    combine1(templates["teleport"])
    turn_around()
    przod(1)
    locate_enemy_and_start_battle(model)
    w84endbattle()


    print("7")
    press_map2()

    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    combine1(templates["storage_zone"])
    click_cords(Storage_Zone_dict["Courtyard"], slow=2)
    click_cords(Cord(1570, 1571, 1007, 1008), slow=2)
    combine1(templates["teleport"])

    locate_enemy_and_start_battle(model)
    w84endbattle()











if __name__ == "__main__":
    play()
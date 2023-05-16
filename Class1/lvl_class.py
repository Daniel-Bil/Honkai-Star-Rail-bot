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
import json

class LVL:
    def __init__(self):

        self.sequence_of_moves = ["move1", "move2"]
        self.number_of_enemies = 10


    def setup_lvl(self):
        #TODO load json with informations
        self.number_of_enemies = None
        pass

    def move(self):
        pass

    def handle_battle(self):
        pass

    def end_battle(self):
        pass

    def handle_move(self, move):
        pass

    def get_hero_position(self):
        pass

    def play_lvl(self):
        for i, move in enumerate(self.sequence_of_moves):
            self.handle_move(move)


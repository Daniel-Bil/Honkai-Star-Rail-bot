import os
import random

import cv2
import numpy as np
import PIL.ImageGrab
import time
import pyautogui
import keyboard
import win32api, win32con
from pynput.mouse import Button, Controller



def sprint():
    keyboard.press('left shift')
    time.sleep(0.1)
    keyboard.release('left shift')

def phone():
    pass

def press_keyboard(key):
    keyboard.press(f'{key}')
    time.sleep(random.uniform(0.1, 0.3))
    keyboard.release(f'{key}')

def press_map():
    keyboard.press('left alt')
    time.sleep(0.1)
    mouse = Controller()
    mouse.position = (200, 200)
    time.sleep(0.1)

    mouse.click(Button.left)
    time.sleep(0.1)

    keyboard.release('left alt')

def scroll(up=True):
    for _ in range(30):
        pyautogui.scroll(1 if up else -1)
    time.sleep(1)

def mouse_move(pos=(2400, 500)):
    time.sleep(0.1)
    mouse = Controller()
    mouse.position = pos
    time.sleep(0.1)

def mouse_move2(pos=(1350, 340)):
    time.sleep(0.2)
    mouse = Controller()
    mouse.position = pos
    mouse.position = (1350, 340)
    time.sleep(0.2)
    mouse.position = (1360, 340)
    time.sleep(0.2)
    mouse.position = (1340, 360)
    time.sleep(0.2)
    mouse.position = (1340, 350)
    time.sleep(0.2)
    mouse.position = pos
    time.sleep(0.2)

def press_map2(slow1=1,slow2=1):
    time.sleep(slow1)
    keyboard.press('m')
    time.sleep(slow1)
    keyboard.release('m')
    time.sleep(slow2)


def przod(run_time=0.1):

    keyboard.press('w')
    time.sleep(run_time)
    keyboard.release('w')


def tyl(run_time=0.1):
    time.sleep(0.1)
    keyboard.press('s')
    time.sleep(run_time)
    keyboard.release('s')
    time.sleep(0.1)

def right(run_time=0.1):

    time.sleep(0.1)
    keyboard.press('d')
    time.sleep(run_time)
    keyboard.release('d')
    time.sleep(0.1)

def left(run_time=0.1):

    time.sleep(0.1)
    keyboard.press('a')
    time.sleep(run_time)
    keyboard.release('a')
    time.sleep(0.1)


def start_autobattle():
    time.sleep(0.5)
    mouse = Controller()
    mouse.position = (2350, 67)
    time.sleep(0.5)

    mouse.click(Button.left)
    time.sleep(0.5)


def click_cords(cord, slow=0.1):
    mouse = Controller()
    time.sleep(slow)
    mouse.position = (cord.x1, cord.y1)
    time.sleep(slow)


    mouse.click(Button.left)
    time.sleep(slow)


def turn_around():
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 3085, 0, 0, 0)
    time.sleep(0.1)

def turn_right():
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1543, 0, 0, 0)
    time.sleep(0.1)

def turn_left():
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1543, 0, 0, 0)
    time.sleep(0.1)


def turn(value):
    deg = 3085/180.
    turn_value = deg * value
    value = int(turn_value)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, value, 0, 0, 0)
    time.sleep(0.1)


def attack(slow=0.1):
    time.sleep(slow)
    mouse = Controller()
    mouse.position = (1280, 720)
    mouse.click(Button.left)





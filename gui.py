import os

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

def press_map():
    keyboard.press('left alt')
    time.sleep(0.1)
    mouse = Controller()
    mouse.position = (200, 200)
    time.sleep(0.1)

    mouse.click(Button.left)
    time.sleep(0.1)

    keyboard.release('left alt')

def przod(run_time=0.1):
    time.sleep(0.1)
    keyboard.press('w')
    time.sleep(run_time)
    keyboard.release('w')
    time.sleep(0.1)

def tyl():
    time.sleep(0.1)
    keyboard.press('s')
    time.sleep(0.1)
    keyboard.release('s')
    time.sleep(0.1)

def right():

    time.sleep(0.1)
    keyboard.press('d')
    time.sleep(0.1)
    keyboard.release('d')
    time.sleep(0.1)

def left():

    time.sleep(0.1)
    keyboard.press('a')
    time.sleep(0.1)
    keyboard.release('a')
    time.sleep(0.1)


def start_autobattle():
    time.sleep(0.1)
    mouse = Controller()
    mouse.position = (2350, 67)
    time.sleep(0.1)

    mouse.click(Button.left)
    time.sleep(0.1)


def click_cords(cord):
    time.sleep(0.1)
    mouse = Controller()
    mouse.position = (cord.x1, cord.y1)
    mouse.click(Button.left)
    time.sleep(0.1)


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

def check_fight():
    pass

import time

import cv2
import keyboard
import numpy as np
import pyautogui

from pynput.mouse import Controller

from graphical_functions import get_screen
from wrappers import print_function_name

import win32api, win32con

@print_function_name
def mouse_move(x_pos: int, y_pos: int) -> None:
    mouse = Controller()
    time.sleep(0.1)
    mouse.position = (x_pos, y_pos)
    time.sleep(0.1)


@print_function_name
def mouse_click() -> None:
    pyautogui.mouseDown()
    pyautogui.sleep(0.1)
    pyautogui.mouseUp()


@print_function_name
def scroll(up=True):
    for _ in range(10):
        pyautogui.scroll(100 if up else -100)
    time.sleep(1)


@print_function_name
def press_map(slow1: float = 0.2, slow2: float = 1) -> None:
    """

    Args:
        slow1:
        slow2:

    Returns:

    """
    time.sleep(slow1)
    keyboard.press('m')
    time.sleep(slow1)
    keyboard.release('m')
    time.sleep(slow2)


@print_function_name
def check_template_exists(template: np.ndarray, screen: np.ndarray) -> bool:
    """

    Args:
        template:
        screen:

    Returns:
        True - yes found template
        False - no
    """
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.8)
    if loc[0].any():
        return True
    return False


@print_function_name
def locate_template(template: np.ndarray, screen: np.ndarray) -> tuple[int, int]:
    """

    Args:
        template:
        screen:

    Returns:

    """
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.7)

    p1, p2 = loc[::-1]

    return p1[0] + w/2, p2[0] + h/2


@print_function_name
def long_check_template_exists(template: np.ndarray, screen: np.ndarray) -> bool:
    number_of_checks = 0
    number_of_hits = 0
    while number_of_checks < 3:
        if number_of_checks > 2:
            print("Template missing")
            return False

        if number_of_hits > 2:
            print("Template found")
            return True

        result = check_template_exists(template, screen)

        if result:
            number_of_hits += 1
        else:
            number_of_checks += 1

        time.sleep(0.4)
    else:
        return False

@print_function_name
def click_template(p1: int, p2: int) -> None:
    mouse_move(p1, p2)
    mouse_click()


@print_function_name
def click_position(p1: int, p2: int) -> None:
    mouse_move(p1, p2)
    mouse_click()

@print_function_name
def choose_planet(template_button: np.ndarray, template_planet: np.ndarray) -> None:
    press_map()


    while True:
        screen = get_screen()
        if long_check_template_exists(template_button, screen):
            break

    position = locate_template(template_button, screen)
    click_template(position[0], position[1])
    time.sleep(1)

    while True:
        screen = get_screen()
        # cv2.imshow("name1", template_planet)
        # cv2.imshow("name2", screen)
        # cv2.waitKey(0)


        if long_check_template_exists(template_planet, screen):
            break

    position = locate_template(template_planet, screen)
    click_template(position[0], position[1])


def move_map(direction: str, x_pos: int, y_pos: int) -> None:
    mouse_move(x_pos, y_pos)
    pyautogui.mouseDown()
    pyautogui.sleep(0.1)

    if direction == "north":
        pyautogui.dragTo(x_pos, y_pos + 150, duration=0.2)

    elif direction == "south":
        pyautogui.dragTo(x_pos, y_pos - 150, duration=0.2)

    elif direction == "west":
        pyautogui.dragTo(x_pos + 150, y_pos, duration=0.2)
    elif direction == "east":
        pyautogui.dragTo(x_pos - 150, y_pos, duration=0.2)

    else:
        raise Exception("wrong direction")
    pyautogui.mouseUp()
    pyautogui.sleep(0.1)


def turn_around() -> None:
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 3085, 0, 0, 0)
    time.sleep(0.1)


def turn_right() -> None:
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1543, 0, 0, 0)
    time.sleep(0.1)


def turn_left() -> None:
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1543, 0, 0, 0)
    time.sleep(0.1)


def turn(value: int) -> None:
    deg = 3085/180.
    turn_value = int(deg * value)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, turn_value, 0, 0, 0)
    time.sleep(0.1)


def run_forward(run_time: float = 0.1) -> None:
    keyboard.press('w')
    time.sleep(run_time)
    keyboard.release('w')


def run_backwards(run_time: float = 0.1) -> None:
    keyboard.press('s')
    time.sleep(run_time)
    keyboard.release('s')


def run_right(run_time: float = 0.1) -> None:
    keyboard.press('d')
    time.sleep(run_time)
    keyboard.release('d')

def run_left(run_time: float = 0.1) -> None:
    keyboard.press('a')
    time.sleep(run_time)
    keyboard.release('a')

def press_keyboard(key: str = "f") -> None:
    keyboard.press(f'{key}')
    time.sleep(0.1)
    keyboard.release(f'{key}')

def wait(wait_time: float = 1):
    time.sleep(wait_time)

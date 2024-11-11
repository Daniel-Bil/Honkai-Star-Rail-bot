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

# from Herta_lvl import play
from dictionaries import in_battle_skillpoint_dict, out_of_battle_cord_dict, Cord, Herta_Space_Station_dict, \
    Storage_Zone_dict, Base_Zone_dict, Supply_Zone_dict, star_map_dict, Jarilo_VI_dict, Outlying_Snow_Plains, \
    Backwater_Pass, templates
from gui import press_map, right, left, przod, tyl, turn_around, turn_right, turn_left, start_autobattle, turn, \
    press_map2, click_cords, attack, mouse_move, mouse_move2, press_keyboard, scroll
from utilities import show_images
from wrappers import print_function_name

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
def check_fight(timer=10):
    h=0
    while True:

        time.sleep(5)
        image = get_image()
        battle = check_if_battle(image)
        if battle:
            time.sleep(1)
            start_autobattle()
            time.sleep(1)
            print("started autobattle")
            break
        if h > timer:
            print("no fight found")
            break
        h += 1
        print("waiting for battle")

def check_end_fight():
    h = 0
    while True:
        h+=1
        time.sleep(5)
        image = get_image()
        battle = check_if_endbattle(image)

        if battle:

            time.sleep(1)
            print("battle finished")
            break
        print("still in battle")

def create_mask(image, color):
    if color == "player":
        mask = ((200 < image[:, :, 0]) & (image[:, :, 0] <= 256) &
                (190 < image[:, :, 1]) & (image[:, :, 1] <= 256) &
                (0 <= image[:, :, 2]) & (image[:, :, 2] < 60))
    elif color == "enemy":
        mask = ((40 < image[:, :, 0]) & (image[:, :, 0] <= 120) &
                (40 < image[:, :, 1]) & (image[:, :, 1] <= 100) &
                (190 <= image[:, :, 2]) & (image[:, :, 2] < 256))
    else:
        raise Exception("Cant create mask")
    return mask
def read_json(path: str):
    with open(f'{path}', 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

def save_json(path, dict):
    with open(f"{path}", "w") as outfile:
        json.dump(dict, outfile)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate_distance(self, point: Union[np.ndarray, list, 'Point']):
        if isinstance(point, list) or isinstance(point, np.ndarray):
            if self.x == point[0] and self.y == point[1]:
                distance = 0
            else:
                x_distance = point[0]-self.x
                y_distance = point[1]-self.y
                distance = np.sqrt((x_distance**2 + y_distance**2))

        elif isinstance(point, Point):
            if self.x == point.x and self.y == point.y:
                distance = 0
            else:
                x_distance = point[0] - self.x
                y_distance = point[1] - self.y
                distance = np.sqrt((x_distance ** 2 + y_distance ** 2))
        else:
            raise Exception("Point calculate distance wrong point type")
        return distance

    def calculate_angle(self, point: Union[np.ndarray, list, 'Point']):

        v1 = point[1] - self.y
        v2 = point[0] - self.x
        print(f"v1 = {v1} v2 = {v2}, point = {point}   self = {self.x, self.y}")
        angle_rad = math.atan2(point[1] - self.y, point[0] - self.x)
        angle_deg = math.degrees(angle_rad)
        return angle_deg
        # if isinstance(point, list) or isinstance(point, np.ndarray):
        #     if self.x == point[0] and self.y == point[1]:
        #         raise Exception("no angle between the same point")
        #     else:
        #         if self.x == point[0] and not self.y == point[1]:
        #             pass
        #         elif not self.x == point[0] and self.y == point[1]:
        #             pass
        #         else:
        #             pass
        #
        # elif isinstance(point, Point):
        #     if self.x == point.x and self.y == point.y:
        #         angle = 0
        #     else:
        #         x_distance = point[0] - self.x
        #         y_distance = point[1] - self.y
        #         angle = np.sqrt((x_distance ** 2 + y_distance ** 2))
        # else:
        #     raise Exception("Point calculate distance wrong point type")
        # return angle






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

def w84endbattle():
    while True:
        img = get_image()
        battle = check_if_endbattle(img)
        time.sleep(3)
        if battle:
            print(f"{Fore.LIGHTRED_EX} END BATTLE {Fore.RESET}")
            break
        print("STILL IN BATTLE")

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


def get_screen(gray: bool = False) -> np.ndarray:
    pil_image = PIL.ImageGrab.grab()
    np_image = np.array(pil_image)
    if gray:
        np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    return np_image


def get_image(convert=True, place="all", gray=False):

    if place == "all":
        im = PIL.ImageGrab.grab()
    elif place == "map":
        im = PIL.ImageGrab.grab((63, 77, 312, 326))
    else:
        raise Exception("sas")

    image = np.array(im)
    if convert:
       image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if gray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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


def calculate_orientation(player, enemy, image):
    kernel = (2,2)

    print(f"img {image.shape}")
    player = cv2.dilate(player,kernel)
    # player = cv2.dilate(player,kernel)
    # player = cv2.dilate(player,kernel)
    # player = cv2.dilate(player,kernel)
    # player = cv2.dilate(player,kernel)
    # player = cv2.dilate(player,kernel)
    # player = cv2.dilate(player,kernel)
    contours, _ = cv2.findContours(player, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(enemy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image_copy = deepcopy(image)


    cnt = contours[0]
    M = cv2.moments(cnt)
    print(M)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    print(cx)
    print(cy)

    print(box)
    cv2.drawContours(image_copy, [box], 0, (0, 0, 255), 2)
    # cv2.drawContours(image_copy, [hull], 0, (255, 0, 0), 3)

    cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 3)
    cv2.drawContours(image_copy, contours2, -1, (0, 255, 0), 3)

    # cv2.circle(image_copy, box[0], radius=5, color=(255, 0, 0), thickness=-1)
    # cv2.circle(image_copy, box[1], radius=5, color=(0, 255, 255), thickness=-1)
    # cv2.circle(image_copy, box[2], radius=5, color=(0, 0, 0), thickness=-1)
    # cv2.circle(image_copy, box[3], radius=5, color=(0, 0, 255), thickness=-1)
    cv2.circle(image_copy, (cx,cy), radius=5, color=(127, 0, 204), thickness=-1)
    print(player.shape)
    reshaped_player = np.expand_dims(player, axis=2)
    reshaped_enemy = np.expand_dims(enemy, axis=2)
    player_rgb = np.repeat(reshaped_player, 3, axis=2)
    enemy_rgb = np.repeat(reshaped_enemy, 3, axis=2)
    place_holder1 = []
    point = Point(cx, cy)
    for i, b in enumerate(contours[0]):
        # print(b)
        b = b[0]

        distance = point.calculate_distance(b)
        # print(f"{i}: {distance}")
        place_holder1.append((distance, b))

    sorted_data = sorted(place_holder1, key=lambda x: x[0])

    cv2.circle(image_copy, sorted_data[0][1], radius=5, color=(0, 0, 0), thickness=-1)
    c_i = np.concatenate((cv2.resize(player_rgb,(700,700)),cv2.resize(enemy_rgb,(700,700)),cv2.resize(image_copy,(700,700))),axis=1)

    cv2.imshow("all", c_i)
    w, h, c = image.shape
    point2 = Point(w // 2, h // 2)
    print()
    print(point.calculate_angle([w//2, 10]))
    print(point.calculate_angle([w//2, 200]))
    print(point.calculate_angle([10, h//2]))
    print(point.calculate_angle([200, h//2]))
    # print(point.calculate_angle())


    print(contours2)
    # if len(contours2) == 1:
    cnt2 = contours2[0]
    # else:
    #     cnt2 = contours2[0]
    M2 = cv2.moments(cnt2)
    print(M2)
    c1x = int(M2['m10'] / M2['m00'])
    c1y = int(M2['m01'] / M2['m00'])

    point3 = Point(c1x, c1y)
    point4 = Point(*sorted_data[0][1])
    print(point4.calculate_angle([point2.x, point2.y]))
    angle = point.calculate_angle(sorted_data[0][1])
    print(angle)
    angle2 = point2.calculate_angle([point3.x, point3.y])
    print(angle2)

    angle_xd1 = angle
    angle_xd2 = angle2
    print(f"hero = {angle_xd1}")
    print(f"enemy = {angle_xd2}")
    f_a = -((180+angle_xd1)+angle_xd2)
    print(f"f_a = {f_a}")

    # turn_angle = int(3085//f_a)
    turn(f_a)

    cv2.circle(image_copy, sorted_data[1][1], radius=5, color=(255, 255, 255), thickness=-1)
    cv2.imwrite("XD.png", image_copy)


    cv2.imshow("2 closest", image_copy)



    cv2.waitKey(0)


def find_enemy():
    image = get_image()
    cord = Cord(63, 312, 77, 326)
    cropped = crop(image, cord)
    blue_cropped = deepcopy(cropped)
    player_mask = create_mask(blue_cropped, "player")
    enemy_mask = create_mask(blue_cropped, "enemy")
    binary_image = np.where(player_mask, 255, 0).astype(np.uint8)
    binary_image2 = np.where(enemy_mask, 255, 0).astype(np.uint8)
    image_copy = deepcopy(blue_cropped)
    calculate_orientation(binary_image, binary_image2, image_copy)

def load_model(planet: str="Herta"):
    """
    Function that loads model for current planet
    :param planet: name of the planet
    :return:
    """
    if planet == "Herta":
        model = torch.hub.load(f'ultralytics/yolov5', 'custom', path=f'E:/Honkai-Star-Rail-bot/model/herta_deeplearning_200.pt')
    elif planet == "Jarilo6":
        model = torch.hub.load(f'ultralytics/yolov5', 'custom', path=f'E:/Honkai-Star-Rail-bot/model/jarilo4.pt')
    elif planet == "xianzhou":
        # model = torch.hub.load(f'ultralytics/yolov5', 'custom',
        #                        path=f'E:/Honkai-Star-Rail-bot/model/hertaSpaceStation.pt')
        raise Exception("Not implemented model")
    elif planet == "panacony":
        raise Exception("Not implemented model")
    else:
        raise Exception("wrong planet")
    return model



def locate_enemy_and_start_battle(model, c_t_l= None):
    if c_t_l is None:
        c_t_l = {0: "eliminator",
                 1: "disruptor",
                 2: "reaver",
                 3: "antibaryon"}
    timeout = 0
    sct = mss()
    monitor = {'top': 0, 'left': 0, 'width': IMAGE_WIDTH, 'height': IMAGE_HEIGHT}
    from PIL import Image
    while True:
        # time.sleep(0.7)

        img = Image.frombytes('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), sct.grab(monitor).rgb)
        # img = np.array(img)
        whole_image = np.array(img)
        screen = np.array(img)
        # screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        screen = cv2.resize(screen, (640, 640))
        # print(screen)

        result = model(screen)

        labels, cord = result.xyxyn[0][:, -1], result.xyxyn[0][:, :-1]

        n = len(labels)
        print(n)
        if n > 0:
            timeout -= 1
            v = 0
            for h, c in enumerate(cord):
                if int(labels[h].cpu().item()) == 13 or int(labels[h].cpu().item()) == 14:
                    v = None
                    pass
                else:
                    row = cord[h]
                    v = h
                    break
            if v is not None:
                if row[4] >= 0.5:
                    x1, y1, x2, y2 = int(row[0] * 640), int(row[1] * 640), int(row[2] * 640), int(row[0] * 640)
                    xc = (x1 + x2) / 2
                    yc = (y1 + y2) / 2
                    print(f"{Fore.GREEN} {xc} {yc} {(x2 - x1)} {Fore.RESET}")
                    if 320 - 64 < xc < 320 + 64:
                        przod(0.1)
                        random_value3 = random.randint(0, 100)
                        if random_value3 < 5:
                            random_value4 = random.randint(0, 1)
                            if random_value4==0:
                                tyl(0.5)
                                right(0.5)
                            else:
                                tyl(0.5)
                                left(0.5)
                        if (x2 - x1) > 45:
                            attack()
                    elif xc < 320 - 64:
                        turn(-5)
                    elif xc > 320 - 64:
                        turn(5)
                    else:
                        print("XDDDD")

                    leb = labels[h].cpu()

                    cv2.rectangle(screen, (x1, y1), (x2, y2), colors[0], 2)
                    try:
                        cv2.putText(screen, f"{c_t_l[int(leb.item())]} {row[4]}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 255, 0), 2)
                    except:
                        pass
            else:
                print(f"{Fore.LIGHTMAGENTA_EX} LOOKING FOR ENEMY inside {timeout} < 60 {Fore.RESET}")
                random_value = random.randint(0, 1)
                random_value2 = random.randint(1, 100)
                if random_value == 0:
                    turn(random_value2)
                else:
                    turn(-random_value2)
                timeout += 1

            if timeout > 60:
                print(f"{Fore.RED} TIMEOUT NO ENEMY FOUND {Fore.RESET}")
                break

            battle = check_if_battle(whole_image)
            if battle:
                print(f"{Fore.LIGHTCYAN_EX} FIGHT STARTED {Fore.RESET}")
                time.sleep(4)
                print("start autobattle")
                start_autobattle()
                break
        else:
            print(f"{Fore.LIGHTMAGENTA_EX} LOOKING FOR ENEMY  {timeout} < 30 {Fore.RESET}")
            random_value = random.randint(0, 1)
            random_value2 = random.randint(1, 100)
            if random_value == 0:
                turn(random_value2)
            else:
                turn(-random_value2)
            timeout+=1

        if timeout > 30:
            print(f"{Fore.RED} TIMEOUT NO ENEMY FOUND {Fore.RESET}")
            break

        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        cv2.namedWindow("Screen")
        cv2.moveWindow("Screen", -2560, 0)
        cv2.imshow("Screen", screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def tp_parlor():
    press_map2()
    tp_cord = Cord(2341, 2342, 1299, 1300)
    Herta_Space_Station_dict["parlor_car"].move_and_click_cord()

    ############### FIRST TP ##############################
    Cord(977, 978, 676, 677).move_and_click_cord()
    tp_cord.move_and_click_cord(slow5=4)
@print_function_name
def long_check_template_exists(template: np.ndarray, screen: np.ndarray) -> bool:
    number_of_checks = 0
    number_of_hits = 0
    while number_of_checks < 5:
        if number_of_checks > 5:
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

        time.sleep(1)



@print_function_name
def check_template_exists(template: np.ndarray, screen: np.ndarray) -> bool:
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.8)
    if loc[0].any():
        return True
    return False

@print_function_name
def return_template_location(template: np.ndarray, screen: np.ndarray) -> tuple[int, int]:
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.8)

    p1, p2 = loc[::-1]

    return p1[0] + w/2, p2[0] + h/2


def wait_for_template(template):
    time.sleep(1)
    print("w8 for template")
    start = True
    while start:
        image = get_image(gray=True)

        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.8)
        for _ in zip(*loc[::-1]):
            start = False
            break

def locate_template(template):
    time.sleep(1)
    print("locate template")

    image = get_image(gray=True)

    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.85)
    p1, p2 = loc[::-1]
    if len(p1)>1:
        return p1[0], p2[0]

def combine1(template):
    print(f"{Fore.GREEN}Combine1{Fore.RESET}")
    wait_for_template(template)
    cord = locate_template(template)
    w, h = template.shape[::-1]
    c = Cord(cord[0]+w//2, cord[1]+h//2)
    c.move_and_click_cord()
    time.sleep(2)



if __name__ == '__main__':






    time.sleep(2)
    c = Cord(400,400)
    c.move_and_click_cord()



    all = True
    if all:

        model = load_model("Herta")


        c_t_l = read_json(".//config//classes_herta.json")


        press_map2()
        time.sleep(1)
        print("scroll")
        for _ in range(10):
            pyautogui.scroll(-1)

        ############### FIRST TP ############################## PARLOR CAR
        print("tp to parlor car")
        click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
        click_cords(Cord(977, 978, 676, 677), slow=2)


        combine1(templates["teleport"])
        # wait_for_template(templates["teleport"])
        #
        # click_cords(tp_cord, slow=0.1)
        wait_for_template(templates["nameless_template"])
        ############### SECOND TP ############################## STORAGE Zone
        print("tp to storage zone")
        press_map2()
        click_cords(Herta_Space_Station_dict["storage_zone"], slow=2)
        click_cords(Storage_Zone_dict["Courtyard"], slow=2)
        click_cords(Cord(1570, 1571, 1007, 1008), slow=2)
        # wait_for_template(templates["teleport"])
        # click_cords(tp_cord, slow=1)
        combine1(templates["teleport"])
        wait_for_template(templates["nameless_template"])
        locate_enemy_and_start_battle(model)
        w84endbattle()
        tp_parlor()
        print("tp to storage zone")
        press_map2()
        click_cords(Herta_Space_Station_dict["storage_zone"], slow=2)
        click_cords(Storage_Zone_dict["Courtyard"], slow=2)
        click_cords(Cord(1570, 1571, 1007, 1008), slow=2)
        click_cords(tp_cord, slow=4)
        turn(-90)
        przod(0.2)
        locate_enemy_and_start_battle(model)
        w84endbattle()

        tp_parlor()
        ############### SECOND TP2 ############################## STORAGE Zone
        press_map2()
        click_cords(Herta_Space_Station_dict["storage_zone"], slow=2)
        click_cords(Storage_Zone_dict["Calyx (Crimson): Bud of Destruction"], slow=2)
        click_cords(tp_cord, slow=4)
        turn_around()
        przod(6)

        locate_enemy_and_start_battle(model)
        w84endbattle()
        tp_parlor()
        ############### SECOND TP3 ############################## STORAGE Zone
        press_map2()
        click_cords(Herta_Space_Station_dict["storage_zone"], slow=2)
        click_cords(Storage_Zone_dict["Outside_the_Control_Center"], slow=2)
        click_cords(tp_cord, slow=4)

        locate_enemy_and_start_battle(model)
        w84endbattle()
        tp_parlor()

        ############### SECOND TP4 ############################## STORAGE Zone
        press_map2()
        click_cords(Herta_Space_Station_dict["storage_zone"], slow=2)
        click_cords(Storage_Zone_dict["Outside_the_Control_Center"], slow=2)
        click_cords(tp_cord, slow=4)

        przod(4)
        turn(-30)
        przod(4)
        locate_enemy_and_start_battle(model)
        w84endbattle()


        #################### THIRD TP ######################
        print("base zone teleport")
        press_map2()
        click_cords(Herta_Space_Station_dict["base_zone"], slow=2)
        click_cords(Base_Zone_dict["Monitoring_Room"], slow=2)
        click_cords(tp_cord, slow=4)
        turn_around()
        przod(1)
        locate_enemy_and_start_battle(model)
        w84endbattle()

        #################### FOURTH TP ######################

        print("supply zone")
        press_map2()
        click_cords(Herta_Space_Station_dict["supply_zone"], slow=2)
        click_cords(Supply_Zone_dict["Spare Parts Warehouse"], slow=2)
        click_cords(tp_cord, slow=4)


        locate_enemy_and_start_battle(model)
        w84endbattle()

        ################# PARLOR CAR ################################
        press_map2()
        click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
        click_cords(Cord(977, 978, 676, 677), slow=2)
        click_cords(tp_cord, slow=4)

        ################ SIXTH TP####################
        press_map2()

        click_cords(Herta_Space_Station_dict["supply_zone"], slow=2)
        click_cords(Supply_Zone_dict["Electrical Room"], slow=2)
        click_cords(Cord(1442, 1443, 999, 1000), slow=2)
        click_cords(tp_cord, slow=4)

        locate_enemy_and_start_battle(model)
        w84endbattle()

        przod(10)

        locate_enemy_and_start_battle(model)
        w84endbattle()
        ######################### seventh tp #######################
        tp_parlor()

        press_map2()

        Herta_Space_Station_dict["supply_zone"].move_and_click_cord()
        Supply_Zone_dict["Calyx"].move_and_click_cord()
        tp_cord.move_and_click_cord(slow5=4)

        turn(-162)
        przod(3.5)
        time.sleep(2)
        press_keyboard("f")
        time.sleep(2)
        przod(1)

        locate_enemy_and_start_battle(model, c_t_l)
        w84endbattle()

        ####################### eight tp ##################

        tp_parlor()

        press_map2()

        Herta_Space_Station_dict["supply_zone"].move_and_click_cord()
        Supply_Zone_dict["Calyx"].move_and_click_cord()
        tp_cord.move_and_click_cord(slow5=4)

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

        ##################### nineth tp ######################

        tp_parlor()

        press_map2()

        Herta_Space_Station_dict["supply_zone"].move_and_click_cord()
        Supply_Zone_dict["Spare Parts Warehouse"].move_and_click_cord()
        tp_cord.move_and_click_cord(slow5=4)

        turn(95)
        przod(6)
        turn(90)
        przod(5)
        locate_enemy_and_start_battle(model, c_t_l)
        w84endbattle()


    ##################################################################################################################
    ################### JARILO 6 #########################################
    ##################################################################################################################
    time.sleep(2)
    print(f"{Fore.RED} TELEPORT TO JARILO {Fore.RESET}")
    model = load_model("Jarilo6")
    c_t_l = {0: "Automaton Spider",
             1: "Vagrant",
             2: "Automaton Beetle",
             3: "Automaton Hound",
             4: "Everwinter Shadewalker",
             5: "Flamespawn",
             6: "Frostspawn",
             7: "Imaginary Weaver",
             8: "Incineration Shadewalker",
             9: "Mask of No Thought",
             10: "Silvermane Cannoneer",
             11: "Silvermane Gunner",
             12: "Windspawn",
             13: "teleport",
             14: "ice statue"}

    press_map2()
    click_cords(Cord(2399, 2400, 183, 184), slow=2)
    print("jarilo6")
    mouse_move((star_map_dict["Jarilo-VI"].x1, star_map_dict["Jarilo-VI"].y1))
    # mouse_move2()


    pyautogui.mouseDown()
    pyautogui.sleep(0.1)
    pyautogui.mouseUp()
    print("0.2")
    pyautogui.mouseDown()
    pyautogui.sleep(0.2)
    pyautogui.mouseUp()
    print("0.3")
    pyautogui.mouseDown()
    pyautogui.sleep(0.3)
    pyautogui.mouseUp()
    mouse_move((1000, 500))
    scroll(up=False)
    time.sleep(3)

    mouse_move((2400,700))
    print("scroll")
    scroll(up=True)
    time.sleep(3)

    # ############### FIRST TP ############################## PARLOR CAR
    # print("tp to parlor car")
    # click_cords(Herta_Space_Station_dict["parlor_car"], slow=2)
    # click_cords(Cord(977, 978, 676, 677), slow=2)
    # click_cords(tp_cord, slow=4)

    #################### Jarilo 1 tp ############################
    click_cords(Jarilo_VI_dict["Outlying Snow Plains"], slow=2)
    click_cords(Outlying_Snow_Plains["Bud of The Hunt"], slow=2)
    click_cords(tp_cord, slow=4)

    turn(-100)
    przod(13)
    # locate_enemy_and_start_battle(model, c_t_l)
    # w84endbattle()

    # time.sleep(2)

    # locate_enemy_and_start_battle(model, c_t_l)
    # w84endbattle()

    # time.sleep(2)

    locate_enemy_and_start_battle(model, c_t_l)
    w84endbattle()

    time.sleep(2)

    locate_enemy_and_start_battle(model, c_t_l)
    w84endbattle()

    tp_parlor()
    press_map2()
    mouse_move()

    mouse_move((2400, 700))
    print("scroll")
    scroll(up=True)
    time.sleep(10)

    click_cords(Jarilo_VI_dict["Outlying Snow Plains"], slow=2)
    click_cords(Outlying_Snow_Plains["Long Slope"], slow=2)
    Cord(1405, 1000).move_and_click_cord()
    click_cords(tp_cord, slow=4)

    turn(-120)
    przod(6)

    locate_enemy_and_start_battle(model, c_t_l)
    w84endbattle()

    tp_parlor()
    press_map2()
    mouse_move()

    mouse_move((2400, 700))
    print("scroll")
    scroll(up=True)
    time.sleep(10)

    click_cords(Jarilo_VI_dict["Outlying Snow Plains"], slow=2)
    click_cords(Outlying_Snow_Plains["Calyx (Golden)"], slow=2)
    click_cords(tp_cord, slow=4)

    turn(-90)
    locate_enemy_and_start_battle(model, c_t_l)
    w84endbattle()

    ###################################################################################################################
    #                                        BACKWATER PASS
    ###################################################################################################################
    for _ in range(3):
        press_map2()
        mouse_move((2400, 700))
        scroll(up=True)
        press_map2()
        time.sleep(2)
        tp_parlor()
        press_map2()
        mouse_move((2400, 700))
        scroll()
        Jarilo_VI_dict["Backwater Pass"].move_and_click_cord()
        Backwater_Pass["Transport Hub"].move_and_click_cord()
        tp_cord.move_and_click_cord(slow5=4)
        turn(180)
        przod(5.5)
        locate_enemy_and_start_battle(model, c_t_l)
        w84endbattle()
    #######################################################




    ###################################
    press_map2()
    mouse_move((2400, 700))

    scroll(up=True)
    press_map2()
    tp_parlor()
    press_map2()
    mouse_move((2400, 700))
    scroll()
    Jarilo_VI_dict["Backwater Pass"].move_and_click_cord()
    Backwater_Pass["Calyx (Crimson)"].move_and_click_cord()
    Cord(1300, 1100).move_and_click_cord()
    tp_cord.move_and_click_cord(slow5=4)
    turn(-45)
    przod(1)
    locate_enemy_and_start_battle(model,c_t_l)
    w84endbattle()


    ###################################
    press_map2()
    mouse_move((2400, 700))
    scroll(up=True)
    press_map2()
    tp_parlor()
    press_map2()
    scroll()
    Jarilo_VI_dict["Backwater Pass"].move_and_click_cord()
    Backwater_Pass["Calyx (Crimson)"].move_and_click_cord()
    Cord(1300, 1000).move_and_click_cord()
    tp_cord.move_and_click_cord(slow5=4)
    turn(180)
    przod(1)
    locate_enemy_and_start_battle(model,c_t_l)
    w84endbattle()

    ###################################
    press_map2()
    mouse_move((2400, 700))
    press_map2()
    scroll(up=True)
    tp_parlor()
    press_map2()
    mouse_move((2400, 700))
    scroll()
    Jarilo_VI_dict["Backwater Pass"].move_and_click_cord()
    Backwater_Pass["Goethe Mansion"].move_and_click_cord()
    tp_cord.move_and_click_cord(slow5=4)
    przod(3)
    turn(-45)
    przod(4)
    locate_enemy_and_start_battle(model, c_t_l)
    w84endbattle()

    ###################################
    press_map2()
    mouse_move((2400, 700))
    press_map2()
    scroll(up=True)
    tp_parlor()
    press_map2()
    mouse_move((2400, 700))
    scroll()
    Jarilo_VI_dict["Backwater Pass"].move_and_click_cord()
    Backwater_Pass["Goethe Mansion"].move_and_click_cord()
    tp_cord.move_and_click_cord(slow5=4)
    przod(3)
    turn(-45)
    przod(4)
    locate_enemy_and_start_battle(model, c_t_l)
    w84endbattle()

    print("END PROGRAM")

















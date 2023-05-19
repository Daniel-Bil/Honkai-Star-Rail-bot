import json
import math
import os
from copy import deepcopy
from typing import Union

import cv2
import numpy as np
import PIL.ImageGrab
import time
import pyautogui
import keyboard
import win32api, win32con
from pynput.mouse import Button, Controller

from Class1.lvl_class import LVL
from dictionaries import in_battle_skillpoint_dict, out_of_battle_cord_dict, Cord, Herta_Space_Station_dict, \
    Storage_Zone_dict
from gui import press_map, right, left, przod, tyl, turn_around, turn_right, turn_left, start_autobattle, turn, \
    press_map2, click_cords
from utilities import show_images

IMAGE_WIDTH: int = 2560
IMAGE_HEIGHT: int = 1440
IMAGE_CHANNELS: int = 3
#RGB
hp_min = (214,253,255)
hp_max = (49,255,249)

lost_hp = (52,59,65)
lost_hp2 = (56,64,71)

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
def read_json(path):
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


def get_image(convert=True, place="all"):
    if place == "all":
        im = PIL.ImageGrab.grab()
    elif place == "map":
        im = PIL.ImageGrab.grab((63, 77, 312, 326))
    else:
        raise Exception("XD")

    image = np.array(im)
    if convert:
       image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
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
    # cv2.drawContours(image_copy, [box], 0, (0, 0, 255), 2)
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

    # cv2.imshow("all", c_i)
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


    # cv2.imshow("2 closest", image_copy)



    # cv2.waitKey(0)


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


if __name__ == '__main__':
    time.sleep(1)

    img = get_image(place = "map")
    show_images(img)


    # click_cords(Cord(200,201,200,201))
    # time.sleep(1)
    # print("start")
    # #Create lvl1
    # lvl = LVL()
    # lvl.number_of_enemies = 3
    # lvl.planet = "Herta_Space_Station"
    # lvl.room = "storage_zone"
    #
    # lvl.sequence_of_moves = [
    #                          press_map2(),
    #                          click_cords(Storage_Zone_dict["Courtyard"], slow=2),
    #                          click_cords(Cord(1570, 1571, 1007, 1008), slow=2),
    #                          click_cords(Cord(2341, 2342, 1299, 1300), slow=4)]

    # [turn(-10),
    #  przod(4.8),
    #  find_enemy(),
    #  przod(5),
    #  click_cords(Cord(1200, 1201, 1001, 1002)),
    #  check_fight(1),
    #  check_end_fight(),
    #  press_map2(),
    #  click_cords(Storage_Zone_dict["Courtyard"], slow=2),
    #  click_cords(Cord(1570, 1571, 1007, 1008), slow=2),
    #  click_cords(Cord(2341, 2342, 1299, 1300), slow=4)]


                            # press_map2(),
                            #  click_cords(Herta_Space_Station_dict[lvl.room], slow=2),
                            #  click_cords(Storage_Zone_dict["Calyx (Crimson): Bud of Destruction"], slow=2),
                            #  click_cords(Cord(2341, 2342, 1299, 1300), slow=4),
                            #  print("teleported to storage zone"),
                            #  tyl(6.5),
                            #  left(3.3),
                            #  przod(6.7),
                            #  left(2.3),
                            #  tyl(4.2),
                            #  check_fight(1),
                            #  check_end_fight(),
                            #  press_map2(),
                            #  click_cords(Storage_Zone_dict["Outside_the_Control_Center"], slow=2),
                            #  click_cords(Cord(2341, 2342, 1299, 1300), slow=4),
                            #  find_enemy(),
                            #  przod(2),
                            #  check_fight(5),
                            #  check_end_fight()],

    # lvl.sequence_of_moves = [press_map2(),
    #                          click_cords(Herta_Space_Station_dict[lvl.room],slow=2),
    #                          click_cords(Storage_Zone_dict["Calyx (Crimson): Bud of Destruction"],slow=2),
    #                          click_cords(Cord(2341,2342,1299,1300),slow=4),
    #                          print("teleported to storage zone"),
    #                          tyl(6.5),
    #                          left(3.3),
    #                          przod(6.7),
    #                          left(2.3),
    #                          tyl(4.2),
    #                          check_fight(1),
    #                          check_end_fight(),
    #                          press_map2(),
    #                          click_cords(Storage_Zone_dict["Outside_the_Control_Center"],slow=2),
    #                          click_cords(Cord(2341,2342,1299,1300),slow=4),
    #                          find_enemy(),
    #                          przod(2),
    #                          check_fight(5),
    #                          check_end_fight()]
    print("END PROGRAM")
    # lvl.play_lvl()
    # time.sleep(1)
    # click_cords(Cord(200,201,200,201))
    #
    #
    # tyl(6.5)
    # turn_around()










    # jsonStr = json.dumps(Cord(1,2,3,4).__dict__)
    # time.sleep(4)
    # przod(0.2)
    # time.sleep(1)
    # image = get_image()
    # image = cv2.imread(f"{os.getcwd()}\\test_images\\enemy_on_map_image.png")
    # cord = Cord(63, 312, 77, 326)
    # cropped = crop(image, cord)
    # # cv2.imshow("name", cropped)
    # cropped_gray = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
    # # cv2.imwrite(f"{os.getcwd()}\\test_images\\locked_enemy.png", image)
    # # threshold = cv2.threshold()
    # blue_cropped = deepcopy(cropped)
    #
    # # blue_cropped[np.all(blue_cropped == (0, 198, 255), axis=2)] = (255, 255, 255)
    # # blue_cropped[np.all(blue_cropped == (255, 198, 0), axis=2)] = (255, 255, 255)
    # # print((200 < blue_cropped[:, :, 0]) & (blue_cropped[:, :, 0] < 256) &
    # #       (190 < blue_cropped[:, :, 1]) & (blue_cropped[:, :, 1] < 256) &
    # #       (0 < blue_cropped[:, :, 2]) & (blue_cropped[:, :, 2] < 60))
    #
    #
    # player_mask = create_mask(blue_cropped, "player")
    # enemy_mask = create_mask(blue_cropped, "enemy")
    #
    # binary_image = np.where(player_mask, 255, 0).astype(np.uint8)
    # binary_image2 = np.where(enemy_mask, 255, 0).astype(np.uint8)
    # print(player_mask)
    # # blue_cropped = blue_cropped[blue_cropped[:,:,0]]
    # # blue_cropped[~np.all(
    # #     (blue_cropped[:, :, 0] > 230) & (150 < blue_cropped[:, :, 1]) & (blue_cropped[:, :, 1] < 250) & (
    # #                 0 < blue_cropped[:, :, 2]) & (blue_cropped[:, :, 2] < 70), axis=1)] = (0, 0, 0)
    # # w, h, _ = blue_cropped.shape
    # # print(w, h)
    # # print(blue_cropped[0,0])
    # # for i in range(w):
    # #     for j in range(h):
    # #         print(f"{blue_cropped[j, i]} == (0, 198, 255)")
    # #         if np.all(blue_cropped[j, i] == [255, 198, 0]):
    # #             print(f"{blue_cropped[j, i]} == (0, 198, 255)")
    # #             blue_cropped[j, i] = (0,0,0)
    # #         else:
    # #             blue_cropped[j, i] = (255, 255, 255)
    #
    # # blue_cropped = np.where(np.all(blue_cropped == (0, 198, 255), axis=2, keepdims=True), (255, 255, 255), blue_cropped)
    #
    # # blue_cropped[np.where(blue_cropped == (0, 198, 255), axis=2)] = (255, 255, 255)
    #
    # # for rgb in blue_cropped:
    # #     if np.all(rgb == (0, 198, 255)):
    # #         rgb = (255, 255, 255)
    # #     else:
    # #         rgb = (0, 0, 0)
    #
    # # blue_cropped = blue_cropped[np.where(blue_cropped==(0,198,255),255,0)]
    # # print(blue_cropped)
    #
    # ret, thresh1 = cv2.threshold(cropped_gray, 150, 255, cv2.THRESH_BINARY)
    #
    #
    #
    #
    #
    # contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # image_copy = deepcopy(blue_cropped)
    #
    #
    #
    #
    # calculate_orientation(binary_image, binary_image2, image_copy)
    #






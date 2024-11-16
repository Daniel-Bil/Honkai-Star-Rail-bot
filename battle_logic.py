import random
import time

import cv2
from colorama import Fore

from graphical_functions import get_screen
from gui_functions import turn, run_forward, run_backwards, run_right, run_left, mouse_click, check_template_exists
from wrappers import print_function_name

INPUT_WIDTH = 640
INPUT_HEIGHT = 640

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


@print_function_name
def locate_enemy_and_start_battle(yolo_model, enemy_classes: dict, battle_template) -> bool:
    timeout = 0

    while True:
        timeout -= 1  # every check increase timeout

        if (timeout < -50) or (timeout > 50):
            print(f"{Fore.RED} TIMEOUT NO ENEMY FOUND {Fore.RESET}")
            return False


        screen = get_screen()

        resized_screen = cv2.resize(screen, (640, 640))

        result = yolo_model(resized_screen)

        labels, cords = result.xyxyn[0][:, -1], result.xyxyn[0][:, :-1]

        number_of_detections = len(labels)

        if number_of_detections < 1:
            print(f"{Fore.LIGHTMAGENTA_EX} LOOKING FOR ENEMY  timeout: {timeout} < 30 | detections: {number_of_detections} {Fore.RESET} ")
            random_value = random.randint(1, 90)
            turn(random_value)
            timeout += 1
            continue

        # some labels are not enemies but model knows them because it can be a mistake
        for idx, cord in enumerate(cords):
            if not (int(labels[idx].cpu().item()) == 13 or int(labels[idx].cpu().item()) == 14):
                row = cords[idx]
                enemy_class_name = enemy_classes[labels[idx].cpu().item()]
                break
        else:
            continue




        Certainty: float = 0.5

        if row[4] >= Certainty:
            print(f"idk testing {int(row[0] * 640)} {int(row[1] * 640)} {int(row[2] * 640)} {int(row[3] * 640)}")

            x1, y1, x2, y2 = int(row[0] * INPUT_WIDTH), int(row[1] * INPUT_HEIGHT), int(row[2] * INPUT_WIDTH), int(row[0] * INPUT_HEIGHT)
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2

            bbox_width = x2 - x1
            bbox_height = y1 - y2
            print(f"{Fore.GREEN} {x_center} {y_center} {bbox_width} {bbox_height} {Fore.LIGHTCYAN_EX} {enemy_class_name} {row[4]} {Fore.RESET}")

            if 320 - 64 < x_center < 320 + 64:
                run_forward(1)

                # TODO THINK ABOUT BETTER SOLUTION TO ENVIRONMENTAL OBSTACLES
                if random.randint(0, 100) < 5:
                    run_backwards(0.5)
                    if random.randint(0, 1) == 0:
                        run_right(0.5)
                    else:
                        run_left(0.5)

                # 20 % of screen -> finetune value
                if (x2 - x1) > INPUT_WIDTH * 0.2:
                    mouse_click() # click to attack enemy

            elif x_center < 320 - INPUT_WIDTH * 0.1:
                if (x_center < 320 - INPUT_WIDTH * 0.2):
                    turn(-10)
                else:
                    turn(-5)

            elif x_center > 320 - INPUT_WIDTH * 0.1:
                if (x_center > 320 - INPUT_WIDTH * 0.2):
                    turn(10)
                else:
                    turn(5)

            else:
                raise Exception("this value shouldn't be possible")

            if check_template_exists(battle_template, screen):
                print(f"{Fore.LIGHTCYAN_EX} FIGHT DETECTED {Fore.RESET}")
                return True


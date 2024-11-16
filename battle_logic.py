import random
import time

import cv2
from colorama import Fore

from graphical_functions import get_screen
from gui_functions import turn, run_forward, run_backwards, run_right, run_left, mouse_click, check_template_exists
from wrappers import print_function_name

INPUT_WIDTH = 640
INPUT_HEIGHT = 640


@print_function_name
def locate_enemy_and_start_battle(yolo_model, enemy_classes: dict, battle_template) -> bool:
    timeout = 0
    last_check_was_enemy = False
    while True:


        if (timeout < -50) or (timeout > 100):
            print(f"{Fore.RED} TIMEOUT NO ENEMY FOUND {Fore.RESET}")
            return False

        screen = get_screen()

        if check_template_exists(battle_template, screen):
            print(f"{Fore.LIGHTCYAN_EX} FIGHT DETECTED {Fore.RESET}")
            return True

        resized_screen = cv2.resize(screen, (640, 640))

        result = yolo_model(resized_screen)

        labels, cords = result.xyxyn[0][:, -1], result.xyxyn[0][:, :-1]

        number_of_detections = len(labels)

        print(f"{Fore.LIGHTMAGENTA_EX} LOOKING FOR ENEMY  timeout: -50 < {timeout} < 100 | detections: {number_of_detections} {Fore.RESET} ")

        if number_of_detections < 1:
            timeout -= 1  # every check increase timeout



            random_value = random.randint(1, 50)
            if last_check_was_enemy:
                last_check_was_enemy = False
                random_value /= 10


            turn(random_value)
            continue


        # some labels are not enemies but model knows them because it can be a mistake
        for idx, cord in enumerate(cords):
            if not (int(labels[idx].cpu().item()) == 13 or int(labels[idx].cpu().item()) == 14):
                row = cords[idx]
                enemy_class_name = enemy_classes[str(int(labels[idx].cpu().item()))]
                break
        else:
            continue

        timeout += 1


        Certainty: float = 0.5

        if row[4] >= Certainty:
            last_check_was_enemy = True
            x1, y1, x2, y2 = int(row[0] * INPUT_WIDTH), int(row[1] * INPUT_HEIGHT), int(row[2] * INPUT_WIDTH), int(row[0] * INPUT_HEIGHT)
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2

            bbox_width = x2 - x1
            bbox_height = y1 - y2
            print(f"{Fore.GREEN} {x_center} {y_center} {bbox_width} {bbox_height} {Fore.LIGHTCYAN_EX} {enemy_class_name} prob: {row[4]:^.3} {Fore.RESET}")

            if 320 - 64 < x_center < 320 + 64:
                run_forward(0.7)

                # TODO THINK ABOUT BETTER SOLUTION TO ENVIRONMENTAL OBSTACLES
                if random.randint(0, 100) < 5:
                    run_backwards(0.5)
                    if random.randint(0, 1) == 0:
                        run_right(0.5)
                    else:
                        run_left(0.5)

                # 12 % of screen -> finetune value
                if bbox_width > INPUT_WIDTH * 0.12:
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
                print("fight started probably")




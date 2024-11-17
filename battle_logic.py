import random
import time

import cv2
import numpy as np
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
    last_check_x_center = 0
    enemy_widths = []
    while True:


        if (timeout < -40) or (timeout > 100):
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

        print(f"{Fore.LIGHTMAGENTA_EX} LOOKING FOR ENEMY  timeout: -40 < {timeout} < 100 | detections: {number_of_detections} {len(cords)} {Fore.RESET} ")

        if number_of_detections < 1:
            timeout -= 1  # every check increase timeout

            random_value = random.randint(1, 50)
            if (INPUT_WIDTH // 2) * 0.8 < last_check_x_center < (INPUT_WIDTH // 2) * 1.2:
                run_forward(0.5)
                last_check_x_center = 0

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
            print("detections more than 1 but continue")
            continue

        timeout += 1


        Certainty: float = 0.5

        if row[4] >= Certainty:
            last_check_was_enemy = True

            x1, y1, x2, y2 = int(row[0] * INPUT_WIDTH), int(row[1] * INPUT_HEIGHT), int(row[2] * INPUT_WIDTH), int(row[0] * INPUT_HEIGHT)
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2

            last_check_x_center = x_center

            bbox_width = x2 - x1
            bbox_height = y1 - y2
            enemy_widths.append(bbox_width)
            print(f"{Fore.GREEN} x_c={x_center} y_c={y_center} width={bbox_width} height={bbox_height} {Fore.LIGHTCYAN_EX} {enemy_class_name} {Fore.LIGHTMAGENTA_EX} {row[4]*100:^.2} % {Fore.RESET}")

            if (INPUT_WIDTH//2) * 0.7 < x_center < (INPUT_WIDTH//2) * 1.3:
                run_forward(0.7)

                if len(enemy_widths) > 4:
                    mean = np.mean(enemy_widths[-5:-1])

                    if mean - 2 < bbox_width < mean + 2:
                        print(f"{mean - 2} < {bbox_width} < {mean + 2}")
                        print(f"{enemy_widths[-5:-1]}, {mean}")
                        run_backwards(0.4)
                        if random.randint(0, 1) == 0:
                            run_right(0.6)
                        else:
                            run_left(0.6)
                        enemy_widths = []

                # 12 % of screen -> finetune value
                print(f"{bbox_width} > {INPUT_WIDTH * 0.06}")
                if bbox_width > INPUT_WIDTH * 0.06:
                    mouse_click() # click to attack enemy

            elif x_center < 320 - INPUT_WIDTH * 0.1:
                if (x_center < 320 - INPUT_WIDTH * 0.2):
                    turn(-5)
                else:
                    turn(-2)

            elif x_center > 320 - INPUT_WIDTH * 0.1:
                if (x_center > 320 - INPUT_WIDTH * 0.2):
                    turn(5)
                else:
                    turn(2)

            else:
                print("fight started probably")




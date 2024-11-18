import sys
import time

import cv2
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import QThread, Signal, Qt, QObject
import keyboard
from colorama import Fore

from battle_logic import locate_enemy_and_start_battle
from config.Configurator import Configurator
from graphical_functions import find_multiple_templates, get_screen
from gui_functions import press_map, scroll, mouse_move, choose_planet, locate_template, click_template, click_position, \
    move_map, long_check_template_exists

import gui_functions
from model_functions import load_model


class KeyPressWorker(QThread):
    quit_signal = Signal()  # Signal to notify when 'Q' is pressed

    def run(self):
        # Continuously check for 'Q' key press

        while True:
            time.sleep(2)
            # print("wait for q")
            if keyboard.is_pressed('q'):
                self.quit_signal.emit()  # Emit signal to quit
                break  # Stop the loop after emitting signal

class Worker(QThread):
    # Signal to indicate the loop has ended
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._running = False
        self.configurator = Configurator()

    def run(self):
        self._running = True
        print("Loop started. Press 'q' to quit.")

        while self._running:

            for i in range(5, 1, 1):
                print("start of the program in")
                time.sleep(1)  # Simulate work

            result = long_check_template_exists(self.configurator.ui_templates["character_menu"], get_screen())

            if not result:
                print("Stopping loop game is off")
                break

            # configure map
            press_map()
            mouse_move(self.configurator.screen_width//2, self.configurator.screen_height//2)
            scroll(up=False)
            press_map()

            planets = list(self.configurator.enemy_info.keys())
            for current_planet in planets:
                if current_planet == "Herta":
                    continue
                print(f"START {current_planet}")
                locations = list(self.configurator.enemy_info[current_planet].keys())


                #1. choose planet
                choose_planet(template_button=self.configurator.ui_templates["Star Rail Map"], template_planet=self.configurator.planet_templates[current_planet])

                #2. find valid locations
                valid_locations = []
                for idx, current_location in enumerate(locations):
                    teleports = list(self.configurator.enemy_info[current_planet][current_location].keys())
                    number_of_enemies_in_location = sum([self.configurator.enemy_info[current_planet][current_location][teleport]["number_of_enemies"] for teleport in teleports])
                    if number_of_enemies_in_location > 0:
                        valid_locations.append(current_location)
                print(f"Valid locations: {valid_locations}")

                if len(valid_locations) > 0:
                    yolo_model = load_model(current_planet)
                    enemy_classes = self.configurator.enemy_classes[current_planet]
                    battle_template = self.configurator.ui_templates["start_autobattle"]

                for idx, current_location in enumerate(valid_locations):
                    print(f"{idx}    CHECK {current_location} location")

                    result = long_check_template_exists(self.configurator.ui_templates["character_menu"],
                                                        get_screen(True))
                    if result:
                        press_map()
                        time.sleep(0.5)


                    location_template = self.configurator.planet_locations_template[current_planet][current_location]

                    print(f"looking for {Fore.LIGHTMAGENTA_EX}{current_location}{Fore.RESET} template ")
                    if not long_check_template_exists(location_template, get_screen()):
                        print(f"{Fore.LIGHTRED_EX} Didn't find location so scroll {Fore.RESET}")
                        mouse_move(2400, 700)
                        scroll(up=False)

                    if not long_check_template_exists(location_template, get_screen()):
                        print(f"{Fore.LIGHTRED_EX} Didn't find location so go to another{Fore.RESET}")
                        break

                    position = locate_template(location_template, get_screen())
                    click_template(position[0], position[1])
                    time.sleep(1)

                    teleports = list(self.configurator.enemy_info[current_planet][current_location].keys())
                    for teleport in teleports:
                        number_of_enemies_in_teleport = self.configurator.enemy_info[current_planet][current_location][teleport]["number_of_enemies"]
                        for enemy_id in range(number_of_enemies_in_teleport):
                            print(f"teleport {teleport}")

                            result = long_check_template_exists(self.configurator.ui_templates["character_menu"],
                                                       get_screen(True))
                            if result:
                                press_map()
                                time.sleep(0.5)

                            teleport_name_template = self.configurator.location_teleports_template[current_planet][current_location][teleport]
                            teleport2_template = self.configurator.ui_templates["teleport 2"]
                            if "Calyx" in teleport:
                                teleport2_template = self.configurator.ui_templates["calyx"]

                            if "Caver of Corrosion" in teleport:
                                teleport2_template = self.configurator.ui_templates["Caver of Corrosion"]

                            if "Stagnant Shadow" in teleport:
                                teleport2_template = self.configurator.ui_templates["Stagnant Shadow"]

                            matches = find_multiple_templates(teleport2_template, get_screen())
                            print(f" found :{len(matches)} teleports")
                            teleport_check = 0
                            while teleport_check < 3:
                                while_escape = False
                                for match in matches:
                                    time.sleep(1)
                                    print(f"will click {match[0]},  {match[1]} pos")
                                    click_position(match[0], match[1])
                                    time.sleep(0.5)

                                    # check if teleport is close to other object so check another template
                                    if teleport + "2" in self.configurator.location_teleports_template[current_planet][current_location]:
                                        print(f"{Fore.LIGHTBLUE_EX} {teleport + '2'} {self.configurator.location_teleports_template[current_planet][current_location].keys()} {Fore.RESET}")
                                        try:
                                            x_pos, y_pos = locate_template(self.configurator.location_teleports_template[current_planet][current_location][teleport + "2"], get_screen())
                                            click_template(x_pos, y_pos)
                                            time.sleep(0.5)
                                        except IndexError:
                                            pass

                                    if long_check_template_exists(teleport_name_template, get_screen()):
                                        while_escape = True
                                        break
                                else:
                                    teleport_check += 1
                                    directions = {0: "north", 1: "south", 2: "west", 3: "east"}
                                    move_map(directions[teleport_check], self.configurator.screen_width//2, self.configurator.screen_height//2)
                                if while_escape:
                                    print(f"found {teleport} teleport")
                                    break
                            else:
                                continue



                            teleport_button_template = self.configurator.ui_templates["teleport"]

                            while True:
                                if long_check_template_exists(teleport_button_template, get_screen()):
                                    break
                            x_pos, y_pos = locate_template(teleport_button_template, get_screen())
                            click_template(x_pos, y_pos)



                            moves = self.configurator.enemy_info[current_planet][current_location][teleport]["moves"][enemy_id]
                            time.sleep(2)
                            #TODO improve end of battle to locate another enemy without doing the same moves again
                            for move in moves:
                                function_to_call = getattr(gui_functions, move["move"])
                                print(f"{move['move']}({str([f'{arg}, ' for arg in move['args']])})")
                                if move["args"]:
                                    function_to_call(*move["args"])
                                else:
                                    function_to_call()

                                time.sleep(0.5)

                            result = locate_enemy_and_start_battle(yolo_model=yolo_model, enemy_classes=enemy_classes, battle_template=battle_template)

                            if result:
                                print(f"{Fore.CYAN}Fight Started{Fore.RESET}")
                                pos1, pos2 = locate_template(battle_template, get_screen())
                                click_template(pos1, pos2)
                                timeout = 0
                                while timeout < 1500:
                                    timeout += 1
                                    end_battle_result = long_check_template_exists(self.configurator.ui_templates["character_menu"], get_screen())
                                    print(f"Fight timeout = {timeout} < 1500")
                                    if end_battle_result:
                                        print(f"{Fore.LIGHTCYAN_EX}BATTLE FINISHED{Fore.RESET}")
                                        break
                                else:
                                    raise Exception("Too long in battle check what is going on")



                print(f"LOCATIONS TO CHECK: {locations}")


            print("brek")
            # 1 check if game opened
            # 2 iterate over planets
            # 3 iterate over location
            # 4 use moves to perform actions




            if keyboard.is_pressed('q'):
                print("Stopping loop")
                self._running = False

        self.finished.emit()

    def stop(self):
        self._running = False


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Non-Blocking Loop Example")
        self.layout = QVBoxLayout()
        self.resize(200, 200)
        self.move(0, 1000)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        # Start Button
        self.start_button = QPushButton("Start Loop")
        self.start_button.clicked.connect(self.start_loop)
        self.layout.addWidget(self.start_button)

        self.label = QLabel("state")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.loop_thread = None

    def start_loop(self):
        if self.loop_thread is None or not self.loop_thread.isRunning():
            self.loop_thread = Worker()
            self.loop_thread.start()

            self.key_press_thread = KeyPressWorker()
            self.key_press_thread.quit_signal.connect(self.close_application)
            self.key_press_thread.start()




    def close_application(self):
        # Stop the thread and close the application
        self.key_press_thread.quit()
        self.key_press_thread.wait()
        self.close()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

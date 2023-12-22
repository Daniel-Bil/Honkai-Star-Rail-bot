import random
import time
from pynput.mouse import Button, Controller
import pyautogui
import cv2

class Cord:
    def __init__(self, x1=None, x2=None, y1=None, y2=None):
        if x1 is None or x2 is None:
            raise Exception("wrong coordinates")
        elif x1 is not None and x2 is not None and y1 is None and y2 is None:
            self.x1 = x1
            self.x2 = x1+1
            self.y1 = x2
            self.y2 = x2+1
        else:
            self.x1 = int(x1)
            self.x2 = int(x2)
            self.y1 = int(y1)
            self.y2 = int(y2)

    def __repr__(self):
        return f"Cord( {self.x1} {self.x2} {self.y1} {self.y2})"

    def click_cord(self,slow1=0.2,slow2=0.3,slow3=0.1):
        pyautogui.mouseDown()
        pyautogui.sleep(random.uniform(slow1, slow2))
        pyautogui.mouseUp()
        pyautogui.sleep(slow3)
    def click_cord_fast(self,slow1=0.2,slow2=0.3,slow3=0.1):
        pyautogui.click()
        # pyautogui.sleep(0.003)
        pyautogui.sleep(random.uniform(0.0003, 0.0004))

    def move_cord(self, slow1=0.1, slow2=0.2):
        mouse = Controller()
        pyautogui.sleep(random.uniform(slow1, slow2))
        mouse.position = (self.x1, self.y1)
        pyautogui.sleep(random.uniform(slow1, slow2))

    def move_and_click_cord(self, slow1=0.1, slow2=0.2, slow3=0.2, slow4=0.3, slow5=0.1):
        self.move_cord(slow1, slow2)
        self.click_cord(slow3, slow4, slow5)

out_of_battle_cord_dict = {"hero1_hp": Cord(2211, 2351, 452, 456),
                           "hero2_hp": Cord(2211, 2351, 577, 581),
                           "hero3_hp": Cord(2211, 2351, 702, 705),
                           "hero4_hp": Cord(2211, 2351, 826, 830),
                           "open_map": [],
                           "skillpoint_1": [],
                           "skillpoint_2": [],
                           "skillpoint_3": [],
                           "skillpoint_4": [],
                           "skillpoint_5": [],
                           "icon1": Cord(1780, 1781, 80, 81),
                           "icon2": Cord(1911, 1912, 70, 71),
                           "icon3": Cord(2036, 2037, 75, 76),
                           "icon4": Cord(2123, 2124, 75, 76),
                           "icon5": Cord(2242, 2243, 84, 85),
                           "icon6": Cord(2353, 2354, 40, 41),
                           "icon7": Cord(2468, 2469, 40, 41),
                           "map": Cord(63, 312, 77, 326)}

in_battle_skillpoint_dict = {"skill1": Cord(1932, 1933, 1292, 1293),
                             "skill2": Cord(1955, 1956, 1292, 1293),
                             "skill3": Cord(1979, 1980, 1292, 1293),
                             "skill4": Cord(2004, 2005, 1292, 1293),
                             "skill5": Cord(2028, 2029, 1292, 1293)}

star_map_dict = {"Herta_Space_Station": Cord(475, 476, 710, 711),
                 "Jarilo-VI": Cord(1350, 1351, 340, 341),
                 "The_Xianzhou_Luofu": Cord(2030, 2031, 1120, 1121)}
# Herta_Space_Station
Herta_Space_Station_dict = {"parlor_car": Cord(2431, 2432, 309, 310),
                            "master_control_zone": Cord(2443, 2444, 437, 438),
                            "base_zone": Cord(2440, 2441, 570, 571),
                            "storage_zone": Cord(2440, 2441, 690, 691),
                            "supply_zone": Cord(2440, 2441, 820, 821)}

Base_Zone_dict = {"Monitoring_Room": Cord(1123, 1124, 216, 217),
                  "Reception_Center": Cord(931, 932, 690, 691)}


Storage_Zone_dict = {"Calyx (Crimson): Bud of Destruction": Cord(660, 661, 680, 681),
                     "Outside_the_Control_Center": Cord(728, 729, 750, 751),
                     "Courtyard": Cord(1070, 1071, 711, 712)}

Supply_Zone_dict = {"Spare Parts Warehouse": Cord(770, 771, 545, 546),
                     "Calyx": Cord(821, 822, 647, 648),
                     "Electrical Room": Cord(420, 421, 775, 776)}

Jarilo_VI_dict = {"parlor_car": Cord(2431, 2432, 309, 310),
                  "Outlying Snow Plains": Cord(2443, 2444, 570, 571),
                  "Backwater Pass": Cord(2440, 2441, 352, 353),
                  "Corridor of Fading Echoes": Cord(2440, 2441, 593, 594),
                  "Everwinter Hill": Cord(2440, 2441, 733, 734),
                  "Great Mine": Cord(2440, 2441, 986, 987),
                  "Rivet Town": Cord(2440, 2441, 1120, 1121),
                  "Robot Settlement": Cord(2440, 2441, 1255, 1256)}

Outlying_Snow_Plains = {"Bud of The Hunt": Cord(1288,1289,556,557),
                        "Long Slope": Cord(1396,1397,650,651),
                        "Calyx (Golden)": Cord(1490,1491,753,754)}

Backwater_Pass = {"Transport Hub": Cord(1020,963),
                  "Calyx (Crimson)": Cord(1100,530),
                  "Leisure Plaza": Cord(1141,493),
                  "Goethe Mansion": Cord(1305,200)}





templates ={"teleport": cv2.imread('.//test_images//templates//teleport.png', cv2.IMREAD_GRAYSCALE),
            "nameless_template": cv2.imread('.//test_images//templates//nameless_template.png', cv2.IMREAD_GRAYSCALE),
            "parlor_car": cv2.imread('.//test_images//templates//Parlor_car_template.png', cv2.IMREAD_GRAYSCALE),
            "master_control_zone": cv2.imread('.//test_images//templates//Master_Control_Zone_template.png', cv2.IMREAD_GRAYSCALE),
            "base_zone": cv2.imread('.//test_images//templates//Base_Zone_template.png', cv2.IMREAD_GRAYSCALE),
            "storage_zone": cv2.imread('.//test_images//templates//Storage_Zone_template.png', cv2.IMREAD_GRAYSCALE),
            "supply_zone": cv2.imread('.//test_images//templates//Supply_Zone_template.png', cv2.IMREAD_GRAYSCALE)}






The_Xianzhou_Luofu = {"parlor_car": Cord(2431, 2432, 309, 310),
                      "master_control_zone": Cord(2443, 2444, 437, 438),
                      "base_zone": Cord(2440, 2441, 570, 571),
                      "storage_zone": Cord(2440, 2441, 690, 691),
                      "supply_zone": Cord(2440, 2441, 820, 821)}

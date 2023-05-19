class Cord:
    def __init__(self, x1, x2, y1, y2):
        if x1 is None or x2 is None or y1 is None or x2 is None:
            raise Exception("wrong coordinates")
        else:
            self.x1 = int(x1)
            self.x2 = int(x2)
            self.y1 = int(y1)
            self.y2 = int(y2)

    def __repr__(self):
        return f"Cord( {self.x1} {self.x2} {self.y1} {self.y2})"


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

Jarilo_VI_dict = {"parlor_car": Cord(2431, 2432, 309, 310),
                  "master_control_zone": Cord(2443, 2444, 437, 438),
                  "base_zone": Cord(2440, 2441, 570, 571),
                  "storage_zone": Cord(2440, 2441, 690, 691),
                  "supply_zone": Cord(2440, 2441, 820, 821)}

The_Xianzhou_Luofu = {"parlor_car": Cord(2431, 2432, 309, 310),
                      "master_control_zone": Cord(2443, 2444, 437, 438),
                      "base_zone": Cord(2440, 2441, 570, 571),
                      "storage_zone": Cord(2440, 2441, 690, 691),
                      "supply_zone": Cord(2440, 2441, 820, 821)}

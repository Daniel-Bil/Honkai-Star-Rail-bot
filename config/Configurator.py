import sys
from pathlib import Path
import json

import cv2

from screeninfo import get_monitors


class Configurator:
    def __init__(self):
        # base path for .exe/file.py during runtime
        try:
            self.base_path = Path(sys._MEIPASS)
        except AttributeError:
            self.base_path = Path()

        # all paths creation
        self.create_paths()

        # all screen info
        self.create_monitor_information()

        # all enemy info
        self.create_base_information()

        # all templates creation
        self.create_templates()

    def create_base_information(self) -> None:
        with open(self.enemy_info_path, "r") as file:
            self.enemy_info = json.load(file)

        with open(self.enemy_classes_path, "r") as file:
            self.enemy_classes = json.load(file)

    def create_monitor_information(self) -> None:
        for m in get_monitors():
            # print(m, m.is_primary)
            if m.is_primary:
                self.screen_width = m.width
                self.screen_height = m.height
                self.width_scale = self.screen_width // 2560
                self.height_scale = self.screen_height // 1440
                break
        else:
            raise Exception("It seems there is no primary monitor so bot cant perform actions -> Plug monitor in")


    def create_paths(self) -> None:
        """
        Creates all needed paths
        """
        self.config_path = self.base_path / "config"

        self.images_path = self.base_path / "images"

        self.locations_path = self.images_path / "locations"
        self.planets_path = self.images_path / "planets"
        self.ui_path = self.images_path / "ui"

        self.herta_locations = self.locations_path / "Herta"
        self.jarilo_locations = self.locations_path / "JariloVI"
        # self.herta_locations = self.locations_path / "Xianzhou"
        # self.herta_locations = self.locations_path / "Panacony"


        self.enemy_info_path = self.config_path / "enemy_info.json"
        self.enemy_classes_path = self.config_path / "enemy_classes.json"

    def create_templates(self) -> None:
        """
        Creates templates needed for checking operations
        """

        self.ui_templates = {}
        for template in list(self.ui_path.glob('*.png')):
            self.ui_templates[template.stem] = cv2.imread(str(template), cv2.IMREAD_GRAYSCALE)

        self.planet_templates = {}
        for template in list(self.planets_path.glob('*.png')):
            self.planet_templates[template.stem] = cv2.imread(str(template), cv2.IMREAD_GRAYSCALE)

        self.location_teleports_template = {}

        self.planet_locations_template = {}
        for directory in self.locations_path.iterdir():
            if directory.is_dir():
                self.planet_locations_template[directory.name] = {}
                self.location_teleports_template[directory.name] = {}

                for template in list(directory.glob('*.png')):
                    self.planet_locations_template[directory.name][template.stem] = cv2.imread(str(template), cv2.IMREAD_GRAYSCALE)
                    for directory2 in directory.iterdir():
                        if directory2.is_dir():

                            self.location_teleports_template[directory.name][directory2.name] = {}
                            for template2 in list(directory2.glob('*.png')):
                                self.location_teleports_template[directory.name][directory2.name][template2.stem] = cv2.imread(str(template2), cv2.IMREAD_GRAYSCALE)

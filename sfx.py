import os
import pygame

BASE_SFX_PATH = "data/sfx/"

class SFXController:
    def __init__(self):
        self.__sfx_list = {}
        self.__last_sfx_vol = {}
        self.muted = False
        pygame.mixer.init()
        
    def add_sfx(self, sfx_name, path, volume=1.0):
        # check file
        sfx_path = BASE_SFX_PATH + str(path)
        if os.path.isfile(sfx_path):
            self.__sfx_list[sfx_name] = pygame.mixer.Sound(sfx_path)
            self.set_volume(sfx_name, volume)
        else:
            raise FileNotFoundError(f"File {sfx_path} not found!")
        
    def set_volume(self, sfx_name, volume, set_last_vol=True):
        if set_last_vol:
            self.__last_sfx_vol[sfx_name] = volume
        self.__sfx_list[sfx_name].set_volume(volume)
    
    def play(self, sfx_name, loop=False):
        if sfx_name in self.__sfx_list:
            if loop:
                self.__sfx_list[sfx_name].play(loops=-1)
            else:
                self.__sfx_list[sfx_name].play(loops=0)
        else:
            raise Exception(f"{sfx_name} does not exist in sfx list!")
        
    def mute(self):
        if self.muted:
            for sfx_name, _ in self.__sfx_list.items():
                self.set_volume(sfx_name, self.__last_sfx_vol[sfx_name])
            self.muted = False
        else:
            for sfx_name, _ in self.__sfx_list.items():
                    self.set_volume(sfx_name, 0, set_last_vol=False)
            self.muted = True
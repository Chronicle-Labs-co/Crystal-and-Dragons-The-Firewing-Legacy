import sys
import pygame
from pygame.locals import *

class Game:
    def __init__(self):
        self.__run = True

    def run(self):
        while self.__run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                
                if event.type == pygame.KEYDOWN:
                    pass
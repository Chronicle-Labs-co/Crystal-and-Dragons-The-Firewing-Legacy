import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *

from model.game import Game

pygame.init()

# Declare variable config
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crystal and Dragons: The Firewing Legacy")

game = Game()
game.run()
import pygame
from constants import *
import random

class Apple(object):
    """docstring for Snake."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.new_loc()

    def update(self):
        pass


    def new_loc(self):
        self.x = random.randint(0, 20) * BLOCK_SIZE
        self.y = random.randint(0, 20) * BLOCK_SIZE





    def draw(self, surface):
        pygame.draw.rect(surface, (200, 0, 0), (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

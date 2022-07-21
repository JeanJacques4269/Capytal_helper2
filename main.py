import pygame
from windows import Front
from constants import *

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    f = Front(win)
    f.run()

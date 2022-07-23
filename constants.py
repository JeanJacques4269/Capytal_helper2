from components.color import *
import pygame

path_driver = r"geckodriver.exe"
auth_link = "https://ent.iledefrance.fr/auth/login"

BG_COLOR = WHITE

WIDTH = 800
HEIGHT = 500

CENTER_W = WIDTH // 2
CENTER_H = HEIGHT // 2

v_img = pygame.image.load("assets/v.png")
v_img = pygame.transform.scale(v_img, (50, 50))

dl_img = pygame.image.load("assets/dl.png")
dl_img = pygame.transform.smoothscale(dl_img, (37, 37))

cross_img = pygame.image.load("assets/red_cross.png")
cross_img = pygame.transform.smoothscale(cross_img, (37, 37))

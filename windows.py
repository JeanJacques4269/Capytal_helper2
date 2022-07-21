import pygame
from constants import *
from components.entry import TextInputBox
from components.buttons import Button, ButtonImg
from browser import fct
from tests import tests


class Front:
    def __init__(self, win):
        self.win = win
        self.running = True
        self.buttons = []

        self.correction_dir = ""

        # Entry
        self.entry = TextInputBox(100, 300, 450, pygame.font.SysFont("Consolas", 15))

        # Buttons
        self.get_correction_btn = Button(400, 200, 50, "Get correction", BLACK, WHITE, self.get_correction_dir)
        self.dl_copies_btn = ButtonImg(dl_img, 576, 313, lambda: fct(self.entry.text))
        self.validate_btn = ButtonImg(v_img, CENTER_W, 400, self.get_correction_dir)

        # Group
        self.group = pygame.sprite.Group(self.entry)
        self.btns_group = pygame.sprite.Group(self.dl_copies_btn, self.validate_btn, self.get_correction_btn)

    def run(self):
        while self.running:
            clock = pygame.time.Clock()
            clock.tick(15)
            self.win.fill(BG_COLOR)
            self.events()
            self.draw()
            pygame.display.flip()

    def events(self):
        eves = pygame.event.get()
        for event in eves:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(event.pos)

        self.btns_group.update(eves)
        self.group.update(eves)

    def draw(self):
        self.group.draw(self.win)
        self.btns_group.draw(self.win)

    def get_correction_dir(self):
        self.correction_dir = prompt_file()

    def validate(self):
        tests("copies", self.correction_dir, [["a", "b", "c"], []])


def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    import tkinter
    import tkinter.filedialog

    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

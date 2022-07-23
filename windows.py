import os
import re

import pygame
from constants import *
from components.entry import TextInputBox, Label
from components.buttons import Button, ButtonImg
from browser import fct
from tests import tests
import multiprocessing


class Front:
    def __init__(self, win):
        self.win = win
        self.running = True
        self.buttons = []

        self.correction_dir = ""

        basicfont = pygame.font.SysFont('comicsans', 30)
        # Label
        self.correction_lbl = Label(f"Fichier correction : {self.correction_dir}", 100, 100, basicfont, BLACK)
        self.entry_lbl = Label(f"Activity link", 100, 250, pygame.font.SysFont("Consolas", 25), BLACK)
        self.downloading_lbl = Label("Downloading...", 630, 300, pygame.font.SysFont("Consolas", 15), BLACK)

        # Entry
        self.entry = TextInputBox(100, 300, 450, pygame.font.SysFont("Consolas", 15))

        # Buttons
        self.parcourir_btn = Button(500, 100, 50, "Parcourir", GRAY, BLACK, basicfont, False,
                                    self.get_correction_dir)
        self.dl_copies_btn = ButtonImg(dl_img, 576, 313, self.download_copies)
        self.cross_btn = ButtonImg(cross_img, 615, 313, self.cancel_dl)
        self.validate_btn = ButtonImg(v_img, CENTER_W, 400, self.validate)

        # Group
        self.group = pygame.sprite.Group(self.entry, self.correction_lbl, self.entry_lbl)
        self.btns_group = pygame.sprite.Group(self.dl_copies_btn, self.parcourir_btn, self.cross_btn)

        # process
        self.procs = []

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
                for proc in self.procs:
                    proc.kill()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(event.pos)

        self.correction_lbl.upd(self.correction_dir)
        self.btns_group.update(eves)
        onlyfiles = next(os.walk("copies"))[2]
        if self.correction_dir != "" and len(onlyfiles) >= 1:
            self.validate_btn.update(eves)
        self.group.update(eves)

    def draw(self):
        self.group.draw(self.win)
        self.btns_group.draw(self.win)

        onlyfiles = next(os.walk("copies"))[2]

        if self.correction_dir != "" and len(onlyfiles) >= 1:
            self.validate_btn.draw(self.win)
        for proc in self.procs:
            proc.join(timeout=0)
            if proc.is_alive():
                self.downloading_lbl.draw(self.win)

    def get_correction_dir(self):
        self.correction_dir = prompt_file()

    def validate(self):
        tests("copies", self.correction_dir, [["a", "b", "c"], []])

    def download_copies(self):
        pattern = re.compile(r"^https://capytale2.ac-paris.fr/web/assignments/.+$")
        if not pattern.match(self.entry.text):
            return
        dl_copies_process = multiprocessing.Process(target=fct, args=(self.entry.text,))
        self.procs[0] = dl_copies_process
        dl_copies_process.start()

    def cancel_dl(self):
        for proc in self.procs:
            proc.kill()


def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    import tkinter
    import tkinter.filedialog

    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

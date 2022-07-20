import pygame
from constants import *
from components.entry import TextInputBox
from components.buttons import Button
from browser import fct


class Front:
    def __init__(self, win):
        self.win = win
        self.running = True
        self.buttons = []

        # Entry
        self.entry = TextInputBox(100, 400, 450, pygame.font.SysFont("Consolas", 19))

        # Buttons
        self.validate_btn = Button(BLACK, BLACK, 600, 400, 50, 50, lambda: fct(self.entry.text), 'dl')
        self.ask_correction = Button(BLACK, BLACK, 600, 400, 50, 50, lambda: fct(self.entry.text), 'dl')

        # Group
        self.group = pygame.sprite.Group(self.entry)
        self.buttons = [self.validate_btn]

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
                for button in self.buttons:
                    if button.isMouseOnIt(event.pos):
                        button.onclick()

            if event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    if button.isMouseOnIt(event.pos):
                        button.hover()
                    else:
                        button.default()

        self.group.update(eves)

    def draw(self):
        self.group.draw(self.win)
        for btn in self.buttons:
            btn.draw(self.win)


def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    import tkinter
    import tkinter.filedialog

    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

import pygame

BLACK = 0, 0, 0
GRAY = (185, 224, 226)

TEXTCOLORDEFAULT = 255,255,255
TEXTCOLORONHOVER = GRAY


class Button:
    def __init__(self, defaultcolor, hovercolor, x, y, width, height, onclick, text):
        self.defaultcolor = defaultcolor
        self.hovercolor = hovercolor
        self.color = defaultcolor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textcolordefault = TEXTCOLORDEFAULT
        self.textcolor = TEXTCOLORDEFAULT
        self.textcolorhover = TEXTCOLORONHOVER
        self.onclick = onclick

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 45)
            text = font.render(self.text, True, self.textcolor)
            win.blit(text, (self.x + 8, self.y + (self.height / 2 - text.get_height() / 2)))

    def isMouseOnIt(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def hover(self):
        self.color = self.hovercolor
        self.textcolor = self.textcolorhover

    def default(self):
        self.color = self.defaultcolor
        self.textcolor = self.textcolordefault

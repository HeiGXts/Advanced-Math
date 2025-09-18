from pygame import *
from globals import *

class Button:
    def __init__(self, app, co, size, colors, border, radius, text, action):
        self.app = app
        self.rect = Rect(0, 0, size[0], size[1])
        self.rect.center = (co[0], co[1])
        self.colors = colors
        self.cIndex = 0
        self.borderColor = border[0]
        self.width = border[1]
        self.radius = radius
        self.action = action
        self.text = fonts(text[1], text[2], text[3], text[4]).render(text[0], True, text[5])
        self.textRect = self.text.get_rect(center = self.rect.center)
        self.hovered = False

    def draw(self):
        draw.rect(self.app.screen, self.colors[self.cIndex], self.rect, border_radius = self.radius)
        draw.rect(self.app.screen, self.borderColor, self.rect, width = self.width, border_radius = self.radius)
        self.app.screen.blit(self.text, self.textRect)

    def handleEvent(self, event):
        if(event.type == MOUSEMOTION):
            if(self.hovered != self.rect.collidepoint(event.pos)):
                self.hovered = not self.hovered
                self.cIndex = (self.cIndex + 1) % 2
        
        if(event.type == MOUSEBUTTONDOWN and self.hovered and event.button == 1):
            self.action()



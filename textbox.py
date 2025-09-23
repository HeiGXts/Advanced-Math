from pygame import *
from globals import *

class TextBox:
    def __init__(self, app, co, size, border, text):
        self.app = app
        self.rect = Rect(co[0], co[1], size[0], size[1])
        self.border = border
        self.color = border[0]
        self.input = ""
        self.key = ""
        self.entering = False
        self.textSetting = text
        self.text = fonts(text[0], text[1], text[2], text[3]).render(self.input, True, text[4])
        self.textRect = self.text.get_rect()
        self.co = co
        self.size = size
        self.lines = 0

    def draw(self):
        draw.rect(self.app.screen, self.color, self.rect, width = self.border[2])
        self.app.screen.blit(self.text, self.textRect)

    def handleEvent(self, event):
        if(event.type == MOUSEBUTTONDOWN and event.button == 1):
            self.entering = self.rect.collidepoint(event.pos)
            if(self.entering):
                self.color = self.border[1]
            else:
                self.color = self.border[0]

        if(event.type == KEYDOWN):
            self.key = event.unicode
            if((self.key.isdigit() or self.key.isalpha() or self.key == '+' or self.key == '-' or self.key == '*' or self.key == '/' or self.key == '(' or self.key == ')' 
                or self.key == '!' or self.key == '=' or self.key == '^' or self.key == '%' or self.key == '.') 
               and self.textRect.right < self.rect.right - self.app.unit // 8):
                self.input += self.key
            if(event.key == K_BACKSPACE):
                self.input = self.input[:-1]
            self.text = fonts(self.textSetting[0], self.textSetting[1], self.textSetting[2], self.textSetting[3]).render(self.input, True, self.textSetting[4])
            self.textRect = self.text.get_rect()
            #print(self.textRect.right, self.rect.right)
            self.textRect.midleft = (self.co[0] + self.app.unit // 8, self.co[1] + self.size[1] // 2)
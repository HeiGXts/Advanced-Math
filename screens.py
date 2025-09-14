from pygame import *
from globals import *

class HomeScreen:
    def __init__(self, app):
        self.app = app

    def draw(self):
        self.app.screen.fill(White)
        message1 = font24.render("Hi, Ms.Croft", True, Black)
        self.app.screen.blit(message1, (10, 10))
from pygame import *
from globals import *
from buttons import *

class HomeScreen:
    def __init__(self, app):
        self.app = app
        self.algebraButton = Button(app, (app.width // 2, 600), (150, 70), (White, Grey), Black, 5, 5, ("Algebra", "Arial", 30, False, False, Black), lambda: self.toAlgebra())
        self.quitButton = Button(app, (app.width // 2, 700), (150, 70), (White, Grey), Black, 5, 5, ("Quit", "Arial", 30, False, False, Black), lambda: exit())
        self.buttons = [self.algebraButton, self.quitButton]
        display.set_caption("Advanced Math Project")

    def draw(self):
        self.app.screen.fill(White)
        message1 = fonts("Arial", 40, True, False).render("Advanced Math Project", True, Black)
        self.app.screen.blit(message1, message1.get_rect(center = (self.app.width // 2, 300)))

        for button in self.buttons:
            button.draw()

    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)

    def toAlgebra(self):
        self.app.currentScreen = GraphingCalculator(self.app)


class GraphingCalculator:
    def __init__(self, app):
        self.app = app
        self.input = ""
        self.backButton = Button(app, (50, 50), (50, 50), (White, Grey), Black, 5, 5, ("←", "Arial", 30, False, False, Black), lambda: self.toHomeScreen())
        self.buttons = [self.backButton]

    def draw(self):
        self.app.screen.fill(White)

        for button in self.buttons:
            button.draw()

    def handleEvent(self, event):
        if(event.type == KEYDOWN):
            if(event.key == K_BACKSPACE):
                pass

        for button in self.buttons:
            button.handleEvent(event)

    def toHomeScreen(self):
        self.app.currentScreen = HomeScreen(self.app)
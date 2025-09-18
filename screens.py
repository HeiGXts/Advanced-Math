from pygame import *
from globals import *
from buttons import *
from textbox import *

class HomeScreen:
    def __init__(self, app):
        self.app = app
        self.algebraButton = Button(app, (app.width // 2, app.unit * 7), (app.unit * 2.2, app.unit * 0.8), (White, Grey), (Black, app.unit // 16), 5, 
                                    ("Algebra", "Arial", app.unit * 0.5, False, False, Black), lambda: self.toAlgebra())
        self.quitButton = Button(app, (app.width // 2, app.unit * 8), (app.unit * 2.2, app.unit * 0.8), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("Quit", "Arial", app.unit * 0.5, False, False, Black), lambda: exit())
        self.buttons = [self.algebraButton, self.quitButton]
        display.set_caption("Advanced Math Project")

    def draw(self):
        self.app.screen.fill(White)
        message1 = fonts("Arial", self.app.unit * 0.9, True, False).render("Advanced Math Project", True, Black)
        self.app.screen.blit(message1, message1.get_rect(center = (self.app.width // 2, self.app.unit * 4)))

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
        self.backButton = Button(app, (app.unit * 0.6, app.unit * 0.6), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("←", "Arial", app.unit * 0.3, False, False, Black), lambda: self.toHomeScreen())
        self.buttons = [self.backButton]
        self.mainTextBox = TextBox(app, (app.unit * 4, app.unit), (app.unit * 11, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   ("Arial", app.unit * 0.3, False, False, Black))
        self.textBox = [self.mainTextBox]

    def draw(self):
        self.app.screen.fill(White)

        for button in self.buttons:
            button.draw()

        for textbox in self.textBox:
            textbox.draw()

    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)

        for textbox in self.textBox:
            textbox.handleEvent(event)

    def toHomeScreen(self):
        self.app.currentScreen = HomeScreen(self.app)
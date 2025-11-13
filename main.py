from pygame import *
from screens import *
from globals import *

class Main:
    def __init__(self):
        init()
        self.width = 1280
        self.height = 800
        self.unit = 80
        self.font = Arial
        self.screen = display.set_mode((self.width, self.height))
        self.currentScreen = HomeScreen(self)
        self.running = True
        self.frame = 60
        self.clock = time.Clock()

        self.searchRange = (-100000, 100000)
        self.searchSteps = 10000
        self.graphingSteps = 10

    def handleEvent(self):
        for events in event.get():
            if(events.type == QUIT):
                self.running = False
            self.currentScreen.handleEvent(events)

    def draw(self):
        self.currentScreen.draw()
        display.flip()

    def run(self):
        while self.running:
            self.handleEvent()
            self.draw()
            self.clock.tick(self.frame)
        quit()
        exit()

if(__name__ == "__main__"):
    app = Main()
    app.run()
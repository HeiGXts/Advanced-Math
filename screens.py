from pygame import *
from globals import *
from buttons import *
from textbox import *
import math

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
        self.enterButton1 = Button(app, (app.unit * 14.5, app.unit * 2), (app.unit, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Enter", "Arial", app.unit * 0.3, False, False, Black), lambda: self.calculate())
        self.buttons = [self.backButton, self.enterButton1]
        self.textBox1 = TextBox(app, (app.unit * 4, app.unit), (app.unit * 11, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   ("Arial", app.unit * 0.3, False, False, Black))
        self.textBox = [self.textBox1]
        self.result = 0
        self.resultRect = 0

        self.displayingGraph = False
        self.minX = -20
        self.minY = -20
        self.maxX = 20
        self.maxY = 20

    def draw(self):
        self.app.screen.fill(White)

        if(self.result != 0):
            self.app.screen.blit(self.result, self.resultRect)

        for button in self.buttons:
            button.draw()

        for textbox in self.textBox:
            textbox.draw()

    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)

        for textbox in self.textBox:
            textbox.handleEvent(event)

        if(event.type == KEYDOWN and self.textBox[0].entering == True and event.key == K_RETURN):
            self.calculate()

    def calculate(self):
        self.result = fonts("Arial", self.app.unit * 0.3, True, False).render(str(self.calculateEquation(self.textBox[0].input)), True, Black)
        self.resultRect = self.result.get_rect()
        self.resultRect.midleft = (self.app.unit * 4, self.app.unit * 2)
        self.displayingGraph = True

    def calculateEquation(self, equation):
        for index in range(len(equation)):
            if(equation[index] == '^'):
                equation = equation[:index] + '**' + equation[index + 1:]
            elif(equation[index] == '!'):
                equation = self.factorial(equation, index)
        try:
            return eval(equation)
        except Exception as e:
            return f"Error: {type(e).__name__}"
        
    def factorial(self, equation, index):
        result = equation
        if(index == 0):
            return result
        elif(equation[index - 1] == ')'):
            i = index - 1
            while i >= 0:
                if(equation[i] == '('):
                    try:
                        result = equation[:i] + str(math.factorial(int(self.calculateEquation(equation[i:index]))))
                    except:
                        return equation
                    if(len(equation) > index + 1):
                        result += equation[index + 1:]
                    return result
                i -= 1
            return result
        else:
            i = index - 1
            while i >= 0:
                if(not equation[i].isdigit() and equation[i] != '.'):
                    try:
                        result = equation[:i + 1] + str(math.factorial(int(equation[i + 1:index])))
                    except:
                        return equation
                    if(len(equation) > index + 1):
                        result += equation[index + 1:]
                    return result
                i -= 1
            try:
                result = str(math.factorial(int(equation[:index])))
            except:
                return equation
            if(len(equation) > index + 1):
                result += equation[index + 1:]
            return result

    def drawGrid(self):
        pass

    def drawGraph(self):
        pass

    def toHomeScreen(self):
        self.app.currentScreen = HomeScreen(self.app)
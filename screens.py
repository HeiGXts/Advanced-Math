from pygame import *
from globals import *
from buttons import *
from textbox import *
from mathprocessing import *


class HomeScreen:
    def __init__(self, app):
        self.app = app
        self.algebraButton = Button(app, (app.width // 2, app.unit * 7), (app.unit * 2.2, app.unit * 0.8), (White, Grey), (Black, app.unit // 16), 5, 
                                    ("Algebra", self.app.font, app.unit * 0.5, False, False, Black), lambda: self.toAlgebra())
        self.quitButton = Button(app, (app.width // 2, app.unit * 8), (app.unit * 2.2, app.unit * 0.8), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("Quit", self.app.font, app.unit * 0.5, False, False, Black), lambda: exit())
        self.buttons = [self.algebraButton, self.quitButton]
        display.set_caption("Advanced Math Project")


    def draw(self):
        self.app.screen.fill(White)
        message1 = fonts(self.app.font, self.app.unit * 0.9, True, False).render("Advanced Math Project", True, Black)
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
                                 ("←", app.font, app.unit * 0.3, False, False, Black), lambda: self.toHomeScreen())
        self.enterButton1 = Button(app, (app.unit * 14.5, app.unit * 1.3), (app.unit, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Enter", app.font, app.unit * 0.3, False, False, Black), lambda: self.calculate(self.textBox[0].input))
        self.enterButton2 = Button(app, (app.unit * 9.5, app.unit * 2), (app.unit, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Enter", app.font, app.unit * 0.3, False, False, Black), lambda: self.substituteVariable())
        self.graphMoveUp = Button(app, (app.unit * 13, app.unit * 4), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 8, 
                                  ("↑", app.font, app.unit * 0.3, False, False, Black), lambda: self.moveGraph((0, 1)))
        self.graphMoveDown = Button(app, (app.unit * 13, app.unit * 6), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 8, 
                                  ("↓", app.font, app.unit * 0.3, False, False, Black), lambda: self.moveGraph((0, -1)))
        self.graphMoveLeft = Button(app, (app.unit * 12, app.unit * 5), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 8, 
                                  ("←", app.font, app.unit * 0.3, False, False, Black), lambda: self.moveGraph((-1, 0)))
        self.graphMoveRight = Button(app, (app.unit * 14, app.unit * 5), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 8, 
                                  ("→", app.font, app.unit * 0.3, False, False, Black), lambda: self.moveGraph((1, 0)))
        self.graphResetButton = Button(app, (app.unit * 13, app.unit * 5), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 8, 
                                  ("R", app.font, app.unit * 0.3, False, False, Black), lambda: self.resetGraph())
        self.buttons = [self.backButton, self.enterButton1, self.graphMoveUp, self.graphMoveDown, self.graphMoveLeft, self.graphMoveRight, self.graphResetButton]
        self.textBox1 = TextBox(app, (app.unit * 4, app.unit * 0.3), (app.unit * 11, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (app.font, app.unit * 0.3, False, False, Black))
        self.textBox2 = TextBox(app, (app.unit * 4.5, app.unit * 1.7), (app.unit * 4, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (app.font, app.unit * 0.3, False, False, Black))
        self.textBox = [self.textBox1]
        self.result = 0
        self.resultRect = 0
        self.radMode = True
        self.substituting = False

        self.displayingGraph = False
        self.minX = -20
        self.minY = -20
        self.maxX = 20
        self.maxY = 20
        self.gridSize = (self.maxX - self.minX) // 20
        self.variable = 0
        self.graphPoints = 125
        self.graphX = [0 for i in range(self.graphPoints)]
        self.graphY = [0 for i in range(self.graphPoints)]

        self.searchRange = self.app.searchRange
        self.searchSteps = self.app.searchSteps


    def draw(self):
        self.app.screen.fill(White)

        if(self.result != 0):
            self.app.screen.blit(self.result, self.resultRect)

        for button in self.buttons:
            button.draw()

        for textbox in self.textBox:
            textbox.draw()

        self.drawGrid()

        if(self.variable):
            message = fonts(self.app.font, self.app.unit * 0.3, True, False).render(f"{self.variable} =", True, Black)
            messageRect = message.get_rect()
            messageRect.midleft = (self.app.unit * 4, self.app.unit * 2)
            self.app.screen.blit(message, messageRect)

        if(self.displayingGraph):
            self.drawGraph()


    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)

        for textbox in self.textBox:
            textbox.handleEvent(event)

        if(event.type == KEYDOWN and event.key == K_RETURN):
            if(self.textBox[0].entering):
                self.calculate(self.textBox[0].input)
            if(len(self.textBox) > 1 and self.textBox[1].entering):
                self.substituteVariable()


    def calculate(self, equation):
        if(self.substituting):
            self.ssubstituting = False
        else:
            self.variable = 0
        self.result = 0
        self.displayingGraph = False
        self.textBox2 = TextBox(self.app, (self.app.unit * 4.5, self.app.unit * 1.7), (self.app.unit * 4, self.app.unit * 0.6), (DarkGrey, Black, self.app.unit // 16), 
                                   (self.app.font, self.app.unit * 0.3, False, False, Black))
        if(equation == ""):
            return
        if(checkAlpha(equation)):
            processAlpha(self, equation)
        elif('=' in equation):
            equalEval(self, equation)
        else:
            self.printResult(str(calculateEquation(self, equation)))


    def printResult(self, result):
        self.result = fonts(self.app.font, self.app.unit * 0.3, True, False).render(result, True, Black)
        self.resultRect = self.result.get_rect()
        self.resultRect.midleft = (self.app.unit * 4, self.app.unit * 1.3)            
                
    
    def substituteVariable(self):
        equation = self.textBox[0].input
        variable = self.textBox[1].input
        index = 0
        self.substituting = True

        for char in variable:
            if(char.isalpha() and char != 'x' and char != 'y' and '=' not in equation):
                self.printResult("Error:MoreThanOneUnknown")
                return

        while self.variable in equation and index < len(equation):
            if(equation[index] == self.variable):
                if(index != 0 and index != len(equation) - 1):
                    if(equation[index - 1].isdigit()):
                        equation = equation[:index] + "*" + equation[index:]
                        index += 1
                    if(equation[index + 1].isdigit()):
                        self.printResult("Error: SyntaxError")
                        return
                    equation = equation[:index] + f"({variable})" + equation[index + 1:]
                elif(index == len(equation) - 1):
                    if(equation[index - 1].isdigit()):
                        equation = equation[:index] + "*" + equation[index:]
                        index += 1
                    equation = equation[:index] + f"({variable})"
                else:
                    if(equation[index + 1].isdigit()):
                        self.printResult("Error: SyntaxError")
                        return
                    equation = f"({variable})" + equation[index + 1:]
            index += 1
        self.calculate(equation)
        

    def solveEquation(self, equation):
        if('y' in equation and 'x' in equation):
            if('=' in equation):
                self.displayingGraph = True
                self.calculateGraph(equation)
            else:
                self.printResult("Error: MoreThanOneUnknown")
        elif('x' in equation):
            if('=' in equation):
                solveForVar(self, equation, 'x')
            else:
                self.displayingGraph = True
                self.calculateGraph("y=" + equation)
        elif('y' in equation):
            if('=' in equation):
                solveForVar(self, equation, 'y')
            else:
                self.displayingGraph = True    


    def drawGrid(self):
        maxY = fonts(self.app.font, self.app.unit * 0.25, False, False).render(str(self.maxY), True, Black)
        minY = fonts(self.app.font, self.app.unit * 0.25, False, False).render(str(self.minY), True, Black)
        maxX = fonts(self.app.font, self.app.unit * 0.25, False, False).render(str(self.maxX), True, Black)
        minX = fonts(self.app.font, self.app.unit * 0.25, False, False).render(str(self.minX), True, Black)
        self.app.screen.blit(maxY, maxY.get_rect(center = (self.app.width // 2, self.app.unit * 2.7)))
        self.app.screen.blit(minY, minY.get_rect(center = (self.app.width // 2, self.app.unit * 8.9)))
        self.app.screen.blit(maxX, maxX.get_rect(center = (self.app.unit * 11.2, self.app.unit * 5.8)))
        self.app.screen.blit(minX, minX.get_rect(center = (self.app.unit * 4.8, self.app.unit * 5.8)))
        for i in range(21):
            if(self.maxY - i * self.gridSize != 0):
                draw.line(self.app.screen, Grey, (self.app.unit * 5, self.app.unit * 2.8 + self.app.unit * 0.3 * i), 
                        (self.app.unit * 11, self.app.unit * 2.8 + self.app.unit * 0.3 * i), width = self.app.unit // 40)
            else:
                draw.line(self.app.screen, Black, (self.app.unit * 5, self.app.unit * 2.8 + self.app.unit * 0.3 * i), 
                        (self.app.unit * 11, self.app.unit * 2.8 + self.app.unit * 0.3 * i), width = self.app.unit // 20)
            
            if(self.minX + i * self.gridSize != 0):
                draw.line(self.app.screen, Grey, (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 2.8), 
                        (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 8.8), width = self.app.unit // 40)
            else:
                draw.line(self.app.screen, Black, (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 2.8), 
                        (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 8.8), width = self.app.unit // 20)
                
    
    def calculateGraph(self, equation):
        self.searchSteps = min(40 * (self.maxY - self.minY), self.app.searchSteps)
        step = (self.maxX - self.minX) / self.graphPoints
        xIndeces = findVarIndeces(equation, 'x')
        yIndeces = findVarIndeces(equation, 'y')
        for i in range(self.graphPoints):
            self.searchRange = (self.minY, self.maxY)
            xEquation = substituteVarInEq(equation, xIndeces, self.minX + i * step)
            self.graphX[i] = solveForVar(self, xEquation, 'y')

            self.searchRange = (self.minX, self.maxX)
            yEquation = substituteVarInEq(equation, yIndeces, self.maxY - i * step)
            self.graphY[i] = solveForVar(self, yEquation, 'x')
            print(self.graphX[i], self.graphY[i])
        self.printResult("Graph Loaded")


    def drawGraph(self):
        for index in range(self.graphPoints):
            for root in self.graphX[index]:
                draw.circle(self.app.screen, Red, 
                            (self.app.unit * 5 + round(index * self.app.unit * 6 / self.graphPoints), 
                             self.app.unit * 2.8 + round((self.maxY - root) / (self.maxY - self.minY) * self.app.unit * 6)), 
                             max(1, self.app.unit // 40))
            
            for root in self.graphY[index]:
                draw.circle(self.app.screen, Red, 
                            (self.app.unit * 5 + round((root - self.minX) / (self.maxX - self.minX) * self.app.unit * 6), 
                             self.app.unit * 2.8 + round(index * self.app.unit * 6 / self.graphPoints)),
                             max(1, self.app.unit // 40))


    def moveGraph(self, delta):
        deltaX, deltaY = delta
        deltaX *= 4
        deltaY *= 4
        if(self.maxX - self.minX > 100):
            deltaX *= 5
            deltaY *= 5
        elif(self.maxX - self.minX >= 1000):
            deltaX *= 10
            deltaY *= 10
        elif(self.maxX - self.minX >= 10000):
            deltaX *= 20
            deltaY *= 20
        self.maxX += deltaX
        self.minX += deltaX
        self.maxY += deltaY
        self.minY += deltaY
        if(self.displayingGraph):
            self.calculate(self.textBox[0].input)


    def resetGraph(self):
        self.maxX, self.minX, self.maxY, self.minY = 20, -20, 20, -20
        if(self.displayingGraph):
            self.calculate(self.textBox[0].input)


    def toHomeScreen(self):
        self.app.currentScreen = HomeScreen(self.app)
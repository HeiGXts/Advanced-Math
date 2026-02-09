from pygame import *
from globals import *
from buttons import *
from textbox import *
from mathprocessing import *


class HomeScreen:
    def __init__(self, app):
        self.app = app
        self.menuButton = Button(app, (app.width // 2, app.unit * 7), (app.unit * 2.2, app.unit * 0.8), (White, Grey), (Black, app.unit // 16), 5, 
                                    ("Start", self.app.font, app.unit * 0.5, False, False, Black), lambda: self.toMenu())
        self.quitButton = Button(app, (app.width // 2, app.unit * 8), (app.unit * 2.2, app.unit * 0.8), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("Quit", self.app.font, app.unit * 0.5, False, False, Black), lambda: exit())
        self.buttons = [self.menuButton, self.quitButton]
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


    def toMenu(self):
        self.app.currentScreen = MenuScreen(self.app)



class MenuScreen:
    def __init__(self, app):
        self.app = app
        self.backButton = Button(app, (app.unit * 0.6, app.unit * 0.6), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("←", app.font, app.unit * 0.3, False, False, Black), lambda: self.toHomeScreen())
        self.algebraButton = Button(app, (app.width // 2, app.unit * 1.5), (app.unit * 4.5, app.unit * 0.8), (White, Grey), (Black, app.unit // 16), 5, 
                                    ("Graphing Calculator", self.app.font, app.unit * 0.4, False, False, Black), lambda: self.toAlgebra())
        self.matricesButton = Button(app, (app.width // 2, app.unit * 2.5), (app.unit * 4.5, app.unit * 0.8), (White, Grey), (Black, app.unit // 16), 5, 
                                    ("Matrices", self.app.font, app.unit * 0.4, False, False, Black), lambda: self.toMatrices())
        self.buttons = [self.backButton, self.algebraButton, self. matricesButton]


    def draw(self):
        self.app.screen.fill(White)
        for button in self.buttons:
            button.draw()


    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)


    def toHomeScreen(self):
        self.app.currentScreen = HomeScreen(self.app)


    def toAlgebra(self):
        self.app.currentScreen = GraphingCalculator(self.app)


    def toMatrices(self):
        self.app.currentScreen = Matrices(self.app)



class Matrices:
    def __init__(self, app):
        self.app = app
        self.backButton = Button(app, (app.unit * 0.6, app.unit * 0.6), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("←", app.font, app.unit * 0.3, False, False, Black), lambda: self.toMenu())
        self.AMButton = Button(app, (app.unit * 1.6, app.unit * 2), (app.unit * 2.2, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("Add/Minus", app.font, app.unit * 0.3, False, False, Black), lambda: self.changeMatrixMode(0))
        self.SMButton = Button(app, (app.unit * 1.6, app.unit * 3), (app.unit * 2.2, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("Scalar Multiply", app.font, app.unit * 0.3, False, False, Black), lambda: self.changeMatrixMode(1))
        self.MDButton = Button(app, (app.unit * 1.6, app.unit * 4), (app.unit * 2.2, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("Multiply/Divide", app.font, app.unit * 0.3, False, False, Black), lambda: self.changeMatrixMode(2))
        self.enterButton = Button(app, (app.unit * 8.2, app.unit * 1), (app.unit * 1.2, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Enter", app.font, app.unit * 0.3, False, False, Black), lambda: self.confirmDimension())
        self.nextButton = Button(app, (app.unit * 8.2, app.unit * 1), (app.unit * 1.2, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Next", app.font, app.unit * 0.3, False, False, Black), lambda: self.nextMatrix())
        self.confirmButton = Button(app, (app.unit * 8.2, app.unit * 1), (app.unit * 1.2, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Confirm", app.font, app.unit * 0.3, False, False, Black), lambda: self.calculateMatrix())
        self.returnButton = Button(app, (app.unit * 9.5, app.unit * 1), (app.unit * 1.2, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Back", app.font, app.unit * 0.3, False, False, Black), lambda: self.returnMatrix())
        self.buttons = [self.backButton, self.AMButton, self.SMButton, self.MDButton, self.enterButton]
        self.textBox1 = TextBox(app, (app.unit * 3.1, app.unit * 1.5), (app.unit * 0.8, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (app.font, app.unit * 0.3, False, False, Black))
        self.textBox2 = TextBox(app, (app.unit * 4.5, app.unit * 1.5), (app.unit * 0.8, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (app.font, app.unit * 0.3, False, False, Black))
        self.textBox3 = TextBox(app, (app.unit * 6.1, app.unit * 1.5), (app.unit * 0.8, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (app.font, app.unit * 0.3, False, False, Black))
        self.textBox4 = TextBox(app, (app.unit * 7.5, app.unit * 1.5), (app.unit * 0.8, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (app.font, app.unit * 0.3, False, False, Black))
        self.textBox = [self.textBox1, self.textBox2]
        
        self.buttons[1].appointedColor = Grey
        self.matrices = []
        self.scalar = None
        self.answer = []
        self.matrixMode = 0

        self.message = 0
        self.messageRect = 0


    def draw(self):
        self.app.screen.fill(White)

        if(self.matrixMode == 0):
            if(self.matrices == []):
                text1 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("Enter Matrices Dimensions", True, Black)
                self.app.screen.blit(text1, text1.get_rect(midleft = (self.app.unit * 3, self.app.unit * 1)))
                text2 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("X", True, Black)
                self.app.screen.blit(text2, text2.get_rect(center = (self.app.unit * 4.2, self.app.unit * 1.8)))
            else:
                if(self.matrices[0][0][0] == None):
                    text1 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("Enter the First Matrix", True, Black)
                else:
                    text1 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("Enter the Second Matrix", True, Black)
                self.app.screen.blit(text1, text1.get_rect(midleft = (self.app.unit * 3, self.app.unit * 1)))
        elif(self.matrixMode == 1):
            if(self.matrices == []):
                text1 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("Enter Matrix Dimension", True, Black)
                self.app.screen.blit(text1, text1.get_rect(midleft = (self.app.unit * 3, self.app.unit * 1)))
                text2 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("X", True, Black)
                self.app.screen.blit(text2, text2.get_rect(center = (self.app.unit * 4.2, self.app.unit * 1.8)))
            else:
                text1 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("Enter the Matrix and the Scalar", True, Black)
                self.app.screen.blit(text1, text1.get_rect(midleft = (self.app.unit * 3, self.app.unit * 1)))
                text2 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("X", True, Black)
                self.app.screen.blit(text2, text2.get_rect(center = (self.app.unit * (len(self.matrices[0][0]) * 1.1 + 3.5), self.app.unit * (len(self.matrices[0]) * 0.4 + 1.4))))
        elif(self.matrixMode == 2):
            if(self.matrices == []):
                text1 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("Enter Matrices Dimensions", True, Black)
                self.app.screen.blit(text1, text1.get_rect(midleft = (self.app.unit * 3, self.app.unit * 1)))
                text2 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("X", True, Black)
                self.app.screen.blit(text2, text2.get_rect(center = (self.app.unit * 4.2, self.app.unit * 1.8)))
                text3 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("X", True, Black)
                self.app.screen.blit(text3, text3.get_rect(center = (self.app.unit * 7.2, self.app.unit * 1.8)))
            else:
                if(self.matrices[0][0][0] == None):
                    text1 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("Enter the First Matrix", True, Black)
                else:
                    text1 = fonts(self.app.font, self.app.unit * 0.3, True, False).render("Enter the Second Matrix", True, Black)
                self.app.screen.blit(text1, text1.get_rect(midleft = (self.app.unit * 3, self.app.unit * 1)))

        for button in self.buttons:
            button.draw()

        for textbox in self.textBox:
            textbox.draw()

        if(self.message != 0):
            self.app.screen.blit(self.message, self.messageRect)


    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)
        
        for textbox in self.textBox:
            textbox.handleEvent(event)

        if(event.type == KEYDOWN and event.key == K_RETURN):
            if(self.answer == []):
                if(self.textBox[-1].entering):
                    self.textBox[-1].entering = False
                    if(self.matrices == []):
                        self.confirmDimension()
                    elif(self.matrices[0][0][0] == None):
                        if(self.matrixMode == 1):
                            self.calculateSM()
                        else:
                            self.nextMatrix()
                    else:
                        self.calculateMatrix()
                else:
                    for i in range(len(self.textBox) - 2, -1, -1):
                        if(self.textBox[i].entering):
                            self.textBox[i + 1].entering = True
                            self.textBox[i].entering = False

    
    def changeMatrixMode(self, mode):
        if(self.matrixMode != mode):
            self.matrices = []
            self.buttons = [self.backButton, self.AMButton, self.SMButton, self.MDButton, self.enterButton]
            self.buttons[self.matrixMode + 1].appointedColor = None
            self.matrixMode = mode
            self.buttons[self.matrixMode + 1].appointedColor = Grey
            if(mode < 2):
                self.textBox = [self.textBox1, self.textBox2]
            else:
                self.textBox = [self.textBox1, self.textBox2, self.textBox3, self.textBox4]

    
    def confirmDimension(self):
        if(self.matrixMode < 2):
            input = self.processDimension(2)
            if(input != None):
                self.message = 0
                self.matrices.append([[None for j in range(input[1])] for i in range(input[0])])
                self.appendTextBoxes(0)
                if(self.matrixMode == 0):
                    self.matrices.append([[None for j in range(input[1])] for i in range(input[0])])
                    self.buttons[4] = self.nextButton
                else:
                    self.textBox.append(TextBox(self.app, (self.app.unit * (len(self.matrices[0][0]) * 1.1 + 3.8), self.app.unit * (len(self.matrices[0]) * 0.4 + 1.1)), 
                                                (self.app.unit, self.app.unit * 0.6), (DarkGrey, Black, self.app.unit // 16), (self.app.font, self.app.unit * 0.3, False, False, Black)))
                    self.buttons[4] = self.confirmButton
        else:
            input = self.processDimension(4)
            if(input != None):
                if(input[0] != input[3] and input[1] != input[2]):
                    self.printMessage("Error: Invalid Dimensions For Multiplication")
                    return
                self.message = 0
                self.matrices.append([[None for j in range(input[1])] for i in range(input[0])])
                self.matrices.append([[None for j in range(input[3])] for i in range(input[2])])
                self.appendTextBoxes(0)
                self.buttons[4] = self.nextButton
        self.buttons.append(self.returnButton)


    def nextMatrix(self):
        textBoxIndex = 0
        for i in range(len(self.matrices[0])):
            for j in range(len(self.matrices[0][0])):
                try:
                    self.matrices[0][i][j] = eval(self.textBox[textBoxIndex].input)
                except Exception as e:
                    self.printMessage(f"Error: {e}")
                    return
                textBoxIndex += 1
        self.appendTextBoxes(1)


    def returnMatrix(self):
        if(self.answer == []):
            if(self.matrices[0][0][0] == None):
                self.matrices = []
                self.buttons = [self.backButton, self.AMButton, self.SMButton, self.MDButton, self.enterButton]
                self.textBox = [self.textBox1, self.textBox2]
                if(self.matrixMode == 2):
                    self.textBox = [self.textBox1, self.textBox2, self.textBox3, self.textBox4]
            else:
                self.matrices[0] = [[None for j in range(len(self.matrices[0][0]))] for i in range(len(self.matrices[0]))]
                self.buttons[4] = self.nextButton
                self.appendTextBoxes(0)
        else:
            self.matrices = []
            self.answer = []
            self.buttons = [self.backButton, self.AMButton, self.SMButton, self.MDButton, self.enterButton]
            self.textBox = [self.textBox1, self.textBox2]
            if(self.matrixMode == 2):
                self.textBox = [self.textBox1, self.textBox2, self.textBox3, self.textBox4]
            

    def appendTextBoxes(self, mode):
        self.textBox = []
        for i in range(len(self.matrices[mode])):
            for j in range(len(self.matrices[mode][0])):
                self.textBox.append(TextBox(self.app, (self.app.unit * (3.2 + j * 1.1), self.app.unit * (1.5 + i * 0.8)), (self.app.unit, self.app.unit * 0.6), 
                                            (DarkGrey, Black, self.app.unit // 16), (self.app.font, self.app.unit * 0.3, False, False, Black)))
                

    def calculateMatrix(self):
        if(self.matrixMode == 0):
            self.calculateAM()
        elif(self.matrixMode == 1):
            self.calculateSM()
        else:
            self.calculateMD()


    def calculateAM(self):
        self.answer = [[None for j in range(len(self.matrices[0][0]))] for i in range(self.matrices[0])]
        for i in range(len(self.answer)):
            for j in range(len(self.answer[0])):
                self.answer[i][j] = self.matrices[0][i][j] + self.matrices[1][i][j]


    def calculateSM(self):
        self.answer = [[None for j in range(len(self.matrices[0][0]))] for i in range(self.matrices[0])]


    def calculateMD(self):
        pass

    
    def processDimension(self, mode):
        input = [0 for i in range(mode)]
        for i in range(mode):
            try:
                input[i] = eval(self.textBox[i].input)
            except Exception as e:
                self.printMessage(f"Error: {e}")
                return
            if(not isinstance(input[i], int)):
                self.printMessage("Error: Not An Integer")
                return
            if(input[i] < 1 or input[i] > 10):
                self.printMessage("Error: Dimension Out of Range (1-10)")
                return
        return input


    def printMessage(self, message):
        self.message = fonts(self.app.font, self.app.unit * 0.3, True, False).render(message, True, Black)
        self.messageRect = self.message.get_rect()
        if(self.matrices == []):
            self.messageRect.midleft = (self.app.unit * 3, self.app.unit * 2.5)
        else:
            self.messageRect.midleft = (self.app.unit * 8, self.app.unit * 1)


    def toMenu(self):
        self.app.currentScreen = MenuScreen(self.app)



class GraphingCalculator:
    def __init__(self, app):
        self.app = app
        self.backButton = Button(app, (app.unit * 0.6, app.unit * 0.6), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 5, 
                                 ("←", app.font, app.unit * 0.3, False, False, Black), lambda: self.toMenu())
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
        self.zoomIn = Button(app, (app.unit * 12.5, app.unit * 7), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 8, 
                                  ("+", app.font, app.unit * 0.3, False, False, Black), lambda: self.zoom(True))
        self.zoomOut = Button(app, (app.unit * 13.5, app.unit * 7), (app.unit * 0.7, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 8, 
                                  ("-", app.font, app.unit * 0.3, False, False, Black), lambda: self.zoom(False))
        self.toggleExtrema = Button(app, (app.unit * 3, app.unit * 3), (app.unit * 2, app.unit * 0.7), (White, Grey), (Black, app.unit // 16), 8, 
                                  ("Extremas", app.font, app.unit * 0.3, False, False, Black), lambda: self.extrema())
        self.buttons = [self.backButton, self.enterButton1, self.graphMoveUp, self.graphMoveDown, self.graphMoveLeft, self.graphMoveRight, 
                        self.graphResetButton, self.zoomIn, self.zoomOut, self.toggleExtrema]
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
        self.graphPoints = 120
        self.graphX = [0 for i in range(self.graphPoints)]
        self.graphY = [0 for i in range(self.graphPoints)]

        self.displayingExtremas = False
        self.max = []
        self.min = []

        self.searchRange = self.app.searchRange
        self.searchSteps = self.app.searchSteps
        self.graphingSteps = self.app.graphingSteps


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
            if(self.displayingExtremas):
                self.drawExtremas()


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
        self.displayingExtremas = False
        self.max = []
        self.min = []
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
            draw.line(self.app.screen, Grey, (self.app.unit * 5, self.app.unit * 2.8 + self.app.unit * 0.3 * i), 
                        (self.app.unit * 11, self.app.unit * 2.8 + self.app.unit * 0.3 * i), width = self.app.unit // 40)
            
            draw.line(self.app.screen, Grey, (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 2.8), 
                        (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 8.8), width = self.app.unit // 40)
            
        if(self.minY < 0 < self.maxY):
            draw.line(self.app.screen, Black, (self.app.unit * 5, self.app.unit * 2.8 + round(self.app.unit * 6 * (self.maxY / (self.maxY - self.minY)))), 
                        (self.app.unit * 11, self.app.unit * 2.8 + round(self.app.unit * 6 * (self.maxY / (self.maxY - self.minY)))), width = self.app.unit // 20)
        if(self.minX < 0 < self.maxX):
            draw.line(self.app.screen, Black, (self.app.unit * 5 + round(self.app.unit * 6 * (abs(self.minX) / (self.maxX - self.minX))), self.app.unit * 2.8), 
                        (self.app.unit * 5 + round(self.app.unit * 6 * (abs(self.minX) / (self.maxX - self.minX))), self.app.unit * 8.8), width = self.app.unit // 20)
                
    
    def calculateGraph(self, equation):
        self.searchSteps = min(self.graphingSteps * (self.maxY - self.minY), self.app.searchSteps // 10)
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
            self.updateExtrema(self.graphX[i], self.graphY[i], self.minX + i * step, self.maxY - i * step)
        self.min = list(set(self.min))
        self.max = list(set(self.max))
        self.printResult("Graph Loaded")

    
    def updateExtrema(self, graphX, graphY, x, y):
        for gx in graphX:
            if(self.max == [] or self.max[0][1] < gx):
                self.max = [(x, gx)]
            elif(self.max[0][1] == gx):
                self.max.append((x, gx))
            
            if(self.min == [] or self.min[0][1] > gx):
                self.min = [(x, gx)]
            elif(self.min[0][1] == gx):
                self.min.append((x, gx))
        
        if(graphY != []):
            if(self.max == [] or self.max[0][1] <= y):
                if(self.max != [] and self.max[0][1] < y):
                    self.max = []
                for gy in graphY:
                    self.max.append((gy, y))
            
            if(self.min == [] or self.min[0][1] >= y):
                if(self.min != [] and self.min[0][1] > y):
                    self.min = []
                for gy in graphY:
                    self.min.append((gy, y))


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
        size = self.maxX - self.minX
        deltaX *= 4
        deltaY *= 4
        if(size >= 10000):
            deltaX *= 250
            deltaY *= 250
        elif(size >= 1000):
            deltaX *= 50
            deltaY *= 50
        elif(size > 100):
            deltaX *= 5
            deltaY *= 5
        self.maxX += deltaX
        self.minX += deltaX
        self.maxY += deltaY
        self.minY += deltaY
        if(self.displayingGraph):
            self.calculate(self.textBox[0].input)
            self.printResult("Graph Shifted")


    def zoom(self, zoomIn):
        size = self.maxX - self.minX
        if(zoomIn):
            if(size == 10):
                return
            if(size == 20):
                self.maxX -= 5
                self.maxY -= 5
                self.minX += 5
                self.minY += 5
            elif(size <= 100):
                self.maxX -= 10
                self.maxY -= 10
                self.minX += 10
                self.minY += 10
            elif(size <= 1000):
                self.maxX -= 100
                self.maxY -= 100
                self.minX += 100
                self.minY += 100
            else:
                self.maxX -= 1000
                self.maxY -= 1000
                self.minX += 1000
                self.minY += 1000
        else:
            if(size == 10):
                self.maxX += 5
                self.maxY += 5
                self.minX -= 5
                self.minY -= 5
            elif(size >= 100):
                self.maxX += 100
                self.maxY += 100
                self.minX -= 100
                self.minY -= 100
            elif(size >= 1000):
                self.maxX += 1000
                self.maxY += 1000
                self.minX -= 1000
                self.minY -= 1000
            else:
                self.maxX += 10
                self.maxY += 10
                self.minX -= 10
                self.minY -= 10
        self.gridSize = (self.maxX - self.minX) // 20
        if(self.displayingGraph):
            self.calculate(self.textBox[0].input)
            self.printResult("Graph Zoomed")
            

    def resetGraph(self):
        self.maxX, self.minX, self.maxY, self.minY = 20, -20, 20, -20
        self.gridSize = 2
        if(self.displayingGraph):
            self.calculate(self.textBox[0].input)
            self.printResult("Graph Reset")

    
    def extrema(self):
        if(self.displayingGraph):
            self.displayingExtremas = not self.displayingExtremas
            print(self.min, self.max)


    def drawExtremas(self):
        messageMin = fonts(self.app.font, self.app.unit * 0.25, True, False).render("Min", True, Black)
        messageMax = fonts(self.app.font, self.app.unit * 0.25, True, False).render("Max", True, Black)
        minRect = messageMin.get_rect()
        minRect.midtop = (self.app.unit * 2.2, self.app.unit * 3.5)
        maxRect = messageMax.get_rect()
        maxRect.midtop = (self.app.unit * 3.8, self.app.unit * 3.5)
        self.app.screen.blit(messageMin, minRect)
        self.app.screen.blit(messageMax, maxRect)
        for i in range(len(self.min)):
            if(i < 15):
                messageMin = fonts(self.app.font, self.app.unit * 0.2, False, False).render(f"({round(self.min[i][0], 2)},{round(self.min[i][1], 2)})", True, Black)
                minRect.midtop = (self.app.unit * 2.2, self.app.unit * 4 + i * 0.5 * self.app.unit)
                self.app.screen.blit(messageMin, minRect)
            draw.circle(self.app.screen, Green, 
                    (self.app.unit * 5 + round((self.min[i][0] - self.minX) / (self.maxX - self.minX) * self.app.unit * 6), 
                     self.app.unit * 2.8 + round((self.maxY - self.min[i][1]) / (self.maxY - self.minY) * self.app.unit * 6)), 
                     max(1, self.app.unit // 20))
        for i in range(len(self.max)):
            if(i < 15):
                messageMax = fonts(self.app.font, self.app.unit * 0.2, False, False).render(f"({round(self.max[i][0], 2)},{round(self.max[i][1], 2)})", True, Black)
                maxRect.midtop = (self.app.unit * 3.8, self.app.unit * 4 + i * 0.5 * self.app.unit)
                self.app.screen.blit(messageMax, maxRect)
            draw.circle(self.app.screen, Blue, 
                    (self.app.unit * 5 + round((self.max[i][0] - self.minX) / (self.maxX - self.minX) * self.app.unit * 6), 
                     self.app.unit * 2.8 + round((self.maxY - self.max[i][1]) / (self.maxY - self.minY) * self.app.unit * 6)), 
                     max(1, self.app.unit // 20))


    def toMenu(self):
        self.app.currentScreen = MenuScreen(self.app)
from pygame import *
from globals import *
from buttons import *
from textbox import *
import math

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
                                 ("←", self.app.font, app.unit * 0.3, False, False, Black), lambda: self.toHomeScreen())
        self.enterButton1 = Button(app, (app.unit * 14.5, app.unit * 2), (app.unit, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Enter", self.app.font, app.unit * 0.3, False, False, Black), lambda: self.calculate())
        self.enterButton2 = Button(app, (app.unit * 8.5, app.unit * 2.5), (app.unit, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Enter", self.app.font, app.unit * 0.3, False, False, Black), lambda: self.calculate())
        self.buttons = [self.backButton, self.enterButton1]
        self.textBox1 = TextBox(app, (app.unit * 4, app.unit), (app.unit * 11, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (self.app.font, app.unit * 0.3, False, False, Black))
        self.textBox2 = TextBox(app, (app.unit * 4.5, app.unit * 2.5), (app.unit * 4, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (self.app.font, app.unit * 0.3, False, False, Black))
        self.textBox = [self.textBox1]
        self.result = 0
        self.resultRect = 0

        self.displayingGraph = False
        self.minX = -20
        self.minY = -20
        self.maxX = 20
        self.maxY = 20
        self.gridSize = (self.maxX - self.minX) // 20
        self.variable = ''

        self.searchRange = (-100000, 100000)
        self.searchSteps = 5000

    def draw(self):
        self.app.screen.fill(White)

        if(self.result != 0):
            self.app.screen.blit(self.result, self.resultRect)

        for button in self.buttons:
            button.draw()

        for textbox in self.textBox:
            textbox.draw()

        self.drawGrid()

        if(self.displayingGraph):
            self.drawGraph()


    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)

        for textbox in self.textBox:
            textbox.handleEvent(event)

        if(event.type == KEYDOWN and event.key == K_RETURN):
            if(self.textBox[0].entering == True):
                self.calculate()


    def calculate(self):
        equation = self.textBox[0].input
        self.variable = ''
        self.displayingGraph = False
        if(len(self.textBox) == 2):
            self.textBox.pop(1)
            self.buttons.pop(1)
        if(equation == ""):
            self.result = 0
            return
        if(self.checkAlpha(equation)):
            self.processAlpha(equation)
        elif('=' in equation):
            self.equalEval(equation)
        else:
            self.printResult(str(self.calculateEquation(equation)))


    def checkAlpha(self, equation):
        for char in equation:
            if(char.isalpha()):
                return True
        return False


    def equalEval(self, equation):
        equalIndex = equation.index('=')
        left = self.processEquation(equation[:equalIndex])
        right = self.processEquation(equation[equalIndex + 1:])
        try:
            self.printResult(str(eval(left) == eval(right)))
        except:
            self.printResult("Error: BooleanError")


    def printResult(self, result):
        self.result = fonts(self.app.font, self.app.unit * 0.3, True, False).render(result, True, Black)
        self.resultRect = self.result.get_rect()
        self.resultRect.midleft = (self.app.unit * 4, self.app.unit * 2)


    def calculateEquation(self, equation):
        equation = self.processEquation(equation)
        if(equation == None):
            return
        print(equation)
        try:
            return eval(equation)
        except Exception as e:
            return f"Error: {type(e).__name__}"
        

    def processEquation(self, equation):
        index = 0
        length = len(equation)
        while index < length:
            print(equation)
            if(equation[index] == '^'):
                equation = self.power(equation, index)
                length = len(equation)
            elif(equation[index] == '!'):
                equation = self.factorial(equation, index)
                length = len(equation)
            elif(equation[index] == '|'):
                equation = self.absolute(equation, index)
                length = len(equation)
            index += 1
        return equation
        

    def processAlpha(self, equation):
        for char in equation:
            if(char.isalpha() and char != 'x' and char != 'y'):
                if(not self.variable):
                    self.variable = char
                elif(self.variable != char):
                    self.printResult("Error: MoreThanOneUnknown")
                    return
                
        if(self.variable and ('x' in equation or 'y' in equation)):
            self.textBox.append(self.textBox2)
            self.buttons.append(self.enterButton2)
        elif(self.variable):
            self.solveForVar(equation, self.variable)
        else:
            self.solveEquation(equation)
        

    def solveEquation(self, equation):
        if('y' in equation and 'x' in equation):
            if('=' in equation):
                self.displayingGraph = True
            else:
                self.printResult("Error: MoreThanOneUnknown")
        elif('x' in equation):
            if('=' in equation):
                self.solveForVar(equation, 'x')
            else:
                self.displayingGraph = True
        elif('y' in equation):
            if('=' in equation):
                self.solveForVar(equation, 'y')
            else:
                self.displayingGraph = True


    def solveForVar(self, equation, var):
        equalIndex = equation.index('=')
        left = self.processEquation(equation[:equalIndex])
        right = self.processEquation(equation[equalIndex + 1:])

        roots = []
        lower, upper = self.searchRange
        step = (upper - lower) / self.searchSteps

        def f(x):
            try:
                return eval(left, {var: x}) - eval(right, {var: x})
            except:
                self.printResult("Error: EquationSolveError")
                return float("nan")
        
        def bisection(x1, x2):
            f1, f2 = f(x1), f(x2)
            if(f1 * f2 > 0):
                return
            for i in range(50):
                mid = (x1 + x2) / 2
                fMid = f(mid)
                if(abs(fMid) < 1e-7):
                    return mid
                if(f1 * fMid < 0):
                    x2, f2 = mid, fMid
                else:
                    x1, f1 = mid, fMid
            return (x1 + x2) / 2
        
        x = lower
        while x < upper:
            root = bisection(x, x + step)
            if(root != None):
                if(not any(abs(root - r) < 1e-5 for r in roots)):
                    roots.append(round(root, 6))
            x += step

        if(self.displayingGraph):
            return roots
        else:
            self.printResult(f"{var} = {roots}")
            return
    

    def power(self, equation, index):
        try:
            equation = equation[:index] + '**' + equation[index + 1:]
            return equation
        except:
            self.printResult("Error: PowerError")

        
    def factorial(self, equation, index):
        result = equation
        if(index == 0):
            self.printResult("Error: FactorialError")
        elif(equation[index - 1] == ')'):
            i = index - 2
            parantheses = 0
            while i >= 0:
                if(equation[i] == '(' and parantheses == 0):
                    try:
                        result = equation[:i] + f"math.factorial({self.processEquation(equation[i:index])})"
                    except:
                        return equation
                    if(len(equation) > index + 1):
                        result += equation[index + 1:]
                    return result
                elif(equation[i] == '('):
                    parantheses -= 1
                if(equation[i] == ')'):
                    parantheses += 1
                i -= 1
            return result
        else:
            i = index - 2
            while i >= -1:
                if((not equation[i].isdigit() and equation[i] != '.') or i == -1):
                    try:
                        result = equation[:i + 1] + f"math.factorial({equation[i + 1:index]})"
                    except:
                        return equation
                    if(len(equation) > index + 1):
                        result += equation[index + 1:]
                    return result
                i -= 1
        

    def absolute(self, equation, index):
        result = equation
        for i in range(index + 2, len(equation)):
            if(equation[i] == '|'):
                try:
                    result = equation[:index] + f"abs({equation[index + 1:i]})"
                    if(i < len(equation) - 1):
                        result += equation[i + 1:]
                except:
                    continue
                return result
        return result


    def drawGrid(self):
        for i in range(21):
            if(self.maxY - i * self.gridSize != 0):
                draw.line(self.app.screen, Grey, (self.app.unit * 5, self.app.unit * 3.5 + self.app.unit * 0.3 * i), 
                        (self.app.unit * 11, self.app.unit * 3.5 + self.app.unit * 0.3 * i), width = self.app.unit // 40)
            else:
                draw.line(self.app.screen, Black, (self.app.unit * 5, self.app.unit * 3.5 + self.app.unit * 0.3 * i), 
                        (self.app.unit * 11, self.app.unit * 3.5 + self.app.unit * 0.3 * i), width = self.app.unit // 20)
            
            if(self.minX + i * self.gridSize != 0):
                draw.line(self.app.screen, Grey, (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 3.5), 
                        (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 9.5), width = self.app.unit // 40)
            else:
                draw.line(self.app.screen, Black, (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 3.5), 
                        (self.app.unit * 5 + self.app.unit * 0.3 * i, self.app.unit * 9.5), width = self.app.unit // 20)


    def drawGraph(self):
        equation = self.textBox[0].input
        step = (self.maxX - self.minX) / 100
        index = 0

        for i in range(100):
            while 'x' in equation:
                if(equation[index] == 'x'):
                    if(index < len(equation) - 1 and equation[index + 1].isdigit()):
                        self.printResult("Error: SyntaxError")
                        return
                    if(index != 0 and equation[index - 1].isdigit()):
                        try:
                            equation = equation[:index - 1] + '*' + str(self.minX + i * step) + equation[index + 1:]
                        except:
                            equation = equation[:index - 1] + '*' + str(self.minX + i * step)
                index += 1


    def toHomeScreen(self):
        self.app.currentScreen = HomeScreen(self.app)
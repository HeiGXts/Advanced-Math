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
                                 ("←", app.font, app.unit * 0.3, False, False, Black), lambda: self.toHomeScreen())
        self.enterButton1 = Button(app, (app.unit * 14.5, app.unit * 1.3), (app.unit, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Enter", app.font, app.unit * 0.3, False, False, Black), lambda: self.calculate(self.textBox[0].input))
        self.enterButton2 = Button(app, (app.unit * 9.5, app.unit * 2), (app.unit, app.unit * 0.5), (White, Grey), (Black, app.unit // 16), 1, 
                                  ("Enter", app.font, app.unit * 0.3, False, False, Black), lambda: self.substituteVariable())
        self.buttons = [self.backButton, self.enterButton1]
        self.textBox1 = TextBox(app, (app.unit * 4, app.unit * 0.3), (app.unit * 11, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (app.font, app.unit * 0.3, False, False, Black))
        self.textBox2 = TextBox(app, (app.unit * 4.5, app.unit * 1.7), (app.unit * 4, app.unit * 0.6), (DarkGrey, Black, app.unit // 16), 
                                   (app.font, app.unit * 0.3, False, False, Black))
        self.textBox = [self.textBox1]
        self.result = 0
        self.resultRect = 0
        self.radMode = True

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
        self.variable = 0
        self.result = 0
        self.displayingGraph = False
        self.textBox2 = TextBox(self.app, (self.app.unit * 4.5, self.app.unit * 1.7), (self.app.unit * 4, self.app.unit * 0.6), (DarkGrey, Black, self.app.unit // 16), 
                                   (self.app.font, self.app.unit * 0.3, False, False, Black))
        if(len(self.textBox) == 2):
            self.textBox.pop(1)
            self.buttons.pop(2)
        if(equation == ""):
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
        self.resultRect.midleft = (self.app.unit * 4, self.app.unit * 1.3)


    def calculateEquation(self, equation):
        equation = self.processEquation(equation)
        if(equation == None):
            return
        try:
            return eval(equation)
        except Exception as e:
            return f"Error: {type(e).__name__}"
        

    def processEquation(self, equation):
        index = 0
        length = len(equation)
        while index < length:
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
        hasAlpha = False
        index = 0
        length = len(equation)
        self.searchRange = self.app.searchRange
        self.searchSteps = self.app.searchSteps
        while index < length:
            if(equation[index].isalpha()):
                if(length - index >= 3):
                    isInverse = -1
                    if(equation[index:index + 3] in Trig):
                        isInverse = 0
                        equation = self.substituteTrig(equation, index, 0)
                    elif(length - index >= 6 and equation[index:index + 6] in InverseTrig):
                        isInverse = 1
                        equation = self.substituteTrig(equation, index, 1)
                    if(isInverse != -1):
                        if(equation == None):
                            self.printResult("Error: SyntaxError")
                            return
                        length = len(equation)
                        index += 9 + isInverse
                        if(not self.radMode):
                            index += 13
                        if(not equation[index].isalpha()):
                            index += 1
                            continue
                
                hasAlpha = True
                if(equation[index] != 'x' and equation[index] != 'y'):
                    if(not self.variable):
                        self.variable = equation[index]
                    elif(self.variable != equation[index]):
                        self.printResult("Error: MoreThanOneUnknown")
                        return
                if(index != 0 and equation[index - 1].isdigit()):
                    equation = equation[:index] + "*" + equation[index:]
                    length += 1
                if(index != length - 1 and equation[index + 1].isdigit()):
                    self.printResult("Error: SyntaxError")
                    return
            index += 1
        if(not hasAlpha):
            self.printResult(str(round(self.calculateEquation(equation), 6)))
            return
                
        if(self.variable and '=' in equation and not('y' in equation or 'x' in equation)):
            self.solveForVar(equation, self.variable)
        elif(self.variable):
            self.textBox.append(self.textBox2)
            self.buttons.append(self.enterButton2)
        else:
            self.solveEquation(equation)

    
    def substituteTrig(self, equation, index, isInverse):
        length = len(equation)
        if(index + 3 + isInverse * 3 == length):
            return
        rad = ''
        i = index + 4 + isInverse * 3
        rad = equation[index + 3 + isInverse * 3:]
        trig = ''
        endIndex = length
        if(isInverse):
            trig = 'a' + equation[index + 3:index + 6]
        else:
            trig = equation[index:index + 3]

        if(equation[index + 3 + isInverse * 3] == '('):
            parantheses = 0
            while i < length:
                if(equation[i] == '('):
                    parantheses += 1
                elif(equation[i] == ')' and parantheses == 0):
                    rad = equation[index + 3 + isInverse * 3:i]
                    endIndex = i + 1
                    break
                elif(equation[i] == ')'):
                    parantheses -= 1
                i += 1
            if(parantheses != 0):
                return
        elif(equation[index + 3 + isInverse * 3].isdigit()):
            while i < length:
                if(not equation[i].isdigit() and equation[i] != '.'):
                    rad = equation[index + 3 + isInverse * 3:i]
                    endIndex = i
                    break
                i += 1
        elif(equation[index + 3 + isInverse * 3].isalpha()):
            rad = equation[index + 3 + isInverse * 3]
            endIndex = index + 4 + isInverse * 3
        if(self.radMode):
            try:
                return equation[:index] + f"math.{trig}({rad})" + equation[endIndex:]
            except:
                return equation[:index] + f"math.{trig}({rad})"
        else:
            try:
                return equation[:index] + f"math.{trig}(math.radians({rad}))" + equation[endIndex:]
            except:
                return equation[:index] + f"math.{trig}(math.radians({rad}))"
                
                
    
    def substituteVariable(self):
        equation = self.textBox[0].input
        variable = self.textBox[1].input
        index = 0

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
                self.solveForVar(equation, 'x')
            else:
                self.displayingGraph = True
                self.calculateGraph("y=" + equation)
        elif('y' in equation):
            if('=' in equation):
                self.solveForVar(equation, 'y')
            else:
                self.displayingGraph = True


    def solveForVar(self, equation, var):
        equalIndex = equation.index('=')
        left = self.processEquation(equation[:equalIndex])
        right = self.processEquation(equation[equalIndex + 1:])
        print(left, right)

        roots = []
        lower, upper = self.searchRange
        step = (upper - lower) / self.searchSteps

        def f(x):
            safeENV = {
                var:x, "math":math
            }
            try:
                return eval(left, safeENV) - eval(right, safeENV)
            except:
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
                if(not any(abs(root - r) < 1e-6 for r in roots)):
                    roots.append(round(root, 6))
            x += step

        if(roots == [] and not self.displayingGraph):
            self.printResult("No Root Found")
            return
        elif(len(roots) == self.searchSteps and not self.displayingGraph):
            self.printResult("Cannot Converge")
            return

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
        xIndeces, yIndeces = self.findVarIndeces(equation)
        for i in range(self.graphPoints):
            xEquation = equation
            self.searchRange = (self.minY, self.maxY)
            for j in range(len(xIndeces) - 1, -1, -1):
                if(xIndeces[j] == len(xEquation) - 1):
                    xEquation = xEquation[:xIndeces[j]] + f"({self.minX + i * step})"
                else:
                    xEquation = xEquation[:xIndeces[j]] + f"({self.minX + i * step})" + xEquation[xIndeces[j] + 1:]
            self.graphX[i] = self.solveForVar(xEquation, 'y')

            yEquation = equation
            self.searchRange = (self.minX, self.maxX)
            for j in range(len(yIndeces) - 1, -1, -1):
                if(yIndeces[j] == len(yEquation) - 1):
                    yEquation = yEquation[:yIndeces[j]] + f"({self.maxY - i * step})"
                else:
                    yEquation = yEquation[:yIndeces[j]] + f"({self.maxY - i * step})" + yEquation[yIndeces[j] + 1:]
            self.graphY[i] = self.solveForVar(yEquation, 'x')
            print(self.graphX[i], self.graphY[i])
        self.printResult("Graph Loaded")

    
    def findVarIndeces(self, equation):
        xIndeces = []
        yIndeces = []
        for i in range(len(equation)):
            if(equation[i] == 'x'):
                xIndeces.append(i)
            elif(equation[i] == 'y'):
                yIndeces.append(i)
        return (xIndeces, yIndeces)


    def drawGraph(self):
        for index in range(self.graphPoints):
            for root in self.graphX[index]:
                draw.circle(self.app.screen, Red, 
                            (self.app.unit * 5 + round(index * self.app.unit * 6 / self.graphPoints), 
                             self.app.unit * 2.8 + round((self.maxY - root) / (self.maxY - self.minY) * self.app.unit * 6)), 
                             max(1, self.app.unit // 40))
            
            for root in self.graphY[index]:
                draw.circle(self.app.screen, Red, 
                            (self.app.unit * 8 + round(root / (self.maxX - self.minX) * self.app.unit * 6), 
                             self.app.unit * 2.8 + round(index * self.app.unit * 6 / self.graphPoints)),
                             max(1, self.app.unit // 40))


    def toHomeScreen(self):
        self.app.currentScreen = HomeScreen(self.app)
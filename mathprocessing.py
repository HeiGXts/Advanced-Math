from pygame import *
from globals import *
import math


def solveForVar(self, equation, var):
    equalIndex = equation.index('=')
    left = processEquation(self, equation[:equalIndex])
    right = processEquation(self, equation[equalIndex + 1:])
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

    if(not self.displayingGraph):
        roots = checkSolution(self, roots, left, right, findVarIndeces(left + "=" + right, var))

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
        

def checkAlpha(equation):
    for char in equation:
        if(char.isalpha()):
            return True
    return False


def processEquation(self, equation):
    index = 0
    length = len(equation)
    while index < length:
        if(equation[index] == '^'):
            equation = power(self, equation, index)
            length = len(equation)
        elif(equation[index] == '!'):
            equation = factorial(self, equation, index)
            length = len(equation)
        elif(equation[index] == '|'):
            equation = absolute(self, equation, index)
            length = len(equation)
        index += 1
    return equation


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
                        result = equation[:i] + f"math.factorial({processEquation(self, equation[i:index])})"
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
        parantheses = 0
        for i in range(index + 2, len(equation)):
            if(equation[i] == '|' and parantheses == 0):
                try:
                    result = equation[:index] + f"abs({equation[index + 1:i]})"
                    if(i < len(equation) - 1):
                        result += equation[i + 1:]
                except:
                    continue
                return result
            elif(equation[i] == '('):
                parantheses += 1
            elif(equation[i] == ')'):
                if(parantheses == 0):
                    self.printResult("Error: SyntaxError")
                else:
                    parantheses -= 1
        return result


def equalEval(self, equation):
        equalIndex = equation.index('=')
        left = processEquation(self, equation[:equalIndex])
        right = processEquation(self, equation[equalIndex + 1:])
        try:
            self.printResult(str(eval(left) == eval(right)))
        except:
            self.printResult("Error: BooleanError")


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
                        equation = substituteTrig(self, equation, index, 0)
                    elif(length - index >= 6 and equation[index:index + 6] in InverseTrig):
                        isInverse = 1
                        equation = substituteTrig(self, equation, index, 1)
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
            self.printResult(str(round(calculateEquation(self, equation), 6)))
            return
        
        if(len(self.textBox) == 2):
            self.textBox.pop(1)
            self.buttons.pop(10)        
        if(self.variable and '=' in equation and not('y' in equation or 'x' in equation)):
            solveForVar(self, equation, self.variable)
        elif(self.variable):
            self.textBox.append(self.textBox2)
            self.buttons.append(self.enterButton2)
        else:
            solveEquation(self, equation)


def calculateEquation(self, equation):
        equation = processEquation(self, equation)
        if(equation == None):
            return
        try:
            return eval(equation)
        except Exception as e:
            return f"Error: {type(e).__name__}"
        

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
                self.calculateGraph("x=" + equation)
            

def checkSolution(self, solution, left, right, indeces):
        index = 0
        while index < len(solution):
            subEquation = substituteVarInEq(left + "=" + right, indeces, solution[index])
            subLeft = subEquation[:subEquation.index("=")]
            subRight = subEquation[subEquation.index("=") + 1:]
            try:
                difference = eval(subLeft, {"math":math}) - eval(subRight, {"math":math})
            except:
                solution.pop(index)
                continue
            if(not((self.displayingGraph and difference < 1e-4) or difference == 0)):
                solution.pop(index)
            else:
                index += 1
        return solution


def substituteVarInEq(equation, indeces, value):
        for i in range(len(indeces) - 1, -1, -1):
            if(indeces[i] == len(equation) - 1):
                equation = equation[:indeces[i]] + f"({value})"
            else:
                equation = equation[:indeces[i]] + f"({value})" + equation[indeces[i] + 1:]
        return equation


def findVarIndeces(equation, var):
        indeces = []
        for i in range(len(equation)):
            if(equation[i] == var):
                indeces.append(i)
        return indeces
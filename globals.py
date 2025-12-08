from pygame import *

Black = (0, 0, 0)
White = (255, 255, 255)
Grey = (160, 160, 160)
DarkGrey = (100, 100, 100)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

Arial = "Arial"

Trig = ["sin", "cos", "tan"]
InverseTrig = ["arcsin", "arccos", "arctan"]

def fonts(fontType, size, bold, italic):
    font.init()
    thisFont = font.SysFont(fontType, int(size), bold = bold, italic = italic)
    return thisFont
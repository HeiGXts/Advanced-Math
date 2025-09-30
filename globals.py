from pygame import *

Black = (0, 0, 0)
White = (255, 255, 255)
Grey = (160, 160, 160)
DarkGrey = (100, 100, 100)

Arial = "Arial"
ComicSans = "Comic Sans"
Roboto = "Roboto"
Symbola = "Symbola"

def fonts(fontType, size, bold, italic):
    font.init()
    thisFont = font.SysFont(fontType, int(size), bold = bold, italic = italic)
    return thisFont
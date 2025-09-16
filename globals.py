from pygame import *

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
DarkRed = (200, 0, 0)
Green = (0, 255, 0)
DarkGreen = (0, 200, 0)
Blue = (0, 0, 255)
DarkBlue = (0, 0, 200)
Yellow = (255, 255, 0)
DarkYellow = (200, 200, 0)
Orange = (255, 128, 0)
Purple = (128, 0, 255)
Grey = (160, 160, 160)

def fonts(fontType, size, bold, italic):
    font.init()
    thisFont = font.SysFont(fontType, size, bold = bold, italic = italic)
    return thisFont
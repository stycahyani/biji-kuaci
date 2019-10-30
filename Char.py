import cv2
import numpy as np
import math

class cariChar:
    def __init__(self, ctrs):
        self.contour = ctrs
        self.Rect = cv2.boundingRect(self.contour)

        [x, y, w, h] = self.Rect
        self.sumbuX = x
        self.sumbuY = y
        self.Width = w
        self.Height = h

        self.Area = self.Width * self.Height
        self.CenterX = ((2 * self.sumbuX) + self.Width) / 2
        self.CenterY = ((2 * self.sumbuY) + self.Height) / 2
        self.Diagonal = math.sqrt((self.Width ** 2) + (self.Height ** 2))
        self.Ratio = float(self.Width) / float(self.Height)

def cekChar(mungkinChar):
    if (mungkinChar.Area > 80 and mungkinChar.Width > 2 and 
        mungkinChar.Height > 8 and 0.1 < mungkinChar.Ratio < 1.0):
        return True
    else:
        return False
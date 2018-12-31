from tkinter import *
from shot import Shot
import math


class Tower:
    def __init__(self, canvas, row, col, cellDim):
        self._canv = canvas
        self._row = row
        self._col = col
        self._cellDim = cellDim
        self._location = self.calculateLocation(self._row, self._col, self._cellDim)
        self._center = self.calculateCenter(self._location)
        self._shots = []
        self._fireRate = 1000
        self._accuracy = .3


    def render(self):
        print("Tower: self.getCenter = ", str(self.getCenter()[0]) + ", " + str(self.getCenter()[1]))
        self._towerImage = PhotoImage(file='img\calvinPresident.png')
        self._towerImage = self._towerImage.subsample(5, 7)
        self._id = self._canv.create_image(self._center[0], self._center[1], image=self._towerImage, anchor=CENTER)


    def getCenter(self):
        return self._center

    def calculateLocation(self, row, col, cellDim):
        startx = col * cellDim
        starty = row * cellDim
        endx = startx + cellDim
        endy = starty + cellDim
        return [startx, starty, endx, endy]

    def calculateCenter(self, location):
        x = (location[2] - location[0]) / 2.0 + location[0]
        y = (location[3] - location[1]) / 2.0 + location[1]
        return x, y

    def fireShot(self, invadersList):
        targetInvader = self.chooseTarget(invadersList)
        if not targetInvader == None:
            shot = Shot(self._canv, self.getCenter(), targetInvader.getCenter(), targetInvader, self._accuracy)
            self._shots.append(shot)
            self._canv.after(self._fireRate, self.fireShot, invadersList)
        else:
            self._canv.after(300, self.fireShot, invadersList)

    def chooseTarget(self, invadersList):
        if not invadersList == []:
            for invader in invadersList:
                if self.findDistance(self, invader) < 200 and invader.getHealth() > 0:
                    return invader

    def findDistance(self, obj0, obj1):
        differences = obj0.getCenter()[0] - obj1.getCenter()[0], obj0.getCenter()[1] - obj1.getCenter()[1]
        distance = math.sqrt(differences[0] ** 2 + differences[1] ** 2)
        return distance

    def setFireRate(self, fireRate):
        #fireRate is time in milliseconds between shots fired
        self._fireRate = fireRate

    def setAccuracy(self, accuracy):
        self._accuracy = accuracy




























#
#
# class BasicTower(Tower):
#     def __init__(self, canvas, row, col, cellDim):
#         super(BasicTower, self).__init__(canvas, row, col, cellDim)
#
#     def fireShot(self, invadersList):
#         targetInvader = self.chooseTarget(invadersList)
#         if not targetInvader == None:
#             shot = Shot(self._canv, self.getCenter(), targetInvader.getCenter(), targetInvader)
#             self._shots.append(shot)
#             self._canv.after(1000, self.fireShot, invadersList)
#         else:
#             self._canv.after(300, self.fireShot, invadersList)
#
#     def chooseTarget(self, invadersList):
#         if not invadersList == []:
#             for invader in invadersList:
#                 if self.findDistance(self, invader) < 200 and invader.getHealth() > 0:
#                     return invader
#
# class AverageTower(Tower):
#     def __init__(self, canvas, row, col, cellDim):
#         super(AverageTower, self).__init__(canvas, row, col, cellDim)
#
#     def fireShot(self, invadersList):
#         targetInvader = self.chooseTarget(invadersList)
#         if not targetInvader == None:
#             shot = Shot(self._canv, self.getCenter(), targetInvader.getCenter(), targetInvader)
#             self._shots.append(shot)
#             self._canv.after(700, self.fireShot, invadersList)
#         else:
#             self._canv.after(300, self.fireShot, invadersList)
#
#     def chooseTarget(self, invadersList):
#         if not invadersList == []:
#             for invader in invadersList:
#                 if self.findDistance(self, invader) < 300 and invader.getHealth() > 0:
#                     return invader
#
# class StrongTower(Tower):
#     def __init__(self, canvas, row, col, cellDim):
#         super(StrongTower, self).__init__(canvas, row, col, cellDim)
#
#     def fireShot(self, invadersList):
#         targetInvader = self.chooseTarget(invadersList)
#         if not targetInvader == None:
#             shot = Shot(self._canv, self.getCenter(), targetInvader.getCenter(), targetInvader)
#             self._shots.append(shot)
#             self._canv.after(500, self.fireShot, invadersList)
#         else:
#             self._canv.after(300, self.fireShot, invadersList)
#
#     def chooseTarget(self, invadersList):
#         if not invadersList == []:
#             for invader in invadersList:
#                 if self.findDistance(self, invader) < 500 and invader.getHealth() > 0:
#                     return invader

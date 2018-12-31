from invader import *


class Wave:
    def __init__(self, canvas, path, waveNumber, app):
        self._invadersThisRound = waveNumber
        self._app = app
        self._invaderList = []
        self._canv = canvas
        self._path = path
        self._timeBetweenInvaders = 1000
        self._nextInvader = 0

        for invader in range(self._invadersThisRound):
            self._invaderList.append(Invader(self._canv, self._path, self._app))

    def startWave(self):
        self._nextInvader = 0
        self.moveNextInvader()

    def moveNextInvader(self):
        if self._nextInvader < self._invadersThisRound:
            self._invaderList[self._nextInvader].startMoving()
            self._nextInvader += 1
            self._canv.after(self._timeBetweenInvaders, self.moveNextInvader)

    def getInvaderList(self):
        return self._invaderList
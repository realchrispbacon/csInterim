class Mediator:
    def __init__(self):
        self._towers = []
        self._invaders = []
        self._shots = []

    def newTower(self, tower):
        self._invaders.append(tower)
        tower.fireShot()

    def newInvader(self, invader):
        self._invaders.append(invader)

    def newShot(self, shot):
        self._shots.append(shot)

    def detectCollisions(self):
        pass

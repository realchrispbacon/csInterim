import math
import random

SPEED = 10
class Shot:
    # origin and target take tuples for the center of each object
    def __init__(self, canvas, origin, target, invader, accuracy):
        self._canv = canvas
        self._x = origin[0]
        self._y = origin[1]
        self._targetx = target[0]
        self._targety = target[1]
        self._invader = invader
        self._size = 2  # radius of circle to draw (for now)
        self._accuracy = accuracy

        self._angle = self.calculateAngle()
        self._dx = -SPEED * math.cos(self._angle)
        self._dy = -SPEED * math.sin(self._angle)
        self._collided = False

        # identifier for the circle we draw to represent the shot
        self._id = None

        self.render()

    def calculateAngle(self):
        randomness = random.uniform(-self._accuracy, self._accuracy)
        x = self._x - self._targetx
        y = self._y - self._targety
        angle = math.atan2(y, x) + randomness
        return angle

    def move(self):
        self._x += self._dx
        self._y += self._dy

    def isOffScreen(self):
        if (self._x < 0 or self._y < 0 or
                self._x > int(self._canv.cget("width")) or
                self._y > int(self._canv.cget('height'))):
            return True
        return False

    def render(self):
        self._canv.delete(self._id)
        if not self.isOffScreen() and not self.isCollision(self._invader, self):
            self.move()
            self._id = self._canv.create_oval(self._x - self._size, self._y - self._size,
                                          self._x + self._size, self._y + self._size, fill="black")
            self._canv.after(60, self.render)

    def getCenter(self):
        return self._x, self._y

    def isCollision(self, invader, shot):
        # print("invader: " + str(invader.getCenter()[0]) + ", " + str(invader.getCenter()[1]) +
        #       " shot: " + str(shot.getCenter()[0]) + ", " + str(shot.getCenter()[1]))

        if self.findDistance(invader, shot) < 10:
            invader.decreaseHealth()
            return True
        return False

    def findDistance(self, obj0, obj1):
        differences = obj0.getCenter()[0] - obj1.getCenter()[0], obj0.getCenter()[1] - obj1.getCenter()[1]
        distance = math.sqrt(differences[0] ** 2 + differences[1] ** 2)
        return distance

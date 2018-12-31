from tkinter import *

class Invader:
    def __init__(self, canvas, path, app):
        self._canv = canvas
        self._path = path
        self._app = app

        self._size = 4   # radius of circle to draw (for now)

        self._next_cell_idx = 0
        self._next_cell = self._path.get_cell(0)
        self._x, self._y = self._next_cell.get_center()
        self._pathLength = len(self._path)
        self._isMoving = False

        #print("Invader: self._x, y = ", self._x, self._y)

        self._compute_new_dir()

        # identifier for the circle we draw to represent the invader
        self._id = None

        self._health = 100

        self._invaderImage = PhotoImage(file='img\invaderImage.png')
        self._invaderImage = self._invaderImage.subsample(15, 15)

    def decreaseHealth(self):
        self._health -= 50

    def isAlive(self):
        if self._health > 0:
            return True
        else:
            self._app._gold += 2
            self._app._goldAmtVar.set(self._app._gold)
            return False

    def getHealth(self):
        return self._health


    def _compute_new_dir(self):
        '''Get (and remember) the next cell in that path, and then
        compute the xdir and ydir to get us from our current position
        to the center of that next cell.'''
        self._next_cell_idx += 1
        self._next_cell = self._path.get_cell(self._next_cell_idx)
        d = self._next_cell.get_center_x() - self._x
        if d > 0:
            self._xdir = 1
        elif d == 0:
            self._xdir = 0
        else:
            self._xdir = -1
        d = self._next_cell.get_center_y() - self._y
        if d > 0:
            self._ydir = 1
        elif d == 0:
            self._ydir = 0
        else:
            self._ydir = -1

    def move(self):
        # move on to the next cell
        if self._next_cell_idx == self._pathLength - 1:
            self._canv.delete(self._id)
        elif (self._x, self._y) == self._next_cell.get_center():
            self._compute_new_dir()
        self._x += self._xdir
        self._y += self._ydir

    def startMoving(self):
        self._isMoving = True
        self.render()

    def render(self):
        self._canv.delete(self._id)
        if not self.isOffScreen() and self.isAlive():
            self.move()
            # self._id = self._canv.create_oval(self._x - self._size, self._y - self._size,
            #                               self._x + self._size, self._y + self._size,
            #                               fill="black")
            self._id = self._canv.create_image(self._x, self._y, image=self._invaderImage, anchor=CENTER)
            self._canv.after(30, self.render)
        elif self._isMoving == False:
            self._app._gameRunning = False

    def isOffScreen(self):
        if (self._x < 0 or self._y < 0 or
                self._x > int(self._canv.cget("width")) or
                self._y > int(self._canv.cget('height'))):
            self._isMoving = False
            return True
        return False

    def getCenter(self):
        return self._x, self._y
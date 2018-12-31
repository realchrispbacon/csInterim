import math
from path import *
from tower import *
from wave import Wave
from interface import implements
from cellObserver import CellObserver


CANVAS_DIM = 1000
SQUARE_SIZE = 50
NUM_CELLS_PER_DIM = int(CANVAS_DIM / SQUARE_SIZE)

TIME_BETWEEN_WAVES = 10    # seconds
INIT_GOLD_AMOUNT = 100
TOWER1_PRICE = 20
TOWER2_PRICE = 40
TOWER3_PRICE = 60


class App(implements(CellObserver)):
    def __init__(self, root):

        self._root = root
        self._gameRunning = False
        self._currWaveNumber = 1
        self._currWave = None

        self.setUpBoard(root)

        self.setUpGrid()

        self.readPathInfo()

        self._gold = INIT_GOLD_AMOUNT

        self._invadersList = []


    def setUpBoard(self, root):
        self._bottom_panel = Frame(root)
        self._bottom_panel.pack()
        self._canv = Canvas(root, width=CANVAS_DIM, height=CANVAS_DIM)
        self._canv.pack()


        self._btStartGame = Button(self._bottom_panel, text="Start Game",
                                   command=self.startGame)
        self._btStartGame.pack(side=LEFT)

        Label(self._bottom_panel, text="Bonus Bucks: ").pack(side=LEFT)
        self._goldAmtVar = IntVar()
        self._goldAmtVar.set(INIT_GOLD_AMOUNT)
        self._goldLbl = Label(self._bottom_panel, textvariable=self._goldAmtVar)
        self._goldLbl.pack(side=LEFT)

        self._btNextWave = Button(self._bottom_panel, text="Start Wave",
                                  command=self.startNextWave, state=DISABLED)
        self._btNextWave.pack(side=LEFT)

        Label(self._bottom_panel, text="Time till next wave starts: ").pack(side=LEFT)
        self._timeLeftTilWave = IntVar()
        self._timeLeftTilWave.set(TIME_BETWEEN_WAVES)
        self._timeLeftLbl = Label(self._bottom_panel, textvariable=self._timeLeftTilWave)
        self._timeLeftLbl.pack(side=LEFT)

    def setUpGrid(self):
        # A 2-d grid of locations
        self._grid = []
        for row in range(NUM_CELLS_PER_DIM):
            rowlist = []
            for col in range(NUM_CELLS_PER_DIM):
                cell = Cell(self._canv, col, row, SQUARE_SIZE)
                cell.registerObserver(self)
                rowlist.append(cell)
            self._grid.append(rowlist)


    def startGame(self):
        self._btNextWave.config(state=NORMAL)
        self._btStartGame.config(state=DISABLED)
        self._gameRunning = True
        # Start the timer, which forces the next wave to start in a few seconds.
        self.updateTimer()

    def startNextWave(self):
        '''Start the next wave now, instead of waiting for the timer to go down to 0.'''
        if not self._gameRunning:
            self._canv.create_text(400, 575, text="Game Over!!!")
            return
        print("Start next wave now...")

        wave = Wave(self._canv, self._path, self._currWaveNumber, self)
        wave.startWave()

        for invader in wave.getInvaderList():
            self._invadersList.append(invader)

        self._currWaveNumber += 1
        self._timeLeftTilWave.set(TIME_BETWEEN_WAVES)

    def updateTimer(self):
        timeLeft = self._timeLeftTilWave.get()
        timeLeft -= 1
        self._timeLeftTilWave.set(timeLeft)
        if timeLeft == 0:
            self._timeLeftLbl = TIME_BETWEEN_WAVES
            self.startNextWave()
        self._canv.after(1000, self.updateTimer)

    def readPathInfo(self):
        '''Read path information from a file and create a path object for it.'''
        self._path = Path(NUM_CELLS_PER_DIM)
        with open('path.txt') as pf:
            for elem in pf:
                elem = elem.strip()
                x, y = map(int, elem.split(','))   # map(int) to make ints.
                self._path.add_cell(self._grid[y][x])
                self._grid[y][x].set_type('path')

    def getRowCol(self, location):
        row = int((location[1] / SQUARE_SIZE))
        col = int((location[0] / SQUARE_SIZE))
        return (row, col)

    def update(self, cell):
        tower = Tower(self._canv, cell.get_y(), cell.get_x(), SQUARE_SIZE)

        if cell.get_type() == "other" and self._gold >= TOWER1_PRICE:
            self._gold -= TOWER1_PRICE
            self._goldAmtVar.set(self._gold)
            cell.set_type('tower1')
            tower.render()
            tower.fireShot(self._invadersList)

        elif cell.get_type() == "tower1" and self._gold >= TOWER2_PRICE:
            self._gold -= TOWER2_PRICE
            self._goldAmtVar.set(self._gold)
            cell.set_type('tower2')
            tower.setAccuracy(.01)
            tower.setFireRate(700)
            tower.fireShot(self._invadersList)

        elif cell.get_type() == "tower2" and self._gold >= TOWER3_PRICE:
            self._gold -= TOWER3_PRICE
            self._goldAmtVar.set(self._gold)
            cell.set_type('tower3')
            tower.setAccuracy(.001)
            tower.setFireRate(500)
            tower.fireShot(self._invadersList)

    def findDistance(self, obj0, obj1):
        differences = obj0.getCenter()[0] - obj1.getCenter()[0], obj0.getCenter()[1] - obj1.getCenter()[1]
        distance = math.sqrt(differences[0] ** 2 + differences[1] ** 2)
        return distance


root = Tk()
root.title("Calvin Tower Defense")
App(root)
root.resizable(width=False, height=False)
root.wm_attributes('-topmost', 1)
root.mainloop()

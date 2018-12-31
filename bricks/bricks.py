''' GUI for Bricks game
Created fall 2016
final project for CS108
@author Christopher Punt (cap32)'''

from random import randint
from tkinter import *


class Gui:
    '''creates gui for bricks game'''

    def __init__(self, window):
        self._canvas_height = 500
        self._canvas_width = 980
        self._ball_diameter = 14
        self._speed = 1

        self.canvas = Canvas(window, height=self._canvas_height, width=self._canvas_width)
        self.window = window

        # create score and lives labels
        self._lives = 2
        self._livesvar = IntVar()
        self._livesvar.set(self._lives)
        Label(window, text='Lives:', width=10).grid(column=1, row=0, sticky=E)
        Label(window, textvariable=self._livesvar, width=1).grid(column=1, row=0, sticky=E)

        self._score = 0
        self._scorevar = IntVar()
        self._scorevar.set(self._score)
        Label(window, text='Score:', width=10).grid(column=1, row=1, sticky=E)
        Label(window, textvariable=self._scorevar, width=2).grid(column=1, row=1, sticky=E)

        # Make a button that will restart the game
        Button(window, text='Restart Game', command=self.restart_game).grid(column=1, row=3, sticky=E)

        # add the game to the gui
        self.canvas.grid(row=2, columnspan=2)

        # add a surrounding rectangle that acts as a wall to bounce from
        self.canvas.create_rectangle(2, 2, 980, 500)

        # create ball and characteristics
        self.ballx = 440
        self.bally = 460
        self.ballDx = self._speed
        self.ballDy = -self._speed
        self.canvas.create_oval(self.ballx, self.bally, self.ballx + self._ball_diameter,
                                self.bally + self._ball_diameter, fill="black", tags='ball')

        # draw bricks
        self.draw_bricks()

        # draw paddle
        self.canvas.create_rectangle(380, 485, 400, 495, fill='black', tags='leftpaddle')
        self.canvas.create_rectangle(400, 485, 500, 495, fill='black', tags='middlepaddle')
        self.canvas.create_rectangle(500, 485, 520, 495, fill='black', tags='rightpaddle')
        self.window.bind('<Motion>', self.move_paddle)

        self.canvas.create_text(450, 300, text='Press the space bar to start game!', tags='start_text')

        # move the ball on the screen
        self.window.bind('<space>', self.move_ball)

    def restart_game(self):
        '''restarts the game'''
        self.canvas.delete('start_text')

        # update lives label and decrease by 1
        self._lives = 2
        self._livesvar.set(self._lives)

        # reset score label
        self._score = 0
        self._scorevar.set(self._score)

        # redraw the bricks
        self.draw_bricks()

        # reset the ball
        self.ballDx = self._speed
        self.ballDy = -self._speed
        self.canvas.delete('ball')
        self.canvas.create_oval(self.ballx, self.bally, self.ballx + self._ball_diameter,
                                self.bally + self._ball_diameter, fill="black", tags='ball')

        # put the start game text back on the screen
        self.canvas.create_text(450, 300, text='Press the space bar to start game!', tags='start_text')

    def get_random_color(self):
        '''
        Taken from lab12 helpers file to assign random colors to the bricks
        Generate random color intensities for red, green & blue and convert them to hex. '''
        return '#{:02X}{:02X}{:02X}'.format(randint(0, 255), randint(0, 255), randint(0, 255))

    def draw_bricks(self):
        '''draws all the bricks on the screen'''

        self.bricks = []
        brick_coords = [5, 5, 65, 25]
        for i in range(64):
            brick = self.canvas.create_rectangle(brick_coords, outline='white', fill=self.get_random_color(),
                                                 tags='brick' + str(i))
            self.bricks.append(brick)
            brick_coords[0] += 60
            brick_coords[2] += 60
            if brick_coords[2] > 980:
                brick_coords[0] = 5
                brick_coords[2] = 65
                brick_coords[1] += 20
                brick_coords[3] += 20

    def move_paddle(self, event):
        '''Moves 3 paddles across the bottom of the screen'''
        leftcoords = self.canvas.coords('leftpaddle')
        middlecoords = self.canvas.coords('middlepaddle')
        rightcoords = self.canvas.coords('rightpaddle')

        middlewidth = middlecoords[2] - middlecoords[0]
        middlecoords[0] = event.x - middlewidth / 2
        middlecoords[2] = event.x + middlewidth / 2
        self.canvas.coords('middlepaddle', middlecoords[0], middlecoords[1], middlecoords[2], middlecoords[3])

        leftwidth = leftcoords[2] - leftcoords[0]
        leftcoords[0] = event.x - leftwidth / 2
        leftcoords[2] = event.x + leftwidth / 2
        self.canvas.coords('leftpaddle', leftcoords[0] - 25, leftcoords[1], leftcoords[2] - 25, leftcoords[3])

        rightwidth = rightcoords[2] - rightcoords[0]
        rightcoords[0] = event.x - rightwidth / 2
        rightcoords[2] = event.x + rightwidth / 2
        self.canvas.coords('rightpaddle', rightcoords[0] + 25, rightcoords[1], rightcoords[2] + 25, rightcoords[3])

    def move_ball(self, Event=None):
        '''moves the ball around the canvas bouncing off objects'''

        self.canvas.delete('start_text')

        self.canvas.move('ball', self.ballDx, self.ballDy)

        ball_position = self.canvas.coords('ball')

        leftpaddle_position = self.canvas.coords('leftpaddle')
        middlepaddle_position = self.canvas.coords('middlepaddle')
        rightpaddle_position = self.canvas.coords('rightpaddle')

        # bounces off the walls
        self.bounceoffwalls(ball_position)

        # bounces off the left side of the paddle
        if self.collides(ball_position, leftpaddle_position):
            if self.ballDx > 0 and self.ballDy > 0:
                self.ballDx = -self.ballDx * .95
                self.ballDy = self.ballDy * -1.05
            else:
                self.ballDy = self.ballDy * -.95
                self.ballDx = self.ballDx * 1.05

        # bounces off the right side of the paddle
        elif self.collides(ball_position, rightpaddle_position):
            if self.ballDx < 0 and self.ballDy > 0:
                self.ballDx = -self.ballDx * .95
                self.ballDy = self.ballDy * -1.05
            else:
                self.ballDy = self.ballDy * -.95
                self.ballDx = self.ballDx * 1.05

        # bounces off the middle of the paddle
        elif self.collides(ball_position, middlepaddle_position):
            self.ballDy = -self.ballDy

        # what happens when the ball hits a brick
        if self.hit_brick(ball_position):
            self.ballDy = -self.ballDy
            self._score += 1
            self._scorevar.set(self._score)

        # checks to see if all bricks are hit
        bricks_left = True
        for i in range(64):
            if self.canvas.coords(self.bricks[i])[1] < 500:
                bricks_left = True
                break
            else:
                bricks_left = False

        if not bricks_left:
            # moves bricks all back in place
            for i in range(64):
                self.canvas.move('brick' + str(i), 0, -500)

            # reset the ball
            self.ballDx = self._speed
            self.ballDy = -self._speed
            self.canvas.delete('ball')
            self.canvas.create_oval(self.ballx, self.bally, self.ballx + self._ball_diameter,
                                    self.bally + self._ball_diameter, fill="black", tags='ball')
            ball_position[3] = 600

        # what happens when the ball hits the bottom of the screen
        if ball_position[3] >= 500:
            if self._lives <= 0:
                self.canvas.create_text(450, 300, text='You lost the game your final score was: ' + str(self._score),
                                        tags='start_text')
            else:
                # update lives label and decrease by 1
                self._lives -= 1
                self._livesvar.set(self._lives)

                # reset the ball
                self.ballDx = self._speed
                self.ballDy = -self._speed
                self.canvas.delete('ball')
                self.canvas.create_oval(self.ballx, self.bally, self.ballx + self._ball_diameter,
                                        self.bally + self._ball_diameter, fill="black", tags='ball')

                # put the start game text back on the screen
                self.canvas.create_text(450, 300, text='Press the space bar to continue the game!', tags='start_text')
        else:
            self.canvas.after(2, self.move_ball)

    def bounceoffwalls(self, ball_position):
        '''bounces the ball off the walls'''

        if ball_position[0] <= 0:
            self.ballDx = -self.ballDx
        if ball_position[1] <= 0:
            self.ballDy = -self.ballDy
        if ball_position[2] >= self._canvas_width:
            self.ballDx = -self.ballDx

    def collides(self, pos1, pos2):
        '''determines if an objects hits another'''

        if pos1[2] >= pos2[0] and pos1[0] <= pos2[2] and pos1[1] <= pos2[3] and pos1[3] >= pos2[1]:
            return True

        else:
            return False

    def hit_brick(self, ball_position):
        '''determines if a brick is hit and if it is the brick is moved off the screen'''

        for i in range(64):
            if self.collides(ball_position, self.canvas.coords(self.bricks[i])):
                self.canvas.move('brick' + str(i), 0, self._canvas_height)
                return True

        return False


if __name__ == '__main__':
    root = Tk()
    root.title('Bricks')
    app = Gui(root)
    root.mainloop()
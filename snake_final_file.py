import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirx=1,diry=0,color=(255,0,0)):
        self.pos = start
        self.dirx = dirx
        self.diry = diry
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface, eyes=False):
        dist = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dist+1, j*dist+1, dist-2, dist-2))
        if eyes:
            center = dist // 2
            radius = 3
            circleMiddle = (i*dist+center-radius,j*dist+8)
            circleMiddle2 = (i*dist + dist -radius*2, j*dist+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    def move(self):
        # TODO : Write code to handle if snake is moving in left direction 
        # then it can't start moving right directly and vice versa. Same for up and down also.
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    
                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    
                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])

                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.diry == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.diry == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.dirx, c.diry)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        self.body.append(cube((tail.pos[0] + dx * -1, tail.pos[1] + dy * -1)))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0 
    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redrawWindow(surface):
    global width, rows, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    pygame.init()
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Snake by @jeff007ali")
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))

    # Game over text
    # over_font = pygame.font.Font("freesansbold.ttf", 32)

    clock = pygame.time.Clock()
    running = True
    while running:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print("Score : {}".format(len(s.body)))
                message_box("You lost!", "Play again...")
                # over_text = over_font.render("GAME OVER", True, (0, 0, 255))
                # win.blit(over_text, (200, 250))
                s.reset((10, 10))
                break

        redrawWindow(win)


main()

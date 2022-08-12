import random
import pygame
import tkinter as tk
from tkinter import messagebox


class block(object):
    row = 20
    w = 500

    def __init__(self, start, dirX=1, dirY=0, color=(255, 0, 0)):
        self.position = start
        self.dirX = 1
        self.dirY = 0
        self.color = color

    def move(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.position = (self.position[0] + self.dirX, self.position[1] + self.dirY)

    def draw(self, surface, eyes=False):
        dis = self.w // self.row
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i * dis + center - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake:
    body = []
    turns = {}

    def __init__(self, color, position):
        self.color = color
        self.head = block(position)
        self.body.append(self.head)
        self.dirX = 0
        self.dirY = 1

    def move(self):
        # webscrapping check it out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirX = -1
                    self.dirY = 0
                    self.turns[self.head.position[:]] = [self.dirX, self.dirY]

                elif keys[pygame.K_RIGHT]:
                    self.dirX = 1
                    self.dirY = 0
                    self.turns[self.head.position[:]] = [self.dirX, self.dirY]

                elif keys[pygame.K_UP]:
                    self.dirX = 0
                    self.dirY = -1
                    self.turns[self.head.position[:]] = [self.dirX, self.dirY]

                elif keys[pygame.K_DOWN]:
                    self.dirX = 0
                    self.dirY = 1
                    self.turns[self.head.position[:]] = [self.dirX, self.dirY]

        for i, c in enumerate(self.body):
            p = c.position[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirX == -1 and c.position[0] <= 0:
                    c.position = (c.row - 1, c.position[1])
                elif c.dirX == 1 and c.position[0] >= c.row - 1:
                    c.position = (0, c.position[1])
                elif c.dirY == 1 and c.position[1] >= c.row - 1:
                    c.position = (c.position[0], 0)
                elif c.dirY == -1 and c.position[1] <= 0:
                    c.position = (c.position[0], c.row - 1)
                else:
                    c.move(c.dirX, c.dirY)

    def reset(self,position):
        self.head = block(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirX = 0
        self.dirY = 1



    def grow(self):
        tail = self.body[-1]
        dx, dy = tail.dirX, tail.dirY

        if dx == 1 and dy == 0:
            self.body.append(block((tail.position[0]-1, tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(block((tail.position[0]+1, tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(block((tail.position[0], tail.position[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(block((tail.position[0], tail.position[1]+1)))

        self.body[-1].dirX = dx
        self.body[-1].dirY = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, h, row, surface):
    sizeB = w // row

    x = 0
    y = 0
    for l in range(row):
        x = x + sizeB
        y = y + sizeB

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (h, y))


def redrawWindow(surface):
    global row, width, height, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, height, row, surface)
    pygame.display.update()


def randomSnack(row, item):
    positions = item.body

    while True:
        x = random.randrange(row)
        y = random.randrange(row)
        if len(list(filter(lambda z: z.position == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, height, row, s, snack
    width = 500
    height = 500
    row = 20
    window = pygame.display.set_mode((width, height))
    s = snake((255, 0, 0), (random.randint(0, 19), random.randint(0, 19)))
    snack = block(randomSnack(row, s), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)  # 60 frames per sec
        s.move()
        if s.body[0].position == snack.position:
            s.grow()
            snack = block(randomSnack(row, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].position in list(map(lambda z:z.position,s.body[x+1:])):
                print("Score: ", + len(s.body))
                message_box("Too bad, better luck next time!", "Wanna go again?")
                s.reset((10,10))
                break

        redrawWindow(window)
    pass


main()

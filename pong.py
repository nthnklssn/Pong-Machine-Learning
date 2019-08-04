import pygame
WINDOWXSIZE = 800
WINDOWYSIZE = 500

class player(object):
    def __init__(self, xpos, ypos, upKey, downKey, colour):
        self.xpos = xpos
        self.ypos = ypos

        self.paddleWidth = 20
        self.paddleHeight = 55
        self.velocity = 5

        self.colour = colour

        self.upKey = upKey
        self.downKey = downKey

    def movePlayer(self, pressedKeys):
        if pressedKeys[self.upKey]:
            if self.ypos - self.velocity <= 0:
                self.ypos = 0
            else:
                self.ypos -= self.velocity
        elif pressedKeys[self.downKey]:
            if self.ypos + self.velocity + self.paddleHeight >= WINDOWYSIZE:
                self.ypos = WINDOWYSIZE - self.paddleHeight
            else:
                self.ypos += self.velocity

    def drawPlayer(self, window):
        pygame.draw.rect(window, self.colour, (self.xpos, self.ypos, self.paddleWidth, self.paddleHeight))

class ball(object):
    def __init__(self, xVel, yVel):
        self.xpos = WINDOWXSIZE / 2
        self.ypos = WINDOWYSIZE / 2
        self.xVel = xVel
        self.yVel = yVel
        self.width = 20
        self.height = 20
        self.colour = (255, 255, 255)

    def moveBall(self, player1, player2):
        self.p1Detect(player1)
        self.p2Detect(player2)
        if self.ypos + self.yVel + self.height >= WINDOWYSIZE or self.ypos + self.yVel <= 0:
            self.yVel = self.yVel * -1
        else:
            self.ypos += self.yVel
        if self.xpos + self.xVel + self.height > WINDOWXSIZE or self.xpos + self.xVel < 0:
            self.xpos = WINDOWXSIZE / 2
        else:
            self.xpos += self.xVel


    def p1Detect(self, player):
        if self.xpos + self.width >= WINDOWXSIZE - player.paddleWidth and self.ypos >= player.ypos and self.ypos <= player.ypos + player.paddleHeight:
            self.xPos = player.xpos - player.paddleHeight - 1
            self.xVel = self.xVel * -1
    def p2Detect(self, player):
        if self.xpos <= player.paddleWidth and self.ypos >= player.ypos and self.ypos <= player.ypos + player.paddleHeight:
            self.xVel = self.xVel * -1
            self.xPos = player.xpos + 1

    def drawBall(self, window):
        pygame.draw.rect(window, self.colour, (self.xpos, self.ypos, self.width, self.height))

def main():


    pygame.init()

    win = pygame.display.set_mode((WINDOWXSIZE,WINDOWYSIZE))

    pygame.display.set_caption("Pong")
    player1 = player(WINDOWXSIZE - 20, WINDOWYSIZE/2, pygame.K_UP, pygame.K_DOWN, (255,100,100))
    player2 = player(0, WINDOWYSIZE/2, pygame.K_w, pygame.K_s, (100,255,255))
    ball1 = ball(-4,4)

    run = True

    while run:
        pygame.time.delay(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.fill((0,0,0))
        player1.drawPlayer(win)
        player2.drawPlayer(win)
        ball1.drawBall(win)

        keys = pygame.key.get_pressed()
        player1.movePlayer(keys)
        player2.movePlayer(keys)
        ball1.moveBall(player1, player2)
        if keys[pygame.K_q]:
            run = False
        pygame.display.update()
    pygame.quit()



if __name__ == "__main__":
    main()

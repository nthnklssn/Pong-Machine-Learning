import pygame
from multiprocessing.connection import Client
WINDOWXSIZE = 800
WINDOWYSIZE = 500
THRESHSCORE = 500


class bot(object):
    def __init__(self, xpos, ypos, colour, playerName, client):
        self.xpos = xpos
        self.ypos = ypos
        self.playerName = playerName

        self.client = client

        self.paddleWidth = 20
        self.paddleHeight = 55
        self.velocity = 5

        self.colour = colour

    def movePlayer(self, command):
        if (command == "ok"):
            return
        if (command == "up"):
            if self.ypos - self.velocity <= 0:
                self.ypos = 0
            else:
                self.ypos -= self.velocity
        elif (command == "down"):
            if self.ypos + self.velocity + self.paddleHeight >= WINDOWYSIZE:
                self.ypos = WINDOWYSIZE - self.paddleHeight
            else:
                self.ypos += self.velocity

    def drawPlayer(self, window):
        self.client.send("Name:{} xPos:{} yPos:{} width:{} height:{}".format(self.playerName, self.xpos, self.ypos, self.paddleWidth, self.paddleHeight))
        self.client.recv()
        pygame.draw.rect(window, self.colour, (self.xpos, self.ypos, self.paddleWidth, self.paddleHeight))

class player(object):
    def __init__(self, xpos, ypos, upKey, downKey, colour, playerName, client):
        self.xpos = xpos
        self.ypos = ypos
        self.playerName = playerName

        self.client = client

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
        self.client.send("Name:{} xPos:{} yPos:{} width:{} height:{}".format(self.playerName, self.xpos, self.ypos, self.paddleWidth, self.paddleHeight))
        self.client.recv()
        pygame.draw.rect(window, self.colour, (self.xpos, self.ypos, self.paddleWidth, self.paddleHeight))

class ball(object):
    def __init__(self, xVel, win, client):
        self.xpos = WINDOWXSIZE / 2
        self.ypos = WINDOWYSIZE / 2
        self.xVel = xVel
        self.startXVel = xVel
        self.yVel = 0
        self.width = 20
        self.height = 20
        self.colour = (255, 255, 255)
        self.p1Score = 0
        self.p2Score = 0
        self.window = win
        self.client = client

    def moveBall(self, player1, player2):
        self.p1Detect(player1)
        self.p2Detect(player2)
        if self.ypos + self.yVel + self.height >= WINDOWYSIZE or self.ypos + self.yVel <= 0:
            self.yVel = self.yVel * -.95
        else:
            self.ypos += self.yVel
        if self.xpos + self.xVel + self.height > WINDOWXSIZE:
            self.client.send("P2 Scored")
            self.scoreEvent("p2")

        if self.xpos + self.xVel < 0:
            self.client.send("P1 Scored")
            self.scoreEvent("p1")
        else:
            self.xpos += self.xVel

    def scoreEvent(self, player):
        if player == "p1":
            self.p1Score += 1
            self.xVel = self.startXVel
        else:
            self.p2Score += 1
            self.xVel = self.startXVel * -1
        for _ in range(8):
            # This loop alternates the colour of the ball for style
            pygame.draw.rect(self.window, (255,100,50), (self.xpos, self.ypos, self.width, self.height))
            pygame.display.update()
            pygame.time.delay(90)
            pygame.draw.rect(self.window, (255,255,255), (self.xpos, self.ypos, self.width, self.height))
            pygame.display.update()
            pygame.time.delay(90)
        pygame.time.delay(700)
        # Resets the ball position
        self.yVel = 0
        self.xpos = WINDOWXSIZE / 2
        self.ypos = WINDOWYSIZE / 2

    def p1Detect(self, player):
        '''
        This function detects whether the ball has collided with P1.
        '''
        if self.xpos + self.width >= WINDOWXSIZE - player.paddleWidth and (self.ypos + self.height >= player.ypos and self.ypos <= player.ypos + player.paddleHeight):
            if self.ypos + self.height/2 < player.ypos + player.paddleWidth/5:
                if abs(self.yVel) <= 2.5:
                    self.yVel -= 1.3
                else:
                    self.yVel *= 1.5
            elif self.ypos + self.height/2 < player.ypos + player.paddleWidth/3:
                if abs(self.yVel) <= 2.5:
                    self.yVel -= 0.7
                else:
                    self.yVel *= 1.1
            elif self.ypos + self.height/2 < player.ypos + 2 * player.paddleWidth/3:
                self.yVel = self.yVel * 0.4
            elif self.ypos + self.height/2 < player.ypos + 4 * player.paddleWidth/5:
                if abs(self.yVel) <= 2.5:
                    self.yVel += 0.7
                else:
                    self.yVel *= 1.1
            else:
                if abs(self.yVel) <= 2.5:
                    self.yVel += 1.3
                else:
                    self.yVel *= 1.5
            if abs(self.yVel) > 9:
                self.yVel = 9
            elif abs(self.xVel) <= 9:
                self.xVel = self.xVel * -1.04
            else:
                self.xVel = self.xVel * - 1.01
            self.xpos = player.xpos - self.width - 1

    def p2Detect(self, player):
        '''
        This function detects whether the ball has collided with P2.
        '''
        if self.xpos <= player.paddleWidth and self.ypos + self.height >= player.ypos and self.ypos <= player.ypos + player.paddleHeight:
            if self.ypos + self.height/2 < player.ypos + player.paddleWidth/5:
                if abs(self.yVel) <= 2.5:
                    self.yVel -= 1.3
                else:
                    self.yVel *= 1.5
            elif self.ypos + self.height/2 < player.ypos + player.paddleWidth/3:
                if abs(self.yVel) <= 2.5:
                    self.yVel -= 0.7
                else:
                    self.yVel *= 1.1
            elif self.ypos + self.height/2 < player.ypos + 2 * player.paddleWidth/3:
                self.yVel = self.yVel * 0.4
            elif self.ypos + self.height/2 < player.ypos + 4 * player.paddleWidth/5:
                if abs(self.yVel) <= 2.5:
                    self.yVel += 0.7
                else:
                    self.yVel *= 1.1
            else:
                if abs(self.yVel) <= 2.5:
                    self.yVel += 1.3
                else:
                    self.yVel *= 1.5
            if abs(self.yVel) > 9:
                self.yVel = 9
            if abs(self.xVel) <= 9:
                self.xVel = self.xVel * -1.04
            else:
                self.xVel = self.xVel * -1.01
            self.xpos = player.paddleWidth + 1
        if self.xVel <= -9:
            self.xVel = -9

    def drawBall(self, window):
        '''
        This function draws the ball and outputs the position to the command line if machineOutput is enabled.
        '''
        self.client.send("Ball: xPos:{} yPos:{} width:{} height:{}".format(self.xpos, self.ypos, self.width, self.height))
        response = self.client.recv()
        pygame.draw.rect(window, self.colour, (self.xpos, self.ypos, self.width, self.height))
        return response

def main():

    c = Client(('localhost', 5000))
    pygame.init()

    win = pygame.display.set_mode((WINDOWXSIZE,WINDOWYSIZE))

    pygame.display.set_caption("Pong")
    colour1 = (255,100,100)
    colour2 = (100,255,255)
    player1 = bot(WINDOWXSIZE - 20, WINDOWYSIZE/2, colour1, "Player1", c)
    player2 = player(0, WINDOWYSIZE/2, pygame.K_w, pygame.K_s, colour2, "Player2", c)
    ball1 = ball(-4, win, c)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Player1: {} - Player2: {}'.format(0, 0), True, (255,155,255), (0,0,100))

    textRect = text.get_rect()
    textRect.center = (WINDOWXSIZE // 2, WINDOWYSIZE // 8)


    run = True

    while run:
        pygame.time.delay(13)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.fill((0,0,0))
        run = checkIfGameOver(ball1.p1Score, ball1.p2Score, win, c)
        text = font.render('Player1: {} - Player2: {}'.format(ball1.p1Score, ball1.p2Score), True, (255,155,255), (0,0,100))
        win.blit(text, textRect)
        player1.drawPlayer(win)
        player2.drawPlayer(win)
        response = ball1.drawBall(win)
        keys = pygame.key.get_pressed()
        player1.movePlayer(response)
        player2.movePlayer(keys)
        ball1.moveBall(player1, player2)
        if keys[pygame.K_q]:
            run = False
        pygame.display.update()
    pygame.quit()
    c.close()

def checkIfGameOver(player1Score, player2Score, win, client):
    if player1Score >= THRESHSCORE:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Player1 WINS!: {} - {}'.format(player1Score, player2Score), True, (255,155,255), (0,0,100))
        client.send("Player1 Wins")
        client.recv()
        textRect = text.get_rect()
        textRect.center = (WINDOWXSIZE // 2, WINDOWYSIZE // 8)
        win.blit(text, textRect)
        pygame.display.update()
        pygame.time.delay(5000)
        return False
    if player2Score >= THRESHSCORE:
        font = pygame.font.Font('freesansbold.ttf', 32)
        client.send("Player2 Wins")
        client.recv()
        text = font.render('Player2 WINS!: {} - {}'.format(player1Score, player2Score), True, (255,155,255), (0,0,100))
        textRect = text.get_rect()
        textRect.center = (WINDOWXSIZE // 2, WINDOWYSIZE // 8)
        win.blit(text, textRect)
        pygame.display.update()
        pygame.time.delay(5000)
        return False
    return True


if __name__ == "__main__":
    main()

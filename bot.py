import numpy as np
import pyscreenshot as ImageGrab
import cv2
import time
from multiprocessing.connection import Listener
import pyautogui

class Opponent(object):
    """docstring for Opponent."""
    def __init__(self, msgParsed):
        self.yPos = int(float(msgParsed[2].split(":")[1]))
        self.xPos = int(float(msgParsed[1].split(":")[1]))
        self.width = int(float(msgParsed[3].split(":")[1]))
        self.height = int(float(msgParsed[4].split(":")[1]))

    def update(self, msgParsed):
        self.yPos = int(float(msgParsed[2].split(":")[1]))
        self.xPos = int(float(msgParsed[1].split(":")[1]))
        self.width = int(float(msgParsed[3].split(":")[1]))
        self.height = int(float(msgParsed[4].split(":")[1]))

class Player(object):
    """docstring for Player."""
    def __init__(self, msgParsed):
        self.yPos = int(float(msgParsed[2].split(":")[1]))
        self.xPos = int(float(msgParsed[1].split(":")[1]))
        self.width = int(float(msgParsed[3].split(":")[1]))
        self.height = int(float(msgParsed[4].split(":")[1]))

    def update(self, msgParsed):
        self.yPos = int(float(msgParsed[2].split(":")[1]))
        self.xPos = int(float(msgParsed[1].split(":")[1]))
        self.width = int(float(msgParsed[3].split(":")[1]))
        self.height = int(float(msgParsed[4].split(":")[1]))

    def move(self, ball, conncection):

        print ball.yPos, "    ", self.yPos
        if ball.yPos + 5 < self.yPos:
            import time
            conncection.send("up")
        elif ball.yPos >= self.yPos + 5:
            conncection.send("down")
        else:
            conncection.send("ok")


class Ball(object):
    """docstring for Opponent."""
    def __init__(self, msgParsed):
        self.yPos = int(float(msgParsed[2].split(":")[1]))
        self.xPos = int(float(msgParsed[1].split(":")[1]))
        self.width = int(float(msgParsed[3].split(":")[1]))
        self.height = int(float(msgParsed[4].split(":")[1]))

    def update(self, msgParsed):
        self.yPos = int(float(msgParsed[2].split(":")[1]))
        self.xPos = int(float(msgParsed[1].split(":")[1]))
        self.width = int(float(msgParsed[3].split(":")[1]))
        self.height = int(float(msgParsed[4].split(":")[1]))
# client
def controller(conn, player1, player2, ball):

    while True:
        try:
            msg = conn.recv()
            #print msg 
            if "Name:Player1" in msg:
                player1.update(msg.split(" "))
            elif "Name:Player2" in msg:
                player2.update(msg.split(" "))
            elif "Ball" in msg:
                ball.update(msg.split(" "))
            player1.move(ball, conn)
        except:
            conn.send("ok")

# server
def mother(address):
    player1 = Player("Name:Player1 xPos:780 yPos:250 width:20 height:55".split(" "))
    player2 = Opponent("Name:Player2 xPos:0 yPos:250 width:20 height:55".split(" "))
    ball = Ball("Ball: xPos:400 yPos:250 width:20 height:20".split(" "))
    serv = Listener(address)
    try:
        while True:
            client = serv.accept()
            controller(client, player1, player2, ball)
    except:
        return
def main():
    mother(('', 5000))

if __name__ == "__main__":
    main()

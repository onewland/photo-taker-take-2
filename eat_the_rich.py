import pygame
import RPi.GPIO as GPIO
import time
import datetime
import boto3
import random
import glob

QUEUE_URL = "https://queue.amazonaws.com/829315242464/button_events"
sqs = boto3.client("sqs")

pygame.init()

channel = 18
red = pygame.Color(255,50,50)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
font = pygame.font.Font(None, 256)
imgPath = 'photos/6fd46727e9df35668c6e1235287e3d6e.jpg'
text = font.render("TEST TRANSMISSION", 1, white, red)

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

def randomImagePath():
    return random.choice(glob.glob('photos/*.jpg'))

while 1:
    GPIO.wait_for_edge(channel,GPIO.FALLING)
    screen.fill(black)
    myimage = pygame.image.load(randomImagePath())
    imagerect = myimage.get_rect()
    screen.blit(myimage, imagerect)
    pygame.display.update()

    GPIO.wait_for_edge(channel,GPIO.RISING)
    sqs.send_message(QueueUrl=QUEUE_URL,MessageBody=unicode(datetime.datetime.now()))
    screen.fill(red)
    screen.blit(text, (100,100))
    pygame.display.update()

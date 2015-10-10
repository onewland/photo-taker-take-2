import pygame
import RPi.GPIO as GPIO
import time
import datetime
import boto3

QUEUE_URL = "https://queue.amazonaws.com/829315242464/button_events"
sqs = boto3.client("sqs")

pygame.init()

channel = 18
red = pygame.Color(255,50,50)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
width = 1824
height = 984
font = pygame.font.Font(None, 256)
text = font.render("EAT THE RICH", 1, white, red)

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

while 1:
    GPIO.wait_for_edge(channel,GPIO.FALLING)
    screen.fill(red)
    screen.blit(text, (100,100))
    pygame.display.update()
    GPIO.wait_for_edge(channel,GPIO.RISING)
    sqs.send_message(QueueUrl=QUEUE_URL,MessageBody=unicode(datetime.datetime.now()))
    time.sleep(1)
    screen.fill(black)
    pygame.display.update()

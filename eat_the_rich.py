import pygame
import RPi.GPIO as GPIO
import time
import datetime
import boto3
import random
import os
import glob

QUEUE_URL = "https://queue.amazonaws.com/829315242464/button_events"
sqs = boto3.client("sqs")

pygame.init()

channel = 18
red = pygame.Color(255,50,50)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
font = pygame.font.Font(None, 192)
imgPath = 'photos/6fd46727e9df35668c6e1235287e3d6e.jpg'
textTransgression = font.render("TRANSGRESSION", 1, white, red)
textRecorded = font.render("RECORDED", 1, white, red)

fontSmaller = pygame.font.Font(None, 72)
propagandaText = fontSmaller.render("WE NEED YOUR HELP TO ERADICATE BUTTON-PUSHERS, CITIZEN.", 1, white)

last_pressed = time.time()
last_image_switch = time.time()
IMAGE_SWITCH_SECONDS = 60

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

GPIO.add_event_detect(channel, GPIO.RISING)

def randomImagePath():
    return random.choice(glob.glob('photos/*.jpg'))

current_image_filename = randomImagePath()
current_image = pygame.image.load(current_image_filename)

def maybe_image_render():
    global last_image_switch, current_image, currnet_image_filename

    now = time.time()
    if now - last_image_switch > IMAGE_SWITCH_SECONDS:
        current_image_filename = randomImagePath()
        current_image = pygame.image.load(current_image_filename)
        render_current_image()
        last_image_switch = now

def md5_from_filename(fname):
    return os.path.splitext(os.path.split(fname)[1])[0]

def render_current_image():
    imagerect = current_image.get_rect()
    screen.blit(current_image, imagerect)

    rect = pygame.Surface((1920,200), pygame.SRCALPHA, 32)
    rect.fill((0, 0, 0, 200))
    rect.blit(propagandaText, (80,50))
    screen.blit(rect, (0,0))

    filenameText = fontSmaller.render("violator-id-" + md5_from_filename(current_image_filename), 1, white)
    screen.blit(filenameText, (80, 850))

    pygame.display.update()

render_current_image()

while 1:
    maybe_image_render()
    if(GPIO.event_detected(channel)):
        now = time.time()
        if now - last_pressed > 3:
            sqs.send_message(QueueUrl=QUEUE_URL,MessageBody=unicode(datetime.datetime.now()))
            last_pressed = now
            screen.fill(red)
            screen.blit(textTransgression, (100,100))
            screen.blit(textRecorded, (100,300))
            pygame.display.update()
            time.sleep(1)
            render_current_image()

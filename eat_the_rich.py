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
font = pygame.font.Font(None, 192)
imgPath = 'photos/6fd46727e9df35668c6e1235287e3d6e.jpg'
text = font.render("TRANSGRESSION RECORDED", 1, white, red)
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

current_image = pygame.image.load(randomImagePath())

def maybe_image_render():
    global last_image_switch, current_image

    now = time.time()
    if now - last_image_switch > IMAGE_SWITCH_SECONDS:
        current_image = pygame.image.load(randomImagePath())
        render_current_image()

def render_current_image():
    current_image = pygame.image.load(randomImagePath())
    imagerect = current_image.get_rect()
    screen.blit(current_image, imagerect)
    pygame.display.update()

while 1:
    # GPIO.wait_for_edge(channel,GPIO.FALLING)
    maybe_image_render()
    # GPIO.wait_for_edge(channel,GPIO.RISING)
    if(GPIO.event_detected(channel)):
        now = time.time()
        if now - last_pressed > 8:
            sqs.send_message(QueueUrl=QUEUE_URL,MessageBody=unicode(datetime.datetime.now()))
            last_pressed = now
        screen.fill(red)
        screen.blit(text, (100,100))
        pygame.display.update()
        time.sleep(1)
        render_current_image()

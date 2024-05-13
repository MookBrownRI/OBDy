import sys
import board
import digitalio
from PIL import Image
import adafruit_ssd1306
import time
import os

# INITIALIZE I2C AND SSD1306 OLED DISPLAY #
def hardwareInit():
    global oled
    global i2c
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
    
def Init():

    oled.fill(0)
    oled.show()
    # DEFINE VARIABLES GLOBALLY #
    global dictEmotions
    global rawEmotion
    global currentEmotion
    global imageFace
    global frame
    global switch
    global stateGAS
    global imageFuelLow
    global vehicleRPM
    global vehicleGASLEVEL
    global vehicleSPEED
    vehicleRPM = 0
    vehicleGASLEVEL = 100
    vehicleSPEED = 0
    imageFuelLow = Image.open("lowfuel.png").convert('RGBA')
    stateGAS = "HIGH"
    switch = 1
    frame = 0
    rawEmotion = 1
    dictEmotions = {1:"happy",
                2:"sad",
                3:"accelhappy",
                4:"accelsad",
                5:"dead",
                6:"error"}
    currentEmotion = dictEmotions[rawEmotion]


    imageFace = (Image.open("{}_cute.png".format(currentEmotion)).convert("1"))


def animationBoot():
    imageAnimation = (Image.open("boot_0.png").convert("1"))
    oled.image(imageAnimation)
    oled.show()
    time.sleep(3)
def getStatistics():
    global vehicleRPM
    global vehicleGASLEVEL
    global vehicleSPEED

    #vehicleRPM = 2500
    #vehicleSPEED += 3
    #if vehicleSPEED >=  120:
    #    vehicleSPEED = 0
    #print(vehicleRPM)
    #print(vehicleSPEED)
    

def updateEmotion():
    global rawEmotion
    global currentEmotion
    global imageFace
    global imageFuelLow
    global switch
    global frame
    global vehicleSPEED
    #if vehicleSPEED <= 5:
    #    frame = 0
    if switch == 1:        
        frame += 1
    if switch == 0:
        frame -= 2
    if frame == 6:
        switch = 0
    if frame == 0:
        switch = 1
    currentEmotion = dictEmotions[rawEmotion]
    imageFace = (Image.open("{}_cute.png".format(currentEmotion)).convert("1"))

    imageFace = imageFace.transform(imageFace.size, Image.AFFINE, (1,0,0,0,1,frame))
    imageFuelLow = imageFuelLow.transform(imageFuelLow.size, Image.AFFINE, (1,0,0,0,1,0))
    if stateGAS == "LOW":
        rawEmotion = 2
        imageFace.paste(imageFuelLow,(0,0),imageFuelLow)
    if vehicleSPEED >= 50:
        if vehicleRPM >=2000:
            if rawEmotion == 1:
                rawEmotion = 3
            if rawEmotion == 2:
                rawEmotion = 4
    #else:
    #    rawEmotion = 1
        

hardwareInit()
Init()
getStatistics()
animationBoot()
while True:
    oled.image(imageFace)
    oled.show()
    oled.fill(0)    
    updateEmotion()
    getStatistics()


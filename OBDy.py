import sys
import board
import digitalio
from PIL import Image
import adafruit_ssd1306
import time
import os
import obd

# INITIALIZE I2C AND SSD1306 OLED DISPLAY #
def hardwareInit():
    global oled
    global i2c
    global connectionOBD
    connectionOBD = obd.OBD()
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

def commandInit():
    global commandSpeed
    global commandRPM
    global commandThrottle
    global commandRunTime
    global commandFuelLevel
    global commandCoolantTemp

    commandSpeed = obd.commands.SPEED
    commandRPM = obd.commands.RPM
    commandThrottle = obd.commands.THROTTLE_POS
    commandRunTime = obd.commands.RUN_TIME
    commandFuelLevel = obd.commands.FUEL_LEVEL
    commandCoolantTemp = obd.commands.COOLANT_TEMP

def updateValues():
    global commandSpeed
    global commandRPM
    global commandThrottle
    global commandRunTime
    global commandFuelLevel
    global commandCoolantTemp
    global valueSpeed
    global valueRPM
    global valueThrottle
    global valueRunTime
    global valueFuelLevel
    global valueCoolantTemp

    valueSpeed = connectionOBD.query(commandSpeed)
    valueRPM = connectionOBD.query(commandRPM)
    valueThrottle = connectionOBD.query(commandThrottle)
    valueRunTime = connectionOBD.query(commandRunTime)
    valueFuelLevel = connectionOBD.query(commandFuelLevel)
    valueCoolantTemp = connectionOBD.query(commandCoolantTemp)
    valueSpeed = valueSpeed.value.to("mph")
    valueRPM = valueRPM.value
    valueThrottle = str(valueThrottle.value)
    valueRunTime = str(valueRunTime.value)
    valueFuelLevel = str(valueFuelLevel.value)
    valueCoolantTemp = str(valueCoolantTemp.value)
    print(valueSpeed)
    print(valueRPM)
    print(valueThrottle)
    print(valueRunTime)
    print(valueFuelLevel)
    print(valueCoolantTemp)
    valueSpeed = [int(i) for i in valueSpeed.split() if i.isdigit()]
    valueRPM = [int(i) for i in valueRPM.split() if i.isdigit()]
    valueThrottle = [int(i) for i in valueThrottle.split() if i.isdigit()]
    valueRunTime = [int(i) for i in valueRunTime.split() if i.isdigit()]
    valueFuelLevel = [int(i) for i in valueFuelLevel.split() if i.isdigit()]
    valueCoolentTemp  = [int(i) for i in valueCoolantTemp.split() if i.isdigit()]

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
#def getStatistics():
    #global vehicleRPM
    #global vehicleGASLEVEL
    #global vehicleSPEED

    #vehicleRPM = 2500
    #vehicleSPEED += 3
    #if vehicleSPEED >=  120:
    #    vehicleSPEED = 0
    #print(vehicleRPM)
    #print(vehicleSPEED)

def updateInDrive():
    global valueSpeed
    global valueRPM
    global valueThrottle
    global valueRunTime
    global valueFuelLevel
    global valueCoolantTemp

   # if valueSpeed > 0:
    if valueRPM > 2500:
        rawEmotion = 3
    if valueRPM <= 2500:
        reEmotion = 1
    #if valueSpeed < 50:
        #if rawEmotion == 3:
         #   rawEmotion = 1
        #if rawEmotion == 4:
         #   rawEmotion = 2
    #if valueFuelLevel < 15:
     #   rawEmotion = 2
      #  stateGAS == "LOW"
    #if valueFuelLevel > 15:
      #  rawEmotion = 1
       # stateGAS == "HIGH"

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

commandInit()
hardwareInit()
Init()
#getStatistics()
animationBoot()
while True:
    updateValues()
    updateInDrive()
    oled.image(imageFace)
    oled.show()
    oled.fill(0)

    #getStatistics()

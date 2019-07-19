from __future__ import print_function
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import requests
import picamera
import subprocess
import os
import sys

def log(s):
    with open("send.log", "a") as log:
        log.write(s+"\n")

#if(os.path.isfile("lock")):
#    log(str(datetime.datetime.now()))
#    log("locked")
#    sys.exit()
open("lock","w").close()

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, 1)
    time.sleep(1)

    camera=picamera.PiCamera()
    imagename="/home/pi/kaiwaimages/"+str(datetime.datetime.now())+".jpg"
    imagename = imagename.replace(" ", "_")
    log(imagename)
    camera.capture(imagename)
    
    time.sleep(1)
    GPIO.output(17, 0)

    id=subprocess.check_output(["curl","-X", "POST", "-F", "file=@"+imagename, "https://kaiware.ihavenojob.work/"])
    log("upload ok")

    # read data using pin 14
    instance = dht11.DHT11(pin=14)

    result = instance.read()
    temp="error"
    hum="error"
    for _ in range(20):
        if result.is_valid():
            temp=result.temperature
            hum=result.humidity
            log("hum ok")
            break;
        time.sleep(1)
    ##    print str(temp)
    ##    print str(hum)
    id=id.split(" ")
    url="https://script.google.com/macros/s/AKfycbzWiL-vPKit8lNthfI7byoilALRKY97BgNSze3iTjb-4GkIvbL3/exec?date="
    url+=str(datetime.datetime.now().year)+","
    url+=str(datetime.datetime.now().month)+","
    url+=str(datetime.datetime.now().day)+","
    url+=str(datetime.datetime.now().hour)+","
    url+=str(datetime.datetime.now().minute)+","
    url+=str(datetime.datetime.now().second)+"&temp="
    url+=str(temp)
    url+="&hum="
    url+=str(hum)
    url+="&bright=hogehoge"
    url+="&imageurl="
    url+=str(id[0])
    requests.get(url)
    log("send ok")
    print(url)
    subprocess.call(["rm",imagename])

    os.remove("lock")
    
    GPIO.cleanup()

except Exception as e:
    log(str(e))
    raise e


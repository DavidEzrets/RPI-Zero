#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from TCS34725 import TCS34725
import pickle

try:
    Light=TCS34725(0X29, debug=False)
    if(Light.TCS34725_init() == 1):
        'print("TCS34725 initialization error!!")'
    else:
        'print("TCS34725 initialization success!!")'
    time.sleep(2)
    while True:
        Light.Get_RGBData()
        Light.GetRGB888()
        Light.GetRGB565()
        #print("R: %d "%Light.RGB888_R),
        #print("G: %d "%Light.RGB888_G),
        #print("B: %d "%Light.RGB888_B),
        #print("C: %#x "%Light.C),
        #print("RGB565: %#x "%Light.RG565),
        #print("RGB888: %#x "%Light.RGB888), 
        #print("LUX: %d "%Light.Get_Lux()),
        #print("CT: %dK "%Light.Get_ColorTemp())
        
        dict_name = {
        'R': Light.RGB888_R,
        'G': Light.RGB888_G,
        'B': Light.RGB888_B, 
        'C': Light.C,
        'RGB565': Light.RG565,
        'RGB888': Light.RGB888,    
        'LUX': Light.Get_Lux(),
        'CT': Light.Get_ColorTemp()
        }
        
        file_name = open('/home/pi/main/sense/temp/TCS34725', 'wb')
        pickle.dump(dict_name,file_name,protocol=0); file_name.close()         
        break;
       
except:
    GPIO.cleanup()
    #print ("\nProgram end")
    exit()
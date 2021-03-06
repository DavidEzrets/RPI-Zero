#!/usr/bin/env python

import signal
import buttonshim
import os
import time
import sys
import pickle
from rgbmatrix5x5 import RGBMatrix5x5


print("main start")

global A; A=0
global B; B=0
global C; C=0
global D; D=0
global E; E=0
global AA; AA=0
global BB; BB=0
global CC; CC=0
global DD; DD=0
global EE; EE=0

buttonshim.set_pixel(0x00, 0x00, 0x00)

rgbmatrix5x5 = RGBMatrix5x5()
rgbmatrix5x5.set_all(0x00, 0x00, 0xFF) #rgb
rgbmatrix5x5.show()
time.sleep(2)
rgbmatrix5x5.set_all(0x00, 0x00, 0x00) #rgb
rgbmatrix5x5.show()

button_was_held = False


@buttonshim.on_press(buttonshim.BUTTON_A) # When begin to press
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state
    buttonshim.set_pixel(0x00, 0xff, 0x00)
    global A; A=0; global B; B=0; global C; C=0; global D; D=0;global E; E=0
    
@buttonshim.on_release(buttonshim.BUTTON_A)
def release_handler(button, pressed):
    if not button_was_held:
      buttonshim.set_pixel(0x00, 0x00, 0x00)
      global A; A=1   

@buttonshim.on_hold(buttonshim.BUTTON_A, hold_time=2)
def hold_handler(button):
    global button_was_held
    button_was_held = True
    buttonshim.set_pixel(0x00, 0x00, 0xff)
    os.system ("sudo python3 /home/pi/main/Display_I2C.py")
    time.sleep(1); buttonshim.set_pixel(0x00, 0x00, 0x00)     
    global AA; AA=1

@buttonshim.on_press(buttonshim.BUTTON_B)
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state
    buttonshim.set_pixel(0x00, 0xff, 0x00)
    global A; A=0; global B; B=0; global C; C=0; global D; D=0;global E; E=0

@buttonshim.on_release(buttonshim.BUTTON_B)
def release_handler(button, pressed):
    if not button_was_held:
      buttonshim.set_pixel(0x00, 0x00, 0x00)
      global B; B=1   

@buttonshim.on_hold(buttonshim.BUTTON_B, hold_time=2)
def hold_handler(button):
    global button_was_held
    button_was_held = True
    buttonshim.set_pixel(0x00, 0x00, 0xff)
    os.system ("sudo python3 /home/pi/main/Display_Sense.py")
    time.sleep(1); buttonshim.set_pixel(0x00, 0x00, 0x00) 
    global BB; BB=1 

@buttonshim.on_press(buttonshim.BUTTON_C)
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state
    buttonshim.set_pixel(0x00, 0xff, 0x00)
    global A; A=0; global B; B=0; global C; C=0; global D; D=0;global E; E=0


@buttonshim.on_release(buttonshim.BUTTON_C)
def release_handler(button, pressed):
    if not button_was_held:
      buttonshim.set_pixel(0x00, 0x00, 0x00)
      global C; C=1   

@buttonshim.on_hold(buttonshim.BUTTON_C, hold_time=2)
def hold_handler(button):
    global button_was_held
    button_was_held = True
    buttonshim.set_pixel(0x00, 0x00, 0xff)
    print ('Begin')
    os.system ("sudo python3 /home/pi/main/Display-Calendar.py")
    time.sleep(1); buttonshim.set_pixel(0x00, 0x00, 0x00)
    global CC; CC=1
    print ('End')

@buttonshim.on_press(buttonshim.BUTTON_D)
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state
    buttonshim.set_pixel(0x00, 0xff, 0x00)
    global A; A=0; global B; B=0; global C; C=0; global D; D=0;global E; E=0


@buttonshim.on_release(buttonshim.BUTTON_D)
def release_handler(button, pressed):
    if not button_was_held:
      buttonshim.set_pixel(0x00, 0x00, 0x00)
      global D; D=1   

@buttonshim.on_hold(buttonshim.BUTTON_D, hold_time=2)
def hold_handler(button):
    global button_was_held
    button_was_held = True
    buttonshim.set_pixel(0x00, 0x00, 0xff)
    print ('Begin')
    os.system ("sudo python3 /home/pi/main/Display_Weather.py")
    time.sleep(1); buttonshim.set_pixel(0x00, 0x00, 0x00) 
    global DD; DD = 1;
    
@buttonshim.on_press(buttonshim.BUTTON_E)
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state
    buttonshim.set_pixel(0x00, 0xff, 0x00)
    global A; A=0; global B; B=0; global C; C=0; global D; D=0;global E; E=0


@buttonshim.on_release(buttonshim.BUTTON_E)
def release_handler(button, pressed):
    if not button_was_held:
        buttonshim.set_pixel(0x00, 0x00, 0x00)
        global E; E=1   

@buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=2)
def hold_handler(button):
    global button_was_held
    button_was_held = True
    buttonshim.set_pixel(0xff, 0x00, 0x00)
    os.system ("sudo shutdown -h now")
    rgbmatrix5x5 = RGBMatrix5x5(); rgbmatrix5x5.set_all(0xFF,0,0); rgbmatrix5x5.show(); time.sleep(1); rgbmatrix5x5.set_all(0,0,0); rgbmatrix5x5.show()
    time.sleep(1); buttonshim.set_pixel(0x00, 0x00, 0x00) 
    global EE; EE=1
    

while E==0:
   time.sleep(1)


rgbmatrix5x5 = RGBMatrix5x5(); rgbmatrix5x5.set_all(0,0xFF,0); rgbmatrix5x5.show(); time.sleep(1); rgbmatrix5x5.set_all(0,0,0); rgbmatrix5x5.show()  
  
 #----------------------------------------------
  


  
#  if A==0 and B==0 and C==0:
#    print ('not pressed')
  
#  while DD!=0:
#    print ('compass')

 #   os.system ("sudo python /home/pi/Sense-HAT-1/ICM20948.py")
 #   file_open = open('/home/pi/Sense-HAT-1/temp/ICM20948', 'rb'); dict_open = pickle.load(file_open); file_open.close()
 #   temp = dict_open['Mag1']
 #   print (temp)
    #buttonshim.set_pixel(0xff, 0x00, 0x00)
    #time.sleep(abs(temp)/1000)
    #buttonshim.set_pixel(0x00, 0x00, 0xff) 
    


  #  buttonshim.set_pixel(0x00, 0x00, 0x00)
  #if C==2:
    #buttonshim.set_pixel(0xff, 0x00, 0x00)
#  print ("A")
#  print (A)   
#  print ("B")
#  print (B)
#  print ("C")
#  print (C)
#  print ("D")
#  print (D)
#  print ("E")
#  print (E) 


print ("end")
#signal.pause()  # Stop script from immediately exiting
#!/usr/bin/env python

import signal
import buttonshim
import os
import time
import sys
import pickle
from rgbmatrix5x5 import RGBMatrix5x5


print("main_bg")


buttonshim.set_pixel(0x00, 0x00, 0x00)

rgbmatrix5x5 = RGBMatrix5x5()


for x in range(3):
    rgbmatrix5x5.set_all(0xFF, 0xFF, 0) #rgb
    rgbmatrix5x5.show()
    time.sleep(1/2)
    rgbmatrix5x5.set_all(0, 0xFF, 0xFF) #rgb
    rgbmatrix5x5.show()
    time.sleep(1/2)

rgbmatrix5x5.set_all(0, 0, 0) #rgb
rgbmatrix5x5.show()


button_was_held = False


@buttonshim.on_press(buttonshim.BUTTON_A) # When begin to press
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state    

@buttonshim.on_press(buttonshim.BUTTON_B)
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state

@buttonshim.on_press(buttonshim.BUTTON_C)
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state

@buttonshim.on_press(buttonshim.BUTTON_D)
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state
    
@buttonshim.on_press(buttonshim.BUTTON_E)
def press_handler(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False   # Reset the button held state


@buttonshim.on_hold(buttonshim.BUTTON_A, hold_time=10)
def hold_handler(button):
    global button_was_held
    button_was_held = True
    rgbmatrix5x5 = RGBMatrix5x5(); rgbmatrix5x5.set_all(0xFF,0xFF,0); rgbmatrix5x5.show(); time.sleep(1); rgbmatrix5x5.set_all(0,0,0); rgbmatrix5x5.show()
    os.system ("sudo python3 /home/pi/main/main.py")
    
    
@buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=10)
def hold_handler(button):
    global button_was_held
    button_was_held = True
    rgbmatrix5x5 = RGBMatrix5x5(); rgbmatrix5x5.set_all(0xFF,0xFF,0); rgbmatrix5x5.show(); time.sleep(1); rgbmatrix5x5.set_all(0,0,0); rgbmatrix5x5.show()
    os.system ("sudo shutdown -h now")
    

while True:
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
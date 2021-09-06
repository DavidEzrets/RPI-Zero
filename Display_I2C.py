#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import subprocess
import pickle
import RPi.GPIO as GPIO
import datetime
from sys import exit

from font_fredoka_one import FredokaOne
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont


PATH = os.path.dirname(__file__)

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

if inky_display.resolution not in ((212, 104), (250, 122)):
    w, h = inky_display.resolution
    raise RuntimeError("This example does not support {}x{}".format(w, h))

inky_display.set_border(inky_display.BLACK)

def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
    """Create a transparency mask.

    Takes a paletized source image and converts it into a mask
    permitting all the colours supported by Inky pHAT (0, 1, 2)
    or an optional list of allowed colours.
    :param mask: Optional list of Inky pHAT colours to allow.
    """
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)

    return mask_image


def print_digit(position, digit, colour):
    """Print a single digit using the sprite sheet.

    Each number is grabbed from the masked sprite sheet,
    and then used as a mask to paste the desired colour
    onto Inky pHATs image buffer.
    """
    o_x, o_y = position

    num_margin = 2
    num_width = 6
    num_height = 7

    s_y = 11
    s_x = num_margin + (digit * (num_width + num_margin))

    sprite = text_mask.crop((s_x, s_y, s_x + num_width, s_y + num_height))

    img.paste(colour, (o_x, o_y), sprite)
    
def print_number(position, number, colour):
    """Print a number using the sprite sheet."""
    for digit in str(number):
        print_digit(position, int(digit), colour)
        position = (position[0] + 8, position[1])


def istring(x,y,string,color1,color2):
  l = len(str(string))
  for i in range (l):
    temp = string[0]
    string=string[1:]
    if temp.isdigit():
      print_number((x+i*8, y), temp, color1)
    else:
      font = ImageFont.truetype(FredokaOne, 10)
      draw.text((x+i*8, y-2), temp, color2, font=font)
    
def istring_minus(x,y,string,color1,color2):
  font = ImageFont.truetype(FredokaOne, 10)
  l = len(str(string))
  offset=0
  minus=0 #if minus sign and number after
  for i in range (l):
    temp = string[0]
  
    temp2 = 'ABC' #pretent 'ABC' it at end of string so if '-' at end of string, it will not effect
    if i!=(l-1):
      temp2 = string[1]
      string = string [1:]
      
    if temp.isdigit():
      if minus==1:
        draw.rectangle((x+(i-offset)*8-2, y-1, x+(i-offset+1)*8, y+7), fill=inky_display.WHITE, outline=inky_display.WHITE)
      print_number((x+(i-offset)*8, y), temp, color1 if minus==0 else inky_display.BLACK)
    elif temp=='-' and temp2.isdigit(): #and string[0].isdigit and i!=l:
      offset=offset+1
      minus=1
    else:
      draw.text((x+(i-offset)*8, y-2), temp, color2, font=font)
      minus=0
     
#draw.line((69, 58, 174, 58))      # Horizontal middle line
#draw.line((169, 58, 169, 58), 2)  # Red seaweed pixel :D
#draw.rectangle((0, 0, 12, 12), fill=inky_display.RED, outline=inky_display.WHITE)
#draw.line((20, 20, 50, 50))      
      
      
text = Image.open(os.path.join(PATH, "inky/calendar.png"))
text_mask = create_mask(text, [inky_display.WHITE])
img = Image.open(os.path.join(PATH, "inky/empty-backdrop.png")).resize(inky_display.resolution)
draw = ImageDraw.Draw(img)


os.system ("sudo i2cdetect -y 1 > /home/pi/main/sense/temp/os_temp3.txt") #----------------------------------------------
file = open ("/home/pi/main/sense/temp/os_temp3.txt")

main1 = []
file.readline()
while True:
  temp = file.readline().upper()
  if len(temp)==0:
    break
  temp=temp.split(' ')
  del temp[0]
  temp = [x for x in temp if x != '\n' and x != '' and x !='--']
  main1 = main1 + temp

I2C_List =["48: SENSE ADC",
           "68: SENSE 9-AXIS",
           "5C: SENSE BAROMETRIC",
           "70: SENSE HUMIDITY",
           "29: SENSE COLOR",
           "3F: BUTTON SHIM",
           "50: DISPLAY",
           "36: BATTERY",
           "74; 5X5 RGB LED"]
n=0
for x1 in range(len(main1)):
  for x2 in range(len(I2C_List)):
    temp=I2C_List[x2]
    temp=temp[0:2]
    space=10
    if main1[x1]==I2C_List[x2][0:2]:   #len(I2C_List[x2])*8
      draw.rectangle((32-2, n*space-1, 30+150, n*space+10), fill=inky_display.RED, outline=inky_display.BLACK)
      #istring(30,00+n*8,I2C_List[x2],inky_display.WHITE,inky_display.WHITE)
      istring(32,n*space,I2C_List[x2][:4],inky_display.WHITE,inky_display.WHITE)
      font = ImageFont.truetype(FredokaOne, 11)
      draw.text((55, n*space-2), I2C_List[x2][4:], inky_display.WHITE, font=font)

      n+=1


istring(10,95,str(inky_display.resolution[0]) + ' x ' + str(inky_display.resolution[1]),inky_display.BLACK,inky_display.RED)



# Display the weather data on Inky pHAT
inky_display.set_image(img)
inky_display.show()
print ('end')

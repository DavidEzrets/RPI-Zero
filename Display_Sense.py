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

def inumber(x,y,number,ending,color1,color2,after,ending_location): 
  if after==0: # 11V
    number=round(float(number))
    l=len(str(int(number)))
    print_number((x, y), int(round(float(number))), color1)
    font = ImageFont.truetype(FredokaOne, 10)
    draw.text((x+l*8, y+ending_location), ending, color2, font=font)
  if after==1: # 11.1V
    number = round(float(number),1)
    l=len(str(int(number)))-2 #-2 because originialy made for 2 digits before .
    print_number((x, y), int(float(number)), color1)
    print_number((x+l*8+18, y),((int(float(number)*10))%10), color1)
    font = ImageFont.truetype(FredokaOne, 10)
    draw.text((x+l*8+15, y-3), '.', color2, font=font)
    draw.text((x+l*8+25, y+ending_location), ending, color2, font=font)
  if after==2: # 1.11V
    number = round(float(number),2)
    l=len(str(int(number)))-1 #-1 because originialy made for 1 digits before .
    print_number((x, y), int(float(number)), color1)
    print_number((x+l*8+10, y),((int(float(number)*10))%10), color1)
    print_number((x+l*8+17, y),((int(float(number)*100))%10), color1)
    font = ImageFont.truetype(FredokaOne, 10)
    draw.text((x+l*8+7, y-3), '.', color2, font=font)
    draw.text((x+l*8+25, y+ending_location), ending, color2, font=font)

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


# Load our sprite sheet and prepare a mask
#img = Image.open(os.path.join(PATH, "resources/empty-backdrop.png")).resize(inky_display.resolution)
img = Image.open(os.path.join(PATH, "inky/backdrop.png")).resize(inky_display.resolution)
draw = ImageDraw.Draw(img)

x = datetime.datetime.now().month
month_x = 2 + (((x - 1) % 3) * 23)
month_y = 20 + (((x - 1) // 3) * 9)
crop_region = (month_x, month_y, month_x + 23, month_y + 9)
month_mask = text_mask.crop(crop_region)
img.paste(inky_display.WHITE, (80, 0), month_mask)

x = datetime.datetime.now().weekday()
crop_region = ((2 + (16 * x)), 0, (2 + (16 * x)) + 16, 9)
day_mask = text_mask.crop(crop_region)
img.paste(inky_display.WHITE, (40, -2), day_mask)

istring (132,0,datetime.datetime.now().strftime('%H:%M'),inky_display.WHITE,inky_display.RED)
istring (60,0,datetime.datetime.now().strftime('%d'),inky_display.WHITE,inky_display.RED)
istring (106,0,datetime.datetime.now().strftime('%y'),inky_display.RED,inky_display.RED)


os.system ("rm /home/pi/main/sense/temp/*") # delete folder with temp file


os.system ("iwgetid > /home/pi/main/sense/temp/os_temp1.txt") #----------------------------------------------
file = open ("/home/pi/main/sense/temp/os_temp1.txt")
txt = file.readline()
if not txt:
  temp = 'N/A'
else:
  temp = txt.split(':')[1].replace('"','').replace('\n','').replace(' ','')
font = ImageFont.truetype(FredokaOne, 12)
draw.text((2, 91), temp, inky_display.BLACK, font=font)
#istring (2,91,temp,inky_display.BLACK)


os.system ("/opt/vc/bin/vcgencmd measure_temp > /home/pi/main/sense/temp/os_temp2.txt") #----------------------------------------------
file = open ("/home/pi/main/sense/temp/os_temp2.txt")
txt = file.readline()
if not txt:
  temp = 'N/A'
else:
  temp = txt.split('=')[1].replace("'C",'').replace('\n','').replace(' ','').replace("'",'')
inumber(101,95,temp,'°C',inky_display.BLACK,inky_display.RED,1,-2)


os.system ("sudo python3 /home/pi/main/sense/UPS_Lite.py") #----------------------------------------------
file_open = open('/home/pi/main/sense/temp/UPS_Lite', 'rb'); dict_open = pickle.load(file_open); file_open.close()
temp = dict_open['Voltage']
if not temp: 
  temp = 'N/A'
else:
  temp = ('%5.2f'% temp)
  
draw.rectangle((140, 92, 211, 103), fill=inky_display.WHITE, outline=inky_display.RED)
inumber(178,95,temp,'V',inky_display.BLACK,inky_display.RED,2,-2)

temp = dict_open['Battery']
inumber(142 if (temp)>100 else 146,95,temp,'%',inky_display.BLACK if float(temp)>20 else inky_display.RED,inky_display.RED,0,-4)


os.system ("sudo python /home/pi/main/sense/SHTC3.py") #----------------------------------------------
file_open = open('/home/pi/main/sense/temp/SHTC3', 'rb'); dict_open = pickle.load(file_open); file_open.close()

font = ImageFont.truetype(FredokaOne, 10)
draw.text((38, 14), "SHTC3", inky_display.RED, font=font)
inumber(77,16, dict_open['Temperature'],'°C',inky_display.WHITE,inky_display.RED,1,-2)
inumber(120,16, dict_open['Humidity'],'%',inky_display.WHITE,inky_display.RED,1,-4)


pz=0
while pz==0:
  os.system ("sudo python /home/pi/main/sense/LPS22HB.py") #----------------------------------------------
  file_open = open('/home/pi/main/sense/temp/LPS22HB', 'rb'); dict_open = pickle.load(file_open); file_open.close()
  pz = (dict_open['Pressure'])
  print ('Pressure try 1')
font = ImageFont.truetype(FredokaOne, 10)
draw.text((38, 24), "LPS22", inky_display.RED, font=font)
inumber(77,26, dict_open['Temperature'],'°C',inky_display.WHITE,inky_display.RED,1,-2)
print_number((120,26), round(float(dict_open['Pressure'])), inky_display.WHITE)
  

os.system ("sudo python /home/pi/main/sense/TCS34725_main.py") #----------------------------------------------
file_open = open('/home/pi/main/sense/temp/TCS34725', 'rb'); dict_open = pickle.load(file_open); file_open.close()
istring (34,36,str(round(dict_open['CT']))+' R'+str(dict_open['R'])+' G'+str(dict_open['G'])+' B'+str(dict_open['B']),inky_display.WHITE,inky_display.RED)


os.system ("sudo python /home/pi/main/sense/ICM20948.py") #----------------------------------------------
file_open = open('/home/pi/main/sense/temp/ICM20948', 'rb'); dict_open = pickle.load(file_open); file_open.close()

istring_minus (30,50,'G '+str(dict_open['Gyro0'])+' '+str(dict_open['Gyro1'])+' '+str(dict_open['Gyro2'])+
               '  '+str(round(dict_open['Pitch']))+' '+str(round(dict_open['Roll']))+' '+str(round(dict_open['Yaw'])),inky_display.WHITE,inky_display.RED)
istring_minus (30,61,'M '+str(dict_open['Mag0'])+' '+str(dict_open['Mag1'])+' '+str(dict_open['Mag2']),inky_display.WHITE,inky_display.RED)
istring_minus (30,72,'A '+str(dict_open['Accel0'])+' '+str(dict_open['Accel1'])+' '+str(dict_open['Accel2']),inky_display.WHITE,inky_display.RED)


#os.system ("sudo python /home/pi/Sense-HAT-1/ADS1015.py")
#file_open = open('/home/pi/Sense-HAT-1/temp/ADS1015', 'rb'); dict_open = pickle.load(file_open); file_open.close()
#UVlist = [50,227,318,408,606,696,795,881,976,1079,1170]
#UVvalue=min(UVlist, key=lambda x:abs(x-dict_open['AIN3']))
#UVindex=UVlist.index(UVvalue)
#inumber(80,95,UVindex,'UV',inky_display.BLACK,inky_display.RED,0,-4)


# Display the weather data on Inky pHAT
inky_display.set_image(img)
inky_display.show()
print ('end')

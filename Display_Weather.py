#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import requests
from datetime import datetime
from pprint import pprint
from sys import exit

from font_fredoka_one import FredokaOne
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont



# Get the current path
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
        
def icone(x,y,icon):
  #draw.rectangle((0, 0, 40, 45), fill=inky_display.BLACK, outline=inky_display.RED)
  if icon=='01':
  #clear sky - 01
    img.paste(Image.open('/home/pi/main/inky/icon-sun.png'), (x, y), create_mask(Image.open('/home/pi/main/inky/icon-sun.png')))
  
  elif icon=='02':
  #few clouds - 02
    img.paste(Image.open('/home/pi/main/inky/icon-cloud.png'), (x, y), create_mask(Image.open('/home/pi/main/inky/icon-cloud.png')))  

  elif icon=='03' or icon=='04':
  #scattered clouds + broken clouds - 03 04
    img.paste(Image.open('/home/pi/main/inky/icon-rain.png'), (x-2, y+5), create_mask(Image.open('/home/pi/main/inky/icon-rain.png')))
    draw.rectangle((x+14, y+29, x+28, y+45), fill=inky_display.BLACK, outline=inky_display.BLACK)
  
  elif icon=='09':
  #shower rain - 09
    img.paste(Image.open('/home/pi/main/inky/icon-rain.png'), (x-2, y), create_mask(Image.open('/home/pi/main/inky/icon-rain.png'))) 
  
  elif icon=='10':
  #rain - 10
    img.paste(Image.open('/home/pi/main/inky/icon-rain.png'), (x-7, y+5), create_mask(Image.open('/home/pi/main/inky/icon-rain.png')))  
    img.paste(Image.open('/home/pi/main/inky/icon-cloud.png'), (x-1, y-7), create_mask(Image.open('/home/pi/main/inky/icon-cloud.png')))
  
  elif icon=='11':
  #thunderstorm 11
    img.paste(Image.open('/home/pi/main/inky/icon-storm.png'), (x-2, y), create_mask(Image.open('/home/pi/main/inky/icon-storm.png'))) 
  
  elif icon=='13':
  #snow - 13
    img.paste(Image.open('/home/pi/main/inky/icon-snow.png'), (x-2, y), create_mask(Image.open('/home/pi/main/inky/icon-snow.png'))) 
  
  elif icon=='50':
  #mist - 50
    x+=10
    y+=11
    draw.line((x+5, y, x+15, y))  
    draw.line((x+5, y+1, x+15, y+1))  
    
    draw.line((x, y+4, x+7, y+4))  
    draw.line((x, y+5, x+7, y+5))
    draw.line((x+13, y+4, x+20, y+4)) 
    draw.line((x+13, y+5, x+20, y+5)) 
    
    draw.line((x, y+8, x+20, y+8)) 
    draw.line((x, y+9, x+20, y+9))
    draw.line((x, y+12, x+20, y+12)) 
    draw.line((x, y+13, x+20, y+13))
    
    draw.line((x, y+16, x+7, y+16))  
    draw.line((x, y+17, x+7, y+17))
    draw.line((x+13, y+16, x+20, y+16)) 
    draw.line((x+13, y+17, x+20, y+17))  
  
    draw.line((x+5, y+20, x+15, y+20))  
    draw.line((x+5, y+21, x+15, y+21))   
  
  
  
def weather(X,Y,city):
  X0=X+106
  Y0=Y+52
  BASE_URL = "http://api.openweathermap.org/data/2.5/weather?appid=06220bf4057e98af502395042010213d&id={0}&units=metric"
  final_url = BASE_URL.format(city)
  weather_data = requests.get(final_url).json()
  pprint(weather_data)    

  icone (X-3,Y-1,weather_data['weather'][0]['icon'][0:2])
  istring_minus (X+51,Y0-20,str(round(weather_data['main']['feels_like'])) + '°',inky_display.WHITE,inky_display.WHITE)


  draw.line((X-1, Y+10, X+8, Y+10),0) 
  draw.line((X+8, Y, X+8, Y+10),3)   
  
  if weather_data['name'] == 'Petah Tikva':
    istring (X,Y+1,weather_data['name'].split(' ')[0][0:1],inky_display.WHITE,inky_display.WHITE)
  if weather_data['name'] == 'Tel Aviv':
    istring (X,Y+1,weather_data['name'].split(' ')[0][0:1],inky_display.WHITE,inky_display.WHITE)
  if weather_data['name'] == 'Netanya':
    istring (X,Y+1,weather_data['name'].split(' ')[0][0:1],inky_display.WHITE,inky_display.WHITE)
  if weather_data['name'] == 'Herzliya':
    istring (X,Y+1,weather_data['name'].split(' ')[0][0:1],inky_display.WHITE,inky_display.WHITE)

  draw.rectangle((X0-33, Y0-20, X0-2, Y0), fill=inky_display.WHITE, outline=inky_display.WHITE)
  istring (X0-32,Y0-9,str(round(weather_data['main']['pressure'])) + '',inky_display.BLACK,inky_display.RED)
  inumber(X0-32,Y0-19,str(round(weather_data['main']['humidity'])),'%',inky_display.BLACK,inky_display.RED,0,-3)

  font = ImageFont.truetype(FredokaOne, 22)
  draw.text((X+35, Y+5), str(int(round(weather_data['main']['temp'],1))) + '°', inky_display.WHITE, font=font)
  istring (X+62,Y+20, '.',inky_display.WHITE,inky_display.RED)
  istring (X+65,Y+21, str(int( round(weather_data['main']['temp'],1)*10%10 )),inky_display.WHITE,inky_display.RED)

  draw.rectangle((X0-33, Y+12, X0-2, Y+29), fill=inky_display.WHITE, outline=inky_display.WHITE)
  istring (X0-32,Y+13,str(datetime.fromtimestamp(weather_data['sys']['sunrise'])).split(' ')[1].split(':')[0]+str(datetime.fromtimestamp(weather_data['sys']['sunrise'])).split(' ')[1].split(':')[1],inky_display.RED,inky_display.RED)
  istring (X0-32,Y+22,str(datetime.fromtimestamp(weather_data['sys']['sunset'])).split(' ')[1].split(':')[0]+str(datetime.fromtimestamp(weather_data['sys']['sunset'])).split(' ')[1].split(':')[1],inky_display.BLACK,inky_display.RED)
  
  istring (X+49,Y+1,str(datetime.fromtimestamp(weather_data['dt'])).split(' ')[0].split('-')[2]+' ' +
                  str(datetime.fromtimestamp(weather_data['dt'])).split(' ')[1].split(':')[0]+
                  str(datetime.fromtimestamp(weather_data['dt'])).split(' ')[1].split(':')[1]
                  ,inky_display.WHITE,inky_display.RED)

  x=int(str(datetime.fromtimestamp(weather_data['dt'])).split(' ')[0].split('-')[1])

  month_x = 2 + (((x - 1) % 3) * 23)
  month_y = 20 + (((x - 1) // 3) * 9)
  crop_region = (month_x, month_y, month_x + 23, month_y + 9)
  month_mask = text_mask.crop(crop_region)
  img.paste(inky_display.WHITE, (X+23,Y+1), month_mask)

  lat=weather_data['coord']['lat']
  lon=weather_data['coord']['lon']
  BASE_URL = "http://api.openweathermap.org/data/2.5/onecall?appid=06220bf4057e98af502395042010213d&lat={0}&lon={1}&exclude=minutely,hourly,daily&units=metric"
  final_url = BASE_URL.format(lat,lon)
  weather_data = requests.get(final_url).json()
  pprint(weather_data)

  istring (X,Y0-10,str(weather_data['current']['clouds']) + '% ' +str(round(weather_data['current']['wind_speed'])) + 'm/s',inky_display.WHITE,inky_display.RED)

  draw.rectangle((X+29, Y0-21, X+48, Y0-13), fill=inky_display.WHITE, outline=inky_display.WHITE)
  inumber(X+31,Y0-20,weather_data['current']['uvi'],'',inky_display.BLACK,inky_display.RED,1,-2)
#weather function ends --------------------------------------------------------------------------------




text = Image.open(os.path.join(PATH, "inky/calendar.png"))
text_mask = create_mask(text, [inky_display.WHITE]) 

img = Image.open(os.path.join(PATH, "inky/backdrop.png")).resize(inky_display.resolution)
draw = ImageDraw.Draw(img)

draw.rectangle((0, 0, 300, 200), fill=inky_display.BLACK, outline=inky_display.BLACK)
draw.line((0, 52, 300, 52))      
draw.line((104, 0, 104, 200))      



weather (0,0,'6693674')
weather (107,0,'293397')
weather (0,53,'294071')
weather (107,53,'294778') #Eilat: 295277















#print (weather_data['current']['clouds'])
#print (weather_data['current']['uvi'])
#print (weather_data['current']['wind_speed'])

#draw.line((X, Y+50, X+5, Y+50))      # Horizontal middle line




# Display the weather data on Inky pHAT
inky_display.set_image(img)
inky_display.show()

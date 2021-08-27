#!/usr/bin/python
# -*- coding:utf-8 -*-
import ctypes
import pickle

class SHTC3:
    def __init__(self):
        self.dll = ctypes.CDLL("/home/pi/Sense-HAT-1/SHTC3.so")
        init = self.dll.init
        init.restype = ctypes.c_int
        init.argtypes = [ctypes.c_void_p]
        init(None)

    def SHTC3_Read_Temperature(self):
        temperature = self.dll.SHTC3_Read_TH
        temperature.restype = ctypes.c_float
        temperature.argtypes = [ctypes.c_void_p]
        return temperature(None)

    def SHTC3_Read_Humidity(self):
        humidity = self.dll.SHTC3_Read_RH
        humidity.restype = ctypes.c_float
        humidity.argtypes = [ctypes.c_void_p]
        return humidity(None)


if __name__ == "__main__":
    shtc3 = SHTC3()
    while True:
        
        dict_name = {'Temperature': shtc3.SHTC3_Read_Temperature(), 'Humidity': shtc3.SHTC3_Read_Humidity()}
        file_name = open('/home/pi/main/sense/temp/SHTC3', 'wb')
        pickle.dump(dict_name,file_name,protocol=0); file_name.close()
        #print('Temperature = %6.2f°C , Humidity = %6.2f%%' % (shtc3.SHTC3_Read_Temperature(), shtc3.SHTC3_Read_Humidity()))
        break;
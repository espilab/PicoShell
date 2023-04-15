#
# set_rtc.py --- set RTC date/time (PCF8563 required)
#

from common.device.pcf8563 import PCF8563
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000)
rtc = PCF8563(i2c)


from machine import Pin, I2C
import machine
import time
import re

def get_weekday(year, month, day):
    # RTCを初期化
    rtc = machine.RTC()
    # 年月日を設定
    rtc.datetime((year, month, day, 0, 0, 0, 0, 0))
    # 曜日を表す整数を取得 (0=月曜日, 1=火曜日, ..., 6=日曜日)
    weekday_num = rtc.datetime()[3]
    return weekday_num


#print('cmd_line=', sep="", end="")
#print(COMMAND_LINE)


arg0, *para_list = (re.sub('\ +', ',', COMMAND_LINE)).split(',')

#print(para_list)

if len(para_list) < 6:
    if len(para_list) == 1:
        print('rtc.datetime=', rtc.datetime())
    else:
        print('usage: set_rtc <year> <month> <day> <hour> <minutes> <seconds>')
else:     
    print('para_list=',para_list)	##DEBUG
    year = int(para_list[0])
    month = int(para_list[1])
    day = int(para_list[2])
    hour = int(para_list[3])
    min = int(para_list[4])
    sec = int(para_list[5]) 
    weekday = get_weekday(year, month, day) + 1
    weekday = 1  #DEBUG
    
    rtc.set_datetime((year, month, day, hour, min, sec, weekday))
    
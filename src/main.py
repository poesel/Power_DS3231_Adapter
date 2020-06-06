# -*- coding: utf-8 -*-
# License: GNU General Public License, Version 3
#

from machine import Pin, I2C, RTC
#import DS3231
import DS3231tokei
import max17043
import utime

i2c = None
ds = None
rtc = None

def main():

    global i2c
    global ds
    global rtc


    print('Start')
    #sclPin = Pin(i2cClockPin, pull = Pin.PULL_UP, mode = Pin.OPEN_DRAIN)
    #sdaPin = Pin(i2cDataPin, pull = Pin.PULL_UP, mode = Pin.OPEN_DRAIN)

    i2c = I2C(sda = Pin(21), scl=Pin(22))

    # LED an
    led = Pin(14,Pin.OUT)
    horn = Pin(26,Pin.OUT)
    led.value(1)
    horn.value(1)
    utime.sleep(1)
    led.value(0)
    horn.value(0)

    max = max17043.DFRobot_MAX17043(i2c)
    print('Voltage: ', max.readVoltage()/1000)
    ds = DS3231tokei.DS3231(i2c)
    interval = 600
    (year,month,day,dotw,hour,minute,second) = ds.getDateTime() # get the current time
    rtc = RTC() # create RTC
    if year < 2001:
        year = 2001 # sanity check, as of mpy 1.12 year must be >= 2001
    rtc.init((year,month,day,dotw,hour,minute,second,0)) # set time
    
    # Compute sleeping duration from measurement interval and elapsed time.
    now_secs = utime.mktime(utime.localtime())
    wake_at = now_secs + interval
    #if (wake_at - now_secs) < 180:  # don't shutoff for less than 3 minutes
    #    wake_at += interval
    print('Now:',now_secs, 'Wake at:', wake_at)

    (year,month,day,hour,minute,second, dotw, doty) = utime.localtime(wake_at) # convert the wake up time

    # set alarm
    ds.setAlarm2(day,hour,minute, DS3231tokei.A2_ON_HOUR_MINUTE)

    # turn off MCU via MOSFET
    print('Good night')
    utime.sleep(1)
    ds.enableAlarm2()
    ds.resetAlarm2()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()


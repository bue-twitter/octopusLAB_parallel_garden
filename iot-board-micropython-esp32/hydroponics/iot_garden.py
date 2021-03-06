"""
this module is to setup your board 
iotBoard for project parallel garden

ampy -p /COM6 put ./hydroponics/iot_garden.py hydroponics/iot_garden.py
from hydroponics.iot_garden import *
"""

import machine
from machine import Pin, ADC
import time, os, ubinascii
from util.pinout import set_pinout

pinout = set_pinout()

pwM = Pin(pinout.PWM1_PIN, Pin.OUT)     # moisture
pin_adcM = Pin(pinout.I35_PIN, Pin.IN)
adcM = machine.ADC(pin_adcM)

pin_adc = Pin(pinout.ANALOG_PIN, Pin.IN)
adc = machine.ADC(pin_adc)

pin_adcL = Pin(pinout.I34_PIN, Pin.IN)
adcL = machine.ADC(pin_adcL)

pin_adcT = Pin(pinout.I39_PIN, Pin.IN)
adcT = machine.ADC(pin_adcT)


pin_pwm = pinout.MFET_PIN # iot - default

 
def getGardenLibVer():
    return "garden lib.ver: 20.10.2019"

# ----------------
def pwm_init(pin=pinout.MFET_PIN, duty = 0):
     from machine import PWM
     # pwm_fet = PWM(pin_fet, 500, 0)
     pwm = PWM(Pin(pin, Pin.OUT), 500, duty)
     return pwm


def pwm_fet(pwm, duty, delay=10):
    pwm.duty(duty)
    time.sleep_ms(delay)


def pwm_fade_in(pwm, r, m = 5, fmax = 3000):
     # duty max - multipl us (2=2us) - fmax
     f = 100
     rs = 35

     pwm.freq(f)
     pwm.duty(1)
     time.sleep_ms(rs*2)

     pwm.duty(5)
     time.sleep_ms(rs)

     for i in range(5,rs):
          pwm.duty(i)
          pwm.freq(f)
          time.sleep_ms(m*(rs-i+1))
          f += int(fmax/rs) 

     pwm.freq(fmax)
     for i in range(rs, r):
          pwm.duty(i)
          time.sleep_ms(m)  


def getAd2RAW(ani): # A/D RAW
     an1 = ani.read()
     an2 = ani.read()
     an = int((an1+an2)/2)
     return an


def getADvolt(Debug): # AD > volts?
     an1 = adc.read()
     an2 = adc.read()
     an = int((an1+an2)/2)
     if Debug:
         print("> analog RAW: " + str(an))
         # TODO improve mapping formula, doc: https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html
         print("volts: {0:.2f} V".format(an/4096*10.74), 20, 50)
     return an

def getAdL(): # AD > light RAW
     an = getAd2RAW(adcL)
     #if Debug:
     #    print("> analog AD RAW Light: " + str(an))
     #TODO: calibration 2 lux?
     return an

def getAdT(): # AD > light RAW
     an = getAd2RAW(adcL)
     #TODO: calibration 2 Celsius?
     return an     

def get_moisture():
    pwM.value(1)
    time.sleep_ms(1000)
    s1 = adcM.read() #moisture sensor
    time.sleep_ms(1000)
    s2 = adcM.read()
    time.sleep_ms(1000)
    s3 = adcM.read()

    s = int((s1+s2+s3)/3)
    pwM.value(0)
    return(s)


def fade_in_sw(p, r, m):
     # pin - range - multipl
     for i in range(r):
          p.value(0)
          time.sleep_us((r-i)*m*2) # multH/L *2
          p.value(1)
          time.sleep_us(i*m)


def fade_out_sw(p, r, m):
     # pin - range - multipl
     for i in range(r):
          p.value(1)
          time.sleep_us((r-i)*m)
          p.value(0)
          time.sleep_us(i*m*2) 


def demo_run():
    fade_in(1024)
    # Demo intensity
    # delayF = 500
    # led_fet(128, delayF)
    # led_fet(1023, delayF)

    # demo Relay
    demo_relay(2,5000)

    led_fet(0, 1000)
    
    
  

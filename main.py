from machine import I2C
import utime
import sys
from lib.lidar import LIDAR
import machine
from machine import Pin
import random


def sens(W_l,St):   # it measures the Lidar distance and finds out if distance is changed or not
    '''
    Implementation of the sensor functionality.
    return:
         isChanged: True if Wl is changed, False if Wl is not changed
         W_l: the new value
    '''
    print ("garbage level  ", W_l)
    print("lidar distance  ", lidar.distance())
    W_l_prev=W_l
    print("previous value of garbage  ",W_l_prev)
    lidar.on_off(1)  #sleep lidar
    print("sensing period  ", St)
    utime.sleep_ms(St) #sleep lidar for 30 seconds
    lidar.on_off(0) #awake lidar
    W_l = bin_size-lidar.distance()
    print("current value of garbage  ",W_l)
    if W_l != W_l_prev:  #if the current value of garbage is not the same as the previous value
        isChanged = True
    elif W_l == W_l_prev:
        isChanged = False
    return W_l, isChanged


def send_notification(message):
    '''
    Implementation of the notification functionality.
    '''
    print(message)


def main(St, St_min, St_max, Th_min, Th_max, W_l):
    print ("Starting program.......")
    while True:
        utime.sleep_ms(2000)
        W_l = bin_size-lidar.distance()
        W_l, isChanged = sens(W_l,St)
        if isChanged == False:
            St *= 2
            print("sensing priod after doubling  ",St)
            if St >= St_max:
                St = St_min
            if W_l >= Th_max:
                if(Th_max>=10):
                  Th_max -= 10
                print("W_l is greater than Th_max and Th_max is greater than 10  ",Th_max)
                send_notification('where are you? come on and empty me!')
                utime.sleep_ms(50)
            elif W_l < Th_max:
                Th_max= 90
        elif isChanged == True and St >= St_min:  # if W_l is changed
            St = St_min
            print("ischanged is true and st is: ",St)
            if W_l >= Th_max:
                Th_max -= 10
                send_notification('where are you? come on and empty me! guy')
                utime.sleep_ms(50)
            elif W_l < Th_max:
                Th_max= 90
                print("W_l is less than Th_max and Th_max is: ",Th_max)


if __name__ == '__main__':
    # initialize variables
    ########################Lidar###############################################
    # TF-Luna has the default slave_address 0x10
    LIDAR_ADDRESS = 0x10
    i2c_0 = I2C(0, mode=I2C.MASTER, baudrate=400000, pins=('P7', 'P8'))
    utime.sleep_ms(50)
    slaves = i2c_0.scan()
    if LIDAR_ADDRESS not in slaves:
        print('Bus error: Please check LIDAR wiring')
        sys.exit()
    lidar = LIDAR(i2c_0, LIDAR_ADDRESS)
    print(lidar.version())
    # Output limit when out of range
    # Output only when between 20cm and 150cm (Up to 800cm)
    lidar.set_min_max(20, 150)
    lidar.set_frequency(250)
    #pin_out = Pin(‘P12’, mode=Pin.OUT)
    #pin_out.value(1)
    #on off LiDAR
    #lidar.on_off(0) #1 is off and zero is on
    #machine.sleep(10000) # SLEEP PYCOM FOR 10 SEC
    #lidar.on_off(1) #OFF LIDAR
    #lidar.on_off(0)
    #1 is off and zero is on
    #lidar.on_off(0)
    #machine.sleep(10000)
    #lidar.on_off(1)
    #machine.sleep(20000)
    #lidar.on_off(0)
    #machine.deepsleep(10000) for micro
    #pybytes.deepsleep(10000) for expansion board sleep
    #while True:
       #print(lidar.distance())
       #machine.sleep(10000) #10 seconds
       #lidar.distance()
    ########################Variables###########################################
    bin_size=200
    St = 30000
    St_min = 30000
    St_max = 3600000
    Th=90
    Th_min= 10
    Th_max=90
    W_l =0  #initial value of waste level
    device_status = True  # True means device(#Micro+Sensor) is on, False means device is off
    isChanged=True
    main(St, St_min, St_max, Th_min, Th_max, W_l)

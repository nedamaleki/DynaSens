#from machine import I2C
#import utime
import sys
#from lib.lidar import LIDAR
#import machine
#from machine import Pin
import random
import time
from datetime import datetime
#from turtle import st
#import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt


def lidar_distance(W_l):
    print ("######### We are inside lidar distance function #################")
    print("value of garbage  ",W_l)
    bin_size=100
    lidardistance = 0
    random_num=random.randint(0,1)
    if (W_l!=bin_size):
       if (random_num==1): # some one put garbage in bin
           W_l=random.randint(W_l+1, bin_size)
           print("current value of garbage changed ",W_l)
           lidardistance=bin_size-W_l
       elif (random_num ==0):
           print("current value of garbage not changed  ",W_l)
           lidardistance=bin_size-W_l
    print("Lidar Distance(random number) is  ",lidardistance)
    print ("######### lidar distance function ---- END #################")
    return W_l,lidardistance

def lidar_on_off(val,St):
    val=0 if True else 1
    if (val==1):
        time.sleep(St)

def time_seconds(start_time):
    dt = datetime.today()  
    start_time = dt.timestamp()
    return start_time
    
    # total_awake_time = new_seconds - seconds

def sens(W_l,St,lidardistance):   # it measures the Lidar distance and finds out if distance is changed or not
    '''
    Implementation of the sensor functionality.
    return:
         isChanged: True if Wl is changed, False if Wl is not changed
         W_l: the new value
    '''
    print ("######### We inside Sens function #################")


    print ("garbage level  ", W_l)
    print("lidar distance  ", lidardistance)
    W_l_prev=W_l
    # print("previous value of garbage  ",W_l_prev)
    # lidar.on_off(1)  #sleep lidar
    print("sensing period  ", St)
    # utime.sleep_ms(St) #sleep lidar for 30 seconds
    # lidar_on_off(1,St)
    # t_new = time.localtime()
    # new_current_time = time.strftime("%H:%M:%S", t_new) 
    # print("new_current time =", new_current_time)
    
    print("Make Lidar Sleep for ",St, " seconds.")
    sleeping_time = time.sleep(St)

    print("Make Lidar Awake")
    # print("current time in seconds", seconds)



    # lidar_on_off(0,0) # by default lidar is on so no need to set the St value
    # lidar.on_off(0) #awake lidar
    print("W_l after awaking lidar hooooooooooooooooooooooraaaaaaaaaaaaaaaaaaa ", W_l)
    W_l, lidardistance=lidar_distance(W_l) # W_l and lidar_distance are updated based on current W_l
    print("New value of garbage  ",W_l)
    if W_l != W_l_prev:  #if the current value of garbage is not the same as the previous value
        isChanged = True
        print("isChanged = True")
    elif W_l == W_l_prev:
        isChanged = False
        print("isChanged = False")

    print ("######### Sens function --- END #################")
    return W_l, isChanged

def send_notification(message):
    '''
    Implementation of the notification functionality.
    '''
    print(message)


def main(St, St_min, St_max, Th_min, Th_max, W_l):
    
    print ("Starting program at...")
    lidardistance = 100
    W_l = 0
    total_energy_consumption_dynasense= 0
    start_time = 0
    end_time = 0
    total_simulation_time = 0 
    idle_power=0.083
    active_power=0.153
    vcc=5
    
    while True:
        print ("######### this is the start of loop #################")
        start_time = time_seconds(start_time)
        print("start_time", start_time)

        # dt = datetime.today()  
        # start_time = dt.timestamp()
        # print("start_time", start_time)
        # utime.sleep_ms(2000)
        W_l, lidardistance=lidar_distance(W_l)
        W_l, isChanged = sens(W_l,St,lidardistance)
        sleeping_time = St
        # W_l = bin_size-lidardistance
        # print("we are in while loop WL and St", W_l, St)

        

        if isChanged == False:
            St *= 2
            print("sensing priod after doubling  ",St)
            if St >= St_max:
                St = St_min
            if W_l >= Th_max:
                if(Th_max>20):
                  Th_max -= 10
                print("W_l is greater than Th_max and Th_max is greater than 20  ",Th_max)
                send_notification('where are you? come on and empty me!')
                if ( lidardistance == 0):
                  if (random.randint(0, 1)==1): # guy come and empty bin after full
                     W_l=0
                     lidardistance=lidar_distance(W_l)
                     print("Nice GUY!")
                  elif (random.randint(0, 1)==0): # guy does not come
                     print("Bad GUY!")

            elif W_l < Th_max:
                Th_max= 90

            print("#######################################################")

        elif isChanged == True and St >= St_min:  # if W_l is changed
            St = St_min
            print("ischanged is true and st is: ",St)
            if W_l >= Th_max:
                Th_max -= 10
                send_notification('where are you? come on and empty me! guy')
            elif W_l < Th_max:
                Th_max= 90
                print("W_l is less than Th_max and Th_max is: ",Th_max)
            print("#######################################################")
        print ("######### This is the end of loop #################")
        
        end_time = time_seconds(end_time)

        
        # dt = datetime.today()  
        # end_time = dt.timestamp()
        # print ("Ending program at time...", dt)
        # print ("Ending Time in seconds is ", end_time)
        simulation_time = end_time - start_time
        total_simulation_time = total_simulation_time + simulation_time
        # print("total simulation time is ", simulation_time)
        awake_time = simulation_time - sleeping_time  
        # print("Total awake time was ", awake_time, "seconds")
        energy_consumption_sleep = vcc * idle_power * sleeping_time
        
        # print ("Energy consumption during sleep, ", energy_consumption_sleep)
        energy_consumption_awake = vcc * active_power * awake_time
        # print ("Energy consumption during awake, ", energy_consumption_awake)
        current_energy_consumption = energy_consumption_sleep + energy_consumption_awake
        print("current_energy_consumption ", current_energy_consumption)
        total_energy_consumption_dynasense = total_energy_consumption_dynasense + current_energy_consumption
        # print("Total Energy Consumption", total_energy_consumption_dynasense)
        # if total_simulation_time >= 100:  
        print("Total Energy Consumption", total_energy_consumption_dynasense, "after", total_simulation_time, "seconds" )

        plt.grid(True)
        plt.title('Energy Consumption of Lidar Sensor Vs Time', fontsize=10)
        plt.xlabel('Time', fontsize=10)
        plt.ylabel('Energy Consumption (J)', fontsize=10)
        plt.axis([25, total_simulation_time , 0, total_energy_consumption_dynasense])
        plt.plot(total_simulation_time, total_energy_consumption_dynasense, color='red', marker='o')
        plt.pause(0.05)   


if __name__ == '__main__':

    ##########################
    lidardistance=100  # lidar is on and its initial value would be equal to bin_size
    bin_size=100
    St = 30
    St_min = 30
    St_max = 86400    # one day 24x60x60
    Th=90
    Th_min= 10
    Th_max=90
    W_l =0            # initial value should be zero
    device_status = True  # True means device(#Micro+Sensor) is on, False means device is off
    isChanged=True
    main(St, St_min, St_max, Th_min, Th_max, W_l)
    # Lidar is on by default

# lidar on, micro on = 153 mA      
# lidar off, micro on = 81 mA   
# lidr off, micro sleep = 76.3 mA       


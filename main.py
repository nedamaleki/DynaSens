#from machine import I2C
#import utime
import sys
#from lib.lidar import LIDAR
#import machine
#from machine import Pin
import random
import time


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
    #print("previous value of garbage  ",W_l_prev)

    #lidar.on_off(1)  #sleep lidar
    print("sensing period  ", St)

    #utime.sleep_ms(St) #sleep lidar for 30 seconds
    #lidar_on_off(1,St)
    print("Make Lidar Sleep for ",St, " seconds.")
    # voltage is Volts, currents is in amps, and time is in seconds
    E = 0.083 * 5 * St 
    time.sleep(St)

    print("Make Lidar Awake")
    #lidar_on_off(0,0) # by default lidar is on so no need to set the St value
    #lidar.on_off(0) #awake lidar
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
    print ("Starting program.......")
    lidardistance = 100
    W_l = 0

    while True:
        print ("######### this is the start of loop #################")

        #utime.sleep_ms(2000)
        W_l, lidardistance=lidar_distance(W_l)
        W_l, isChanged = sens(W_l,St,lidardistance)
        #W_l = bin_size-lidardistance
        print("we are in while loop WL",W_l)

        ########

        if isChanged == False:
            St *= 2
            print("sensing priod after doubling  ",St)
            if St >= St_max:
                St = St_min
            if W_l >= Th_max:
                if(Th_max>Th_min):
                  Th_max -= 10
                print("W_l is greater than Th_max and Th_max is greater than 20  ",Th_max)
                send_notification('where are you? come on and empty me!')
                if ( lidardistance == 0):
                  if (random.randint(0, 1)==1): #guy come and empty bin after full
                     W_l=0
                     lidardistance=lidar_distance(W_l)
                     print("not FUCKING GUY!")
                  elif (random.randint(0, 1)==0): # guy does not come
                     print("FUCKING GUY!")

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

if __name__ == '__main__':

    ##########################
    lidardistance=100  #lidar is on and its initial value would be equal to bin_size
    bin_size=100
    St = 30
    St_min = 30
    St_max = 86400 #one day 24x60x60
    Th=90
    Th_min= 10
    Th_max=90
    W_l =0  #initial value should be zero
    device_status = True  # True means device(#Micro+Sensor) is on, False means device is off
    isChanged=True
    main(St, St_min, St_max, Th_min, Th_max, W_l)
    # Lidar is on by default

import socket
import time
import pyautogui

import select

pyautogui.FAILSAFE = True


bufferSize = 1024

ServerPort = 8080
ServerIP = '192.168.137.1'

print('Start')

mode = 0
next_time = time.time()
timeout = 0.01
interval = 0.00001
mouseDownTime = 0
mouseUpTime = 0
prev_x = 0
prev_y = 0

mouseIsDown = 0

try:
    while True:
        
        PCsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        PCsocket.bind((ServerIP, ServerPort))
        
        # ready = select.select([PCsocket], [], [], 0.001)

        # if ready[0]:
        # curr_time = time.time()

        # if curr_time >= next_time:
            


        message, address = PCsocket.recvfrom(bufferSize)
        message = message.decode('utf-8')
        data = message.split(',')
        touch_x, touch_y, mode = map(float, data)
        touch_x = int(touch_x)
        touch_y = int(touch_y)
        
        mode = int(mode)


        if mode == 1:
            prev_x = touch_x
            prev_y = touch_y
            mouseDownTime = time.time()

        elif mode == 2:
            x = (touch_x - prev_x) * 2
            y = -(touch_y - prev_y) * 2
            prev_x = touch_x
            prev_y = touch_y
            pyautogui.moveRel(x, y)


        elif mode == 3:
            mouseUpTime = time.time()

            if((mouseUpTime - mouseDownTime)*1000 < 200):
                pyautogui.click()
                print("Clicked")

            elif((mouseUpTime - mouseDownTime)*1000 > 200):
                pyautogui.mouseUp()
                mouseIsDown = False
                print("Mouse Up")
                    
        
    #else:
        if(time.time() - mouseDownTime) * 1000 > 200:
                if mode != 3:
                    if mouseIsDown == False:
                        pyautogui.mouseDown()
                        mouseIsDown = True
                        print("Mouse Down")    
                
                
                
                #next_time = curr_time + interval


except KeyboardInterrupt:
    print("CTRL + C detected. Exiting...")       
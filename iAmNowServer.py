import socket
import time
import pyautogui
import select

pyautogui.FAILSAFE = True


bufferSize = 1024

ServerPort = 8080
ServerIP = '192.168.137.1'

PCsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PCsocket.bind((ServerIP, ServerPort))
PCsocket.setblocking(0)

timeout = 0.01

print('Server is Up and Listening')



try:

    mouseIsDown = False
    clicked = False
    mouseDownTime = 0
    mouseUpTime = 0
    mode = 3

    while True:

        ready = select.select([PCsocket], [], [], timeout)

        if ready[0]:
            #start_time = time.perf_counter()
            message, address = PCsocket.recvfrom(bufferSize)
            message = message.decode('utf-8')
            data = message.split(',')
            x, y, mode = map(float, data)
            x = int(x)
            y = int(y)
            mode = int(mode)

            #print(f"x: {x}, y:{y}, mode: {mode}")
            # elapsed_time = (time.perf_counter() - start_time)*1000
            # while elapsed_time <= 100:
            #     elapsed_time = (time.perf_counter() - start_time)*1000


            if mode == 1:
                mouseDownTime = time.perf_counter()
                #print(mouseDownTime)

            if mode == 2:
                pyautogui.moveRel(x, y)

            if mode == 3:
                mouseUpTime = time.perf_counter()
                #print(mouseUpTime)
                if ((mouseUpTime - mouseDownTime)*1000 < 300) and ((mouseUpTime - mouseDownTime)*1000 > 0):
                    pyautogui.click()
                    print("Clicked")
                elif ((mouseUpTime - mouseDownTime)*1000 > 300):
                    pyautogui.mouseUp()
                    print("Mouse Up")
                    mouseIsDown = False
            
        else:
            if((time.perf_counter() - mouseDownTime)*1000 > 300):
            #print("Enter here?")
                if mode != 3:
                    if mouseIsDown == False:
                        pyautogui.mouseDown()
                        mouseIsDown = True
                        print("Mouse Down")

        
        # if time.time() - start_time > 0.0001:        
        #     if mode == 1:
        #         pyautogui.click()

        #     elif mode == 2:
        #         pyautogui.moveRel(x, y)

        #     elif mode == 3:
        #         if mouseIsDown == True:
        #             pyautogui.moveRel(x, y)
        #         elif mouseIsDown == False:
        #             time.sleep(0.3)
        #             pyautogui.mouseDown()
        #             mouseIsDown = True
        #             pyautogui.moveRel(x, y)
                
        #     elif mode == 4:
        #         pyautogui.doubleClick()

        #     elif mode == 5:
        #         pyautogui.mouseUp()
        #         mouseIsDown = False

        # else:
        #     pass

        # print(f"x: {x}, y:{y}, mode: {mode}")
        # print('Client Address', address)

except KeyboardInterrupt:
    print("CTRL + C detected. Exiting...")       
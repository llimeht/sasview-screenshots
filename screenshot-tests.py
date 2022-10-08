# -*- coding: utf-8 -*-
#!/usr/bin/env python

import logging
import os
#import threading
import subprocess
import time
from time import sleep

import pyautogui
pyautogui.FAILSAFE = True

#from sas.qtgui.MainWindow.MainWindow import run_sasview

logger = logging.getLogger('guitester')
logging.basicConfig(level=logging.INFO)

#run_sasview()

class LocationError(ValueError):
    pass

def waitfor(image, poll=0.1, timeout=10):
    loc = None
    stop = time.time() + timeout
    logger.info("Image search for %s", image)
    while loc is None:
        try:
            loc = pyautogui.locateCenterOnScreen(image)
            if loc:
                logger.info("Image located: %s", loc)
                return loc
            logger.debug("Image not located")
        except Exception as e:
            logger.debug("Image not located")
            pass
        if time.time() > stop:
            raise LocationError(f"Could not find {image}")
        sleep(poll)

def tester():

    try:
        screenWidth, screenHeight = pyautogui.size()
        logger.info("Viewport %d, %d", screenWidth, screenHeight)

        try:
            waitfor("prompts/splashscreen.png")
            pyautogui.screenshot('00-splash.png')
        except LocationError:
            logger.warning("Splash screen not detected")

        sleep(2.0)
        pyautogui.screenshot('00-mainwindow.png')

        sleep(1.0)
        logger.info("Open data file")
        pyautogui.hotkey('alt', 'f')
        pyautogui.press('enter')
        sleep(0.2)
        pyautogui.write('sphere_80.txt')
        pyautogui.press('enter')
        sleep(0.5)
        pyautogui.screenshot('01-data-loaded-1.png')

        loc = waitfor("prompts/data-explorer-send-data-to.png")
        pyautogui.click(*loc)
        sleep(1.0)
        pyautogui.screenshot('01-data-loaded-2.png')

        # select sphere model
        loc = waitfor("prompts/fitpanel-model-category.png")
        pyautogui.click(*loc)
        sleep(0.1)
        pyautogui.press('down', presses=8)
        pyautogui.press('enter')
        pyautogui.press(['tab', 's', 'enter'])
        pyautogui.click(*loc)
        pyautogui.click(*loc)
        # select parameters
        #pyautogui.hotkey('shift', 'tab')
        pyautogui.press(['tab', 'tab', 'tab', 'space'])   # scale
        pyautogui.press(['down', 'space'])   # bg
        pyautogui.press(['down', 'down', 'down', 'down', 'space'])   # bg
        #pyautogui.screenshot('01-data-loaded-2.png')

        sleep(10000)
    except LocationError as e:
        print("Location not found. Exiting")
        #os._exit(1)


    #currentMouseX, currentMouseY = pyautogui.position() # Returns two integers, the x and y of the mouse cursor's current position.
    #pyautogui.moveTo(100, 150) # Move the mouse to the x, y coordinates 100, 150.
    #pyautogui.click() # Click the mouse at its current location.
    #pyautogui.click(200, 220) # Click the mouse at the x, y coordinates 200, 220.
    #pyautogui.move(None, 10)  # Move mouse 10 pixels down, that is, move the mouse relative to its current position.
    #pyautogui.doubleClick() # Double click the mouse at the
    #pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad) # Use tweening/easing function to move mouse over 2 seconds.
    #pyautogui.write('Hello world!', interval=0.25)  # Type with quarter-second pause in between each key.
    #pyautogui.press('esc') # Simulate pressing the Escape key.
    #pyautogui.keyDown('shift')
    #pyautogui.write(['left', 'left', 'left', 'left', 'left', 'left'])
    #pyautogui.keyUp('shift')
    #pyautogui.hotkey('ctrl', 'c')

    #os._exit(0)


#t = threading.Thread(target=tester)
#t.start()


#run_sasview()

with subprocess.Popen("sasview") as proc:
    tester()
    proc.terminate()
    sleep(1)
    proc.kill()



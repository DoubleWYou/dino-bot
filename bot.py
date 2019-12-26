# Made with love on Christmas day, 2019

import pyautogui as auto
from time import sleep
from threading import Thread
from colorama import Fore

auto.PAUSE = 0
waiting = True

sleep_time = 0.03  # Raise/lower to change jump height
length = 2.5  # Change this to alter the distance dino jumps from
tolerance = 0.8  # Raise/lower this (0.01 - 0.99) to change tolerance


def timeInterval():
    global length, scan_region, sleep_time
    sleep(30)
    length += 0.65
    if sleep_time > 0.02:
        sleep_time -= 0.0025
    scan_region = ((dino[0] + (dino[2] - 3)), (dino[1] + 5), round(dino[2] * length), dino[3] - 11)
    print(Fore.MAGENTA + "[Increment L] ", length)
    print(Fore.MAGENTA + "[Increment H] ", sleep_time, "\n")
    if length > 5:
        return
    timeInterval()


def find_dino():
    auto.screenshot("screen.png")
    x = 0.99
    find = None
    while find is None and x > 0.6:
        find = auto.locate("dino_start.png", "screen.png", confidence=x, grayscale=True)
        x -= 0.1
    if find is None:
        find_dino()
    else:
        return find


dino = find_dino()
scan_region = ((dino[0] + round(dino[2] * length)), (dino[1] + 5), round(dino[2] / 1.5), dino[3] - 11)
obj = None
print(Fore.LIGHTBLUE_EX + "[L] ", length)
print(Fore.LIGHTBLUE_EX + "[H] ", sleep_time)
print(Fore.LIGHTBLUE_EX + "[Dino found, scanning for obstacles...]\n-------")

while True:
    while obj is None:
        obj = auto.locateOnScreen("object1.png", minSearchTime=0, region=scan_region, confidence=tolerance,
                                  grayscale=True)
        if obj is None:
            obj = auto.locateOnScreen("object2.png", minSearchTime=0, region=scan_region, confidence=tolerance,
                                      grayscale=True)
        else:
            break

    auto.keyDown("up")
    sleep(sleep_time)
    auto.keyUp("up")
    obj = None
    if waiting:
        waiting = False
        Thread(target=timeInterval).start()
        print(Fore.MAGENTA + "[First obstacle found, thread started]\n")

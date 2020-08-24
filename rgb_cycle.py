from utils import img_avg
from pywizlight import wizlight, PilotBuilder
import asyncio
import numpy as np
import pyautogui
import time
from PIL import Image, ImageGrab
import cProfile
import mss

LOW_THRESHOLD = 10
MID_THRESHOLD = 40
HIGH_THRESHOLD = 240

loop = asyncio.get_event_loop()

light = wizlight("192.168.0.4")

def party_cycle(light):
    while True:
        for i in range(0, 256):
            for j in range(0, 256):
                for k in range(0, 256):
                    if i == 0 and j == 0:
                        asyncio.run(light.turn_on(PilotBuilder(rgb=(i, j, k))))

party_cycle(light)
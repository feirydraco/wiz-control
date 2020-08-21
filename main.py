'''
1: Ocean
2: Romance
3: Sunset
4: Party
5: Fireplace
6: Cozy
7: Forest
8: Pastel Colors
9: Wake up
10: Bedtime
11: Warm White
12: Daylight
13: Cool white
14: Night light
15: Focus
16: Relax
17: True colors
18: TV time
19: Plantgrowth
20: Spring
21: Summer
22: Fall
23: Deepdive
24: Jungle
25: Mojito
26: Club
27: Christmas
28: Halloween
29: Candlelight
30: Golden white
31: Pulse
32: Steampunk
'''
from utils import img_avg
from pywizlight import wizlight, PilotBuilder
import asyncio
import time
import cv2
import numpy as np
from mss import mss
import pyautogui
import matplotlib.pyplot as plt
from PIL import Image, ImageGrab


loop = asyncio.get_event_loop()

light = wizlight("192.168.0.7")

while True:
    image = np.array(ImageGrab.grab())
    image = Image.fromarray(image)
    data = img_avg(image)
    dominant_color = np.argmax(data['rgb'])
    print(dominant_color)

    data['rgb'] = list(int(x) for x in data['rgb'])
    print(data)
    asyncio.run(light.turn_on(PilotBuilder(
        rgb=(data['rgb'][0], data['rgb'][1], data['rgb'][2]))))

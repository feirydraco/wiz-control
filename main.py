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

def main(): 
    with mss.mss() as sct:
        # Get rid of the first, as it represents the "All in One" monitor:
        for num, monitor in enumerate(sct.monitors[1:], 1):
            # Get raw pixels from the screen
            sct_img = sct.grab(monitor)

            # Create the Image
            image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            # The same, but less efficient:
            # img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)



            # image = Image.fromarray(image)
            #data = img_avg(image) #cProfile.run('img_avg(image)')
            #data = img_avg(image) 
                
            dark_pixels = 1
            mid_range_pixels = 1
            total_pixels = 1
            r = 1
            g = 1
            b = 1

            # Create list of pixels
            pixels = list(image.getdata())[::100]


            for red, green, blue in pixels:
                # Don't count pixels that are too dark
                if red < LOW_THRESHOLD and green < LOW_THRESHOLD and blue < LOW_THRESHOLD:
                    dark_pixels += 1
                # Or too light
                elif red > HIGH_THRESHOLD and green > HIGH_THRESHOLD and blue > HIGH_THRESHOLD:
                    pass
                else:
                    if red < MID_THRESHOLD and green < MID_THRESHOLD and blue < MID_THRESHOLD:
                        mid_range_pixels += 1
                        dark_pixels += 1
                    r += red
                    g += green
                    b += blue
                total_pixels += 1

            n = len(pixels)
            r_avg = r / n
            g_avg = g / n
            b_avg = b / n
            rgb = [r_avg, g_avg, b_avg]

            # If computed average below darkness threshold, set to the threshold
            for index, item in enumerate(rgb):
                if item <= LOW_THRESHOLD:
                    rgb[index] = LOW_THRESHOLD

            rgb = (rgb[0], rgb[1], rgb[2])

            data = {
                'rgb': rgb,
                'dark_ratio': float(dark_pixels) / float(total_pixels) * 100
            }
            
        
            # data['rgb'] = list(int(x) for x in data['rgb'])
            print(data)
            try:
                asyncio.run(light.turn_on(PilotBuilder(
                    rgb=(data['rgb'][0], data['rgb'][1], data['rgb'][2]))))
            except:
                pass
while True:
    # cProfile.run('main()')
    main()


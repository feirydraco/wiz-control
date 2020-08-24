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
import random

LOW_THRESHOLD = 20
MID_THRESHOLD = 40
HIGH_THRESHOLD = 250

loop = asyncio.get_event_loop()

light = wizlight("192.168.0.4")

def main(): 
    with mss.mss() as sct:
        # Get rid of the first, as it represents the "All in One" monitor:
        for num, monitor in enumerate(sct.monitors[1:], 1):
            # Get raw pixels from the screen
            sct_img = sct.grab(monitor)
            # image = np.array(sct_img)
            # Create the Image
            image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            # no. of pixels in image
            npixels = image.size[0]*image.size[1]
            # get colors as [(cnt1, (r1, g1, b1)), ...]

            cols = image.getcolors(npixels)
            # cols = [list(x) for x in image.getcolors(npixels)]
            # colorsOnly = list(map(lambda x: x[1], cols))
           
            # # get [(c1*r1, c1*g1, c1*g2),...]
            # for i in range(len(cols)):
            #     cols[i][1] = [cols[i][1][j] // 10 * 10 for j in range(3)]
            # #     pass


            # # for col in cols:
            # #     col[1] = [[x//10*10, y//10*10, z//10*10] for x,y,z in col[1]]

            colsShort = sorted(cols)[-10:]
            # print(colsShort)
            colsShortShort = []
            for x in colsShort:
                if x[1][0] < LOW_THRESHOLD and x[1][1] < LOW_THRESHOLD and x[1][2] < LOW_THRESHOLD:
                    pass
                elif x[1][0] > HIGH_THRESHOLD and x[1][1]  > HIGH_THRESHOLD and x[1][2] > HIGH_THRESHOLD:
                    pass
                else:
                    colsShortShort.append(x)
            print(colsShortShort)
            # randomColor = random.choice(colsShortShort)
            
            try: 
                modeColor = colsShortShort[-1][1]
            except:
                continue
            # sumRGB = [(x[0]*x[1][0], x[0]*x[1][1], x[0]*x[1][2]) for x in cols]
            # # # calculate (sum(ci*ri)/np, sum(ci*gi)/np, sum(ci*bi)/np)
            # # # the zip gives us [(c1*r1, c2*r2, ..), (c1*g1, c1*g2,...)...]
            # avg = tuple([sum(x)//npixels for x in zip(*sumRGB)])

            data = {
                'rgb': modeColor
            }
            print(data)

            try:
                asyncio.run(light.turn_on(PilotBuilder(
                    rgb=(data['rgb'][0], data['rgb'][1], data['rgb'][2]), brightness = 150)))
            except:
                pass
while True:
    # cProfile.run('main()')
    main()


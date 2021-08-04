
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import pytesseract
import numpy as np
import requests
from requests.api import request
import os
import shutil
import time

key = '324ddd0c-2350-435d-9610-eb4fd6f1ec9d'
path = '/Users/shrayswarup/Library/Application Support/minecraft/screenshots/'

class Player:
    def __init__(self, name):
        self.name = name
    def getUUID(self):
        out = str(requests.get("https://api.mojang.com/users/profiles/minecraft/" + self.name).content)
        if len(str(out)) == 3:
            return '0'
        else:
            return out[out.find("id\":") + 5:out.find("\"", out.find("id\":") + 5)]
        
    def getFKDR(self):
        uuid = self.getUUID()
        if uuid == '0':
            return "\t"
        pData = requests.get('https://api.hypixel.net/player?uuid=' + uuid + '&key=' + key).json()
        if pData['success'] and pData["player"] and pData["player"]["stats"] and pData["player"]["stats"]["Bedwars"]:
            deaths = int(pData["player"]["stats"]["Bedwars"]["final_deaths_bedwars"])
            kills = int(pData["player"]["stats"]["Bedwars"]["final_kills_bedwars"])
            # fours specific stat - four_four_final_deaths_bedwars
            return round(kills/deaths, 2)
        else:
            return "\t"
    def toString(self):
        numTabs = 4
        if len(self.name) > 9:
            numTabs = 3
        if len(self.name) > 17:
            numTabs = 2
        tabs = '\t' * numTabs
        return 'NAME: ' + self.name + tabs + 'FKDR: ' + str(self.getFKDR()) + '\t\tUUID: ' + self.getUUID()

def calculate():
    # TRANSFORM IMAGE

    img_cv = img[59:490,832:1080]   # Crop to Tab Menu 1/3:832 4:815  1:9/16, 3: 6/16, 4: 9/16
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
    alpha = 3       # Contrast Multiplier
    beta = -200     # Brightness Addition
    final = cv2.addWeighted(img_rgb, alpha, np.zeros(img_rgb.shape, img_rgb.dtype), 0, beta)

    # DISPLAY IMAGE - STOPS PROGRAM

    cv2.imshow('Image', final)
    cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # MANIPULATE STRINGS

    print('RAW ===========================================')
    print(pytesseract.image_to_string(final))
    print('POST ==========================================')

    players = [Player(y) for y in (x.strip() for x in pytesseract.image_to_string(final).splitlines()) if y]
    for x in range(len(players)):
        players[x].name = players[x].name.replace('@','0')    # 0 @ confusion fix
        players[x].name = players[x].name.translate({ord(c): None for c in ' .©?()[]!-—=+'})    # Remove blacklisted chars
        if players[x].name.startswith('0'):
            players[x].name = players[x].name[1:]
        print(players[x].name)

    # Print Data

    print()
    for x in range(len(players)):
        print(players[x].toString())

    shutil.move(path + f, path + "UsedDodger/")


# PULL IMAGE
#img = cv2.imread('img1.png')

while 'true':
    files = os.listdir(path)
    if len(files) > 3:
        time.sleep(1)
        for f in files:
            #print(f)
            if f[0] == '2':
                #print('starts with 2')
                img = cv2.imread(os.path.expanduser(path + f))
                calculate()
                #shutil.move(path + f, path + "UsedDodger/")

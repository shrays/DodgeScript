
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
import statistics

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
        try:
        #if pData['success'] and pData["player"] and pData["player"]["stats"] and pData["player"]["stats"]["Bedwars"]:
            deaths = int(pData["player"]["stats"]["Bedwars"]["final_deaths_bedwars"])
            kills = int(pData["player"]["stats"]["Bedwars"]["final_kills_bedwars"])
            # fours specific stat - four_four_final_deaths_bedwars
            return round(kills/deaths, 2)
        except:
            return "\t"
    def toString(self):
        numTabs = 4
        if len(self.name) > 9:
            numTabs = 3
        if len(self.name) > 17:
            numTabs = 2
        tabs = '\t' * numTabs
        return 'NAME: ' + self.name + tabs + 'FKDR: ' + str(self.getFKDR()) + '\t\tUUID: ' + self.getUUID()
def imageCrop(img):
    # CONVERT TO GRAYSCALE, ADD CONTRAST
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
    con1 = 20       # Contrast Multiplier
    bright1 = -1000     # Brightness Addition
    final = cv2.addWeighted(img_rgb, con1, np.zeros(img_rgb.shape, img_rgb.dtype), 0, bright1)

    # 2D LIST, PIXEL COLORS
    print(type(int(final[65,1135])))
    color = []
    for i in range(355):
        temp = []
        for j in range(5):
            temp.append(int(final[60 + 5*j, 1135-i]))
        color.append(temp)

    # MEAN OF COLUMNS OF 355 ROWS
    #print(color)
    value = []
    for row in color:
        value.append(statistics.mean(row))
    #print(value)

    # FIND CONTRAST DIFFERENCE
    for i in range(len(value) - 1, 0, -1):
        if value[i] + 100 < value[i-1]:
            crop = i + 783
            break
    #print(crop)

    crop = img[59:490,960 - (crop - 960) + 24:crop - 33]   # Crop to Tab Menu 
    return crop

def imageRead(crop):
    # TRANSFORM IMAGE

    #img_cv = img[59:490,832:1080]   # Crop to Tab Menu 1/3:832 4:815  1:9/16, 3: 6/16, 4: 9/16
    img_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
    alpha = 3       # Contrast Multiplier
    beta = -200     # Brightness Addition
    final = cv2.addWeighted(img_rgb, alpha, np.zeros(img_rgb.shape, img_rgb.dtype), 0, beta)

    # DISPLAY IMAGE - STOPS PROGRAM

    #cv2.imshow('Image', final)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return final

def text(final):
    # MANIPULATE STRINGS

    #print('RAW ===========================================')
    #print(pytesseract.image_to_string(final))
    #print('POST ==========================================')

    players = [Player(y) for y in (x.strip() for x in pytesseract.image_to_string(final).splitlines()) if y]
    for x in range(len(players)):
        players[x].name = players[x].name.replace('@','0')    # 0 @ confusion fix
        players[x].name = players[x].name.translate({ord(c): None for c in ' .©?()[]!-—=+'})    # Remove blacklisted chars
        if players[x].name.startswith('0'):
            players[x].name = players[x].name[1:]
        #print(players[x].name)

    # Print Data

    for x in range(len(players)):
        print(players[x].toString())

    shutil.move(path + f, path + "UsedDodger/")

# PULL IMAGE
#img = cv2.imread('img1.png')

while True:
    files = os.listdir(path)
    if len(files) > 3:
        time.sleep(1) # Lets image load into 
        for f in files:
            #print(f)
            if f[0] == '2':
                #print('starts with 2')
                img = cv2.imread(os.path.expanduser(path + f))
                text(imageRead(imageCrop(img)))
                #shutil.move(path + f, path + "UsedDodger/")


# PIXEL CROPPING

# 1920 x 1080
# Half X = 960

# RIGHT MOST LIGHT TO DARK TRANSITION
# X = 1055 1130
# LEFT MOST (IN LIGHT)
# X =  868  789

# Y = 59/60 - 488/499
# Head Width - 24 pixels
# Wifi Width - 33 pixels

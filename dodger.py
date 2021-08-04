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
import sys
import shutil
import time
import statistics


test_img = os.getcwd() + os.sep + "sampleImages"

key = ''
if "HYPIXEL_API_KEY" not in os.environ:
    raise OSError("Environment variable \"HYPIXEL_API_KEY\" is not defined; please define it")
else:
    key = os.environ["HYPIXEL_API_KEY"]

path = ""
if os.name == "posix": # unix
    if sys.platform.startswith("darwin"):
        path = os.path.join(os.environ["HOME"] + "/Library/Application Support/minecraft/screenshots/")
    elif sys.platform.startswith('linux'):
        path = os.path.join(os.environ["HOME"] + "/.minecraft/screenshots")
elif os.name == "nt": # windows
    path = os.path.join(os.environ["APPDATA"] + "\\.minecraft\\screenshots")

if path == "":
    raise OSError("Operating system not supported")


class Player:

    def __init__(self, name):
        self.name = name

    def getUUID(self): # Read username to UUID via Mojang
        out = str(requests.get("https://api.mojang.com/users/profiles/minecraft/" + self.name).content)
        if len(str(out)) == 3: # 3 character - invalid user, empty string
            return '0'
        else:
            return out[out.find("id\":") + 5:out.find("\"", out.find("id\":") + 5)]
        
    def getFKDR(self): # UUID to stats via Hypixel API
        uuid = self.getUUID()
        if uuid == '0':
            return "\t"

        pData = requests.get('https://api.hypixel.net/player?uuid=' + uuid + '&key=' + key).json()

        try:
            deaths = int(pData["player"]["stats"]["Bedwars"]["final_deaths_bedwars"])
            kills = int(pData["player"]["stats"]["Bedwars"]["final_kills_bedwars"])

            # fours specific stat - four_four_final_deaths_bedwars
            return round(kills/deaths, 2)

        except:
            return "\t"

    def toString(self): # Prints player and stats
        numTabs = 4
        if len(self.name) > 9:
            numTabs = 3
        if len(self.name) > 17:
            numTabs = 2
        tabs = '\t' * numTabs
        return 'NAME: ' + self.name + tabs + 'FKDR: ' + str(self.getFKDR()) + '\t\tUUID: ' + self.getUUID()

def imageCrop(img): # Detects width of tab list and crops
    # PIXEL CROPPING


    # Screen Resolution - 1920 x 1080
    # Head logo Width - 24 pixels
    # Wifi logo Width - 33 pixels
    # Brightness check within bounds of smallest X: 785 and largest X: 1135


    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
    con1 = 20           # Contrast Multiplier
    bright1 = -1000     # Brightness Addition
    final = cv2.addWeighted(img_rgb, con1, np.zeros(img_rgb.shape, img_rgb.dtype), 0, bright1) # Add contrast/brightness

    # DISPLAY IMAGE - STOPS PROGRAM
    #cv2.imshow('Image', final)
    #cv2.waitKey(0)
    
    # 2D LIST, PIXEL COLORS
    color = []
    for i in range(355):
        temp = []
        for j in range(5):
            temp.append(int(final[60 + 5*j, 1135-i]))
        color.append(temp)

    # MEAN OF COLUMNS OF 355 ROWS
    value = []
    for row in color:
        value.append(statistics.mean(row))

    # FIND CONTRAST DIFFERENCE
    for i in range(len(value) - 1, 0, -1):
        if value[i] + 100 < value[i-1]:
            crop = i + 783
            break

    crop = img[59:490,960 - (crop - 960) + 24:crop - 33]   # Crop to Tab Menu 
    return crop

def imageRead(crop):    # Image to text
    img_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
    alpha = 3       # Contrast Multiplier
    beta = -200     # Brightness Addition
    final = cv2.addWeighted(img_rgb, alpha, np.zeros(img_rgb.shape, img_rgb.dtype), 0, beta)

    # DISPLAY IMAGE - STOPS PROGRAM
    #cv2.imshow('Image', final)
    #cv2.waitKey(0)

    return final

def text(final): # Cleans and sorts text
    #print('RAW ===========================================')
    #print(pytesseract.image_to_string(final))
    #print('POST ==========================================')

    players = [Player(y) for y in (x.strip() for x in pytesseract.image_to_string(final).splitlines()) if y]
    for x in range(len(players)):
        players[x].name = players[x].name.replace('@','0')     #@ to 0 confusion fix
        players[x].name = players[x].name.translate({ord(c): None for c in ' .©?()[]!-—=+'})    # Remove blacklisted chars
        if players[x].name.startswith('0'): # Lunar client symbol fix
            players[x].name = players[x].name[1:]

    # Print Data
    for x in range(len(players)):
        print(players[x].toString())
    print('\n\n')

while True: # Always Runs
    if len(sys.argv) >= 2 and sys.argv[1] == "--test":
        files = os.listdir(test_img)
        path = test_img + os.sep
    else:
        files = os.listdir(path) # Checks screenshots folders (.DS(mac), UsedDodger Folder, and Regular SS )
    if len(files) > 3:
        time.sleep(1) # Lets image load into 
        for f in files:
            if f[0] == '2':
                print(path + f)
                img = cv2.imread(os.path.expanduser(path + f))
                text(imageRead(imageCrop(img)))
                shutil.move(path + f, path + "UsedDodger/") # Moves image away from SS folder (UsedDodger file in SS)



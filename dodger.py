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
import yaml


test_img = os.getcwd() + os.sep + "sampleImages"

key = ''
with open('config.yml', 'r') as config_file:
    data = yaml.safe_load(config_file)
    if "hypixel_api_key" not in data or data["hypixel_api_key"] == "12345678-9abc-def0-1234-56789abcdef0":
        raise KeyError("Hypixel API Key is not defined. Obtain a key from hypixel by running /api in the server and put it in config.yml")
    else:
        key = data["hypixel_api_key"]
    if "gui_scale" not in data or (data["gui_scale"] != "normal" and data["gui_scale"] != "large"):
        raise KeyError("Invalid GUI scale setting. Set gui_scale to 'normal' or 'large in config.yml")
    else:
        scale = data["gui_scale"]


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

def displayImage(img):  # Stops program when run
    cv2.imshow('Image', img)
    cv2.waitKey(0)

def saveImage(img, name):
    cv2.imwrite(path + "UsedDodger/" + name + '.png', img)

def imageCrop(img): # Detects width of tab list and crops
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
    con1 = 20           # Contrast Multiplier
    bright1 = -1000     # Brightness Addition
    final = cv2.addWeighted(img_rgb, con1, np.zeros(img_rgb.shape, img_rgb.dtype), 0, bright1) # Add contrast/brightness
    #displayImage(final)
    #saveImage(final, 'DetectCrop')

    Xmid = int(final.shape[1] / 2) # Pixel length of half of X
    if scale == 'normal':
        Ytop = 39
        Ybottom = 326
        Yinc = 2
        headWidth = 16
        wifiWidth = 22
    elif scale == 'large':
        Ytop = 59
        Ybottom = 489
        Yinc = 5
        headWidth = 24
        wifiWidth = 33

    # 2D LIST, PIXEL COLORS
    color = []
    for i in range(355):
        temp = []
        for j in range(5):
            temp.append(int(final[Ytop + 1 + Yinc*j, Xmid + 175-i])) # 175 constant, 960 + 175 = 1135
        color.append(temp)
    # MEAN OF COLUMNS OF 355 ROWS
    value = []
    for row in color:
        value.append(statistics.mean(row))
    # FIND CONTRAST DIFFERENCE
    for i in range(len(value) - 1, 0, -1):
        if value[i] + 100 < value[i-1]:
            crop = i + 175 + Xmid - 352
            break

    # CROP TO TAB MENU
    crop = img[Ytop:Ybottom,Xmid - (crop - Xmid) + headWidth:crop - wifiWidth]
    #saveImage(crop, 'Cropped')
    return crop

def imageRead(crop):    # Image to text
    img_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
    alpha = 3       # Contrast Multiplier
    beta = -200     # Brightness Addition
    final = cv2.addWeighted(img_rgb, alpha, np.zeros(img_rgb.shape, img_rgb.dtype), 0, beta)
    #displayImage(final)
    #saveImage(final, 'Text')
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
        #print(players[x].name)

    # Print Data
    for x in range(len(players)):
        print(players[x].toString())
    print('\n')

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
                img = cv2.imread(os.path.expanduser(path + f))
                text(imageRead(imageCrop(img)))
                shutil.move(path + f, path + "UsedDodger/") # Moves image away from SS folder (UsedDodger file in SS)



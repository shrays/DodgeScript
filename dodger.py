
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import pytesseract
import numpy as np
import requests
from requests.api import request

key = '324ddd0c-2350-435d-9610-eb4fd6f1ec9d'

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
        #print(pData['success'])
        if pData['success'] and pData["player"] and pData["player"]["stats"] and pData["player"]["stats"]["Bedwars"]:
            deaths = int(pData["player"]["stats"]["Bedwars"]["final_deaths_bedwars"])
            kills = int(pData["player"]["stats"]["Bedwars"]["final_kills_bedwars"])
            # fours specific stat - four_four_final_deaths_bedwars
            return round(kills/deaths, 2)
        else:
            return -1
    def toString(self):
        # numTabs = 6 - (len(self.name) - 6) // 8
        numTabs = 4
        if len(self.name) > 9:
            numTabs = 3
        if len(self.name) > 17:
            numTabs = 2
        #numTabs = 6 
        tabs = '\t' * numTabs
        return 'NAME: ' + self.name + tabs + 'FKDR: ' + str(self.getFKDR()) + '\t\tUUID: ' + self.getUUID()

# PULL IMAGE

img = cv2.imread('img1.png')

# TRANSFORM IMAGE

img_cv = img[59:490,832:1080]   # Crop to Tab Menu 1/3:832 4:815  1:9/16, 3: 6/16, 4: 9/16
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
alpha = 3       # Contrast Multiplier
beta = -200     # Brightness Addition
final = cv2.addWeighted(img_rgb, alpha, np.zeros(img_rgb.shape, img_rgb.dtype), 0, beta)

# MANIPULATE STRINGS

#print(pytesseract.image_to_string(final))
players = [Player(y) for y in (x.strip() for x in pytesseract.image_to_string(final).splitlines()) if y]
for x in range(len(players)):
    players[x].name = players[x].name.replace('@','0')    # 0 @ confusion fix
    players[x].name = players[x].name.translate({ord(c): None for c in ' ©?()[]!-—=+'})    # Remove blacklisted chars
    print(players[x].name)

print()
for x in range(len(players)):
    print(players[x].toString())


# DISPLAY IMAGE

#cv2.imshow('Image', final)
#cv2.waitKey(0)



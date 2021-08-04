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

# CONVERT TO GRAYSCALE, ADD CONTRAST
img_cv = cv2.imread('img2.png')
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
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

print(crop)
img_cv = img_cv[59:490,960 - (crop - 960) + 24:crop - 33]   # Crop to Tab Menu 1/3:832 4:815  1:9/16, 3: 6/16, 4: 9/16

cv2.imshow('Image', img_cv)
cv2.waitKey(20000)
cv2.destroyAllWindows()

        
# Y = 59/60 - 488/499
# Head Width - 24 pixels
# Wifi Width - 33 pixels



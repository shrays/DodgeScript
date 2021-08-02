
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import pytesseract
import numpy as np

img = cv2.imread('img1.png')

# TRANSFORM IMAGE

img_cv = img[59:490,832:1080]   # Crop to Tab Menu
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)  # Convert to Grayscale
alpha = 3       # Contrast Multiplier
beta = -200     # Brightness Addition
final = cv2.addWeighted(img_rgb, alpha, np.zeros(img_rgb.shape, img_rgb.dtype), 0, beta)

# MANIPULATE STRINGS

print(pytesseract.image_to_string(final))
names = [y for y in (x.strip() for x in pytesseract.image_to_string(final).splitlines()) if y]
for x in range(len(names)):
    if names[x] == '0':
        print('test')
print(names)
#Remove spaces, anything with illegal characters, and copyright symbol

# DISPLAY IMAGE

cv2.imshow('Image', final)
cv2.waitKey(0)



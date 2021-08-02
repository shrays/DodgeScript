
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import pytesseract

print('test')

img = cv2.imread('img1.png')
print(img.shape)                    # Full Screen: 1080 1920
img_cv = img[59:490,832:1080]   # Tab Menu: X: 

# Display Image
#cv2.imshow('Image', img_cv)
#cv2.waitKey(0)

img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
print(pytesseract.image_to_string(img_rgb))

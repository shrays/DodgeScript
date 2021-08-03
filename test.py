
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import os


img = cv2.imread(os.path.expanduser('~/Library/Application Support/minecraft/screenshots/test.png'))

cv2.imshow('Image', img)
cv2.waitKey(10000)
cv2.destroyAllWindows()

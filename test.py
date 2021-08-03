
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import os
import glob
import os.path

folder_path = r'~/Library/Application Support/minecraft/screenshots/'
file_type = '\*png'
files = glob.glob(folder_path + file_type)
max_file = max(files, key=os.path.getctime)

print (max_file)

img = cv2.imread(os.path.expanduser('~/Library/Application Support/minecraft/screenshots/test.png'))

cv2.imshow('Image', img)
cv2.waitKey(10000)
cv2.destroyAllWindows()

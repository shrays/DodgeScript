
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import os
import shutil
import time

path = '/Users/shrayswarup/Library/Application Support/minecraft/screenshots/'

def calculate():
    img_cv = img[59:490,832:1080] 
    shutil.move(path + f, path + "UsedDodger/")


while 'true':
    files = os.listdir(path)
    if len(files) > 3:
        time.sleep(1)
        for f in files:
            print('CHECKING')
            print(f)
            if f[0] == '2':
                print('starts with 2')

                img = cv2.imread(os.path.expanduser(path + f))
                calculate()
                #cv2.imshow('Image', img)
                #cv2.waitKey(1000)
                #cv2.destroyAllWindows()



        




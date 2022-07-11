# imports
import cv2
import os


size = 120
WHITE = [255,255,255]
folders = ["A","B","C"]
for f in folders:
    files_dir = f"C:\\Users\\10\\Desktop\\test2\\{f}\\"
    files = os.listdir(files_dir)
    for i in files:
        img = cv2.imread(files_dir+i)
        x = img.shape[1]
        y = img.shape[0]


        top = int((size - y)/2)
        bottom = top

        if top < 0:
            top = 0
            bottom = top

        left = int((size - x)/2)
        right = left

        if left < 0:
            left = 0
            right = left

        padded = cv2.copyMakeBorder(img,top,bottom,left,right,cv2.BORDER_CONSTANT,value=WHITE)

        cv2.imwrite(f"C:\\Users\\10\\Desktop\\Dataset padded\\test\\{f}\\padded{i}.jpg",padded)
        print(f"{i} padded created")

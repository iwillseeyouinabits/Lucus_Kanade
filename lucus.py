import numpy as np
from PIL import Image
import cv2
import time

def imageToArr(imgPath):
    imgArrTemp = np.array(Image.open(imgPath))
    imgArr = np.array([[0]*len(imgArrTemp[0])]*len(imgArrTemp))
    for i in range(len(imgArrTemp)):
        for j in range(len(imgArrTemp[0])):
            imgArr[i][j] = sum(imgArrTemp[i][j])/3
    return imgArr

def getWs(imgPath, wlen):
    img = cv2.imread(imgPath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 20, 0.01, 10)
    corners = np.int0(corners)
    output = []
    img = imageToArr(imgPath)
    print(img)
    for corner in corners:
        y,x = corner.ravel()
        w = [ [0]*wlen for i in range(wlen)]
        for i in range(wlen):
            for j in range(wlen):
                w[i][j] = img[x + i - wlen//2][y + j - wlen//2]
        output.append((x,y,w))
    return output

def lucus(imgPath1, imgPath2, wlen):
    ws = getWs(imgPath1, wlen)
    img2 = imageToArr(imgPath2)
    output = []
    for w in ws:
        print(w)
        for x in range(len(img2) - wlen):
            for y in range(len(img2[0]) - wlen):
                wcount = 0
                for i in range(wlen):
                    for j in range(wlen):
                        if w[2][i][j] == img2[x+i][y+j]:
                            wcount += 1
                if wcount/(wlen*wlen) >= 0.4:
                    print((w[0], w[1], x-w[0], y-w[1]))
                    output.append((w[0], w[1], x-w[0], y-w[1]))
    return output

def main():
    lucus("img1.png", "img1.png", 5)

if __name__ == '__main__':
    main()


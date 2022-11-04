import pickle
import cv2 as cv2
#import cvzone
#import numpy as np


widht, height = 105, 45
try:
    with open('../park_control/parking_space_coordinates.bin', 'rb') as f:
        coordinates = pickle.load(f)
except:
    coordinates=[]

def mouse_click(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        coordinates.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, coordinate in enumerate(coordinates):
            _x, _y = coordinate
            if _x < x < _x + widht and _y < y < _y + height:
                coordinates.pop(i)

def main():
    while True:
        image = cv2.imread('../park_control/carParkImg.png')

        for coordinate in coordinates:
            cv2.rectangle(image,
                          coordinate,
                          (coordinate[0] + widht, coordinate[1] + height),
                          (255, 0, 255),
                          2)

        cv2.imshow('Parking-Space-Picker', image)
        cv2.setMouseCallback('Parking-Space-Picker', mouse_click)
        if cv2.waitKey(1) &  0xff == 27:
            break

if __name__ == '__main__':
    main()
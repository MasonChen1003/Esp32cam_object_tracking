import time
import cv2
import numpy as np
import math
import serial
from urllib.request import urlopen

import os
import datetime
import sys

url = 'http://192.168.4.1'
CAMERA_NAME = 'mason'
CAMERA_BUFFER_SIZE = 1536
stream = urlopen(url)
bbb = b''
    
while True:
   bbb += stream.read(CAMERA_BUFFER_SIZE)
   # Find the beginning / end of an JPG file 
   a = bbb.find(b'\xff\xd8')
   b = bbb.find(b'\xff\xd9')
   # Check if we actually got any bytes
   if a>-1 and b >-1:
      jpg = bbb[a:b+2]
      
      image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR) 

      hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # find red color
      low_red = np.array([151, 50, 84])
      high_red = np.array([189, 255, 255])
      red_mask = cv2.inRange(hsv_frame, low_red, high_red)
      contours, hierarchy  = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	  
      contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

      rows, cols, _ = image.shape

      x_center = int(cols / 2)
      y_center = int(rows / 2)
    
      for cnt in contours:
          (x, y, w, h) = cv2.boundingRect(cnt)
        
          x_center = int((x + x + w) / 2)
          y_center = int((y + y + h) / 2)
          break
    
      cv2.line(image, (x_center, 0), (x_center, 480), (0, 255, 0), 2)
      cv2.line(image, (0, y_center), (640, y_center), (0, 255, 0), 2)
    
      cv2.imshow("Frame", image)
        
      bbb = bbb[b+2:]
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break
    
cv2.destroyAllWindows()

import cv2, os
import numpy as np

WIDTH  = 240  # width of image to process (pixels)
HEIGHT = 160 # height of image to process (pixels)

PALLET_COLOR_RANGE = np.array([[10, 80, 120], [255, 140, 160]]) # declare LAB range before overwrighting with user inputs

class PalletFilter:

    # exposure_absolute=10

    def colorTracking(self, image, range=PALLET_COLOR_RANGE, min_size=6, max_size=6):
        global WIDTH, HEIGHT

        image = cv2.resize(image,(WIDTH, HEIGHT)) # resize the image

        image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)  # convert image to hsv colorspace RENAME THIS TO IMAGE_HSV

        blur = cv2.GaussianBlur(image_lab, (5, 5), 0)  # apply a gaussian blur to the image

        thresh = cv2.inRange(blur, PALLET_COLOR_RANGE[0], PALLET_COLOR_RANGE[1]) # Converts a 240x160x3 matrix to a 240x160x1 matrix
        # cv2.inrange discovers the pixels that fall within the specified range and assigns 1's to these pixels and 0's to the others.

        # apply a blur function
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel) # Apply blur
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) # Blur again

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] #generates number of contiguous "1" pixels
        center = None # create a variable for x, y location of target

        if len(cnts) > 0:   # begin processing if there are "1" pixels discovered
            c = max(cnts, key=cv2.contourArea)          # return the largest target area
            x,y,w,h = cv2.boundingRect(c)               # Get bounding rectangle (x,y,w,h) of the largest contour

            center = (int(x+0.5*w), int(y+0.5*h))       # defines center of rectangle around the largest target area

            if 0.5*w > min_size:
                cv2.rectangle(image, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 255), 2)  # draw bounding box
                cv2.circle(image, center, 3, (0, 0, 0), -1) # draw a dot on the target center
                cv2.circle(image, center, 1, (255, 255, 255), -1) # draw a dot on the target center

                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.2,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.2,(255,255,255),1,cv2.LINE_AA)
        
        image_height, image_width, channels = image.shape   # get image dimensions

        spacer = np.zeros((image_height,3,3), np.uint8)
        spacer[:,0:WIDTH//2] = (255,255,255)      # (B, G, R)

        # make 3 images to have the same colorspace, for combining
        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        # border1 = np.array() # use H, height of photos to define
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        # border2 = np.array() # same as above

        # draw text on top of the image for identification
        cv2.putText(image,'Original',(10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(image,'Original',(10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(255,255,255),1,cv2.LINE_AA)

        # draw text on top of the image for identification
        cv2.putText(thresh,'Thresh',(10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(thresh,'Thresh',(10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(255,255,255),1,cv2.LINE_AA)

        # draw text on top of the image for identification
        cv2.putText(mask,'Mask',(10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(mask,'Mask',(10,int(image_height/10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(255,255,255),1,cv2.LINE_AA)

        all = np.vstack((image, thresh, mask))
        return all
    
def init_filter():  # The function MJPG-Streamer calls.
    pallet_filter = PalletFilter()
    return pallet_filter.colorTracking

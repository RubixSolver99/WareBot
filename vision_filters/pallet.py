import cv2, os, socket      # pyright: ignore[reportMissingImports]
import numpy as np

WIDTH  = 240  # width of image to process (pixels)
HEIGHT = 160 # height of image to process (pixels)

ASPECT = 11.5  # width / height of pallet in real life 
MIN_PALLET_SIZE = 25  # minimum pallet width in pixels to consider valid

# PALLET_COLOR_RANGE = np.array([[45, 70, 110], [255, 150, 170]]) # LAB Values For MXET Lab
PALLET_COLOR_RANGE = np.array([[20, 110, 130], [40, 130, 150]]) # LAB Values for Carson's House

class PalletFilter:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target = ("127.0.0.1", 3657)


    def color_tracking(self, image, range=PALLET_COLOR_RANGE, min_size=MIN_PALLET_SIZE, max_size=6):
        global WIDTH, HEIGHT

        image = cv2.resize(image,(WIDTH, HEIGHT)) # resize the image

        image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)  # convert image to LAB colorspace

        blur = cv2.GaussianBlur(image_lab, (7, 7), 5)  # apply a blur to the image

        thresh = cv2.inRange(blur, PALLET_COLOR_RANGE[0], PALLET_COLOR_RANGE[1]) # Converts a 240x160x3 matrix to a 240x160x1 matrix
        # cv2.inrange discovers the pixels that fall within the specified range and assigns 1's to these pixels and 0's to the others.

        # apply a blur function
        kernel = np.ones((7,7),np.uint8)

        dilated = cv2.dilate(thresh, kernel, iterations=2)  # Dilate to fill in gaps

        mask = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, kernel) # Apply blur
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) # Blur again

        mask = cv2.GaussianBlur(mask, (25, 25), 0)  # final blur to smooth edges

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] #generates number of contiguous "1" pixels
        center = None # create a variable for x, y location of target

        if len(cnts) > 0:   # begin processing if there are "1" pixels discovered
            c = max(cnts, key=cv2.contourArea)          # return the largest target area
            x,y,w,h = cv2.boundingRect(c)               # Get bounding rectangle (x,y,w,h) of the largest contour

            h = int(w / ASPECT)

            cx = x + w // 2
            cy = y + h // 2
            x = int(cx - w / 2)
            y = int(cy - h / 2) + 10  # adjust y to better center box on pallet

            center = (int(x+0.5*w), int(y+0.5*h))       # defines center of rectangle around the largest target area

            if 0.5*w > min_size:
                angle = round(((center[0]/WIDTH)-0.5)*75, 3)  # angle of vector towards target center from camera, where 0 deg is centered
                message = f"PALLET_FOUND,{w},{angle}"

                cv2.rectangle(image, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 255), 2)  # draw bounding box
                cv2.circle(image, center, 3, (0, 0, 0), -1) # draw a dot on the target center
                cv2.circle(image, center, 1, (255, 255, 255), -1) # draw a dot on the target center

                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.2,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.2,(255,255,255),1,cv2.LINE_AA)
            else:
                message = "PALLET_NOT_FOUND"
            
            self.sock.sendto(message.encode(), self.target)

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
    return pallet_filter.color_tracking

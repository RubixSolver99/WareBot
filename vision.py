import cv2, os, time
import numpy as np

WIDTH  = 240  # width of image to process (pixels)
HEIGHT = 160 # height of image to process (pixels)
IMAGE_PATH = "/tmp/vision/frame.jpg" # Folder where Node-RED will read images
MIN_INTERVAL = 0.03  # 30 FPS max (adjust as desired)
COLOR_RANGE = np.array([[35, 80, 5], [65, 255, 240]]) # declare HSV range before overwrighting with user inputs

# _last_save = 0
# cap = None


# def send_frame(frame):
#     """Save frame to disk for Node-RED to read"""
#     global _last_save

#     now = time.time()
#     if now - _last_save < MIN_INTERVAL:
#         return  # limit frame rate to avoid SD wear

#     _last_save = now
#     cv2.imwrite(IMAGE_PATH, frame)

# def start_camera():
#     global cap

#     # Create folder if missing
#     os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)

#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
#     cap.set(cv2.CAP_PROP_FPS, 30)  # Requesting 30 FPS from the camera

#     if not cap.isOpened():
#         print("Camera failed to open.")
#         exit()

# def update_camera():
#     global cap
    
#     ret, frame = cap.read()
#     if not ret:
#         return None

#     # Process your frame however you want here...

#     # Send frame to Node-RED
#     send_frame(frame)




class PalletFilter:

    # exposure_absolute=10

    def colorTracking(self, image, range=COLOR_RANGE, min_size=6, max_size=6):
        global WIDTH, HEIGHT

        image = cv2.resize(image,(WIDTH, HEIGHT)) # resize the image

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # convert image to hsv colorspace RENAME THIS TO IMAGE_HSV

        thresh = cv2.inRange(hsv_image, COLOR_RANGE[0], COLOR_RANGE[1]) # Converts a 240x160x3 matrix to a 240x160x1 matrix
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
    f = PalletFilter()
    return f.colorTracking

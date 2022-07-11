# imports
import cv2
import mediapipe as mp
import tensorflow as tf
import numpy as np

# Object declerations (i think XD)
# https://pythonprogramming.net/using-trained-model-deep-learning-python-tensorflow-keras/
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands =  mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=1)

model = tf.keras.models.load_model("C:\\Users\\10\\Jupyter notes\\Models\\paper_26C_0.h5")

classes = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
#fucntions declerations
def rectHand(hand_landmarks,image_w,image_h):
    ''' A function that returns the coordinates of the plam'''
    x_max = 0
    y_max = 0
    x_min = image_w
    y_min = image_h
    # hand_landmarks = results.multi_hand_landmarks
    if hand_landmarks:
        for handLMs in hand_landmarks:

            for lm in handLMs.landmark:
                x,y = int(lm.x * image_w),int(lm.y * image_h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y

        # regulating rctangle size
        x_max += 20
        y_max += 20
        x_min -= 20
        y_min -= 20

        if x_max > image_w:
            x_max = image_w
        if x_min < 0:
            x_min = 0
        if y_max > image_h:
            y_max = image_h
        if y_min < 0:
            y_min = 0
    else:
        x_min=0
        y_min=0
    return x_min,y_min,x_max,y_max

def prepareImg(img):
    size = 200
    img = cv2.resize(img,(size,size))
    return img.reshape(-1,size,size,3)

def findHandInImg(image):
     # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    # Change images from BGR to RGBss
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Start detecting hand
    results = hands.process(image)

    # get coorrdinates of hand if there is a handd in image.
    x_min,y_min,x_max,y_max = rectHand(results.multi_hand_landmarks,image.shape[1],image.shape[0])
    # if there is a hand draw rectangle andd return image else return image as it is.
    if x_min == 0 and x_max == 0 and y_max ==0 and y_min==0:
         pass   # do nothing
    else:
        cv2.rectangle(image,(x_max,y_max),(x_min,y_min),color=(0,255,0),thickness=2)
        croppedImg = image[y_min:y_max,x_min:x_max]
        croppedImg = prepareImg(croppedImg)
        letter = classes[np.argmax(model.predict([croppedImg]))]
  
        # image =cv2.flip(image,1)
        cv2.putText(image,str(letter),(x_min,y_min),cv2.FONT_HERSHEY_TRIPLEX,1.0,color=(0,0,255))
        
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)   
    image =cv2.flip(image,1)   
    return image
   

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

# function definition
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
# Main code
model = tf.keras.models.load_model("..\\models\\PP_10C_model0.h5")


classes = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]
# Capture frames feed from web cam
cap = cv2.VideoCapture(0)

hands =  mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=1)

# main loop
while cap.isOpened():
    # get frames from capture
    success, image = cap.read()

    if not success:
      print("Ignoring empty camera frame.")
      continue

    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    # Change images from BGR to RGBss
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Start detecting hand
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    x_min,y_min,x_max,y_max = rectHand(results.multi_hand_landmarks,image.shape[1],image.shape[0])
    cv2.rectangle(image,(x_max,y_max),(x_min,y_min),(0,255,0),2)




    if x_min == 0 and x_max == 0 and y_max ==0 and y_min==0:
        pass
    else:
        cropped = image[y_min:y_max,x_min:x_max]
        cropped = prepareImg(cropped)
        letter = classes[np.argmax(model.predict([cropped]))]
        print(letter)
        cv2.putText(image,str(letter),(x_min,y_min),cv2.FONT_HERSHEY_TRIPLEX,1.0,color=(0,0,255))

    cv2.imshow('MediaPipe Hands',image)

    # Press esp to close program
    if cv2.waitKey(1) & 0xFF == 27:
      break

cap.release()
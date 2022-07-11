# imports
import cv2
import mediapipe as mp
import os
# Object declerations (i think XD)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands =  mp_hands.Hands(
        static_image_mode=True,
        min_detection_confidence=0.5,
        max_num_hands=1)
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

# Main code
counter = 0
files_dir = "C:\\Users\\10\\Desktop\\Graduation project\\Datasets\\Dataset1\\My ASL Dataset\\C\\"
files = os.listdir(files_dir)

for i in range(0,len(files)):
    # Capture frames feed from webcam
    image = cv2.imread(files_dir+files[i])
    # Change images from BGR to RGBss
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Start detecting hand
    results = hands.process(image)

    # change image back
    image.flags.writeable = True

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


    x_min,y_min,x_max,y_max = rectHand(results.multi_hand_landmarks,image.shape[1],image.shape[0])

    if x_min == 0 and y_min == 0 and x_max == 0 and y_max == 0:
        print(f"file:{files[i]} has no hand in it")
    else:
        cv2.rectangle(image,(x_max,y_max),(x_min,y_min),(0,255,0),2)
        cropped = image[y_min:y_max,x_min:x_max]
        print(f"({x_min},{y_min})({x_max},{y_max})")
        cv2.imwrite(f"images\\croped_{files[i]}.jpg",cropped)
        print(f"file:{files[i]} is cropped and saved")
        counter+=1
    #
    # Press esp to close program
    #cv2.waitKey(0)

print(f"pics:{counter}")

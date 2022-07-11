# imports
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands =  mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=1)

# function definition
def rectHand(hand_landmarks,image_w,image_h):
    ''' A function that returns the coordinates of a rectangle to be drawn around plam'''
    x_max = 0
    y_max = 0
    x_min = image_w
    y_min = image_h

    # if image found find boarder
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

        # adding 20 points off set
        x_max += 20
        y_max += 20
        x_min -= 20
        y_min -= 20

        # regulating rctangle size
        if x_max > image_w:
            x_max = image_w
        if x_min < 0:
            x_min = 0
        if y_max > image_h:
            y_max = image_h
        if y_min < 0:
            y_min = 0
    # if the hand was't found return all borders as zeroes
    else:
        x_min=0
        y_min=0

    return x_min,y_min,x_max,y_max

# Constants
#text color
textColor = (0,0,255)
imgNum = 0  #number of saved images
folder = 0  #
letter = 65 # letter A ascii
#folder dir
folderDir = "C:\\Users\\10\\Desktop\\Dataset collector\\hossin\\"

# Capture video frames
cap = cv2.VideoCapture(0)
# Main loop
while cap.isOpened():

    success,image = cap.read()

    if success:
        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        # Change images from BGR to RGBss
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # Start detecting hand
        results = hands.process(image)


        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        x_min,y_min,x_max,y_max = rectHand(results.multi_hand_landmarks,image.shape[1],image.shape[0])
        cv2.rectangle(image,(x_max,y_max),(x_min,y_min),(0,255,0),2)



        # wait for a key to be pressed
        key_pressed = cv2.waitKey(10)
        # check which key is pressed
        if key_pressed & 0xFF == ord("s"):                          # if s is pressed save image
            cv2.imwrite(folderDir + f"{chr(letter)}\\{chr(letter)}{imgNum}.jpg",image[y_min:y_max,x_min:x_max])
            print(f"Image taken: {imgNum}")
            imgNum += 1
        elif key_pressed & 0xFF == ord("i"):                        # if i is pressed go to next folder
            imgNum = 0
            folder += 1
            letter += 1
            print(f"Change Folder: {folder}")
        elif key_pressed & 0xFF == ord("j"):                        # if j is pressed goto prvoius folder
            imgNum = 0
            folder -= 1
            letter -= 1
            print(f"Change Folder: {folder}")
        elif key_pressed == 0xFF&27:                                # if esc is pressed exit program
            break



        # put instructions on images
        cv2.putText(image,f"Collected Images:{imgNum}",(0,30),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1,color=(0,0,255),thickness=2)
        cv2.putText(image,f"letter:{chr(letter)}",(500,30),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1,color=(0,0,255),thickness=2)

        cv2.imshow("this",image)



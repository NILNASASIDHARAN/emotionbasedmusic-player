

import time
import cv2
import label_image
import os,random
import subprocess
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

size = 4
# We load the xml file
classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
global text
webcam = cv2.VideoCapture(0)  # Using default WebCam connected to the PC.
now = time.time()###For calculate seconds of video
future = now + 30  ####here is second of time which taken by emotion recognition system ,you can change it
while True:
    (rval, im) = webcam.read()
    im = cv2.flip(im, 1, 0)  # Flip to act as a mirror
    # Resize the image to speed up detection
    mini = cv2.resize(im, (int(im.shape[1] / size), int(im.shape[0] / size)))
    # detect MultiScale / faces
    faces = classifier.detectMultiScale(mini)
    # Draw rectangles around each face
    for f in faces:
        (x, y, w, h) = [v * size for v in f]  # Scale the shapesize backup
        sub_face = im[y:y + h, x:x + w]
        FaceFileName = "test.jpg"  # Saving the current image from the webcam for testing.
        cv2.imwrite(FaceFileName, sub_face)
        text = label_image.main(FaceFileName)  # Getting the Result from the label_image file, i.e., Classification Result.
       # text = ''  
        font = cv2.FONT_HERSHEY_TRIPLEX

        if text == 'angry':
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
            cv2.putText(im, text, (x + h, y), font, 1, (0, 25,255), 2)

        if text == 'happy':
            cv2.rectangle(im, (x, y), (x + w, y + h), (0,260,0), 7)
            cv2.putText(im, text, (x + h, y), font, 1, (0,260,0), 2)

        if text == 'neutral':
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 255), 7)
            cv2.putText(im, text, (x + h, y), font, 1, (0, 255, 255), 2)

        if text == 'sad':
            cv2.rectangle(im, (x, y), (x + w, y + h), (0,191,255), 7)
            cv2.putText(im, text, (x + h, y), font, 1, (0,191,255), 2)

    # Show the image/
    cv2.imshow('Music player with Emotion recognition', im)
    key = cv2.waitKey(30)& 0xff
    
    if time.time() > future:##after 20second music will play
        try:
            cv2.destroyAllWindows()
            print(text)
            mp = 'C:/Program Files (x86)/Windows Media Player/wmplayer.exe'
            if text == 'angry':
                randomfile = random.choice(os.listdir("C:/Users/BINU/Desktop/Pro_musicplayer/Music/angry/"))
                print('You are angry !!!! please calm down:) ,I will play song for you :' + randomfile)
                file = ('C:/Users/BINU/Desktop/Pro_musicplayern/Music/angry/' + randomfile)
                subprocess.call([mp, file])

            if text == 'happy':
                randomfile = random.choice(os.listdir("C:/Users/BINU/Desktop/Pro_musicplayer/Music/Happy/"))
                print('You are smiling :) ,I playing special song for you: ' + randomfile)
                file = ('C:/Users/BINU/Desktop/Pro_musicplayer/Music/Happy/' + randomfile)
                subprocess.call([mp, file])

            if text == 'neutral':
                randomfile = random.choice(os.listdir("C:/Users/BINU/Desktop/Pro_musicplayer/Music/neutral/"))
                print('I playing song for you: ' + randomfile)
                file = ('C:/Users/BINU/Desktop/Pro_musicplayer/Music/neutral/' + randomfile)
                subprocess.call([mp, file])

            if text == 'sad':
                randomfile = random.choice(os.listdir("C:/Users/BINU/Desktop/Pro_musicplayer/Music/sad/"))
                print('You are sad,dont worry:) ,I playing song for you: ' + randomfile)
                file = ('C:/Users/BINU/Desktop/Pro_musicplayer/Music/sad/ ' + randomfile)
                subprocess.call([mp, file])
            break

        except :
            print('Please stay focus in Camera frame atleast 15 seconds & run again this program:)')
            break

    if key == 27:  # The Esc key
        break


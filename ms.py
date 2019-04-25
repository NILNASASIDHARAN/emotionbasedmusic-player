import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json, cv2
import numpy as np
import cv2
import os
import keyboard
from time import sleep
import time
import pygame
import sys
import random
import keyboard
import threading
from threading import Thread
#songs array list
_songs = ['music/0.mp3','music/1.mp3','music/2.mp3','music/3.mp3','music/4.mp3','music/5.mp3','music/6.mp3','music/7.mp3','music/8.mp3','music/9.mp3', 'music/10.mp3', 'music/11.mp3', 'music/12.mp3' ,'music/13.mp3','music/14.mp3']
_currently_playing_song = None
_songsindex = 0
ans = {}
#initial values
ans['answer'] = 'happy'
ans['flag'] = False


#play
def playsound(soundfile):
    """Play sound through default mixer channel in blocking manner.
       This will load the whole sound into memory before playback
    """

    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(soundfile)
    clock = pygame.time.Clock()
    sound.play()
    while pygame.mixer.get_busy():
        print("Playing...")
        #clock.tick(1000)

##3
def playmusic(soundfile):
    """Stream music with mixer.music module in blocking manner.
       This will stream the sound from disk while playing.
    """
    global ans
    #: No need for global declaration to just read value
    #pygame.init()
    #pygame.mixer.init()
    #clock = pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # print(pygame.mixer.music.get_pos())
        if pygame.mixer.music.get_pos() >= 18000:
            #print(pygame.mixer.music.get_pos())
            play_next_song() # if it happy
            #print("You are loving this song, try this song now from the same singer !")

        if ans['answer'] == 'sad' and ans['flag'] == True:
            pygame.mixer.music.stop()
            #print("You don't seem to like this song, try song from a new singer !")
            #time.sleep(2)
            ans['flag'] = False
            play_next_genre()

def stopmusic():
    """stop currently playing music"""
    pygame.mixer.music.stop()

def getmixerargs():
    pygame.mixer.init()
    freq, size, chan = pygame.mixer.get_init()
    return freq, size, chan


def initMixer():
    BUFFER = 3072  # audio buffer size, number of samples since pygame 1.8.
    FREQ, SIZE, CHAN = getmixerargs()
    pygame.init()
    pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)


def play_a_different_song():
    global _currently_playing_song, _songs
    next_song = random.choice(_songs)
    print(next_song)
    while next_song == _currently_playing_song:
        print(_currently_playing_song)
        next_song = random.choice(_songs)
        print(next_song)
    _currently_playing_song = next_song
    pygame.mixer.music.load(next_song)
    pygame.mixer.music.play()

def play_next_song():
    global _songs
    global _songsindex
    if _songsindex == 14:
        _songsindex = 0
    else:
        _songsindex =_songsindex+1
    pygame.mixer.music.load(_songs[_songsindex])
    print("Now playing : {}".format(_songsindex))
    pygame.mixer.music.play()
    #print(pygame.mixer.music.get_pos())


def play_next_genre():
    global _songs
    global _songsindex
    _songsindex+=3;
    if _songsindex > 14:
        _songsindex = 0
    pygame.mixer.music.load(_songs[_songsindex])
    print("Now playing : {}".format(_songsindex))
    pygame.mixer.music.play()

##################

#face emotion recognition
def playvideo():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    img_counter = 1
    timer = 0
    processed = 0
    #print('\n\tHappiness'.ljust(18)+'Surprise'.ljust(18)+'Neutral'.ljust(18)+'Sadness'.ljust(18)+'Disgust'.ljust(18)+'Anger'.ljust(18)+'Contempt'.ljust(18)+'Fear'.ljust(18))
    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        img_name = "img_frame{}.jpg".format(img_counter)
        # print("Created img_frame{}.jpg".format(img_counter))
        key = cv2.waitKey(25) # 1000/25 = 40 FPS
        if timer % 40 == 0:
            print('Tip :  {}'.format(4-(timer / 40)), end='\r')

        # start processing the image emotions when timer is
        #if
        if timer / 40 == 4 :
            cv2.imwrite(img_name, frame)
            processed+=1
            find_emotions(img_name)
            key = cv2.waitKey(50) # milliseconds
            timer=1
            if os.path.isfile(img_name):
                os.remove(img_name)
                continue
                # deleting the image after processing it
                #print("Deleted img_frame{}.jpg".format(i))
            else: ## Show an error ##
                print("Error: %s file not found" % myfile)
                continue
        timer+=1

        # take less frames
        # end processing this frame

        # deleting the image after processing it
        # print("Deleted img_frame{}.jpg".format(img_counter))

        # this can be put in a try catch box
        ## if file exists, delete it ##
        img_counter+=1

        if key == 27 or processed == 18: # exit on ESC
            break

    cv2.destroyWindow("preview")
   # print('API calls made or number frames processed for emotion detection : {}'.format(processed))
    vc.release()
    
    

#####################################3


def backgroundmusic():
    initMixer()
    global _songsindex
    _songsindex = 0   # random number can also be used
    filename = (_songs[_songsindex ])
    #print(filename)
    print("Now playing : {}".format(_songsindex))
    playmusic(filename)

# playvideo()
# backgroundmusic()

def printit():
    # run your code
    print('Time :  ', end='\r')
    threading.Timer(1.0, printit).start()
    end = time.time()
    elapsed = int(end - start)
    print('Time :  {}'.format(elapsed), end='\r')


if __name__ == '__main__':
    #start = time.time()
    #printit()
    p1 = Thread(target=backgroundmusic)
    p1.start()
    p2 = Thread(target=playvideo)
    p2.start()
    p1.join()
    p2.join()


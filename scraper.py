import urllib.request
import time
import sys      # For accepting parameters
import cv2      # For video combining
import os       # "
import glob     # "
from datetime import datetime

# Apgar Mt. Northeast View NPS Webcam
url = 'https://www.nps.gov/webcams-glac/'

# Retrieve a photo and save it in the correct folder depending on the time of day
# folderName = whetehr to place in day/night folder
# cam = name of cam to get image from
def getPhoto(folderName, cam):
    # File location and name of the photo to save
    nameString = 'Output/' + cam + '/' + folderName + '/' + cam + str(time.time()) + '.jpg'
    # Save the webcam capture in the desired location
    urllib.request.urlretrieve(url + cam + '.jpg', nameString)

# Combine images from photos into a video
# folderName = whether in day/night folder
# cam = name of cam we got image from
def createVideo(folderName, cam):
    # Largely from https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
    imgList = []
    #C:/Working/WebcamScraper
    initialLocation = 'Output/' + cam + '/'
    locationToIterate = initialLocation + folderName + '/*.jpg'
    # Iterate through every photo in given folder, adding to the list
    # In the order that they are in in the folder
    for fileName in glob.glob(locationToIterate):
        img = cv2.imread(fileName)
        height, width, layers = img.shape
        size = (width, height)
        imgList.append(img)

    # Create the 'video' that has yet to have images added to it
    # file name, fourcc, fps/images per second, size
    out = cv2.VideoWriter(initialLocation + cam + folderName + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 2, size)

    # Add image to video
    for i in range(len(imgList)):
        out.write(imgList[i])
    out.release()

if __name__ == "__main__":

    # Returns the hour (0-24). Meant to be used in the Pacific timezone
    timeLocal = time.localtime(time.time()).tm_hour
    folderName = 'Day'

    # If a night photo - from 8 pm to 4 am
    if timeLocal > 19 or timeLocal < 4:
        folderName = 'Night'

    webcamToQuery = sys.argv[1]

    getPhoto(folderName, webcamToQuery)
    createVideo(folderName, webcamToQuery)
    


    
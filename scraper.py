import urllib.request
import time
import cv2      # For video combining
import os       # "
import glob     # "
from datetime import datetime

# Apgar Mt. Northeast View NPS Webcam
url = 'https://www.nps.gov/webcams-glac/aplocam.jpg'

# Retrieve a photo and save it in the correct folder depending on the time of day
def getPhoto(folderName):
    nameString = folderName + '/aplocam'
    # Save the webcam capture in the desired location
    urllib.request.urlretrieve(url, nameString + str(time.time()) + '.jpg')

# Combine images from photos into a video
def createVideo(folderName):
    # Largely from https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
    imgList = []
    # Iterate through every photo in given folder, adding to the list
    # In the order that they are in in the folder
    for fileName in glob.glob('C:/Working/WebcamScraper/' + folderName + '/*.jpg'):
        # print('File Name = ' + fileName)      # For testing
        img = cv2.imread(fileName)
        height, width, layers = img.shape
        size = (width, height)
        imgList.append(img)

    # Create the 'video' that has yet to have images added to it
    # file name, fourcc, fps/images per second, size
    out = cv2.VideoWriter('project' + folderName + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 2, size)

    # Add imagee to video
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
    print('Folder Name = ' + folderName + ', Time = ' + str(timeLocal))

    getPhoto(folderName)
    createVideo(folderName)
    


    
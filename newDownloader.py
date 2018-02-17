#######################################################################################################################
#Header
#This was made by Ryan Schlueter rschlueter98@gmail.com, (314) 603-4504, BSEE '18 on Sep. 18th 2017
#I'm not a coder, so don't hate if this doesn't follow PEP-8 or whatever other standards
#
#This program downloads images from a list of m3u8 streams. It doesn't save them or run yolo or anything
#Run it with: python image_downloader.py <input_filename> <type> <inputValue>
#input_filename is the filename of m3u8 streams you want to download from
#type is either "num" or "time" based of if you want to download for x minutes, or download x images
#inputValue is the above mentioned x. Like 5000 images, or 60 minutes
#
#No output files, FPS is display at the end
#######################################################################################################################

import time
import cv2



if __name__ == '__main__':
  downloadCounter=0

  url="http://video3.earthcam.com/fecnetwork/10347.flv/playlist.m3u8"
  cap = cv2.VideoCapture(url)
  print("Stream opened")
  time.sleep(0.5)
  for x in range (0,10):
    frame = cap.read()[1]
    filename = ("z_" + str(downloadCounter) + ".jpg")
    fullpath = ("home/rschluet/imageDownloads/" + filename)
    cv2.imwrite(str(fullpath), frame)
    print(str(downloadCounter + " downloaded")



  cap.release()
  print("Stream closed")



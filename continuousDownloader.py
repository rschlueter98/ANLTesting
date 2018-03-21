###############################################################################
#Theoretical downloader for 12k FPS on argonne usign Earthcam m3u8s
#
#Dont run this code with less than 512 processing cores. That many is needed
# for 12k FPS worth of streams to be opened
#
#Enter the following args for this to run
#python twelveKdownlader.py <input file name>
#
#
###############################################################################

import threading
import time
import sys
import cv2
import psutil
import datetime
import os

now=datetime.datetime.now()

#Active core counters based on system specs
cores_current = []
cores_max = psutil.cpu_count()

#List and queue for loaded streads and downloaded image data
loadedStreams = []
streamNames = []
imageData = []

timeToDownload = 5#*60


# Controls the number of feeds to be opened with how many threads. Currently reads in from an input text file of
# m3u8 feeds links. Can be altered to read in from ip cameras as well
def loadStreams(streams_file):
  while(True):
    streamsDatabase = open(streams_file)
    for line in streamsDatabase:
      if not line.startswith("#"):
        opened = False
        while (not opened):
          if(len(cores_current) < cores_max):
            t = threading.Thread(target=download, args=(line,))
            t.start()
            cores_current.append(t)
            time.sleep(0.01)
            opened = True
          else:
            time.sleep(0.01)
    streamsDatabase.close()

def download(line):
  global downloadCounter
  global timeToDownload
  earthcamID = line.split("/")[4].split(".")[0]

  try:
    cap = cv2.VideoCapture(line)
    if (cap.isOpened()):
      print ("Stream: " + earthcamID + " loaded")

      # Initialize save path for new stream
      now = datetime.datetime.now()
      # path = "/home/ryan/Research/imageDownloadTesting" # Local
      path = "/projects/SE_HPC/cam2/ryan/downloadedImages"  # ANL
      path = path + "/" + str(now.strftime("%Y-%m-%d-%H-%M"))
      path = path + "/" + earthcamID

      os.makedirs(path)
      # Initialize new variables for exiting download
      breaker = False
      startTime = time.time()

      while ((time.time() - startTime) < timeToDownload):
        if (breaker):
          break
        try:
          frame = cap.read()[1]
          filename = ("z_" + str(downloadCounter) + ".jpg")
          fullpath = (str(path) + "/" + filename)
          if (str(frame) != "None"):
            cv2.imwrite(str(fullpath), frame)
            downloadCounter = downloadCounter + 1
          # This else handles if a stream is downloaded as blank, and exits the loop
          else:
            breaker = True
            print ("BLANK FRAME STREAM, EXITING")
        # This except handles if a frame downloads, but cannot be saved for whatever reason
        except:
          print ("Bad Frame")
          pass
      print ("\t\tStream: " + str(earthcamID) +" finished downloading")

      cap.release()
      cores_current.pop()

  # This Except handles if the stream never wants to load
  except:
      cap.release()
      print (str(earthcamID) + " failed to load")
      cores_current.pop()

if __name__ == '__main__':
  #input validation
  if(len(sys.argv) < 2):
    print("Invalid input parameters.")
    print("Re-run with python twelveKdwonloader.py <input_filename.txt>")
    exit()

  # Initialize data structures
  global downloadCounter
  downloadCounter = 0

  #Start the loading and downloading
  loadStreams(sys.argv[1])

  #Stop timer and calclation
  print("Done.")


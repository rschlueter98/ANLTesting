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


systemCores=0

cores_load_max = psutil.cpu_count()
cores_download_max = psutil.cpu_count()

#Active core counters for various functions
cores_load_current = []
cores_download_current = []

#List and queue for loaded streads and downloaded image data
loadedStreams = []
streamNames = []
imageData = []

# Controls the number of feeds to be opened with how many threads. Currently reads in from an input text file of
# m3u8 feeds links. Can be altered to read in from ip cameras as well
def loadStreams(streams_file):
  streamsDatabase = open(streams_file)
  for line in streamsDatabase:
    for x in range(0,1):
      if not line.startswith("#"):
        opened = False
        while (not opened):
          if(len(cores_load_current) < cores_load_max):
            # print("OPening")
            t = threading.Thread(target=loadStream, args=(line, x,))
            t.start()
            cores_load_current.append(t)
            time.sleep(0.01)
            opened = True
          else:
            time.sleep(0.01)


# Function to load one individual stream. Called from the loadStreams
def loadStream(url, num):
  try:
    cap = cv2.VideoCapture(url)
    if (cap.isOpened()):
      loadedStreams.append(cap)
      temp = url.split("/")[4]
      temp = temp.split(".")[0]
      temp=temp + str(num)
      print ("Stream " + str(len(loadedStreams)) + ": " + temp + " loaded")
      streamNames.append(temp)
  except:
      print (str(url) + " failed to load")
  cores_load_current.pop()


# Controls number of threads being used for downloading images. Also chooses num or time based off input args
def downloadImages(input, saveImage):
  print ("Downloading images")
  for x in range((len(loadedStreams))):
    opened = False
    while (not opened):
      if (len(cores_download_current) < cores_download_max):
        print("Downloading from: " + str(streamNames[x]))
        t = threading.Thread(target=timeDownloadImage, args=(loadedStreams[x], streamNames[x],  input, saveImage,))
        t.start()
        cores_download_current.append(t)
        opened = True
      else:
        time.sleep(0.01)


# Downloads images for a set time
def timeDownloadImage(stream, streamName, timeToDownload, saveImage):
  global downloadCounter
  # path = "/home/ryan/Research/imageDownloadTesting"                  #loacl
  path = "/projects/SE_HPC/cam2/ryan/downloadedImages"               #ANL
  path=path+"/"+str(now.strftime("%Y-%m-%d-%H-%M"))
  path=path+"/"+streamName
  os.makedirs(path)
  # print(path)
  timeToDownload = timeToDownload * 60
  breaker = False
  startTime = time.time()
  while ((time.time()-startTime)<timeToDownload):
    if(breaker):
      break
    try:
      frame = stream.read()[1]
      if (saveImage):
        filename = ("z_" + str(downloadCounter) + ".jpg")
        fullpath = (str(path) + "/" + filename)
        if(frame=='None'):
          cv2.imwrite(str(fullpath), frame)
      else:
        imageData.append(frame)
      downloadCounter = downloadCounter + 1
    except:
      print ("Bad Frame")
      pass
  print ("Stream finished downloading")
  cores_download_current.pop()





if __name__ == '__main__':
  systemCores = psutil.cpu_count()
  #system validation
  # if(systemCores < 512):
  #   print("Not enough cores, re-run on a node with more cores")
  #   exit()

  #input validation
  if(len(sys.argv) < 2):
    print("Invalid input parameters.")
    print("Re-run with python twelveKdwonloader.py <input_filename.txt>")
    exit()



  # Initialize data structures
  global downloadCounter
  downloadCounter = 0
  fpses = []
  times = []


  #Timer to find the total time ellapsed
  programStartTime=time.time()


  #Start the actual downloading
  loadStreams(sys.argv[1])


  while(len(cores_load_current) > 0):
    time.sleep(0.05)
  print ("All streams opened. Downloading now")


  # time to download (minutes), save or not
  downloadImages(5, 1)

  # Wait while not done downloading yet
  while (len(cores_download_current) > 0):
    # print (str(len(imageData)) + " images downloaded")
    # print ("Downloaded " + str(downloadCounter) + " in " + str(time.time() - ti2) + " seconds.")
    # print (str(downloadCounter / (time.time() - ti2)) + " FPS")
    # fpses.append(str(downloadCounter / (time.time() - ti2)))
    # times.append(time.time() - ti2)
    print ("waiting on downloading threads to shut down. " + str(len(cores_download_current)) + " remaining")
    time.sleep(0.5)

  #Stop timer and calclation
  programStopTime=time.time()
  programEllapsedTime=programStopTime-programStartTime




  print("\n\n\n\n\n\n")
  print("Program finished.")
  print("Total time: " + str(programEllapsedTime))
  print("Total Frames downloaded: " + str(downloadCounter))
  # print("Final file size downloadd: "+str(downloadSize))
  # print("Final Average FPS: " + str(endAVGFPS))
  print("Done.")


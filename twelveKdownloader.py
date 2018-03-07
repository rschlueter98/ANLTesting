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
import cv2


downloadCores=50  #Change based off what nproc returns (minus one for allocation)
systemCores=50
loadedStreams = []
downloadCounter


def loadStreams(streamsFile):
  openedStreamsFile = open(streamsFile)
  for line in openedStreamsFile:
    for x in 0 to 4:
      try:
        cap = cv2.VideoCapture(line)
        loadedStreams.append(cap, line.split("/")[4].split(".")[0]
)
        print("Stream " + str(len(loadedStreams))  + " out of " + str(4*len(openedStreamsFile))  + " loaded.")
      except:
        print("Stream " + str(len(loadedStreams)) + " failed")


#Will download based off time downloader found in newDownloader.py
def downloadImages():
  activeCores=0
  for x in range((len(loadedStreams))):
    opened = False
    while (not opened):
      if (activeCores < systemCores):
        t = threading.Thread(target=downloadImage, args=(loadedStreams[x], streamNames[x],  input, saveImage,))
        t.start()
        activeCores = activeCores + 1
        opened = True
      else:
        time.sleep(0.01)







# Downloads images for a set time
#def timeDownloadImage(stream, saveImage):
def timeDownloadImage(stream):

  global downloadCounter
  path = "/home/ryan/Research/imageDownloadTesting"
  timeToDownload = 60
  breaker = False
  startTime = time.time()
  while ((time.time()-startTime)<timeToDownload):
   try:
      frame = stream[0].read()[1]
      filename = ("z_" + str(stream[1]) + "__"  + str(downloadCounter) + ".jpg")
      fullpath = (str(path) + "/" + filename)
      cv2.imwrite(str(fullpath), frame)
      downloadCounter = downloadCounter + 1
    except:
      print ("Bad Frame")
      pass
  print ("Stream finished downloading")
  activeCores = activeCores -1




if __nme__ == '__main__':
  #system validation
  if($(nproc) < 512):
    print("Not enough cores, re-run on a node with more cores")
    exit()
  
  #input validation
  if(len(sys.argv) < 2):
    print("Invalid input parameters.")
    print("Re-run with python twelveKdwonloader.py <input_filename.txt")
    exit()
  
  
  
  
  #Timer to find the total time ellapsed
  programStartTime=time.time()
  
  
  
  
  #Start the actual downloading
  loadStreams(sys.argv[1])
  downloadImages()
  
  
  
  #Stop timer and calclation
  programStopTime=time.time()
  programEllapsedTime=time.time()
  
  
  
  
  print("\n\n\n\n\n\n")
  print("Program finished.")
  print("Total time: " + str(programEllapsedTime))
  print("Total Frames downloaded: " + str(frames))
  print("Final file size downloadd: "+str(downloadSize))
  print("Final Average FPS: " + str(endAVGFPS))
  print("Done.")


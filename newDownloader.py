import time
import cv2



if __name__ == '__main__':
  import cv2

  # url = "http://video3.earthcam.com/fecnetwork/10072.flv/playlist.m3u8"
  url = "http://video3.earthcam.com/fecnetwork/10147.flv/playlist.m3u8"
  # url = "http://video3.earthcam.com/fecnetwork/10294.flv/playlist.m3u8"
  # url = "http://video3.earthcam.com/fecnetwork/10347.flv/playlist.m3u8"
  # url = "http://video3.earthcam.com/fecnetwork/10551.flv/playlist.m3u8"

  cap = cv2.VideoCapture(url)

  ret, frame = cap.read()
  # print(frame)
  path = "/home/rschluet/imageDownloads"
  filename = ("z_" + "1" + ".jpg")
  fullpath = (str(path) + "/" + filename)
  cv2.imwrite(str(fullpath), frame)

  #
  #
  #
  # downloadCounter=0
  #
  # url="http://video3.earthcam.com/fecnetwork/10347.flv/playlist.m3u8"
  # stream = cv2.VideoCapture(url)
  # print("Stream opened")
  # time.sleep(0.5)
  # for x in range (0,10):
  #   frame = stream.read()[1]
  #   print(frame)
  #   filename = ("z_" + str(x) + ".jpg")
  #   fullpath = ("home/rschluet/imageDownloads/" + filename)
  #   cv2.imwrite(str(fullpath), frame)
  #   print(str(x) + " downloaded")
  #
  #
  #
  # stream.release()
  # print("Stream closed")
  #
  #

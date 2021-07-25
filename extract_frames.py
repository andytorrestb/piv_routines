"""
    Extracts frames (as images) from a given video file. 
"""
import cv2, os, sys


def process_img_number(number):
  while len(number) < 4:
    number = "0" + number
  return number

def extract_frames(file_name):
    if file_name.__contains__('.mp4') or file_name.__contains__('.avi'):
      # Make directory to save results. 
      name, ext = file_name.split('.')
      img_dir = './' + name + '/' + 'img/input/'

      if not os.path.exists(img_dir):
        dirs = img_dir.split('/')

        curr_dir = dirs[0] + '/' + dirs[1]
        print(curr_dir)
        os.mkdir(curr_dir)
        curr_dir = curr_dir + '/' + dirs[2]
        print(curr_dir)
        os.mkdir(curr_dir)
        curr_dir = curr_dir + '/' + dirs[3]
        print(curr_dir)
        os.mkdir(curr_dir)

      capture = cv2.VideoCapture(file_name)
      success, image = capture.read()

      i=0
      while(capture.isOpened()):
          ret, frame = capture.read()
          if ret == False:
            break
          digit = process_img_number(str(i))
          img_file = img_dir + name  + '.' + digit + '.jpg'
          # print(img_file)
          cv2.imwrite(img_file, frame)
          # print(digit)
          i+=1

      capture.release()
      cv2.destroyAllWindows()

      return img_dir

"""
    Extracts frames (as images) from a given video file. 
"""
import cv2, os, sys

def process_img_number(number):
  while len(number) < 4:
    number = "0" + number
  return number

def mkdir_crop(path):
  crop_dir = path
  print(crop_dir)

  crop_dirs = ['left', 'center', 'right']

  for dir in range(len(crop_dirs)):
    # print(crop_dir + crop_dirs[dir])
    if not os.path.exists(crop_dir + crop_dirs[dir]):
      os.mkdir(crop_dir + crop_dirs[dir])

def extract_frames(file_name):
    # Decompose file name.
    if file_name.__contains__('.mp4') or file_name.__contains__('.avi'):
      name, ext = file_name.split('.')
      # print(name)
      img_dir = './' + name + '/' + 'img/input/'
      # print(name)

      # if name has extra values, from upper level directories.
      if '/' in name:
        name = name.split('/')[-1]

      # Make directory to save results. 
      if not os.path.exists(img_dir):
        print(img_dir)
        dirs = img_dir.split('/')
        print(dirs)
        # curr_dir = ./name/
        curr_dir = dirs[0] + '/' + dirs[1]
        print(curr_dir)
        if not os.path.exists(curr_dir):
          os.mkdir(curr_dir)
        curr_dir = curr_dir + '/' + dirs[2]
        print(curr_dir)
        os.mkdir(curr_dir)
        # curr_dir = ./name/img/input/
        curr_dir = curr_dir + '/' + dirs[3]
        print(curr_dir)
        os.mkdir(curr_dir)
        curr_dir = curr_dir + '/' + dirs[4]
        print(curr_dir)
        if not os.path.exists(curr_dir):
          os.mkdir(curr_dir)

      mkdir_crop(img_dir)

      # print(name)
      # Extract frames using OpenCV
      # print('file_name = ', os.getcwd() + '/' + file_name)
      capture = cv2.VideoCapture(os.getcwd() + '/' + file_name)
      success, image = capture.read()

      print('success = ', success)

      print('entering while loop')
      i=0
      while(capture.isOpened()):
          ret, frame = capture.read()
          if ret == False:
            break
          digit = process_img_number(str(i))
          print(img_dir, name, digit)
          img_file = img_dir + name  + '.' + digit + '.jpg'
          print(img_file)
          print(cv2.imwrite(img_file, frame))
          print(digit)
          i+=1

      capture.release()
      cv2.destroyAllWindows()

      return img_dir

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os
from PIL import Image
import seaborn as sns
import glob

def process_img_number(number):
  while len(number) < 4:
    number = "0" + number
  return number

def crop_img(path, percent = 0.4, offset = (0.035, 0.017)):
  #Check path
  img = Image.open(path)
  width, height = img.size

  l_offset = offset[0]
  r_offset = offset[1]

  p = percent

  x0 = 0
  y0 = 0

  x1 = (p - l_offset) * width
  y1 = height

  x2 = (1.0 - p + r_offset) * width

  x3 = width

  # Crop images
  left = img.crop((x0, y0, x1, y1))
  center = img.crop((x1, y0, x2, y1))
  right = img.crop((x2, y0, x3, y1))

  return [left, center, right]

def save_cropped_images(path, name, cropped_frames):
  counter = 0
  for img_array in cropped_frames:
    file_num = process_img_number(str(counter))
    img_array[0].save(path + 'left/' + name + '.' + file_num+ '.jpg')
    img_array[1].save(path + 'center/' + name + '.' + file_num+ '.jpg')
    img_array[2].save(path + 'right/' + name + '.' + file_num+ '.jpg')
    counter = counter + 1
  return

def crop_images(path):
  cropped_frames = []

  print('all files in ', path)

  files = sorted(glob.glob(path + '*.jpg'))

  for file_name in files:
    print(file_name)
    cropped_frames.append(crop_img(file_name))

  # Sloppy way to parse path of file and get name for cropped image files. 
  name = files[0].rpartition('/')[-1].rpartition('.')[0].rpartition('.')[0]

  save_cropped_images(path, name, cropped_frames)

  return cropped_frames

def plot_cropped_img(img_array):
  # Plot images 
  rows, columns = 1, 3
  fig, ax = plt.subplots(rows, columns, figsize = (30, 8))
  fig.tight_layout()

  fig.add_subplot(rows, columns, 1)
    
  # showing image
  plt.imshow(img_array[0])
  plt.axis('off')
  plt.title("First")

  fig.add_subplot(rows, columns, 2)
    
  # showing image
  plt.imshow(img_array[1])
  plt.axis('off')
  plt.title("First")

  fig.add_subplot(rows, columns, 3)
    
  # showing image
  plt.imshow(img_array[2])
  plt.axis('off')
  plt.title("First")

  print(type(fig), type(ax))
  return fig, ax
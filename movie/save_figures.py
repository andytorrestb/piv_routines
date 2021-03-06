import os, glob
import matplotlib.pyplot as plt
from openpiv import tools, pyprocess, validation, filters, scaling
import numpy as np
import cv2
import piv_config as cfg

import sys
from PIL import Image

def process_img_number(number):
  while len(number) < 4:
    number = "0" + number
  return number

def read_cfd_images(path):
  cfd_images = []
  size = cfg.params['video']['size'] 
  white = (255, 255, 255)

  for file in sorted(os.listdir(path)):
    # Checks if file is frame a.
    # + 1 is required bc .find returns
    # position of string and -1 if not found
    if file.find('.jpg') + 1:
      if cfg.params['crop']['crop']:
        name, num, ext = file.split('.')
      else:
        name, num, frame, ext = file.split('.')

      if int(num) % 2 == 1:

        # Open image of current file
        img = Image.open(path + file)
        AR = img.size[0] / img.size[1]
        img = img.resize((size, int(size/ 2)))
        img_w, img_h = img.size

        # Make background image
        background = Image.new('RGBA', (size, size), white)
        bg_w, bg_h = background.size

        # Paste img on background and save to array to be returned. 
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        background.paste(img, offset)
        cfd_images.append(background)

  return cfd_images

def read_piv_images(path):
  piv_images = []

  print('IN FUNCTION: read_piv_images')
  print(len(sorted(os.listdir(path))))
  print(path)
  for file in sorted(os.listdir(path)):
    piv_images.append(
        Image.open(
            path + file
        )
    )

  return piv_images

def merge_image_pair(cfd_image, piv_image):
  # print('   ', type(cfd_image), cfd_image)
  # print('   ', type(piv_image), piv_image)
  
  (cfd_width, cfd_height) = cfd_image.size
  (piv_width, piv_height) = piv_image.size

  # print('   size of cfd_images', cfd_width, cfd_height)
  # print('   size of piv_images', piv_width, piv_height)    

  result_width = cfd_width + piv_width
  result_height = max(cfd_height, piv_height)

  result = Image.new('RGB', (result_width, result_height))
  result.paste(im = cfd_image, box = (0, 0))
  result.paste(im = piv_image, box = (cfd_width, 0))

  print(type(result))
  return result
     

def merge_images(cfd_images, piv_images):

  merged_images = []

  for image in range(len(cfd_images)):
    # print('Merging image at index =', image)

    merged_images.append(
        np.array(
            merge_image_pair(
                cfd_images[image],
                piv_images[image]
            )
        )
    )
  return merged_images

def save_piv_figures(path):
  print('IN FUNCTION: save_piv_figures')
  
  input_dir = path + '/data/results/'
  path = path + '/img/piv/'

  print()

  results = sorted(os.listdir(input_dir))

  print(len(results))
  scaling_factor = 50

  for ascii_file in results:
    print(ascii_file)
    # This can be a terrible bug
    if ascii_file.find('test') + 1:

      name, number, ext = ascii_file.split('.')
      
      # Display result as a matplotlib figure
      # fig, ax = plt.subplots(1, 2, figsize=(16,8))
      fig, ax = plt.subplots(figsize=(8,8))

      flowfield = tools.display_vector_field(
        input_dir + ascii_file, # file to read
        ax=ax, scaling_factor=scaling_factor,
        scale=5e6, # scale defines here the arrow length
        width=0.0035, # width is the thickness of the arrow
        on_img=False, # overlay on the image
        # image_name='exp1_001_a.bmp',  
        );

      number = process_img_number(number)

      # Save to file.
      file_path = path + name + '.' + number + '.jpg'
      print(file_path)
      print('')
      # print(type(flowfield[0]), file_path, number)
      flowfield[0].savefig(file_path)

      plt.close(flowfield[0])
    else:
      print(ascii_file, ' not found.')
def img_to_mp4(img_array):
  """
      Make video from array of images. 
  """
  fps = 8
  h,w,l = img_array[0].shape
  size = (w,h)
  out = cv2.VideoWriter('test.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
  for i in range(len(img_array)):
      out.write(img_array[i])
  out.release()
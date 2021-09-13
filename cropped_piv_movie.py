from openpiv import tools, pyprocess, validation, filters, scaling

import cv2, os, sys

import extract_frames as ef 
import rename_images as ri
import process_img_pair as piv
import save_figures as fig
import crop_images as ci

import piv_config as cfg

def main():
  # Check for valid input
  if (len(sys.argv) == 1):
    raise Exception('Provide video file to process')

  if (len(sys.argv) > 2):
    raise Exception('Too many arguments. Expected 1')

  if (len(sys.argv) == 2):
        # Extract frames from video file
        file_name = sys.argv[1]
        input_dir = ef.extract_frames(file_name)

  # Crop images, save to files
  cropped_images = ci.crop_images(input_dir)

  # Rename images for each cropped picture.
  for pos in ['left', 'center', 'right']:
    ri.rename_images(input_dir + pos + '/')

  # Make directories to hold PIV results.
  results_dir = input_dir.rpartition('/')[0]
  results_dir = results_dir.rpartition('/')[0]
  results_dir = results_dir.rpartition('/')[0] + '/data'
  os.mkdir(results_dir)
  os.mkdir(results_dir + '/results')  
  os.mkdir(results_dir + '/results/left')
  os.mkdir(results_dir + '/results/center')
  os.mkdir(results_dir + '/results/right')

  # Process images using OpenPIV. Save results as text file.
  # Process each cropped image seperatly.
  params = cfg.params
  params['crop']['crop'] = True

  for pos in ['left', 'center', 'right']:
    print(results_dir + '/results/' + pos)
    params['crop']['pos'] = pos

    file_name = os.listdir(input_dir + params['crop']['pos'])[0]
    print(file_name)
    name, number, frame, ext = file_name.split('.')
    pattern_a = name + '.*.a.' + ext
    pattern_b = name + '.*.b.' + ext
    print(input_dir + pos + '/')

    task = tools.Multiprocesser(
      data_dir = input_dir + pos + '/',
      pattern_a= pattern_a,
      pattern_b=pattern_b
      )

    task.run( func = piv.process_img_pair, n_cpus=1, params = cfg.params )


main()
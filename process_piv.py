from openpiv import tools, pyprocess, validation, filters, scaling


import cv2, os, sys

import extract_frames as ef 
import rename_images as ri
import process_img_pair as piv


def main():
  # Check for valid input
  if (len(sys.argv) == 1):
    raise Exception('Provide video file to process')

  # Extract frames from video file
  if (len(sys.argv) == 2):
        file_name = sys.argv[1]
        input_dir = ef.extract_frames(file_name)

  # Rename images accoriding to a-b pairs
  ri.rename_images(input_dir)
  
  file_name = os.listdir(input_dir)[0]

  name, number, frame, ext = file_name.split('.')
  print(name, number, frame, ext)
  # Process images using OpenPIV
  pattern_a = name + '.*.a.' + ext
  pattern_b = name + '.*.b.' + ext

  results_dir = input_dir.rpartition('/')[0]
  results_dir = results_dir.rpartition('/')[0] + '/results'
  os.mkdir(results_dir)

  task = tools.Multiprocesser(
      data_dir = input_dir,
      pattern_a= pattern_a,
      pattern_b=pattern_b
      )

  task.run( func = piv.process_img_pair, n_cpus=8 )


main()
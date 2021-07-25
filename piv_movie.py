from openpiv import tools, pyprocess, validation, filters, scaling

import cv2, os, sys

import extract_frames as ef 
import rename_images as ri
import process_img_pair as piv
import save_figures as fig

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

  # Rename images accoriding to a-b pairs
  ri.rename_images(input_dir)
  
  # Make directories to hold PIV results.

  results_dir = input_dir.rpartition('/')[0]
  results_dir = results_dir.rpartition('/')[0]
  results_dir = results_dir.rpartition('/')[0] + '/data'
  os.mkdir(results_dir)
  os.mkdir(results_dir + '/results')

  # Process images using OpenPIV. Save results as text file.
  file_name = os.listdir(input_dir)[0]
  name, number, frame, ext = file_name.split('.')
  pattern_a = name + '.*.a.' + ext
  pattern_b = name + '.*.b.' + ext

  task = tools.Multiprocesser(
      data_dir = input_dir,
      pattern_a= pattern_a,
      pattern_b=pattern_b
      )

  task.run( func = piv.process_img_pair, n_cpus=8 )

  # Plot results and save image.
  piv_results = input_dir.rpartition('/')[0].rpartition('/')[0].rpartition('/')[0]
  os.mkdir(piv_results +'/img/piv/')
  fig.save_piv_figures(piv_results)

  # Save input images and resulting images as one image.
  cfd_images = fig.read_cfd_images(piv_results + '/img/input/')
  piv_images = fig.read_piv_images(piv_results + '/img/piv/')
  print(len(cfd_images), len(piv_images))
  print(cfd_images[0].size, piv_images[0].size)  

  merged_images = fig.merge_images(cfd_images, piv_images)

  print(len(merged_images), merged_images[0].size)

  # Compose images into a movie.
  fig.img_to_mp4(merged_images)

main()
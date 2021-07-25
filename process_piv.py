
import cv2, os, sys

import extract_frames as ef 
import rename_images as ri

def main():
  # Check for valid input
  if (len(sys.argv) == 1):
    raise Exception('Provide video file to process')

  # Extract frames from video file
  if (len(sys.argv) == 2):
        file_name = sys.argv[1]
        img_dir = ef.extract_frames(file_name)

  # Rename images accorind to a-b pairs
  ri.rename_images(img_dir)
  


main()
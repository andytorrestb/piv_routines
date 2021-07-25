import os

def process_img_number(number):
  while len(number) < 4:
    number = "0" + number
  return number

def rename_images( path ):
  """Re-name images in given path so they are set up for processing in pairs.
     This is in preparation for the batch jobs. This assumes files are named
     according to the following format and numbered in order starting at 0000.

     This exact format is important for two reasons.
        First, the periods (.) will be used split the string for processing
        Second, the frames will be split into a nd b pairs according to even
        or odd numbering.   

     '<case_name>.<frame_number>.<file_extension>' 
  """

  # Save a sorted list of files
  files = sorted(os.listdir(path))

  for img in files:
    # Unpack name info
    name, number, ext = img.split('.', 3)

    # Logic used to determine renaming of file.
    even_number = int(number) % 2 == 0
    not_last_file = int(number) < len(files) - 1

    if even_number & not_last_file:


      # Process new number: used to re-name file (frame a).
      new_num = str(int(number) // 2)
      new_num = process_img_number(new_num)

      # Process next number: used as frame b
      next_num = str(int(number) + 1)
      next_num = process_img_number(next_num)

      # Names of new files
      file_a = name + '.' + new_num + '.a.'  + ext
      file_b = name + '.' + new_num + '.b.'  + ext

      # Name of file used to supply frame b
      next_image = name + '.' + next_num + '.' + ext 

      # Print info
      print(
          'orginal number',
           number,
          'next number',
          next_num,
          'new_number',
           new_num)
      
      print('Original files ===>', img, next_image)

      print('New files ===>', file_a, file_b)

      print('')

      # Rename files
      os.rename(path + img, path + file_a)
      os.rename(path + next_image, path + file_b)


def main():
  # print('hello')
  rename_images('./test/')



main()
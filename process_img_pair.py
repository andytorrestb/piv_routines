from openpiv import tools, pyprocess, validation, filters, scaling
import numpy as np

def process_img_pair( args ):
  """
      Custom function used to calculate a flowfield from an image pair.
      It is fed to the Multiprocessor object and produces flowfields in batches.
  """

  # Unpack arguments. All are required.
  file_a, file_b, counter = args

  # print(file_a, file_b, counter)

  path , seperator , name = file_a.rpartition('/')
  # print(path , seperator , name)

  # read images into numpy arrays
  frame_a = tools.imread( file_a )
  frame_b = tools.imread( file_b )

  # Search parameters
  winsize = 32 # pixels, interrogation window size in frame A
  searchsize = 38  # pixels, search area size in frame B
  overlap = 17 # pixels, 50% overlap
  dt = 2e-5 # sec, time interval between the two frames

  # # --- Process Data ---
  u0, v0, sig2noise = pyprocess.extended_search_area_piv(
    frame_a.astype(np.int32),
    frame_b.astype(np.int32),
    window_size=winsize,
    overlap=overlap,
    dt=dt,
    search_area_size=searchsize,
    sig2noise_method='peak2peak',
  )
  
  u1, v1, mask = validation.sig2noise_val(
    u0, v0,
    sig2noise,
    threshold = 1.05,
    )
  
  u2, v2 = filters.replace_outliers(
    u1, v1,
    method='localmean',
    max_iter=3,
    kernel_size=3,
  )

  # get window centers coordinates
  x, y = pyprocess.get_coordinates(
    image_size=frame_a.shape,
    search_area_size=searchsize,
    overlap=overlap,
  )

  # Scale data
  scaling_factor = 5
  x, y, u3, v3 = scaling.uniform(
      x, y, u2, v2,
      scaling_factor = scaling_factor,  # 96.52 pixels/millimeter
  )

  # 0,0 shall be bottom left, positive rotation rate is counterclockwise
  x, y, u3, v3 = tools.transform_coordinates(x, y, u3, v3)  
  
  # save to a file
  case_name, f_num, letter, ext = name.split('.')
  path = path.rpartition('/')[0]
  filename = path.rpartition('/')[0] + '/data/results/' + case_name + '.' + f_num + '.' + 'txt'
  print('finished processing ', filename)
  tools.save(x, y, u3, v3, mask, filename)
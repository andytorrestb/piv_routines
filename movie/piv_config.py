#!/usr/bin/env python

basic_params = {
  'winsize': 32,
  'searchsize': 38,
  'overlap': 17,
  'dt': 2e-5
}

validation_params = {
  'using': True,
  'threshold': 1.05
}

outlier_params = {
  'using': True,
  'method': 'localmean',
  'max_iter': 3,
  'kernel_size': 3
}

scaling_params = {
  'using': True,
  'scale': 5
}

video_params = {
  'size': 800
}

cropping_params = {
  'crop': False,
  'pos': None,
  'l_x_max': 0,
  'c_x_max': 0
}

params = {
  'basic': basic_params,
  'validation': validation_params,
  'outliers': outlier_params,
  'scale': scaling_params,
  'video': video_params,
  'crop': cropping_params
}

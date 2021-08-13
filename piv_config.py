#!/usr/bin/env python
# import preprocessing

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

params = {
  'basic': basic_params,
  'validation': validation_params,
  'outliers': outlier_params,
  'scale': scaling_params
}

use_anonymous = True
# IMAGES = {
#     'path_to_dir':'../../openpiv-python-examples/test1',
#     'file_a':'exp1_001_a.bmp',
#     'file_b':'exp1_001_b.bmp',
# }
IMAGES = {
    'path_to_dir':'../../openpiv-python-examples/test9/',
    'file_a':'karman_16Hz_000_A.jpg',
    'file_b':'karman_16Hz_000_B.jpg',
}

PIV_CROSS_CORR = {
    'winsize': 32,
    'searchsize': 38,
    'overlap': 17,
    'dt': 0.02, 
    'sig2noise_method':'peak2peak',
}

SIG2NOISE_VAL = {
    'threshold': 1.05,
}

REPLACE_OUTLIERS = {
    'method':'localmean',
    'max_iter': 3,
    'kernel_size': 3,
}

SCALE_UNIFORM = {
    'scaling_factor':96.52
}

DISPLAY_RESULTS = {
    'scale':50,
    'width':0.0035,
    'on_img': True
}

SAVE_RESULTS = {
    'fname': 'karman_16Hz_000'
}
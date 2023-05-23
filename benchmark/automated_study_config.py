INPUT_DATA = {
    # 'path_to_dir':'../../openpiv-python-examples/test16/',
    # 'file_a':'exp1_001_b.bmp',
    # 'file_b':'exp1_001_c.bmp',
    # 'results':'exp1_001_b.txt' 
    'path_to_dir':'../../openpiv-python-examples/test17/',    
    'file_a':'frame_a.png',
    'file_b':'frame_b.png',
    'results':'ground-truth.txt' 
}

PIV_CROSS_CORR = {
    'winsize': 32,
    'searchsize': 32,
    'overlap': 0,
    'dt': 1,
    'sig2noise_method':'peak2peak',
}

SIG2NOISE_VAL = {
    'threshold': 0.95,
}

REPLACE_OUTLIERS = {
    'method':'disk',
    'max_iter': 3,
    'kernel_size': 3,
}

SCALE_UNIFORM = {
    'scaling_factor':1
}

DISPLAY_RESULTS = {
    'scale':50,
    'width':0.0035,
    'on_img': True
}

# SAVE_RESULTS = {
#     'fname': 'karman_16Hz_000'
# }
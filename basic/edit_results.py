import pandas as pd
import process_img_pair_config as config

results = pd.read_csv(
    config.IMAGES['path_to_dir'] + 'karman_16Hz_000_A.jpg.txt',
    delimiter = '\t'
    )
# print(results)

mask = results.pop("mask")    

results['flags'] = 0.000

results['mask'] = mask

print(results)

results.to_csv(
    'edited-karman_16Hz_000_A.txt',
    sep = '\t',
    index = False,
)
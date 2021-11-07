import os
import save_figures as fig
from data_reader import DataReader

def merge_results(path):
  sorted_files = sorted(os.listdir(path + 'left'))
  rebuilt_img = []
  dr = DataReader()

  for file_name in sorted_files:
    print('')
    l_img = dr.load_pandas(path + 'left/' + file_name)
    c_img = dr.load_pandas(path + 'center/' + file_name)
    r_img = dr.load_pandas(path + 'right/' + file_name)

    print(type(l_img), type(c_img), type(r_img))

    img = l_img.append(c_img).append(r_img)
    print(type(img))

    dump_name = 'dump.' + file_name
    img.to_csv(
        path + dump_name,
        sep =' ',
        header = True,
        quotechar = ' ',
        index = False)
    
    result_name = 'result.' + file_name

    dump = open(path + dump_name, 'r+')
    result = open(path + result_name, 'w')
    
    header = "# " + dump.readline()
    body = dump.read()

    result.write(header)
    result.write(body)
    
    dump.close()
    result.close()

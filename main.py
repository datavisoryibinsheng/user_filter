import os
import argparse
from util import write_csv_to_file
from util import load_data_from_csv
from util import read_xlsx

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', default='tmp/dv_input')
parser.add_argument('--output_dir', default='tmp/dv_output')
parser.add_argument('--client_dir_name', default='client')
parser.add_argument('--dv_dir_name', default='dv')
ns = parser.parse_args()

if __name__ == '__main__':
    # create dirs
    client_root = os.path.join(ns.input_dir, ns.client_dir_name)
    dv_root = os.path.join(ns.input_dir, ns.dv_dir_name)
    for root, subdirs, files in os.walk(dv_root):
        try:
            os.mkdir(root.replace('dv_input', 'dv_output'))
        except FileExistsError as e:
            pass

    # establish b
    b = set()
    for root, subdirs, files in os.walk(client_root):
        for file in files:
            if '.' not in file:
                continue
            if file.endswith('.xlsx'):
                path = os.path.join(root, file)
                t = read_xlsx(path)
            elif file.endswith('.csv'):
                path = os.path.join(root, file)
                (header, t) = load_data_from_csv(path)
            else:
                continue

            for row in t:
                if 'AppsFlyer ID' in row:
                    b.add(row['AppsFlyer ID'])

    for root, subdirs, files in os.walk(dv_root):
        for file in files:
            if '.' not in file or not file.endswith('.csv'):
                continue
            path = os.path.join(root, file)
            opath = os.path.join(path.replace('dv_input', 'dv_output'))
            header, a = load_data_from_csv(path)
            a = [row for row in a if 'user_id' in row and row['user_id'] not in b]
            write_csv_to_file(opath, header, a)

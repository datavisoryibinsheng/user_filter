import argparse
import json
import os

from util import uniform_read
from util import uniform_write

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', default='tmp/dv_input')
parser.add_argument('--output_dir', default='tmp/dv_output')
parser.add_argument('--client_dir_name', default='client')
parser.add_argument('--client_key_col', default='AppsFlyer ID')
parser.add_argument('--our_key_col', default='user_id')
parser.add_argument('--dv_dir_name', default='dv')
ns = parser.parse_args()

if __name__ == '__main__':
    # create dirs
    client_root = os.path.join(ns.input_dir, ns.client_dir_name)
    dv_root = os.path.join(ns.input_dir, ns.dv_dir_name)
    for root, subdirs, files in os.walk(dv_root):
        try:
            os.makedirs(root.replace('dv_input', 'dv_output'))
        except FileExistsError as e:
            pass

    # establish b
    b = set()
    for root, subdirs, files in os.walk(client_root):
        for file in files:
            if '.' not in file:
                continue
            path = os.path.join(root, file)
            _, t = uniform_read(path)
            for row in t:
                if ns.client_key_col in row:
                    b.add(row[ns.client_key_col])

    for root, subdirs, files in os.walk(dv_root):
        for file in files:
            path = os.path.join(root, file)
            opath = os.path.join(path.replace('dv_input', 'dv_output'))
            header, a = uniform_read(path)
            a = [row for row in a if ns.our_key_col in row and row[ns.our_key_col] not in b]
            uniform_write(opath, a, header)


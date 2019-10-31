import os

targets = ['tmp/dv_input/dv', 'tmp/dv_input/client', 'tmp/dv_output']

for target in targets:
    try:
        os.mkdir(target)
    except FileExistsError:
        print("{} exist!".format(target))
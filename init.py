import os

targets = ['tmp/dv_input/dv', 'tmp/dv_input/client']

for target in targets:
    try:
        os.makedirs(target)
    except FileExistsError:
        print("{} exist!".format(target))

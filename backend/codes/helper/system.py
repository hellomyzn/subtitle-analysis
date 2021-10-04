import sys
import os

import glob


def get_args(num):
    args = sys.argv
    try:
        return args[num]
    except:
        print(str.upper("***   choose file which you want to try   ***"))
        exit()


def get_files_name(folder_path):
    files = []
    for f in glob.glob(folder_path + "/*"):
        files.append(os.path.split(f)[-1])

    return files


def make_dir(path, dir_name):
    os.mkdir(path + dir_name)
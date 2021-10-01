import os
import shutil


def main():
    data_dir = 'data'

    shutil.rmtree(data_dir)
    os.mkdir(data_dir)

if __name__ == "__main__":
    main()
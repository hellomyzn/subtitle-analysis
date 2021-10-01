import os
import shutil


def main():
    csvs_dir = 'data'
    noises_dir = 'noises'

    shutil.rmtree(csvs_dir)
    os.mkdir(csvs_dir)

    shutil.rmtree(noises_dir)
    os.mkdir(noises_dir)

if __name__ == "__main__":
    main()
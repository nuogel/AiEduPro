import os
import glob


def rename(dir):
    path_list = glob.glob(os.path.join(dir, '*.ass'))
    for path in path_list:
        basedir = os.path.dirname(path)
        basename = os.path.basename(path)
        tmp = os.path.basename(path).split('.')
        des_path = os.path.join(basedir, tmp[0].lower() + tmp[1].lower() + '.' + tmp[2].lower() + '.' + tmp[-1])
        # des_path = os.path.join(basedir, basename.lower())
        os.rename(path, des_path)


if __name__ == '__main__':
    rename(dir)

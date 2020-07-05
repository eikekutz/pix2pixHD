import os
import argparse
import numpy as np
from shutil import copyfile


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='seperate dir  with random idx')
    parser.add_argument('--dataroot_old', type=str)
    parser.add_argument('--dataroot_new', type=str, default=None)
    parser.add_argument('--del_old_dir', type=str2bool, default=False)
    args = parser.parse_args()
    if not args.dataroot_new:
        args.dataroot_new = os.path.split(args.dataroot_old)[0]
    root, dirs, files = next(os.walk(args.dataroot_old))
    files = [x for x in sorted(files) if x != '.DS_Store']
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    print(files)
    ix = np.random.choice(len(files), len(files), False)
    a, b = np.split(ix, [int(len(files) * 0.5)])
    print(a)
    print(b)
    # create dirs
    # sep_train_A
    path_1_mask = os.path.join(args.dataroot_new, 'sep_train_A')
    path_1_img = os.path.join(args.dataroot_new, 'sep_train_B')
    path_2_mask = os.path.join(args.dataroot_new, 'sep_train_A_2')
    path_2_img = os.path.join(args.dataroot_new, 'sep_train_B_2')

    os.makedirs(path_1_mask, exist_ok=True)
    os.makedirs(path_1_img, exist_ok=True)
    os.makedirs(path_2_mask, exist_ok=True)
    os.makedirs(path_2_img, exist_ok=True)

    for i in a:
        src = os.path.join(args.dataroot_old, files[i])
        dst = os.path.join(path_1_mask, files[i])
        copyfile(src, dst)
        src = os.path.join(os.path.split(args.dataroot_old)[0], 'train_B', files[i])
        dst = os.path.join(path_1_img, files[i])
        copyfile(src, dst)
    for i in b:
        src = os.path.join(args.dataroot_old, files[i])
        dst = os.path.join(path_2_mask, files[i])
        copyfile(src, dst)
        src = os.path.join(os.path.split(args.dataroot_old)[0], 'train_B', files[i])
        dst = os.path.join(path_2_img, files[i])
        copyfile(src, dst)

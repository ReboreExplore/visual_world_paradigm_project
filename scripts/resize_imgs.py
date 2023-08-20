import os
import cv2
import glob
import argparse

import tqdm

# this script resizes all images in the 'path' directory to the desired image 
# size (default: 256x256)

ag = argparse.ArgumentParser()
ag.add_argument('-p', '--path', help='path to image folder', default='./', type=str)
ag.add_argument('-s', '--size', help='size of resized image', default=256, type=int)
ag.add_argument('-r', '--rename', help='rename resized images by appending _resized to filename', action='store_true')
ag.add_argument('-o', '--output', help='output folder', default='./resized', type=str)
args = vars(ag.parse_args())

# ensure output folder exists
if not os.path.exists(args['output']):
    os.makedirs(args['output'])

# path to image folder
path = args['path']
size = (args['size'], args['size'])

# get list of images in folder with extension .png
img_list = glob.glob(path + '*.png')

# resize images (maintain aspect ratio)
for img_path in tqdm.tqdm(img_list):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    print(img.shape)
    img = cv2.resize(img, size)
    # add resized string to filename
    if args['rename']:
        img_path = img_path.split('.')[0] + '_resized.png'
    cv2.imwrite(os.path.join(args['output'], os.path.basename(img_path)), img)
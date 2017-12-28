import argparse
import cv2
import sys
import os
import fnmatch
import re

ap = argparse.ArgumentParser()
ap.add_argument('-id', '--idir', required=True, help='Path to image')
args = vars(ap.parse_args())

# a function you may want to use in debugging
def display_image_pix(image, h, w):
    image_pix = list(image)
    for r in xrange(h):
        for c in xrange(w):
            print list(image_pix[r][c]), ' ',
        print

# luminosity conversion
def luminosity(rgb, rcoeff=0.2126, gcoeff=0.7152, bcoeff=0.0722):
    return rcoeff*rgb[0]+gcoeff*rgb[1]+bcoeff*rgb[2]

def compute_avrg_luminosity(imagepath):
    image = cv2.imread(imagepath)
    (i_height, i_width, i_num_channels) = image.shape
    total_luminosity = 0
    image_by_pixel = list(image)
    for row in xrange(i_height):
        for column in xrange(i_width):
            total_luminosity += luminosity(list(image_by_pixel[row][column]))
    return total_luminosity/(i_height*i_width)

def gen_avrg_lumin_for_dir(imgdir, filepat):
    for path, dir_list, image_list in os.walk(imgdir):
        for image_name in fnmatch.filter(image_list, filepat):
            image_path = os.path.join(path, image_name)
            yield (image_path.replace('/home/pi/Desktop/Assignment_07/beepix/morepix/pix/', ''), compute_avrg_luminosity(image_path))

# run ghe generator and output into STDOUT
for fp, lum_avrg in gen_avrg_lumin_for_dir(args['idir'], r'*.png'):
    sys.stdout.write(fp+'\t'+str(lum_avrg)+'\n')
    sys.stdout.flush()

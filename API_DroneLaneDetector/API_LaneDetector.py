import argparse
import cv2
import numpy
import math
import sys
import os
import fnmatch

def line_deg_angle(x1, y1, x2, y2):
    return math.atan2(y2-y1, x2-x1) * (180 / numpy.pi)

def is_angle_in_range(a, ang_lower, ang_upper):
    if a >= ang_lower and a <= ang_upper:
        return True
    else:
        return False

def is_vertical_lane(x1, y1, x2, y2, ang_lower, ang_upper):
    return is_angle_in_range(line_deg_angle(x1, y1, x2, y2), ang_lower, ang_upper)

def is_horizontal_lane(x1, y1, x2, y2, ang_lower, ang_upper):
    return is_angle_in_range(line_deg_angle(x1, y1, x2, y2), ang_lower, ang_upper)

def filter_vertical_lines(lines, ang_lower=-10, ang_upper=10):
    return [(x1,y1,x2,y2) for (x1,y1,x2,y2) in lines if is_vertical_lane(x1,y1,x2,y2, ang_lower, ang_upper)]

def filter_horizontal_lines(lines, ang_lower=80, ang_upper=100):
    return [(x1,y1,x2,y2) for (x1,y1,x2,y2) in lines if is_horizontal_lane(x1,y1,x2,y2, ang_lower, ang_upper)]

def detect_lines_in_image(image_path, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap):
    image = cv2.imread(image_path) ## read the image
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) ## grayscale
    edges = cv2.Canny(gray, 50, 150, apertureSize=3) ## detect edges
    lines = cv2.HoughLinesP(edges, rho_accuracy, theta_accuracy, num_votes, min_len, max_gap) ## detect hough lines
    if lines == None:
        return (0, 0)
    x, y, z = lines.shape # converts 3D numpy array into a 2D python list
    lines.shape = (x, z)
    ll_lines = filter_vertical_lines(lines)
    rl_lines = filter_horizontal_lines(lines)
    return (len(ll_lines), len(rl_lines))
    
def find_lanes_in_images_in_dir(imgdir, filepat, rho_acc, th_acc, num_votes, min_len, max_gap):
    for path, dir_list, image_list in os.walk(imgdir):
        for image_name in fnmatch.filter(image_list, filepat):
            image_path = os.path.join(path, image_name)
            yield (image_path, detect_lines_in_image(image_path, rho_acc, th_acc, num_votes, min_len, max_gap))


test_output = False

for fp, ll_rl in find_lanes_in_images_in_dir(sys.argv[1], '*.png', 1, numpy.pi/180, 50, 100, 15):            
    fp = fp.strip('/home/pi/Desktop/')
    fp = fp.strip('.png')
    
    if test_output:
        if ll_rl[0] > 0 and ll_rl[1] > 0:
            print fp, ll_rl[0], ll_rl[1], '\t', 'CROSS'
        elif ll_rl[0] > 0 or ll_rl[1] > 0:
            print fp, ll_rl[0], ll_rl[1], '\t', 'LANE'
        elif ll_rl[0] == 0 and ll_rl[1] == 0:
            print fp, ll_rl[0], ll_rl[1], '\t', 'CARPET'
        else:
            print fp, ll_rl[0], ll_rl[1], '\t', 'NOTHING'
    else:
        if ll_rl[0] > 0 and ll_rl[1] > 0:
            print fp, '\t', 'CROSS'
        elif ll_rl[0] > 0 or ll_rl[1] > 0:
            print fp, '\t', 'LANE'
        elif ll_rl[0] == 0 and ll_rl[1] == 0:
            print fp, '\t', 'CARPET'
        else:
            print fp, '\t', 'NOTHING'

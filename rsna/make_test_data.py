import pandas as pd
import numpy as np
import pydicom
import pylab
import os
from glob import glob
import matplotlib.pyplot as plt
from PIL import Image

DCM_FILE_FMT = '/home/ubuntu/rsna/stage_1_test_images/{}.dcm'
IMAGE_FILE_FMT = '/home/ubuntu/rsna/testdata/{}.jpg'
TEST_FILES = '/home/ubuntu/rsna/stage_1_test_images/*.dcm'

def make_training_image_file(pid, f):
    dcmpath = DCM_FILE_FMT.format(pid)
    dcmdata = pydicom.read_file(dcmpath)
    img = np.stack([dcmdata.pixel_array] * 3, axis=2)
    jpg_path = IMAGE_FILE_FMT.format(pid)
    Image.fromarray(img).save(jpg_path)
    f.write('{}\n'.format(jpg_path))

df = pd.DataFrame({'file':glob(TEST_FILES)})

f = open('rsna_detect.txt', 'w')

for _, row in df.iterrows():
    make_training_image_file(os.path.splitext(os.path.basename(row[0]))[0], f)

f.close()



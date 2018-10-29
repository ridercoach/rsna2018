import pandas as pd
import numpy as np
import pydicom
#import pylab
#import matplotlib.pyplot as plt
from PIL import Image
from sklearn.model_selection import train_test_split

DCM_FILE_FMT = '/home/ubuntu/rsna/stage_1_train_images/{}.dcm'
IMAGE_FILE_FMT = '/home/ubuntu/rsna/data/{}.jpg'
LABEL_FILE_FMT = '/home/ubuntu/rsna/data/{}.txt'
LIST_FILE_FMT = '/home/ubuntu/rsna/rsna_{}.txt'

def make_training_image_file(pid):
    dcmpath = DCM_FILE_FMT.format(pid)
    dcmdata = pydicom.read_file(dcmpath)
    img = np.stack([dcmdata.pixel_array] * 3, axis=2)
    Image.fromarray(img).save(IMAGE_FILE_FMT.format(pid))
    
def make_training_label_file(pid, x, y, w, h):
    f = open(LABEL_FILE_FMT.format(pid), "w")
    # x, y are top left corner, must be converted to center
    # all dims must be converted from pixels to fraction of image size
    x = (x + w/2) / 1024
    y = (y + h/2) / 1024
    w /= 1024
    h /= 1024
    f.write('0 {} {} {} {}\n'.format(x, y, w, h))
    f.close()


df_lbl = pd.read_csv('stage_1_train_labels.csv')
df_lbl_pos = df_lbl[df_lbl['Target'] == 1]
print(df_lbl_pos.shape[0], 'bounding boxes for', df_lbl_pos['patientId'].nunique(), 'unique patients')

df_boxes = df_lbl_pos.groupby('patientId').size().reset_index(name='boxes')
df_comb1 = pd.merge(df_lbl_pos, df_boxes, on='patientId')
df_onebox = df_comb1[df_comb1['boxes'] == 1]
print(df_onebox.shape[0], 'patients with one box')
print(df_onebox['boxes'].nunique(), 'unique value(s) in boxes column')
print(df_onebox.head())

df_train = df_onebox

#for _, row in df_train.iterrows():
#    pid, x, y, w, h = row[0:5]
#    make_training_image_file(pid)
#    make_training_label_file(pid, x, y, w, h)

df_all = df_onebox.sample(2000)

df_train, df_test = train_test_split(df_all, test_size=.3, random_state=42)
print(df_train.shape[0], 'images in training set')
print(df_test.shape[0], 'images in test set')

s_onebox = set(df_onebox['patientId'])
s_train = set(df_train['patientId'])
s_test = set(df_test['patientId'])
s_leftover = s_onebox - (s_train | s_test)

print('{} {} {} {}\n'.format(len(s_onebox), len(s_train), len(s_test), len(s_leftover)))

print('len(s_train & s_test):', len(s_train & s_test))
print('len(s_train & s_leftover):', len(s_train & s_leftover))
print('len(s_test & s_leftover):', len(s_test & s_leftover))

f = open(LIST_FILE_FMT.format('train'), "w")
for _, row in df_train.iterrows():
    f.write(IMAGE_FILE_FMT.format(row[0]) + '\n')
f.close()

f = open(LIST_FILE_FMT.format('test'), "w")
for _, row in df_test.iterrows():
    f.write(IMAGE_FILE_FMT.format(row[0]) + '\n')
f.close()

f = open(LIST_FILE_FMT.format('leftover'), "w")
for pid in s_leftover:
    f.write('{}\n'.format(pid))
f.close()


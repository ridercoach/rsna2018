# rsna2018  ** under construction **
Notes, etc, for Kaggle RSNA Pneumonia Detection Challenge

This repository contains the basic file structure and most of the files 
used for my entry in the competition.  It does not include the files 
that take a lot of space, such as the weights file and the full set 
of data files. In general, the "darknet" directory pertains to the training 
and use of the model, and the "rsna" directory pertains to the pre- and
post-processing of the data. The Jupyter notebook in the root of the
repository just illustrates some of the explanation given here.

I used the Darknet framework with the "regular" version of the YOLOv2
model. I started with the yolov2.weights file and trained for 12,300 
iterations with 2000 (1400 training, 600 test) of the labeled images 
provided by RSNA. I did the training on an AWS p2.xlarge EC2 instance, 
which took about 24 hours.  I scored .098 (top score .260).

### Table of Contents

[1. Exploratory Data Analysis (EDA)](link)

[2. Setting Up the Model](link)

## 1. Exploratory Data Analysis (EDA)

some text here

## 2. Setting Up the Model

more text here

## 3. Prepare Training Data

blah blah blah

## 4. Train the Model

Bleep bleep

## 5. Generate Predictions

hahaha

## 6. Prepare Submission

heehee





# rsna2018  ** under construction **
Notes, etc, for Kaggle RSNA Pneumonia Detection Challenge

This repository contains a minimal set of files related to the 
explanation in this README. 
The "darknet" directory pertains to the training 
and use of the model, and the "rsna" directory pertains to the pre- and
post-processing of the data. The Jupyter
[notebook](https://github.com/ridercoach/rsna2018/blob/master/rsna2018-notes.ipynb)
 in the root of the
repository illustrates some of the explanation given here.

I used the Darknet framework with the "regular" version of the YOLOv2
model. I started with the yolov2.weights file and trained for 12,300 
iterations with 2000 (1400 training, 600 test) of the labeled images 
provided by RSNA. I did the training on an AWS p2.xlarge EC2 instance 
($0.90/hr), which took about 24 hours.  I scored .098 (top score .260). It 
occurred to me after the contest closed that I might have scored better 
if I had lowered the detection threshold when running the model; by 
default, it reports only objects it is at least 25% confident about. 

If you start exploring YOLO you will find that there is a huge amount 
of information available. However, in my opinion, the best initial 
introduction is probably [this page](https://pjreddie.com/darknet/yolo) 
from Joseph Redmon, who is one of the creators of YOLO.

I worked in Linux, but I think most of what is discussed here could be 
done in Windows too.  In particular, 
[this page](https://github.com/AlexeyAB/darknet) by AlexeyAB has a wealth 
of Darknet/YOLO how-to information for both Windows and Linux.

### Table of Contents

[Exploratory Data Analysis (EDA)](#exploratory-data-analysis)   
[Setting Up the Model](#setting-up-the-model)   
[Prepare Training Data](#prepare-training-data)   
[Train the Model](#train-the-model)   
[Generate Predictions](#generate-predictions)   
[Prepare Submission](#prepare-submission)   
[Ideas for Future Work](#ideas-for-future-work)   

## Exploratory Data Analysis

I did a few notebooks (called "kernels" on Kaggle) of
EDA work, one of which I made public
[(link).](https://www.kaggle.com/ridercoach/rsna2018-ridercoach-eda-1)
However, while this work was definitely worthwhile and a good learning 
experience, in the end I did not use any of the ideas I got from it, 
so I will not include it here.

## Setting Up the Model

### Installing and Testing Darknet

[This page](https://pjreddie.com/darknet/install) gives instructions for 
installing Darknet on Linux, which is very easy.  Then, 
[this page](https://pjreddie.com/darknet/yolo) gives instructions for 
trying out YOLO on the included sample images (or any image you want, 
as long as it is a JPG.)

Note that to use YOLO you must specify a neural network configuration 
(.cfg file) and a **matching** set of trained parameters (.weights file.) 
"Matching" means that the set of parameters in the .weights file is 
compatible with the structure of the network in the .cfg file -- the 
actual base filenames don't have to be the same, but it's helpful 
if they indicate the pairing. 
There are lots of configurations to choose from in the "cfg" subdirectory 
of the Darknet installation, but the weights files are **not** included 
because they are huge. You can download the one you want from the 
second page linked above. It generally goes right in the "darknet" 
directory, not in a subdirectory.

### Customizing the .cfg file

It may be that one of the standard YOLO configurations is perfect for 
what you are doing, but for this project we have to make some changes.

First, ...

## Prepare Training Data

### Downloading the Training Data

To work with Kaggle contest data on your own computer, you will 
need the Kaggle API; [this page](https://github.com/Kaggle/kaggle-api)
gives instructions for installing and using it.

Once you have the Kaggle API working, the following command would 
download the contest data files to your current directory (assuming 
that (a) the contest is active, and (b) you have already entered 
the competition on the Kaggle website and accepted the rules.)

```
kaggle competitions download rsna-pneumonia-detection-challenge
```

### Converting Training Data to YOLO Format

blah blah blah

## Train the Model

Bleep bleep

## Generate Predictions

hahaha

## Prepare Submission

heehee

## Ideas for Future Work

If I were to continue on this project (and I probably won't, because 
despite how much fun it was, I want to move on to learning other things,) 
here are a few things I might work on.

First, in terms of trying to improve my score (which is moot because 
the contest is closed,) I might:

1. try a lower detection threshold (default is 25% confidence -- maybe too high for a problem this difficult)   
2. try different anchor boxes (I did some EDA about this)   
3. try training longer and with more images (I used only 2000 of the 5000+ available)   
4. try preprocessing the images in some way   
5. maybe try YOLOv3   

Second, in terms of exploring YOLO beyond this particular contest, 
I might spend more time working with Allan Zelener's
[YAD2K](https://github.com/allanzelener/YAD2K) package, which 
converts a Darknet .cfg/.weights file pair into a Keras/Tensorflow 
model stored in an .h5 file.  I spent a lot of time on this during the 
contest because I think Keras is pretty nice and I would like to 
improve my knowledge of it, but I ended up not using it.







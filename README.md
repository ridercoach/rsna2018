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

[This page](https://pjreddie.com/darknet/install) gives instructions for 
installing Darknet on Linux, which is very easy.  Then, 
[this page](https://pjreddie.com/darknet/yolo) gives instructions for 
trying out YOLO on the included sample images (or any image you want, 
really, as long as it is a JPG.)

Understand that to use YOLO you must specify a neural network configuration 
(.cfg file) and a _matching_ set of trained parameters (.weights file.) 
There are lots of configurations to choose from in the "cfg" subdirectory 
of the Darknet repository, but the weights files are _not_ included 
because they are huge. You can download the one you want from the 
second page linked above.

## Prepare Training Data

blah blah blah

## Train the Model

Bleep bleep

## Generate Predictions

hahaha

## Prepare Submission

heehee

## Ideas for Future Work

hohoho





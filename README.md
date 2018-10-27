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

### Table of Contents

[Exploratory Data Analysis (EDA)](#exploratory-data-analysis)   
[Setting Up the Model](#setting-up-the-model)   
[Prepare Training Data](#prepare-training-data)   
[Train the Model](#train-the-model)   
[Generate Predictions](#generate-predictions)   
[Prepare Submission](#prepare-submission)   
[Ideas for Future Work](#ideas-for-future-work)   

## Exploratory Data Analysis

I did a few different notebooks of EDA work, one of which I made public 
on Kaggle [(link).](https://www.kaggle.com/ridercoach/rsna2018-ridercoach-eda-1) However, while this work was definitely worhtwhile, and a good learning 
experience, in the end I ran out of time and did not use any of what I 
learned from it, so I will not include it here.

## Setting Up the Model

more text here

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





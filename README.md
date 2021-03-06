# rsna2018
Notes, etc, for Kaggle RSNA Pneumonia Detection Challenge

This repository contains only the files essential 
to the explanation in this README. 
The "darknet" directory relates to the training 
and use of the model, and the "rsna" directory to the 
contest data. The Jupyter
[notebook](https://github.com/ridercoach/rsna2018/blob/master/rsna2018-notes.ipynb)
 in the root of the
repository presents a small sample of x-ray images, comparing model 
predictions to human diagnoses.

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

I did this project on Linux, but I think most of what is discussed
here could be done on Windows too. For more information, 
[this page](https://github.com/AlexeyAB/darknet) by AlexeyAB has a wealth 
of Darknet/YOLO how-to information for both Windows and Linux.

### Table of Contents

[Exploratory Data Analysis (EDA)](#exploratory-data-analysis)   
[Setting Up the Model](#setting-up-the-model)   
[Preparing Training Data](#preparing-training-data)   
[Training the Model](#training-the-model)   
[Generating Predictions](#generating-predictions)   
[Submitting Results](#submitting-results)   
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
trying out YOLO on the included sample images.

Using YOLO requires a neural network configuration 
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

### Customizing the Darknet Installation

It may be that one of the standard YOLO configurations is perfect for 
what you are doing, but for this project we have to make some changes. 
Some of these changes are in the .cfg file, and we would like to 
preserve the generic configuration in case we want to go back to it, 
so we will copy yolov2.cfg into rsna.cfg and work with that.

#### _Number of Classes Detected_

The generic YOLOv2 configuration detects 80 different kinds of 
objects (dog, bicycle, horse, etc), and we need to detect only one 
(pneumonia). So we make two changes in rsna.cfg, both near
the bottom of the file. 
First, in the "[region]" section, "classes=80" must be changed to 
"classes=1". Then, in the section just above that (the last "[convolutional]" 
layer of the network), "filters=425" must be changed to "filters=30".

Understanding this "filters" change gets 
into some of the details about how YOLO works, which is really 
interesting but probably not something to include in this procedure 
document.

(The number of classes being detected is also referenced in the 
rsna.data file mentioned below under "Setting Up Input Files")

#### _Using the GPU_

One big reason I used an AWS p2.xlarge type instance is because it 
has a GPU, which **_greatly_** speeds up the training process. 
However, in order to take advantage of the GPU, the Darknet framework 
must be compiled for it. To do this, edit the Makefile in the "darknet" 
directory, change the first line from "GPU=0" to "GPU=1", and do "make",
just as when you initially installed Darknet.

Note that for Darknet to use the GPU, the system must also have CUDA 
installed. I did not have to do this myself because when I created 
the cloud machine I used one of the "Deep Learning" AMIs, which 
already has it.

#### _Producing the Output Required for the Competition_

Out of the box, the Darknet framework will print to the screen the 
class type and confidence level for each object it finds, but not 
the box coords, and we need these for the RSNA submission file.

To fix this, go into the "darknet/src" directory, edit image.c, and 
add the `printf` statement shown in the code fragment below. This is 
in the `draw_detections` function, just before the `draw_box_width` call, 
near line 300. Then rebuild Darknet by doing "make".

```

            if(left < 0) left = 0;
            if(right > im.w-1) right = im.w-1;
            if(top < 0) top = 0;
            if(bot > im.h-1) bot = im.h-1;

            printf("L=%d, T=%d, R=%d, B=%d\n", left, top, right, bot); 
            draw_box_width(im, left, top, right, bot, width, red, green, blue);
            if (alphabet) {
                image label = get_label(alphabet, labelstr, (im.h*.03));
                draw_label(im, top + width, left, label, rgb);
                free_image(label);
            }
```

Obviously you don't have to format your print statement exactly as 
shown above, but the script that converts the Darknet output to the 
submission file looks for it to be formatted this way.

#### _Batch Size and Subdivisions_

Two other parameters you should be aware of, in rsna.cfg near the top of the 
file, are "batch" and "subdivisions". The values often used for these
(especially if you have at least one GPU) are 
64 and 8, respectively, but when 
you first start to try training the network, you might want to set them 
both to 1 (as you can see in the commented lines in the file), to lessen 
the chances of running up against system limitations.

## Preparing Training Data

### Downloading the Contest Data

To work with Kaggle contest data on your own computer, you will 
need the Kaggle API; [this page](https://github.com/Kaggle/kaggle-api)
gives instructions for installing and using it.

Once you have the Kaggle API working, the command below will 
download the contest data files to your current directory (assuming 
that (a) the contest is active, and (b) you have already entered 
the competition on the Kaggle website and accepted the rules.) Having 
your own copy of the data is not only convenient, but 
if Kaggle removes access to the files after the contest closes 
(as seems to have been the case with the RSNA competition), you will 
still have them to work with.

```
kaggle competitions download rsna-pneumonia-detection-challenge
```

After downloading the data, you will need to unzip any archives, and 
you may want to organize things into some helpful directory structure.

### Adjusting Data Format

In order to prepare the RSNA data for ingestion by Darknet/YOLO, two 
main tasks must be accomplished: (1) the grayscale x-ray images must be 
extracted from the DICOM files and converted to 3-color JPG files, and 
(2) the ground truth box info in the CSV file must be extracted into 
individual TXT files, and converted from pixels to fractions of image 
size, with the box location changed from upper-left corner to center.

All of this work (as well as the creation of the list files mentioned 
in the next section) is accomplished by the `make_training_data.py` 
script in the "rsna/data" directory. Note that if you want to use this 
script, you will probably have to adjust the file paths,
and you may also want to change the train/test split fraction, etc.

### Setting Up Input Files

Finally, we have to tell Darknet where to look for our data. 
[This page](https://timebutt.github.io/static/how-to-train-yolov2-to-detect-custom-objects/)
gives more background about this, as well 
as additional information about the entire process described in this README.

The central file in this setup process is `darknet/cfg/rsna.data`,
which contains just 5 lines:

```
classes= 1
train  = /home/ubuntu/darknet/data/rsna_train.txt
valid  = /home/ubuntu/darknet/data/rsna_test.txt
names = /home/ubuntu/darknet/data/rsna.names
backup = /home/ubuntu/darknet/backup
```

Obviously we have classes=1. The "train" and "valid" entries point to 
the list files created by the `make_training_data.py` script in the 
previous step.  I copied those files into "darknet/data" but you could 
probably instead just point these paths to the place where the files 
already reside. The "names" entry points to a file in "darknet/data" 
that contains the names of all the classes being detected, one name 
per line. The "backup" entry is the directory in which Darknet will 
save its current set of weights after each 100 iterations.

## Training the Model

With everything set up as described above, the command below will start 
training the network.  Note that we are not training from scratch here, 
because we are starting with the yolov2.weights file downloaded from 
the Darknet site.  Rather, we are simply fine-tuning the model to detect 
the objects **_we_** need to find. (This technique of starting with ML 
parameters taken from another application is called "transfer learning".)

Note that when we start with a weights file like yolov2.weights, which 
indicates internally that training is complete, we must use "-clear 1" on 
the command line, or Darknet will simply exit because it thinks there is 
no more training to do.

```
./darknet detector train cfg/rsna.data cfg/rsna.cfg yolov2.weights -clear 1
```

The training process can take many hours.  Darknet will print to the 
screen the average prediction error after each iteration, and this number
should slowly come down. The article linked in the previous section shows 
an example of the training output.

**It is interesting to note the difference in training performance between the 
article and this project. In the article, the author is trying to detect 
something that has sharp edges, a uniform shape, and 5 colors, and he 
gets down to an average error of 0.08 with only 300 training images and 
1000 iterations. Here we are trying to detect something 
that is almost invisible to the untrained human eye and has only one 
channel of color information, and I trained for 12,300 iterations with 2000 
images and only got down to an error of around 1.5. However, this was 
good enough for the model to be moderately successful on the test set.**

You can interrupt the training process at any time by pressing 
ctrl-C.  The most recent set of saved weights will be in the backup 
directory. If you want to continue training from that point, copy 
the most recent backup weights into the "darknet" directory with some 
suitable name, and use the above command **_except_** specify the 
new weights file instead of yolov2.weights, and **_do not_** use 
"-clear 1".

## Generating Predictions

### Preparing the Test Images

RSNA provided a separate set of images for testing the algorithm, and 
for which the results are submitted and scored. Just like the training 
images, these are in DICOM files and must be extracted into JPGs. The 
script `make_test_data.py` in the "rsna" directory will do this, as well 
as create the list of filenames for doing batch detection with Darknet (which
I copied into the "darknet/data" directory.)

Note that we do not have to create the TXT label files as we did for the 
training images, because we aren't training now (and because there aren't 
any labels to convert :)).

### Running the Detection

With everything set up as described above, the command line below will 
run the batch detection.  Note that we pipe the output to a file, and it 
is this file that is processed in the next section to create the submission 
file. Note also that we specify the final weights file from the training 
process.

```
./darknet detector test cfg/rsna.data cfg/rsna.cfg rsna_12300.weights < data/rsna_detect.txt > rsna_result.txt
```

## Submitting Results

If you modified image.c as described above and did the batch detection 
on the test set as shown, then the `parse_darknet_output.py` script in the 
darknet directory of the repository should convert the batch output 
to a correct file for submission for the RSNA contest.  It's good to 
use a descriptive name for the submission file.

Then the command shown below will submit your file via the Kaggle API 
and your score will be visible almost immediately on the Kaggle website.

```
kaggle competitions submit rsna-pneumonia-detection-challenge -f rsna-ridercoach-sub02.csv
```

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



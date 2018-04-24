# TubingenSecondment
CNN using digital DVS to predict biological retina response


DATASET FOLDER:
-original video (train and test)
-DVS video - threshold contrast 1% (train and test)
-DVS video - threshold contrast 5% (train and test)
-DVS video - threshold contrast 10% (train and test)
-DVS video - threshold contrast 20% (train and test)
-jittered video - frame max jump 1 pixel (train and test)
-jittered video - frame max jump 2 pixel (train and test)

SCRIPTS FOLDER:
.PY: (spyder)
  -DVSevents_converter: tranform the original tiff files in a stream of events. Spikes converter.
  -DVSimages_converter: tranform the original tiff files in an video of differential frame. DVS frame converter.
  -create_jittered_video: import original tiff files, jitter the images, save .avi file
  -data_utils: usefull function for the other files.

.IPYNB: (jupyter notebook)
  -Preprocessing_for_DVS_image: tranform the original tiff files in an video of DVS frame. 
  -CNN_DVS: training model

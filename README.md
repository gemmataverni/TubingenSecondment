# TubingenSecondment
CNN using digital DVS to predict biological retina response


DATASET FOLDER:
-original video (train and test)
-jittered video - frame max jump 1 pixel (train and test)
-jittered video - frame max jump 2 pixel (train and test)

SCRIPTS FOLDER:
-DVSevents_converter: tranform the original tiff files in a stream of events. Spikes converter.
-DVSimages_converter: tranform the original tiff files in an video of differential frame. DVS frame converter.
-create_jittered_video: import original tiff files, jitter the images, save .avi file
-data_utils: usefull function for the other files.

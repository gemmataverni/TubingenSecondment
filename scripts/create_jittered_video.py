# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 10:18:11 2018

@author: Gemma
"""

# =============================================================================
# DIGITAL SILICON RETINA 
# =============================================================================
import tiffcapture as tc 
import numpy as np
from matplotlib import pyplot as plt
import random
import cv2
import data_utils

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def return_xy(index,side_length,jitter):
    y=(index//side_length)-jitter
    x=(index%side_length)-jitter
    return x,y

# =============================================================================
# CREATE JITTERED IMAGES
# =============================================================================
def jitterImages(filename,numbJitt,jitter,augmented_border,debug):
    
    if jitter>2:
        #max value that the frame can jump
        print("ERROR! jitter must be smaller than 2")
        return
    
    tiff = tc.opentiff(filename) #open img
    tiff_length=tiff.length
    tiff_shape=tiff.shape
    print("Number of images:", tiff_length)#number of images
    print("Image shape:", tiff_shape)#size of images
    xdim=tiff_shape[0]
    ydim=tiff_shape[1]
    
    tiff_new_shape=tiff_shape+2*augmented_border*np.ones(len(tiff_shape), dtype=np.int16)
    print("Image new shape:", tiff_new_shape)
    
    JitterVideo=[]
    x0=3 #initial position of the image, centered in the frame
    y0=3 #initial position of the image, centered in the frame
    jitter_index_max=((1+2*jitter)**2)
    jitter_sqaure=1+2*jitter
    center_index=(jitter_sqaure*(jitter_sqaure-1)/2)+(jitter_sqaure-1)/2
    
    for img in tiff:
        c=0
        mean_value=np.mean(img)
        jitterImg=np.ones(tiff_new_shape, dtype=np.int16)
        jitterImg=mean_value*jitterImg
        
        while (c<numbJitt):
            
            idex_value=np.arange(0,jitter_index_max)
            next_pixel=random.choice(idex_value)
            x,y=return_xy(next_pixel,jitter_sqaure,jitter)
            x0 += x
            y0 += y
            
            while (x0 < 0)|(x0 >= 6)|(y0 < 0)|(y0 >= 6)|(next_pixel==center_index):
                p=np.where(idex_value==next_pixel)
                idex_value=np.delete(idex_value,p)
                next_pixel=random.choice(idex_value)
                x,y=return_xy(next_pixel,jitter_sqaure,jitter)
                x0 += x
                y0 += y
            
            if debug:
                print("x0:",x0)
                print("y0:",y0)            
            
            jitterImg[x0:x0+xdim, y0:y0+ydim]=img
            c += 1
            
            JitterVideo.append(jitterImg)
            
            if debug:
                plt.figure()
                plt.imshow(jitterImg)
                plt.show()

    JitterVideo_array=np.asarray(JitterVideo)
    print("Jitter video len:",JitterVideo_array.shape)
    
    return JitterVideo_array


# =============================================================================
# MAIN
# =============================================================================
def main(datasetpath):
    
    train_image_path=datasetpath+"/train.tiff"
    test_image_path=datasetpath+"/test.tiff"
    
    CREATE_AVI_FROM_ORIGINAL_IMAGES=False
    CREATE_JITTER_IMAGES=False
    saveAVI=False
    fps_original=30
# =============================================================================
# SAVE ORIGINAL VIDEO AS .AVI        
# =============================================================================
    if CREATE_AVI_FROM_ORIGINAL_IMAGES:
        print("=========CONVERT ORIGINAL TIFF IN AVI=========")
        train_originalimages=data_utils.form_tiff_to_listarray(train_image_path)
        test_originalimages=data_utils.form_tiff_to_listarray(test_image_path)
        if saveAVI:
            videoname=datasetpath+"/train_original.avi"
            data_utils.create_video(videoname,train_originalimages,fps_original)
            videoname=datasetpath+"/test_original.avi"
            data_utils.create_video(videoname,test_originalimages,fps_original)
        
# =============================================================================
#   CREATE AND SAVE JITTER IMAGES
# =============================================================================
    num_of_jitter_images=10
    fps=fps_original*num_of_jitter_images
    jitter=2 #how many step the image can jump! it can not staz in the same postion for following step
    augmented_border=3 #numbers of pixels around the image 
    
    if CREATE_JITTER_IMAGES:
        train_jitterimages_path=datasetpath+"/train_jitter_step"+str(jitter)+".npy"
        test_jitterimages_path=datasetpath+"/test_jitter_step"+str(jitter)+".npy"
        try: 
            print("=========LOAD FILES=========")
            train_jitterimages=np.load(train_jitterimages_path)
            test_jitterimages=np.load(test_jitterimages_path)
        except IOError:
            print("=========GENERATE JITTERED IMAGES=========")
            train_jitterimages=jitterImages(train_image_path,num_of_jitter_images,jitter,augmented_border,debug=False)
            np.save(train_jitterimages_path,train_jitterimages)
            
            test_jitterimages=jitterImages(test_image_path,num_of_jitter_images,jitter,augmented_border,debug=False)
            np.save(test_jitterimages_path,test_jitterimages)
        
        if saveAVI:
            print("=========SAVE JITTERED IMAGES=========")
            videoname=datasetpath+"/test_video_jitter_step"+str(jitter)+".avi"
            data_utils.create_video(videoname,test_jitterimages,fps)
            videoname=datasetpath+"/train_video_jitter_step"+str(jitter)+".avi"
            data_utils.create_video(videoname,train_jitterimages,fps)
    
if __name__ == "__main__":
    datasetpath='C:/Users/Gemma/Desktop/TubingenSecondment/dataset'
    main(datasetpath)
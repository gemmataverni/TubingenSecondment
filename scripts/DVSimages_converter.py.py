# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:28:21 2018

@author: Gemma
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 13:51:24 2018

@author: Gemma
"""

import numpy as np
from matplotlib import pyplot as plt
import data_utils
import os

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
# SYNCHRONOUS ACCUMULATED EVENTS IMAGES GENERATOR
#     Read .tiff video
#     For each image create ad image of the same size with information of the 
#     ON and OFF spiking pixels
#     Pixels spike when the pixel value goes above the threshold compared to 
#     the previosus frame: -1 means OFF event, 1 ON event and 0 any event
# =============================================================================

def DVSimages_SYNC(video,thrP,thrN,conversionFunction,debug):
# TODO add refractory period, refresh image, can simulate the refractory 
# period of the retina, in the DVS is a variable parameter
    video_shape=  video[0].shape  
    last_img=np.zeros(video_shape, dtype=np.int16)
    DVSimg=np.zeros(video_shape, dtype=np.int16)
    DVSvideo=[]
    DVSvideo.append(DVSimg)
    
    count=0
    
    for img in video:
        count=count+1
        img=np.int16(img)
        
#       TODO DEFINE DIFFERENT CONVERSION FUNCTION: Linear, Logaritmic, LinLog 
#       data_utils.conversionFunction(img,ThrLinLog)
            
        #check if the changes surpass a fix threshold (different thresholds for ON and OFF)
        tmp=img-last_img
        onEvents=tmp>thrP
        offEvents=tmp<thrN

        #DVS image
        DVSimg=np.zeros(video_shape, dtype=np.int16)
        DVSimg[onEvents]=1
        DVSimg[offEvents]=-1
        DVSvideo.append(DVSimg)
        
        last_img=img

    return DVSvideo


# =============================================================================
# ASYNCHRONOUS ACCUMULATED EVENTS IMAGES GENERATOR
# For each image create ad image of the same size with information of the 
# differential value for each pixeal at each timestamp
# =============================================================================

def DVSimages_ASYNC(video,thrP,thrN,conversionFunction,debug):
# TODO add refractory period, refresh image, can simulate the refractory 
# period of the retina, in the DVS is a variable parameter
    video_shape=  video[0].shape  
    last_img=np.zeros(video_shape, dtype=np.int16)
    DVSimg=np.zeros(video_shape, dtype=np.int16)
    DVSvideo=[]
    DVSvideo.append(DVSimg)
    
    count=0
    
    for img in video:
        count=count+1
        img=np.int16(img)
        
#       TODO DEFINE DIFFERENT CONVERSION FUNCTION: Linear, Logaritmic, LinLog 
#       data_utils.conversionFunction(img,ThrLinLog)
            
        #check if the changes surpass a fix threshold (different thresholds for ON and OFF)
        tmp=img-last_img
        onEvents=tmp>thrP
        offEvents=tmp<thrN
        
        #DVS image
        DVSimg=np.zeros(video_shape, dtype=np.int16)
        DVSimg[onEvents]=1
        DVSimg[offEvents]=-1
        DVSvideo.append(DVSimg)
        
        last_img[onEvents]=img[onEvents]
        last_img[offEvents]=img[offEvents]

    return DVSvideo
        

# =============================================================================
# MAIN
# =============================================================================
def main(datasetpath):   
    
    thrP=20#positive threshold in DN
    thrN=-20#negative threshold in DN (negative value)
    
#    TODO conversion function
    
    conversionFunction="Linear" #options: Linear, Logaritmic, LinLog

#    TODO add refractory period time that the photodiode need to record a new event
    
    debug=True
    

    for file in os.listdir(datasetpath):
        video_path=os.path.join(datasetpath, file).replace("\\","/")
        print(video_path)
        if file.endswith(".tiff"):
            video=data_utils.form_tiff_to_listarray(video_path)
            print("number video frame",len(video))
            DVSvideo_SYNC=DVSimages_SYNC(video,thrP,thrN,conversionFunction,debug)
            DVSvideo_ASYNC=DVSimages_ASYNC(video,thrP,thrN,conversionFunction,debug)
            
            if debug:
#                print("Input frame")
#                data_utils.print_frame_in_listarray(video,30)
#                print("Sync DVS frame")
#                data_utils.print_frame_in_listarray(DVSvideo_SYNC,20)
#                print("Asynch DVS frame")
#                data_utils.print_frame_in_listarray(DVSvideo_ASYNC,20)
                
                data_utils.print_subplot_frame_from_two_listarray(DVSvideo_SYNC,"SYNC",DVSvideo_ASYNC,"ASYNC",50)
        break
#            
            
# FOR NOW JUST USE ORIGINAL TIFF
#        if file.endswith(".avi"):
#            video=data_utils.form_avi_to_listarray(video_path)
#            print(len(video))
#            continue
        
            
    
        
    
if __name__ == "__main__":
    datasetpath='C:/Users/Gemma/Desktop/TubingenSecondment/dataset'
    main(datasetpath)
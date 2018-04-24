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
# ASYNCHRONOUS ACCUMULATED EVENTS IMAGES GENERATOR
# Compare image with state image
# =============================================================================

def DVSimages_ASYNC(video,thrP,thrN,conversionFunction):
    video_shape=  video[0].shape  
    state_img=np.zeros(video_shape, dtype=np.int16)
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
        tmp=img-state_img
        onEvents=tmp>thrP
        offEvents=np.absolute(tmp)>thrN
        
        #DVS image
        DVSimg=np.zeros(video_shape, dtype=np.int16)
        DVSimg[onEvents]=1
        DVSimg[offEvents]=-1
        DVSvideo.append(DVSimg)
        
        state_img[onEvents]=img[onEvents]
        state_img[offEvents]=img[offEvents]

    return DVSvideo
        

# =============================================================================
# MAIN
# =============================================================================
def main():   
    datasetpath='C:/Users/Gemma/Desktop/TubingenSecondment/dataset'
    
    thrP=20#positive threshold in DN
    thrN=20#negative threshold in DN (positive value)
    fps=30
    
#    TODO different conversion function
    
    conversionFunction="Linear" #options: Linear, Logaritmic, LinLog
    
    saveAVI=True
    debug=False

    for file in os.listdir(datasetpath):
        video_path=os.path.join(datasetpath, file).replace("\\","/")
        if file.endswith(".tiff"):
            print(video_path)
            video=data_utils.form_tiff_to_listarray(video_path)
            print("number video frame",len(video))
            DVSvideo=DVSimages_ASYNC(video,thrP,thrN,conversionFunction)
            
            if debug:
#                print("Input frame")
#                data_utils.print_frame_in_listarray(video,20)
#                print("DVS frame")
#                data_utils.print_frame_in_listarray(DVSvideo,20)
                
                data_utils.print_subplot_frame_from_two_listarray(video,"Input video",DVSvideo,"DVS video",50)
                
                break
            
            if saveAVI:
                DVSvideo_path=video_path.replace(".tiff", "")+"_DVS.avi"
                print(DVSvideo_path)
                data_utils.create_DVSvideo(DVSvideo_path,DVSvideo,fps)

       
# FOR NOW JUST USE ORIGINAL TIFF
#        if file.endswith(".avi"):
#            video=data_utils.form_avi_to_listarray(video_path)
#            print(len(video))
#            ...continue...
        




            
    
        
    
if __name__ == "__main__":
<<<<<<< HEAD:scripts/DVSimages_converter.py.py
    main()
=======
    datasetpath='C:/Users/Gemma/Desktop/TubingenSecondment/dataset'
    main(datasetpath)
>>>>>>> c8dc5952e396c5a4ff7c35b5eb743ca6873117b3:scripts/DVSimages_converter.py

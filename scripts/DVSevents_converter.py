# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 13:51:24 2018

@author: Gemma
"""

# =============================================================================
# DIGITAL SILICON RETINA 
# =============================================================================
import tiffcapture as tc 
import numpy as np
from matplotlib import pyplot as plt
import data_utils

# =============================================================================
# STREAM OF EVENTS GENERATOR
#    Read .tiff video
#    For each image it computes the On and Off events as the DVS
    
#    The DVS responds to temporal intensity contrast with a stream of pixel addresses. 
#    Each output event address represents a quantized change of log intensity at a particular pixel 
#    since the last event from that pixel. The address includes a sign bit that distinguishes positive 
#    from negative changes.
    
#    Difference between the current image and the previous saved image, the events
#    are generated if that value go above the threshold. On and Off events have different thresholds
#    return the list of events (x-value,y-value,timestamp: frame-time or linear timestamp,polarity: 1 On/ 0 Off)
# =============================================================================
def siliconRetinaEventsGenerator(filename,thrP,thrN,ThrLinLog,lintime,frameTimeStamp,debug):

    tiff = tc.opentiff(filename) #open img
    print("Number of images:", tiff.length)#number of images
    print("Image shape:", tiff.shape)#size of images
    
    timestamp=0#timestamp sets to 0, incremented by 1 for each image
    onEvents=[]
    offEvents=[]
    last_img=np.zeros(tiff.shape, dtype=np.int16)
    events=[]
    
    for img in tiff:
        img=np.int16(img)
                
        data_utils.conversionFunctionISCAS2012(img,ThrLinLog)
            
        #check if the changes surpass a fix threshold (different thresholds for ON and OFF)
        tmp=img-last_img
        onEvents=tmp>thrP
        offEvents=tmp<thrN
        #find the address of the events
        indexOn=np.where(onEvents)
        indexOff=np.where(offEvents)
        numbOn=indexOn[0].shape[0]
        numbOff=indexOff[0].shape[0]
        
        if debug:
            print("On events:",numbOn)
            print("Off events:",numbOff)
        
        if (numbOn==0)&(numbOff==0):
            continue
        
        if lintime:
            timestamp_array=timestamp+np.linspace(0, frameTimeStamp, num=numbOn+numbOff, endpoint=False)
            data_utils.linearTimestampISCAS2012(events,indexOn,indexOff,timestamp_array)
            
        else:        
            #create output stream of events
            eventsOn=np.stack([indexOn[0],indexOn[1],1*np.ones(numbOn),timestamp*np.ones(numbOn)],axis=0)
            eventsOff=np.stack([indexOff[0],indexOff[1],0*np.ones(numbOff),timestamp*np.ones(numbOff)],axis=0)
            tmp_events=np.concatenate((eventsOn,eventsOff), axis=1)
            events.append(np.transpose(tmp_events))           
        
        #update last_img
        last_img[onEvents]=img[onEvents]
        last_img[offEvents]=img[offEvents]
            
        timestamp=(1+timestamp)*frameTimeStamp
    
    return events

# =============================================================================
# MAIN
# =============================================================================
def main(datasetpath):
#    datasetpath='C:/Users/Gemma/Desktop/Tubingen/dataset/movies_for_gemma'
    train_image_path=datasetpath+"/train.tiff"
    test_image_path=datasetpath+"/test.tiff"
    
    thrP=20#positive threshold in DN
    thrN=-20#negative threshold in DN (negative value)
    
    #ISCAS 2012 PAPER
    linlog=False #LinLog conversion as in the iscas 2012 paper
    lintime=False #Linear time as in the iscas 2012 paper
    
    if linlog:
        ThrLinLog=20 #LinLog threshold
    else:
        ThrLinLog=256
    
    frameTimeStamp=1/30 #.tiff data info time resolution 30Hz=0.033s
    
    debug=False
    
# =============================================================================
#    EVENT STREAM GENERATOR
# =============================================================================

    print("CONVERT TIFF VIDEO IN DVS EVENTS AER RAPPRESENTATION")
    train_DVSevents=siliconRetinaEventsGenerator(train_image_path,thrP,thrN,ThrLinLog,lintime,frameTimeStamp,debug)
    print(len(train_DVSevents))
    
    test_DVSevents=siliconRetinaEventsGenerator(test_image_path,thrP,thrN,ThrLinLog,lintime,frameTimeStamp,debug)
    print(len(test_DVSevents))

    
if __name__ == "__main__":
    datasetpath='C:/Users/Gemma/Desktop/TubingenSecondment/dataset'
    main(datasetpath)
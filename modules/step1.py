# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:34:19 2019

@author: bastien.lemaire
"""
import pandas as pd
import cv2
import os 
import matplotlib
#matplotlib.use( 'Agg' )
from matplotlib import pyplot as plt



    
# function to convert seconds to number of frames
def get_frames(time_str, cap, numbframes):
    h, m, s = time_str.split(':') # take data from excel sheet: time should be written hh:mm:ss 
    fps = cap.get(cv2.CAP_PROP_FPS) # get frame rate
    if (fps > 80) | (fps < 1) :
        fps = numbframes # if problem of framerate in your videos
    sec = (int(h) * 3600 + int(m) * 60 + int(s))*fps
    return int(sec)

# function to replace time by its frame number in dataset
def time_to_frames(dataset, cap, numbframes):
    for column in dataset[['start (min)','stop (min)']]:
        for i in range(len(dataset.index)):
            time_str = str(dataset.iloc[i,dataset.columns.get_loc(column)])
            sec = get_frames(time_str, cap, numbframes) # call other function
            dataset[column]=dataset[column].replace([dataset.iloc[i,dataset.columns.get_loc(column)]],sec)
    return dataset


# create file for a left_right style apparatus
def create_new_file_lr(cap, ID, input_xls, animal_type, pathfile, movfix, asym, numbframes): 
    # call other functions to get start and stop number of frames
    dataset = pd.read_excel(input_xls, sheet_name = animal_type + '%s' %ID, header = 1)
    dataset = time_to_frames(dataset, cap, numbframes) # convert from min to sec 
    newDataset = pd.DataFrame(dataset, columns= ['ID', 'sex', 'condition', 'trial', 'object', 'position_object', 'start (min)', 'stop (min)'])

    # select first frame of the starting point of the video
    cap.set(1,(newDataset['start (min)'][0])); 
    success, image = cap.read()
    cv2.imwrite("frame.jpg",image)
    plt.imshow(image)
                  
    # select arena borders with mouse click
    plt.text(0, 0, "Click on top left corner", color="black", fontsize=10)
    arena_border = plt.ginput(1)
    newDataset['topLeftX'] = round(arena_border[0][0])
    newDataset['topLeftY'] = round(arena_border[0][1])
    plt.close()

    plt.imshow(image) 
    plt.text(0, 0, "Click on top right corner", color="black", fontsize=10)
    arena_border = plt.ginput(1)
    newDataset['topRightX'] = round(arena_border[0][0])
    newDataset['topRightY'] = round(arena_border[0][1])
    plt.close()

    plt.imshow(image) 
    plt.text(0, 0, "Click on bottom left corner", color="black", fontsize=10)
    arena_border = plt.ginput(1)
    newDataset['bottomLeftX'] = round(arena_border[0][0])
    newDataset['bottomLeftY'] = round(arena_border[0][1])
    plt.close()

    plt.imshow(image) 
    plt.text(0, 0, "Click on bottom right corner", color="black", fontsize=10)
    arena_border = plt.ginput(1)
    newDataset['bottomRightX'] = round(arena_border[0][0])
    newDataset['bottomRightY'] = round(arena_border[0][1])
    plt.close()

    plt.imshow(image) 

    # select position of the stim if needed
    if (movfix == 0) & (asym == False):
        
        plt.text(0, 0, "Click on the bottom position of the stimulus", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['bottomStimX'] = round(arena_border[0][0])
        newDataset['bottomStimY'] = round(arena_border[0][1])
        plt.close()

        plt.imshow(image)  
        plt.text(0, 0, "Click on top position of the stimulus", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['topStimX'] = round(arena_border[0][0])
        newDataset['topStimY'] = round(arena_border[0][1])
        
    if (movfix == 0) & (asym == True):
        plt.text(0, 0, "Click on the bottom position of the stimulus, on the left side", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['bottomLeftStimX'] = round(arena_border[0][0])
        newDataset['bottomLeftStimY'] = round(arena_border[0][1])
        plt.close()

        plt.imshow(image)  
        plt.text(0, 0, "Click on top position of the stimulus, on the left side", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['topLeftStimX'] = round(arena_border[0][0])
        newDataset['topLeftStimY'] = round(arena_border[0][1])
        plt.close()

        plt.imshow(image)  
        plt.text(0, 0, "Click on bottom position of the stimulus, on the right side", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['bottomRightStimX'] = round(arena_border[0][0])
        newDataset['bottomRightStimY'] = round(arena_border[0][1])
        plt.close()

        plt.imshow(image)  
        plt.text(0, 0, "Click on top position of the stimulus, on the right side", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['topRightStimX'] = round(arena_border[0][0])
        newDataset['topRightStimY'] = round(arena_border[0][1])
                
    newDataset['leftBorder'] = round((newDataset['topLeftX'] + newDataset['bottomLeftX'])/2)
    newDataset['rightBorder'] = round((newDataset['topRightX'] + newDataset['bottomRightX'])/2)
        
    plt.close()
    os.remove("frame.jpg")
    cap.release()
    cv2.destroyAllWindows()

    newDataset.rename(index=str, columns={"start (min)":"startingFrame", "stop (min)":"endingFrame"}, inplace=True) # rename columns
    newDataset.to_csv(pathfile + '/' + animal_type + '%s.csv' %ID, index = False)

   
# create file for a bottom_top style apparatus
def create_new_file_bt(cap, ID, input_xls, animal_type, pathfile, movfix, asym, numbframes): 
    dataset = pd.read_excel(input_xls, sheet_name = animal_type + '%s' %ID, header = 1)
    time_to_frames(dataset, cap, numbframes) # convert from min to sec 
    newDataset = pd.DataFrame(dataset, columns= ['ID', 'sex', 'condition', 'trial', 'object', 'position_object', 'start (min)', 'stop (min)'])


    # select first frame of the starting point of the video
    cap.set(1,(newDataset['start (min)'][0])); 
    success, image = cap.read()
    cv2.imwrite("frame.jpg",image)
    plt.imshow(image)
                 
    # select arena borders with mouse click
    plt.text(0, 0, "Click on top left corner", color="black", fontsize=10)
    arena_border = plt.ginput(1)
    newDataset['topLeftX'] = round(arena_border[0][0])
    newDataset['topLeftY'] = round(arena_border[0][1])
    plt.close()

    plt.imshow(image) 
    plt.text(0, 0, "Click on top right corner", color="black", fontsize=10)
    arena_border = plt.ginput(1)
    newDataset['topRightX'] = round(arena_border[0][0])
    newDataset['topRightY'] = round(arena_border[0][1])
    plt.close()

    plt.imshow(image)    
    plt.text(0, 0, "Click on bottom left corner", color="black", fontsize=10)
    arena_border = plt.ginput(1)
    newDataset['bottomLeftX'] = round(arena_border[0][0])
    newDataset['bottomLeftY'] = round(arena_border[0][1])
    plt.close()

    plt.imshow(image)    
    plt.text(0, 0, "Click on bottom right corner", color="black", fontsize=10)
    arena_border = plt.ginput(1)
    newDataset['bottomRightX'] = round(arena_border[0][0])
    newDataset['bottomRightY'] = round(arena_border[0][1])
    plt.close()

    # select position of the stim if needed
    if (movfix == 0) & (asym == False):
        plt.imshow(image)    
        plt.text(0, 0, "Click on left position of the stimulus", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['leftStimX'] = round(arena_border[0][0])
        newDataset['leftStimY'] = round(arena_border[0][1])
        plt.close()

        plt.imshow(image)
        plt.text(0, 0, "Click on right position of the stimulus", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['rightStimX'] = round(arena_border[0][0])
        newDataset['rightStimY'] = round(arena_border[0][1])
        
    if (movfix == 0) & (asym == True):
        plt.imshow(image)    
        plt.text(0, 0, "Click on left position of the stimulus, on the top", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['leftTopStimX'] = round(arena_border[0][0])
        newDataset['leftTopStimY'] = round(arena_border[0][1])
        plt.close()

        plt.imshow(image)
        plt.text(0, 0, "Click on right position of the stimulus, on the top", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['rightTopStimX'] = round(arena_border[0][0])
        newDataset['rightTopStimY'] = round(arena_border[0][1])
        plt.close()

        plt.imshow(image)
        plt.text(0, 0, "Click on left position of the stimulus, on the bottom", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['leftBottomStimX'] = round(arena_border[0][0])
        newDataset['leftBottomStimY'] = round(arena_border[0][1])
        plt.close()

        plt.imshow(image)
        plt.text(0, 0, "Click on right position of the stimulus, on the bottom", color="black", fontsize=10)
        arena_border = plt.ginput(1)
        newDataset['rightBottomStimX'] = round(arena_border[0][0])
        newDataset['rightBottomStimY'] = round(arena_border[0][1])
        
    newDataset['topBorder'] = round((newDataset['topLeftY'] + newDataset['topRightY'])/2)
    newDataset['bottomBorder'] = round((newDataset['bottomLeftY'] + newDataset['bottomRightY'])/2)
        
    plt.close()
    os.remove("frame.jpg")
    cap.release()
    cv2.destroyAllWindows()
    
    newDataset.rename(index=str, columns={"start (min)":"startingFrame", "stop (min)":"endingFrame"}, inplace=True) # rename columns
    newDataset.to_csv(pathfile + '/' + animal_type + '%s.csv' %ID, index = False)
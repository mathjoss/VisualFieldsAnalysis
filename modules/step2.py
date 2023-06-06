# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 09:28:52 2019

@author: mathilde.josserand
"""
import numpy as np
import pandas as pd
import sys
import cv2

# compute distance between two points
def calculateDistance(x1,y1,x2,y2):  
     dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) 
     return dist  

# function to detect outliers given a certain thresh
outliers=[]
def detect_outlier(data_1, thresh):   
    threshold=int(thresh)
    mean_1 = np.mean(data_1)
    std_1 =np.std(data_1)
    for y in data_1:
        z_score= (y - mean_1)/std_1 
        if np.abs(z_score) > threshold:
            outliers.append(y)
    return outliers

# main function to check errors
def check_errors(cap, trialFrames, txtFile, orientation, thresh, movfix, asym, resp_gofast, ID, pathfile, animal_type):
    import interface
    
    # check if distance between side and top head is above N standard error (N is defined by the user in thresh)
    trialFrames["distLeftTop"] = calculateDistance(trialFrames['leftheadx'], trialFrames['leftheady'], trialFrames['topheadx'], trialFrames['topheady']) 
    outlier_datapoints = detect_outlier(trialFrames["distLeftTop"], thresh)
    if len(outlier_datapoints)!=0
        trialFrames["distLeftTop"] = trialFrames["distLeftTop"].map(lambda x: np.nan if x in outlier_datapoints else x)
          
    # same for all distances between tophead, rightHead and leftHead
    trialFrames["distRightTop"]= calculateDistance(trialFrames['rightheadx'], trialFrames['rightheady'], trialFrames['topheadx'], trialFrames['topheady']) 
    outlier_datapoints = detect_outlier(trialFrames["distRightTop"], thresh)
    if len(outlier_datapoints)!=0 :
          # replace outlier value with nan in "distRightTop" column
          trialFrames["distRightTop"] = trialFrames["distRightTop"].map(lambda x: np.nan if x in outlier_datapoints else x)
          
          # replace "distLeftTop" column value with NAN if the "distRightTop" column's value in the same row is NAN
          trialFrames.loc[trialFrames["distRightTop"].isnull(), "distLeftTop"]=np.nan
          
    trialFrames["distLeftRight"]= calculateDistance(trialFrames['leftheadx'], trialFrames['leftheady'], trialFrames['rightheadx'], trialFrames['rightheady']) 
    outlier_datapoints = detect_outlier(trialFrames["distLeftRight"], thresh)
    if len(outlier_datapoints)!=0 :
          # replace outlier value with nan in "distLeftRight" column
          trialFrames["distLeftRight"] = trialFrames["distLeftRight"].map(lambda x: np.nan if x in outlier_datapoints else x)
          
          # replace "distLeftTop" column value with NAN if the "distRightTop" column's value is NAN
          trialFrames.loc[trialFrames["distLeftRight"].isnull(), "distLeftTop"]=np.nan
          
    # print number of errors detected with this method
    errors_distance_percent = trialFrames["distLeftTop"].isna().sum() / len(trialFrames) *100
    print('% of outliers nan found with threshold method : ' + str(round(errors_distance_percent,2)))
    
    # store in variable the index of deleted frame, in order to be able to visualize them later
    index = trialFrames['distLeftTop'].index[trialFrames['distLeftTop'].apply(np.isnan)]
    df_index = trialFrames.index.values.tolist()
    frames_to_visualize = [df_index.index(i) for i in index]
    
    # ask user if he wants to visualize frames 
    if resp_gofast=="n":
        resp, resp_gofast = interface.check_errors_q1(errors_distance_percent)

        # VISUALIZE ERRORS
        if resp == 'y' :
    
            for picnum in frames_to_visualize :
                indexpic = picnum + txtFile.startingframe[0]
                cap.set(1,indexpic); 
                ret, img = cap.read() # Read the frame
                
                #print stimulus location on top and border
                cv2.circle(img, (int(trialFrames.iloc[picnum, trialFrames.columns.get_loc("leftheadx")]), int(trialFrames.iloc[picnum, trialFrames.columns.get_loc("leftheady")])), 3, (255,0,0), -1)
                cv2.circle(img, (int(trialFrames.iloc[picnum, trialFrames.columns.get_loc("rightheadx")]), int(trialFrames.iloc[picnum, trialFrames.columns.get_loc("rightheady")])), 3, (0,255,0), -1)
                cv2.circle(img, (int(trialFrames.iloc[picnum, trialFrames.columns.get_loc("topheadx")]), int(trialFrames.iloc[picnum, trialFrames.columns.get_loc("topheady")])), 3, (0,0,255), -1)
                cv2.putText(img, 'blue:leftHead', (100,150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,100,200),1)
                cv2.putText(img, 'green:rightHead', (100,200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,100,200),1)
                cv2.putText(img, 'red:topHead', (100,250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,100,200),1)
                
                imS = cv2.resize(img, (960, 540)) 
                cv2.imshow('check_errors', imS)
                
                # press any keyboard key to go to the next image
                cv2.waitKey(0)
                cv2.destroyAllWindows
        
     
    # if you want to compute location without have NAN for stimulus
    # you will need to apply step 3 exactly here
    # import step3
    # step3.computelocation () see more details in main_coordinator
    
    # check DLC errors and remove frames where likelihood is < than 0.9
    frame_number = trialFrames['frame_number']
    trialFrames.loc[trialFrames.isnull().any(axis=1), :] = np.nan
    trialFrames['frame_number'] = frame_number
    
    # change the value from 0.9 to 0.1 to remove the likelihood <0.9
    trialFrames["leftheadlikelihood"]= trialFrames["leftheadlikelihood"].where(trialFrames['leftheadlikelihood']>0.9) 
    trialFrames["rightheadlikelihood"]= trialFrames["rightheadlikelihood"].where(trialFrames['rightheadlikelihood']>0.9)
    trialFrames["topheadlikelihood"]= trialFrames["topheadlikelihood"].where(trialFrames['topheadlikelihood']>0.9)
    
    trialFrames_for_loc = trialFrames.copy()
    
    if (movfix == 1) & (asym == False):
        trialFrames["stimlikelihood"]= trialFrames["stimlikelihood"].where(trialFrames['stimlikelihood']>0.9)
    if (movfix == 1) & (asym == True) & (orientation == "lr"):
        trialFrames["stimleftlikelihood"]= trialFrames["stimleftlikelihood"].where(trialFrames['stimleftlikelihood']>0.9)
        trialFrames["stimrightlikelihood"]= trialFrames["stimrightlikelihood"].where(trialFrames['stimrightlikelihood']>0.9)
    if (movfix == 1) & (asym == True) & (orientation == "bt"):
        trialFrames["stimtoplikelihood"]= trialFrames["stimtoplikelihood"].where(trialFrames['stimtoplikelihood']>0.9)
        trialFrames["stimbottomlikelihood"]= trialFrames["stimbottomlikelihood"].where(trialFrames['stimbottomlikelihood']>0.9)
   
    # apply nan to all columns
    frame_number = trialFrames['frame_number']
    trialFrames.loc[trialFrames.isnull().any(axis=1), :] = np.nan
    trialFrames_for_loc.loc[trialFrames_for_loc.isnull().any(axis=1), :] = np.nan
        
    trialFrames['frame_number'] = frame_number
    trialFrames_for_loc['frame_number'] = frame_number
    
    # total percentage of error
    errors_total_percent = trialFrames["distLeftRight"].isna().sum() / len(trialFrames) *100
    print('% of nan in total : : ' + str(round(errors_total_percent,2)))
     
    # save the percentage of nan computed by threshold method and DLC likelihood to csv file
    d={'id': ID, 'ratio outliers nan found with threshold method': str(round(errors_distance_percent,2)), 'ratio nan in total': str(round(errors_total_percent,2))}
    df = pd.DataFrame(data=d, index=[0])
    df.to_csv(pathfile + '/' + animal_type + '%s_nanratio.csv' %ID, sep=',')
     
    # ask user if he wants to continue 
    if resp_gofast == "n":   
        resp2 = interface.check_errors_q2(errors_total_percent)
        
        # exit system if he wants to leafe
        if resp2 == 'n' :
            sys.exit()
        
    # remove columns that just have been created     
    trialFrames = trialFrames.drop(['distLeftRight', 'distLeftTop', 'distRightTop'], axis=1)
    
    #cv2.destroyWindow('check_errors') 
    return trialFrames, trialFrames_for_loc, frame_number, resp_gofast 
        

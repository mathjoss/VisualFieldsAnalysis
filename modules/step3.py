# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:35:55 2019

@author: mathilde.josserand
"""
import numpy as np
import math

# function to compute distance between 2 points
def calculateDistance(x1,y1,x2,y2):  
     dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) 
     return dist
 
# find location of animal in areas given by the user, for a bottom/top style apparatuys   
def find_location_bt(trialFrames, trialFrames_for_loc, txtFile, area1, area2, area3, area4, area5, numbframes):
    
    # Calcutale the size of the arena in pixels
    topborder = txtFile.topborder[0]
    bottomborder = txtFile.bottomborder[0]
    lengthArena = txtFile.bottomborder[0] - txtFile.topborder[0]
        
    delimiter_area12 = (area1*lengthArena/(area1+area2+area3+area4+area5)) 
    delimiter_area23 = ((area1+area2)*lengthArena/(area1+area2+area3+area4+area5))
    delimiter_area34 = ((area1+area2+area3)*lengthArena/(area1+area2+area3+area4+area5))
    delimiter_area45 = ((area1+area2+area3+area4)*lengthArena/(area1+area2+area3+area4+area5))

    #Calculate the distance moved in cm
    distanceList = [0]
    for m in range(2,trialFrames.shape[0]):
        tempDistance =  calculateDistance(trialFrames_for_loc.topheadx.iloc[m-1], trialFrames_for_loc.topheady.iloc[m-1], trialFrames_for_loc.topheadx.iloc[m], trialFrames_for_loc.topheady.iloc[m])
        distanceMoved = distanceList.append(tempDistance)
        
    distanceMoved = np.asarray(distanceList)
    distanceMoved2 = np.append (distanceMoved, [0])
    trialFrames['distanceMoved'] = distanceMoved2 

     # Create the columns we need for the location
    trialFrames['TOPCLOSE'] = 0
    trialFrames['TOP'] = 0
    trialFrames['CENTER'] = 0
    trialFrames['BOTTOM'] = 0
    trialFrames['BOTTOMCLOSE'] = 0
    trialFrames['nan'] = 0
      
    trialFrames['TOPCLOSE'] = np.where( (trialFrames_for_loc['topheady'] > topborder) & (trialFrames_for_loc['topheady'] < (topborder + delimiter_area12)), 1/numbframes, 0)
    trialFrames['TOP'] = np.where( (trialFrames_for_loc['topheady'] > (topborder + delimiter_area12)) & (trialFrames_for_loc['topheady'] < (topborder + delimiter_area23)), 1/numbframes, 0)
    trialFrames['CENTER'] = np.where( (trialFrames_for_loc['topheady'] > (topborder + delimiter_area23)) & (trialFrames_for_loc['topheady'] < (topborder + delimiter_area34)), 1/numbframes, 0)
    trialFrames['BOTTOM'] = np.where( (trialFrames_for_loc['topheady'] > (topborder + delimiter_area34)) & (trialFrames_for_loc['topheady'] < (topborder + delimiter_area45)), 1/numbframes, 0)
    trialFrames['BOTTOMCLOSE'] = np.where( (trialFrames_for_loc['topheady'] > (topborder + delimiter_area45)) & (trialFrames_for_loc['topheady'] < bottomborder), 1/numbframes, 0)
    
    trialFrames['index_nan_no_stim'] = trialFrames_for_loc['index']
     
    final4 = trialFrames.copy()

    #delete first column
    trialFrames = trialFrames.drop(['index'], axis=1)
    
    return trialFrames, final4

# find location of animal in areas given by the user, for a left/right style apparatuys   
def find_location_lr(trialFrames, trialFrames_for_loc, txtFile, area1, area2, area3, area4, area5, numbframes):
    
    # Calcutale the size of the arena in pixels
    rightborder = txtFile.rightborder[0]
    leftborder = txtFile.leftborder[0]
    lengthArena = txtFile.rightborder[0] - txtFile.leftborder[0]
        
    delimiter_area12 = (area1*lengthArena/(area1+area2+area3+area4+area5)) 
    delimiter_area23 = ((area1+area2)*lengthArena/(area1+area2+area3+area4+area5))
    delimiter_area34 = ((area1+area2+area3)*lengthArena/(area1+area2+area3+area4+area5))
    delimiter_area45 = ((area1+area2+area3+area4)*lengthArena/(area1+area2+area3+area4+area5))

    #Calculate the distance moved in cm
    distanceList = [0]
    for m in range(2,trialFrames.shape[0]):
        tempDistance =  calculateDistance(trialFrames_for_loc.topheadx.iloc[m-1], trialFrames_for_loc.topheady.iloc[m-1], trialFrames_for_loc.topheadx.iloc[m], trialFrames_for_loc.topheady.iloc[m])
        distanceMoved = distanceList.append(tempDistance)
        
    distanceMoved = np.asarray(distanceList)
    distanceMoved2 = np.append (distanceMoved, [0])
    trialFrames['distanceMoved'] = distanceMoved2 

     # Create the columns we need for the location
    trialFrames['LEFTCLOSE'] = 0
    trialFrames['LEFT'] = 0
    trialFrames['CENTER'] = 0
    trialFrames['RIGHT'] = 0
    trialFrames['RIGHTCLOSE'] = 0
    trialFrames['nan'] = 0
    
    
    trialFrames['LEFTCLOSE'] = np.where( (trialFrames_for_loc['topheadx'] > leftborder) & (trialFrames_for_loc['topheadx'] < (leftborder + delimiter_area12)), 1/numbframes, 0)
    trialFrames['LEFT'] = np.where( (trialFrames_for_loc['topheadx'] > (leftborder + delimiter_area12)) & (trialFrames_for_loc['topheadx'] < (leftborder + delimiter_area23)), 1/numbframes, 0)
    trialFrames['CENTER'] = np.where( (trialFrames_for_loc['topheadx'] > (leftborder + delimiter_area23)) & (trialFrames_for_loc['topheadx'] < (leftborder + delimiter_area34)), 1/numbframes, 0)
    trialFrames['RIGHT'] = np.where( (trialFrames_for_loc['topheadx'] > (leftborder + delimiter_area34)) & (trialFrames_for_loc['topheadx'] < (leftborder + delimiter_area45)), 1/numbframes, 0)
    trialFrames['RIGHTCLOSE'] = np.where( (trialFrames_for_loc['topheadx'] > (leftborder + delimiter_area45)) & (trialFrames_for_loc['topheadx'] < rightborder), 1/numbframes, 0)
    
    trialFrames['index_nan_no_stim'] = trialFrames_for_loc['index']
    
    final4 = trialFrames.copy()
    
    return trialFrames, final4

def find_location_cen(trialFrames, trialFrames_for_loc, txtFile, area1, area2, area3, area4, area5, numbframes, movfix):
    
# Calcutale the size of the arena in pixels
    lengthArena = txtFile.arenarightx[0] - txtFile.arenaleftx[0]

    sum_areas = area1 + area2 + area3 + area4 + area5

    size_area1 = (lengthArena*area1) / sum_areas
    size_area2 = (lengthArena*area2) / sum_areas
    size_area3 = (lengthArena*area3) / sum_areas
    size_area4 = (lengthArena*area4) / sum_areas
    size_area5 = (lengthArena*area5) / sum_areas

    # if movfix==0 and asym == False:
    #     # compute location of the center of the stimulus
    #     center_x = (txtFile.leftstimx + txtFile.rightstimx)/2
    #     center_y = (txtFile.leftstimy + txtFile.rightstimy)/2
    #     # compute radius of the stimulus (actually it is useless...)
    #     radius = math.sqrt((txtFile.rightstimx - txtFile.leftstimx)^2 + (txtFile.rightstimy - txtFile.leftstimy)^2)
    if movfix == 0:
        center_x = int(txtFile.stimx)
        center_y = int(txtFile.stimy)
    # elif movfix == 0 and asym == True:
    #     center1_x = int(txtFile.stim1x)
    #     center1_y = int(txtFile.stim1y)
    #     center2_x = int(txtFile.stim2x)
    #     center2_y = int(txtFile.stim2y)
    
         
         
     #Calculate the distance moved in cm
    distanceList = [0]
    for m in range(2,trialFrames.shape[0]):
        tempDistance =  calculateDistance(trialFrames_for_loc.topheadx.iloc[m-1], trialFrames_for_loc.topheady.iloc[m-1], trialFrames_for_loc.topheadx.iloc[m], trialFrames_for_loc.topheady.iloc[m])
        distanceMoved = distanceList.append(tempDistance)
        
    distanceMoved = np.asarray(distanceList)
    distanceMoved2 = np.append (distanceMoved, [0])
    trialFrames['distanceMoved'] = distanceMoved2 
    
     # Create the columns we need for the location
    trialFrames['VERYCLOSE'] = 0
    trialFrames['CLOSE'] = 0
    trialFrames['DISTANT'] = 0
    trialFrames['VERYDISTANT'] = 0
    trialFrames['VERYVERYDISTANT'] = 0
    trialFrames['nan'] = 0
    
    if movfix == 0:
        trialFrames_for_loc['dist_stim'] = np.sqrt((trialFrames_for_loc['topheadx'] - center_x)**2 + (trialFrames_for_loc['topheady'] - center_y)**2 )
    elif movfix == 1 :
        trialFrames_for_loc['dist_stim'] = np.sqrt((trialFrames_for_loc['topheadx'] - trialFrames_for_loc['stimx'])**2 + (trialFrames_for_loc['topheady'] - trialFrames_for_loc['stimy'])**2 )
    
    trialFrames['VERYVERYDISTANT'] = np.where( trialFrames_for_loc['dist_stim']  > size_area5, 1/numbframes, 0)
    trialFrames['VERYDISTANT'] = np.where( (trialFrames_for_loc['dist_stim']  < size_area5) & (trialFrames_for_loc['dist_stim']  >= size_area4) , 1/numbframes, 0)
    trialFrames['DISTANT'] = np.where( (trialFrames_for_loc['dist_stim']  < size_area4) & (trialFrames_for_loc['dist_stim']  >= size_area3), 1/numbframes, 0)
    trialFrames['CLOSE'] = np.where( (trialFrames_for_loc['dist_stim']  < size_area3) & (trialFrames_for_loc['dist_stim']  >= size_area2), 1/numbframes, 0)
    trialFrames['VERYCLOSE'] = np.where( trialFrames_for_loc['dist_stim']  < size_area1 , 1/numbframes, 0)
 
    trialFrames['index_nan_no_stim'] = trialFrames_for_loc['index']

    final4 = trialFrames.copy()
  
    return trialFrames, final4

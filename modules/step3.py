# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:35:55 2019

@author: mathilde.josserand
"""
import numpy as np

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
    trialFrames['RIGHT'] = 0
    trialFrames['nan'] = 0
    
    
    trialFrames['LEFTCLOSE'] = np.where( (trialFrames_for_loc['topheadx'] > leftborder) & (trialFrames_for_loc['topheadx'] < (leftborder + delimiter_area12)), 1/numbframes, 0)
    trialFrames['LEFT'] = np.where( (trialFrames_for_loc['topheadx'] > (leftborder + delimiter_area12)) & (trialFrames_for_loc['topheadx'] < (leftborder + delimiter_area23)), 1/numbframes, 0)
    trialFrames['CENTER'] = np.where( (trialFrames_for_loc['topheadx'] > (leftborder + delimiter_area23)) & (trialFrames_for_loc['topheadx'] < (leftborder + delimiter_area34)), 1/numbframes, 0)
    trialFrames['RIGHT'] = np.where( (trialFrames_for_loc['topheadx'] > (leftborder + delimiter_area34)) & (trialFrames_for_loc['topheadx'] < (leftborder + delimiter_area45)), 1/numbframes, 0)
    trialFrames['RIGHTCLOSE'] = np.where( (trialFrames_for_loc['topheadx'] > (leftborder + delimiter_area45)) & (trialFrames_for_loc['topheadx'] < rightborder), 1/numbframes, 0)
    
    trialFrames['index_nan_no_stim'] = trialFrames_for_loc['index']
    
    final4 = trialFrames.copy()
    
    return trialFrames, final4
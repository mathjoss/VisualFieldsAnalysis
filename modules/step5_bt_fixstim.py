# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:42:54 2019

@author: mathilde.josserand
"""
import numpy as np
import sys
import math     
import cv2
import random


#Rotate a point counterclockwise by a given angle (in radians) around a given origin  
def rotate(originx, originy, pointx, pointy, angle):
    qx = originx + math.cos(angle) * (pointx - originx) - math.sin(angle) * (pointy - originy)
    qy = originy + math.sin(angle) * (pointx - originx) + math.cos(angle) * (pointy - originy)
    return qx, qy

# find slope between two points
def slope(x1, y1, x2, y2): 
    return (y2-y1)/(x2-x1)    
    
def yintercept(x, y, m):
    return y - m * x

# compute visual fields in the bottom side
def visual_fields_bottom(txtFile, final4, asym):

    # find stim according to conditions
    if asym == False:
        stimR = txtFile.rightstimx[0]
        stimL = txtFile.leftstimx[0]
    if asym == True:
        stimR = txtFile.rightbottomstimx[0]
        stimL = txtFile.leftbottomstimx[0]
    
    # Give name to variable to make the next step easier to read and understand :        
    frontalR = final4["interceptfrontalRbottom"]
    frontalL = final4["interceptfrontalLbottom"]
    blindR = final4["interceptblindRbottom"]
    blindL = final4["interceptblindLbottom"]
    middle = final4['interceptmiddlebottom']
    
  
    # SPECIAL CASE : only frontal    
    final4['frontalbottom'] = np.where( ((np.isnan(frontalL)==True) & (np.isnan(frontalR)==False) & (frontalR<stimL)) | ((np.isnan(frontalR)==True) & (np.isnan(frontalL)==False) & (frontalL > stimL)) | ((np.isnan(frontalR)==False) & (np.isnan(frontalL)==False) & (frontalL>stimR) & (frontalR<stimL)), 1, final4['frontalbottom'])

    # SPECIAL CASE : only blind     
    final4['blindbottom'] = np.where( (((np.isnan(blindL)==True) & (np.isnan(blindR)==False) & (blindR>stimR)) | ((np.isnan(blindR)==True) & (np.isnan(blindL)==False) & (blindL<stimL)) | ((np.isnan(blindR)==False) & (np.isnan(blindL)==False) & (blindR>stimR) & (blindL<stimL))), 1, final4['blindbottom'])

    # SPECIAL CASE : only lateral-right           
    final4['lateralRightbottom'] = np.where( ((np.isnan(blindR)== False) & (blindR<stimL) & ((frontalR>stimR)|(np.isnan(frontalR)== True))) | ((np.isnan(frontalR)== False) & (frontalR>stimR) & ((blindR<stimL)|(np.isnan(blindR)== True))), 1, final4['lateralRightbottom'])
    
    # SPECIAL CASE : only lateral-left                 
    final4['lateralLeftbottom'] = np.where( ((np.isnan(blindL)== False) & (blindL>stimR) & ((frontalL<stimL)|(np.isnan(frontalL)== True))) | ((np.isnan(frontalL)== False) & (frontalL<stimL) & ((blindL>stimR)|(np.isnan(blindL)== True))), 1, final4['lateralLeftbottom'])

    # FRONTAL VIEW: mix between frontal and lateral-left  
    final4['frontalbottom'] = np.where( (np.isnan(frontalL) == False) & (frontalL > stimL) & (frontalL < stimR) & ((frontalL>frontalR) | (np.isnan(frontalR)==True)), ((frontalL - stimL)/(stimR - stimL)), final4['frontalbottom'])
    final4['lateralLeftbottom'] = np.where( (np.isnan(frontalL) == False) & (frontalL > stimL) & (frontalL < stimR) & ((frontalL>frontalR) | (np.isnan(frontalR)==True)), (1 - final4['frontalbottom']), final4['lateralLeftbottom'])

    # FRONTAL VIEW: mix between frontal and lateral-right     
    final4['frontalbottom'] = np.where( (np.isnan(frontalR) == False) & (frontalR < stimR) & (frontalR > stimL) & ((frontalL>frontalR) | (np.isnan(frontalL) == True)), ((stimR - frontalR)/(stimR - stimL)), final4['frontalbottom'])
    final4['lateralRightbottom'] = np.where( (np.isnan(frontalR) == False) & (frontalR < stimR) & (frontalR > stimL) & ((frontalL>frontalR) | (np.isnan(frontalL) == True)), (1 - final4['frontalbottom']), final4['lateralRightbottom'])  
      
    # FRONTAL VIEW: mix between frontal, lateral-left and lateral-right                  
    final4['lateralRightbottom'] = np.where( (np.isnan(frontalR) == False) & (np.isnan(frontalL) == False) & (frontalL>frontalR) & (frontalL<stimR) & (frontalR>stimL), ((frontalR - stimL) / (stimR - stimL)), final4['lateralRightbottom'])
    final4['lateralLeftbottom'] = np.where( (np.isnan(frontalR) == False) & (np.isnan(frontalL) == False) & (frontalL>frontalR) & (frontalL<stimR) & (frontalR>stimL), ((stimR - frontalL) / (stimR - stimL)), final4['lateralLeftbottom'])
    final4['frontalbottom'] = np.where( (np.isnan(frontalR) == False) & (np.isnan(frontalL) == False) & (frontalL>frontalR) & (frontalL<stimR) & (frontalR>stimL), (1 - ( final4['lateralRightbottom'] + final4['lateralLeftbottom'])), final4['frontalbottom'])
 
    # BLIND VIEW: mix between blind and lateral-left
    final4['lateralLeftbottom'] = np.where( (np.isnan(blindL) == False) & (blindL > stimL) & (blindL < stimR) & ((blindL<blindR) | (np.isnan(blindR)==True)), ((blindL - stimL)/(stimR - stimL)), final4['lateralLeftbottom'])
    final4['blindbottom'] = np.where( (np.isnan(blindL) == False) & (blindL > stimL) & (blindL < stimR) & ((blindL<blindR) | (np.isnan(blindR)==True)), (1 - final4['lateralLeftbottom']), final4['blindbottom'])
     
    # BLIND VIEW: mix between blind and lateral-right     
    final4['lateralRightbottom'] = np.where( (np.isnan(blindR) == False) & (blindR < stimR) & (blindR > stimL) & ((blindL<blindR) | (np.isnan(blindL) == True)), ((stimR - blindR)/(stimR - stimL)), final4['lateralRightbottom'])
    final4['blindbottom'] = np.where( (np.isnan(blindR) == False) & (blindR < stimR) &( blindR > stimL) & ((blindL<blindR) | (np.isnan(blindL) == True)), (1 - final4['lateralRightbottom']), final4['blindbottom'])
     
    # BLIND VIEW: mix between blind, lateral-left and lateral-right                  
    final4['lateralRightbottom'] = np.where( (np.isnan(blindR) == False) & (np.isnan(blindL) == False) & (blindL>blindR) & (blindL<stimR) & (blindR>stimL), ((blindR - stimL) / (stimR - stimL)), final4['lateralRightbottom'])
    final4['lateralLeftbottom'] = np.where( (np.isnan(blindR) == False) & (np.isnan(blindL) == False) & (blindL>blindR) & (blindL<stimR) & (blindR>stimL), ((stimR - blindL) / (stimR - stimL)), final4['lateralLeftbottom'])
    final4['blindbottom'] = np.where( (np.isnan(blindR) == False) & (np.isnan(blindL) == False) & (blindL>blindR) & (blindL<stimR) & (blindR>stimL), (1 - ( final4['lateralRightbottom'] + final4['lateralLeftbottom'])), final4['blindbottom'])
    
    # check if error : if not, this column is supposed to be always equal to 1
    final4['sumallbottom']= final4['blindbottom'] + final4['frontalbottom'] + final4['lateralRightbottom'] + final4['lateralLeftbottom']
    
    # lateral without frontal
    final4['LeftALLbottom']  = np.where( ((np.isnan(middle) == False) & (middle<stimL) & ((blindL>stimR)|(np.isnan(blindL) == True))) | ((np.isnan(middle) == True) & (np.isnan(blindL) == False) & (blindL>stimR)), 1, final4['LeftALLbottom'])
    final4['RightALLbottom']  = np.where( ((np.isnan(middle) == False) & (middle>stimR) & ((blindR<stimL)|(np.isnan(blindR) == True))) | ((np.isnan(middle) == True) & (np.isnan(blindR) == False) & (blindR<stimL)), 1, final4['RightALLbottom'])
    
    final4['LeftALLbottom']  = np.where( (np.isnan(middle) == False) & (middle>stimL) & (middle<stimR), ((stimR-middle)/(stimR-stimL)), final4['LeftALLbottom'])
    final4['RightALLbottom']  = np.where( (np.isnan(middle) == False) & (middle>stimL) & (middle<stimR), 1-final4['LeftALLbottom'], final4['RightALLbottom'])
    
    final4['LeftALLbottom']  = np.where( ((np.isnan(middle) == True) | ((np.isnan(middle) == False) & (middle<stimL))) & (np.isnan(blindL) == False) & (blindL>stimL) & (blindL<stimR), ( (blindL-stimL)/(stimR-stimL)), final4['LeftALLbottom'])
    final4['RightALLbottom']  = np.where( ((np.isnan(middle) == True)| ((np.isnan(middle) == False) & (middle>stimR))) & (np.isnan(blindR) == False) & (blindR>stimL) & (blindR<stimR), ( (stimR-blindR)/(stimR-stimL)), final4['RightALLbottom'])
    
    final4['LeftALLbottom']  = np.where( (np.isnan(middle) == True) & (np.isnan(blindR) == False) & (np.isnan(blindL) == False) & (blindL<stimL) & (blindR>stimR), 0, final4['LeftALLbottom'])
    final4['RightALLbottom']  = np.where( (np.isnan(middle) == True) & (np.isnan(blindR) == False) & (np.isnan(blindL) == False) & (blindL<stimL) & (blindR>stimR), 0, final4['RightALLbottom'])

    return final4

# compute visual fields in the top side
def visual_fields_top(txtFile, final4, asym):
    
    # find stim according to conditions
    if asym == False:
        stimR = txtFile.rightstimx[0]
        stimL = txtFile.leftstimx[0]
    if asym == True:
        stimR = txtFile.righttopstimx[0]
        stimL = txtFile.lefttopstimx[0]
    
    # Give name to variable to make the next step easier to read and understand :    
    frontalR = final4["interceptfrontalRtop"]
    frontalL = final4["interceptfrontalLtop"]
    blindR = final4["interceptblindRtop"]
    blindL = final4["interceptblindLtop"]
    middle = final4['interceptmiddletop']

    
    # SPECIAL CASE : only frontal    
    final4['frontaltop'] = np.where( ((np.isnan(frontalL)==True) & (np.isnan(frontalR)==False) & (frontalR>stimR)) | ((np.isnan(frontalR)==True) & (np.isnan(frontalL)==False) & (frontalL<stimL)) | ((np.isnan(frontalR)==False) & (np.isnan(frontalL)==False) & (frontalL<stimL) & (frontalR>stimR)), 1, final4['frontaltop'])

    # SPECIAL CASE : only blind     
    final4['blindtop'] = np.where( ((np.isnan(blindL)==True) & (np.isnan(blindR)==False) & (blindR<stimL)) | ((np.isnan(blindR)==True) & (np.isnan(blindL)==False) & (blindL > stimL)) | ((np.isnan(blindR)==False) & (np.isnan(blindL)==False) & (blindL>stimR) & (blindR<stimL)), 1, final4['blindtop'])

    # SPECIAL CASE : only lateral-right           
    final4['lateralRighttop'] = np.where( ((np.isnan(frontalR)== False) & (frontalR<stimL) & ((blindR>stimR)|(np.isnan(blindR)== True))) | ((np.isnan(blindR)== False) & (blindR>stimR) & ((frontalR<stimL)|(np.isnan(frontalR)== True))), 1, final4['lateralRighttop'])
    
    # SPECIAL CASE : only lateral-left                 
    final4['lateralLefttop'] = np.where( ((np.isnan(frontalL)== False) & (frontalL>stimR) & ((blindL<stimL)|(np.isnan(blindL)== True))) | ((np.isnan(blindL)== False) & (blindL<stimL) & ((frontalL>stimR)|(np.isnan(frontalL)== True))), 1, final4['lateralLefttop'])

    # FRONTAL VIEW: mix between frontal and lateral-left  
    final4['frontaltop'] = np.where( (np.isnan(frontalL) == False) & (frontalL>stimL) & (frontalL<stimR) & ((frontalL<frontalR) | (np.isnan(frontalR)==True)), ((stimR - frontalL)/(stimR - stimL)), final4['frontaltop'])
    final4['lateralLefttop'] = np.where( (np.isnan(frontalL) == False) & (frontalL>stimL) & (frontalL<stimR) & ((frontalL<frontalR) | (np.isnan(frontalR)==True)), (1 - final4['frontaltop']), final4['lateralLefttop'])

    # FRONTAL VIEW: mix between frontal and lateral-right     
    final4['frontaltop'] = np.where( (np.isnan(frontalR) == False) & (frontalR<stimR) & (frontalR>stimL) & ((frontalR>frontalL) | (np.isnan(frontalL) == True)), ((frontalR - stimL)/(stimR - stimL)), final4['frontaltop'])
    final4['lateralRighttop'] = np.where( (np.isnan(frontalR) == False) & (frontalR<stimR) & (frontalR>stimL) & ((frontalR>frontalL) | (np.isnan(frontalL) == True)), (1 - final4['frontaltop']), final4['lateralRighttop'])  
      
    # FRONTAL VIEW: mix between frontal, lateral-left and lateral-right                  
    final4['lateralRighttop'] = np.where( (np.isnan(frontalR) == False) & (np.isnan(frontalL) == False) & (frontalR>frontalL) & (frontalR<stimR) & (frontalL>stimL), ((stimR - frontalR) / (stimR - stimL)), final4['lateralRighttop'])
    final4['lateralLefttop'] = np.where( (np.isnan(frontalR) == False) & (np.isnan(frontalL) == False) &(frontalR>frontalL) & (frontalR<stimR) & (frontalL>stimL), ((frontalL - stimL) / (stimR - stimL)), final4['lateralLefttop'])
    final4['frontaltop'] = np.where( (np.isnan(frontalR) == False) & (np.isnan(frontalL) == False) &(frontalR>frontalL) & (frontalR<stimR) & (frontalL>stimL), (1 - ( final4['lateralRighttop'] + final4['lateralLefttop'])), final4['frontaltop'])
 

    # BLIND VIEW: mix between blind and lateral-left
    final4['lateralLefttop'] = np.where( (np.isnan(blindL) == False) & (blindL > stimL) & (blindL < stimR) & ((blindL>blindR) | (np.isnan(blindR)==True)), ((stimR - blindL)/(stimR - stimL)), final4['lateralLefttop'])
    final4['blindtop'] = np.where( (np.isnan(blindL) == False) & (blindL > stimL) & (blindL < stimR) & ((blindL>blindR) | (np.isnan(blindR)==True)), (1 - final4['lateralLefttop']), final4['blindtop'])
     
    # BLIND VIEW: mix between blind and lateral-right     
    final4['lateralRighttop'] = np.where( (np.isnan(blindR) == False) & (blindR < stimR) & (blindR > stimL) & ((blindL>blindR) | (np.isnan(blindL) == True)), ((blindR - stimL)/(stimR - stimL)), final4['lateralRighttop'])
    final4['blindtop'] = np.where( (np.isnan(blindR) == False) & (blindR < stimR) &( blindR > stimL) & ((blindL>blindR) | (np.isnan(blindL) == True)), (1 - final4['lateralRighttop']), final4['blindtop'])
     
    # BLIND VIEW: mix between blind, lateral-left and lateral-right                  
    final4['lateralRighttop'] = np.where( (np.isnan(blindR) == False) & (np.isnan(blindL) == False) & (blindL>blindR) & (blindL<stimR) & (blindR>stimL), ((blindR - stimL) / (stimR - stimL)), final4['lateralRighttop'])
    final4['lateralLefttop'] = np.where( (np.isnan(blindR) == False) & (np.isnan(blindL) == False) & (blindL>blindR) & (blindL<stimR) & (blindR>stimL), ((stimR - blindL) / (stimR - stimL)), final4['lateralLefttop'])
    final4['blindtop'] = np.where( (np.isnan(blindR) == False) & (np.isnan(blindL) == False) & (blindL>blindR) & (blindL<stimR) & (blindR>stimL), (1 - ( final4['lateralRighttop'] + final4['lateralLefttop'])), final4['blindtop'])
    
    # check if error : if not, this column is supposed to be always equal to 1
    final4['sumalltop']= final4['blindtop'] + final4['frontaltop'] + final4['lateralRighttop'] + final4['lateralLefttop']
    
    # lateral without frontal
    final4['RightALLtop']  = np.where( ((np.isnan(middle) == False) & (middle<stimL) & ((blindR>stimR)|(np.isnan(blindR) == True))) | ((np.isnan(middle) == True) & (np.isnan(blindR) == False) & (blindR>stimR)), 1, final4['RightALLtop'])
    final4['LeftALLtop']  = np.where( ((np.isnan(middle) == False) & (middle>stimR)) & ((blindL<stimL)|(np.isnan(blindL) == True)) | ((np.isnan(middle) == True) & (np.isnan(blindL) == False) & (blindL<stimL)), 1, final4['LeftALLtop'])
    
    final4['LeftALLtop']  = np.where( (np.isnan(middle) == False) & (middle>stimL) & (middle<stimR), ((middle-stimL)/(stimR-stimL)), final4['LeftALLtop'])
    final4['RightALLtop']  = np.where( (np.isnan(middle) == False) & (middle>stimL) & (middle<stimR), 1-final4['LeftALLtop'], final4['RightALLtop'])
    
    final4['RightALLtop']  = np.where( ((np.isnan(middle) == True) | ((np.isnan(middle) == False)&(middle<stimL))) & (np.isnan(blindR) == False) &(blindR>stimL) & (blindR<stimR), ( (blindR-stimL)/(stimR-stimL)), final4['RightALLtop'])
    final4['LeftALLtop']  = np.where( ((np.isnan(middle) == True) | ((np.isnan(middle) == False)&(middle>stimR))) & (np.isnan(blindL) == False) & (blindL>stimL) & (blindL<stimR), ( (stimR-blindL)/(stimR-stimL)), final4['LeftALLtop'])
    
    final4['RightALLtop']  = np.where( (np.isnan(middle) == True) & (np.isnan(blindL) == False) & (np.isnan(blindR) == False) & (blindL>stimR) & (blindR<stimL), 0, final4['RightALLtop'])
    final4['LeftALLtop']  = np.where( (np.isnan(middle) == True) & (np.isnan(blindL) == False) & (np.isnan(blindR) == False) & (blindL>stimR) & (blindR<stimL), 0, final4['LeftALLtop'])

    return final4



## create data points to determinate visual fields
def create_visual_fields(txtFile, final4, frontalangle, lateralangle, cap, numbframes, asym, problem, resp_gofast) :    
    import interface
    ## create data points to determinate visual fields


    #rotate point created with 16.5 degrees difference (binoc vision)
    final4['frontalRX'], final4['frontalRY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'], math.radians(frontalangle))
    final4['frontalLX'], final4['frontalLY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'], math.radians(-frontalangle))
    
    #rotate point created with 27 degrees difference (blind vision)
    final4['blindRX'], final4['blindRY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'],  math.radians(lateralangle))
    final4['blindLX'], final4['blindLY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'],  math.radians(-lateralangle))

    #straight line between-the-eyes-point and top head y
    final4['m'] = slope(final4['topheadx'], final4['topheady'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])  
    final4['interceptmiddletop'] = np.where((final4['topheady']<final4['betweeneyesY']), (txtFile.topborder[0] - final4['c'])/final4['m'],  np.NaN)
    final4['interceptmiddlebottom'] = np.where((final4['topheady']>final4['betweeneyesY']), (txtFile.bottomborder[0] - final4['c'])/final4['m'], np.NaN)
    
    #straight line between-the-eyes-point and FRONTAL-vision-RIGHT point
    final4['m'] = slope(final4['frontalRX'], final4['frontalRY'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])  
    final4['interceptfrontalRtop'] = np.where((final4['frontalRY']<final4['betweeneyesY']), (txtFile.topborder[0] - final4['c'])/final4['m'],  np.NaN)
    final4['interceptfrontalRbottom'] = np.where((final4['frontalRY']>final4['betweeneyesY']), (txtFile.bottomborder[0] - final4['c'])/final4['m'], np.NaN)
    
    #straight line between-the-eyes-point and FRONTAL-vision-LEFT point
    final4['m'] = slope(final4['frontalLX'], final4['frontalLY'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])      
    final4['interceptfrontalLtop'] = np.where((final4['frontalLY']<final4['betweeneyesY']), (txtFile.topborder[0] - final4['c'])/final4['m'], np.NaN)
    final4['interceptfrontalLbottom'] = np.where((final4['frontalLY']>final4['betweeneyesY']), (txtFile.bottomborder[0] - final4['c'])/final4['m'], np.NaN)
    
    #straight line between-the-eyes-point and BLIND-vision-RIGHT point
    final4['m'] = slope(final4['blindRX'], final4['blindRY'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])     
    final4['interceptblindRtop'] = np.where((final4['blindRY']<final4['betweeneyesY']), (txtFile.topborder[0] - final4['c'])/final4['m'], np.NaN)
    final4['interceptblindRbottom'] = np.where((final4['blindRY']>final4['betweeneyesY']), (txtFile.bottomborder[0] - final4['c'])/final4['m'], np.NaN)
    
    #straight line between-the-eyes-point and BLIND-vision-LEFT point
    final4['m'] = slope(final4['blindLX'], final4['blindLY'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])      
    final4['interceptblindLtop'] = np.where((final4['blindLY']<final4['betweeneyesY']), (txtFile.topborder[0] - final4['c'])/final4['m'], np.NaN)
    final4['interceptblindLbottom'] = np.where((final4['blindLY']>final4['betweeneyesY']), (txtFile.bottomborder[0] - final4['c'])/final4['m'], np.NaN)
    
    # find visual fields for BOTTOM #
    final4['frontalbottom'] = 0
    final4['blindbottom']  = 0
    final4['lateralLeftbottom']  = 0
    final4['lateralRightbottom']  = 0  
    final4['LeftALLbottom']  = 0
    final4['RightALLbottom']  = 0  
    final4 = visual_fields_bottom(txtFile, final4, asym)

    # find visual fields for TOP #
    final4['frontaltop'] = 0
    final4['blindtop']  = 0
    final4['lateralLefttop']  = 0
    final4['lateralRighttop']  = 0
    final4['LeftALLtop']  = 0
    final4['RightALLtop']  = 0
    final4 = visual_fields_top(txtFile, final4, asym)
    
    
    # VISUALIZE 
    
    # copy table (useful if problem == True)
    finalgood = final4.copy()
    
    if resp_gofast == "n":
    
        # ask user if he wants to visualize
        response, numbpic, screen_width, screen_height = interface.visualize_fields_q1()
    
        if response == 'y':
            
            # if problem == True, reduced all dimensions by 2
            if problem == True :
                final4.iloc[:,2:final4.columns.get_loc("frontalleft")] = final4.iloc[:,:final4.columns.get_loc("frontalleft")]/2
                txtFile.iloc[:,8:] = txtFile.iloc[:,8:]/2
            
            # ask user to select the number of random frames
            #numbpic = interface.visualize_fields_q2()  
            
            # numbpic random frames selected
            randompic = random.sample(range(int(final4.frame_number[0]),int(final4.frame_number[-1:])), numbpic)
    
            # visualize for all frames        
            for picnum in randompic :
                
                indexpic = picnum - txtFile.startingframe[0] 
                cap.set(1,picnum); 
                ret, frame = cap.read() 
                
                # check whether stimulus in on the top or bottom if asym=False
                if asym==False:
                    if abs(txtFile.topborder[0] - txtFile.leftstimy[0]) < abs(txtFile.bottomborder[0] - txtFile.leftstimy[0]):             
                        side="top"
                    else:
                        side="bottom"
                else:
                    side="both"
                
                # create black rectangle where the white text will be printed
                lengthArena = txtFile.bottomborder[0] - txtFile.topborder[0]
                
                if asym==False:
                    center_stim_x = (txtFile.leftstimx + txtFile.rightstimx)/2
                    if side == "top":                    
                        center_stim_y = txtFile.topborder[0]
                    elif side == "bottom":
                        center_stim_y = txtFile.bottomborder[0]
                        
                elif asym==True:
                    center_stim_x_bottom = (txtFile.leftbottomstimx + txtFile.rightbottomstimx)/2
                    center_stim_y_bottom = txtFile.bottomborder[0]
                    center_stim_x_top = (txtFile.lefttopstimx + txtFile.righttopstimx)/2
                    center_stim_y_top = txtFile.topborder[0]

                if side == "top" or asym==True:
                    cv2.rectangle(frame, (90, int(txtFile.topborder[0] + lengthArena/10 - 10)), (350, int(txtFile.topborder[0] + lengthArena/10 + 130)), (0,0,0), -1)
                if side =="bottom" or asym==True:
                    cv2.rectangle(frame, (90, int(txtFile.topborder[0] + 7*lengthArena/10 - 20)), (350, int(txtFile.topborder[0] + 7*lengthArena/10 + 130)), (0,0,0), -1)
   
                # print text in each frames
                textprint=list() 
                textprint2=list() 
    
                for el in range(final4.columns.get_loc("frontaltop"), final4.columns.get_loc("sumalltop")):
                    if final4.iloc[indexpic, el] != 0:
                        textprint.append(final4.columns[el][:-3] + ' ' + str(round(final4.iloc[indexpic, el],3)))
                for el in range(final4.columns.get_loc("frontalbottom"), final4.columns.get_loc("sumallbottom")):
                    if final4.iloc[indexpic, el] != 0:
                        textprint2.append(final4.columns[el][:-6] + ' ' + str(round(final4.iloc[indexpic, el],3)))
                
    
                if side == "top" and asym==False:
                    index_angle_col = final4.columns.get_loc("angle")
                    textprint.append(final4.columns[index_angle_col] + ' ' + str(round(final4.iloc[indexpic, index_angle_col])) + ' deg')
                    for i in range(0,len(textprint)):
                        starttextpoint1 = txtFile.topborder[0] + lengthArena/10
                        cv2.putText(frame, textprint[i], (100,int(starttextpoint1)+(i*30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
                    
                elif side == "bottom" and asym==False:
                    index_angle_col = final4.columns.get_loc("angle")
                    textprint2.append(final4.columns[index_angle_col] + ' ' + str(round(final4.iloc[indexpic, index_angle_col])) + ' deg')
                    for i in range(0,len(textprint2)): 
                        starttextpoint2 = txtFile.topborder[0] + 7*lengthArena/10
                        cv2.putText(frame, textprint2[i], (100,int(starttextpoint2)+(i*30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
                
                elif asym==True:
                    index_angletop_col = final4.columns.get_loc("angle_stimtop")
                    textprint.append(final4.columns[index_angletop_col] + ' ' + str(round(final4.iloc[indexpic, index_angletop_col]))+ ' deg')
                    for i in range(0,len(textprint)):
                        starttextpoint1 = txtFile.topborder[0] + lengthArena/10
                        cv2.putText(frame, textprint[i], (100,int(starttextpoint1)+(i*30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
                    index_anglebot_col = final4.columns.get_loc("angle_stimbottom")
                    textprint2.append(final4.columns[index_anglebot_col] + ' ' + str(round(final4.iloc[indexpic, index_anglebot_col]))+ ' deg')
                    for i in range(0,len(textprint2)): 
                        starttextpoint2 = txtFile.topborder[0] + 7*lengthArena/10
                        cv2.putText(frame, textprint2[i], (100,int(starttextpoint2)+(i*30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
               
                    
                 # print visual fields
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRtop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRtop")]), int(txtFile.topborder[0])),(255,0,0),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRbottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRbottom")]), int(txtFile.bottomborder[0])),(255,0,0),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLtop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLtop")]), int(txtFile.topborder[0])),(255,0,0),2)        
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLbottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLbottom")]), int(txtFile.bottomborder[0])),(255,0,0),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRtop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRtop")]), int(txtFile.topborder[0])),(0, 255, 255),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRbottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRbottom")]), int(txtFile.bottomborder[0])),(0, 255, 255),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLtop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLtop")]), int(txtFile.topborder[0])),(0, 255, 255),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLbottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLbottom")]), int(txtFile.bottomborder[0])),(0, 255, 255),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")]), int(txtFile.topborder[0])),(0, 255, 0),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddlebottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddlebottom")]), int(txtFile.bottomborder[0])),(0, 255, 0),2)
                
                # print angle line
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc('betweeneyesX')])==False:
                    if side == "top" and asym==False :
                        cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(center_stim_x), int(txtFile.topborder[0])),(150, 150, 150),1)
                    elif side == "bottom" and asym==False:
                        cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(center_stim_x), int(txtFile.bottomborder[0])),(150, 150, 150),1)
                    elif asym == True:
                        cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(center_stim_x_bottom), int(txtFile.bottomborder[0])),(150, 150, 150),1)
                        cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(center_stim_x_top), int(txtFile.topborder[0])),(150, 150, 150),1)

                        
                # print stimuli borders
                if side=="top" and asym == False:
                    cv2.circle(frame, (int(txtFile.leftstimx[0]), int(txtFile.topborder[0])), 3, (68, 1, 84), -1)
                    cv2.circle(frame, (int(txtFile.rightstimx[0]), int(txtFile.topborder[0])), 3, (68, 1, 84), -1)
                    cv2.line(frame,( int(txtFile.leftstimx[0]), int(txtFile.topborder[0])),(int(txtFile.rightstimx[0]), int(txtFile.topborder[0])), (68, 1, 84),2)
                elif side=="bottom" and asym==False:
                    cv2.circle(frame, (int(txtFile.leftstimx[0]), int(txtFile.bottomborder[0])), 3, (68,1,84), -1)
                    cv2.circle(frame, (int(txtFile.rightstimx[0]), int(txtFile.bottomborder[0])), 3, (68,1,84), -1)
                    cv2.line(frame,( int(txtFile.leftstimx[0]), int(txtFile.bottomborder[0])),(int(txtFile.rightstimx[0]), int(txtFile.bottomborder[0])), (68, 1, 84),2)
                
                elif asym==True:
                    cv2.circle(frame, (int(txtFile.lefttopstimx[0]), int(txtFile.topborder[0])), 3, (68, 1, 84), -1)
                    cv2.circle(frame, (int(txtFile.righttopstimx[0]), int(txtFile.topborder[0])), 3, (68, 1, 84), -1)
                    cv2.line(frame,( int(txtFile.lefttopstimx[0]), int(txtFile.topborder[0])),(int(txtFile.righttopstimx[0]), int(txtFile.topborder[0])), (68, 1, 84),2)
                    cv2.circle(frame, (int(txtFile.leftbottomstimx[0]), int(txtFile.bottomborder[0])), 3, (68,1,84), -1)
                    cv2.circle(frame, (int(txtFile.rightbottomstimx[0]), int(txtFile.bottomborder[0])), 3, (68,1,84), -1)
                    cv2.line(frame,( int(txtFile.leftbottomstimx[0]), int(txtFile.bottomborder[0])),(int(txtFile.rightbottomstimx[0]), int(txtFile.bottomborder[0])), (68, 1, 84),2)

    
                # resize image (indeed, if they are too big, it is hard to see them on the screen)
                ratio_size = frame.shape[1]/frame.shape[0]
                imS = cv2.resize(frame, (int(screen_width/1.5), int((screen_width/1.5)/ratio_size)))
    
                # show frame on window
                cv2.imshow('Random_pictures', imS)
                
                # press any keyboard key to go to the next image
                cv2.waitKey(0)
                cv2.destroyAllWindows
            
    #cv2.destroyWindow('Random_pictures')     
    # if group by seconds, divide the results by the framerate    
    if numbframes != 1 :
        finalgood['frontalbottom'] = finalgood['frontalbottom'] / numbframes
        finalgood['blindbottom']  = finalgood['blindbottom']/ numbframes
        finalgood['lateralLeftbottom']  =  finalgood['lateralLeftbottom']/ numbframes
        finalgood['lateralRightbottom']  = finalgood['lateralRightbottom'] / numbframes
        finalgood['LeftALLbottom']  = finalgood['LeftALLbottom']/ numbframes
        finalgood['RightALLbottom']  = finalgood['RightALLbottom'] / numbframes
        finalgood['frontaltop'] = finalgood['frontaltop']/ numbframes
        finalgood['blindtop']  = finalgood['blindtop']/ numbframes
        finalgood['lateralLefttop']  = finalgood['lateralLefttop']/ numbframes
        finalgood['lateralRighttop']  = finalgood['lateralRighttop']/ numbframes
        finalgood['LeftALLtop']  = finalgood['LeftALLtop']/ numbframes
        finalgood['RightALLtop']  = finalgood['RightALLtop']/ numbframes
    
    # aks user if he wants to continue
    if resp_gofast == "n":
        resp = interface.visualize_fields_q3()
    else:
        resp= "y"
        
    return finalgood, resp

## If you want to check a specific frame, write in indexpic the index of the frame you want to visualize, uncomment and run this part
## to run this part, you have to run main_coordinator and answer no to 'Do you want to continue ?' question
#        indexpic = 98 
#        picnum = indexpic + txtFile.startingframe[0] 
#        
#        cap.set(1,picnum); 
#        ret, frame = cap.read() 
#        
#        # print text in each frames
#        textprint=list() 
#        textprint2=list() 
#        #textprint.append('index' + str(indexpic))
#        for el in range(final4.columns.get_loc("frontaltop"), final4.columns.get_loc("sumalltop")):
#            if final4.iloc[indexpic, el] != 0:
#                textprint.append(final4.columns[el][:-3] + ' ' + str(round(final4.iloc[indexpic, el],3)))
#        for el in range(final4.columns.get_loc("frontalbottom"), final4.columns.get_loc("sumallbottom")):
#            if final4.iloc[indexpic, el] != 0:
#                textprint2.append(final4.columns[el][:-6] + ' ' + str(round(final4.iloc[indexpic, el],3)))
#                
#        lengthArena = txtFile.bottomborder[0] - txtFile.topborder[0]
#        for i in range(0,len(textprint)):
#            starttextpoint1 = txtFile.topborder[0] + lengthArena/10
#            cv2.putText(frame, textprint[i], (100,int(starttextpoint1)+(i*30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
#        for i in range(0,len(textprint2)): 
#            starttextpoint2 = txtFile.topborder[0] + 7*lengthArena/10
#            cv2.putText(frame, textprint2[i], (100,int(starttextpoint2)+(i*30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
#        
#       
#        # print visual fields
#        import math
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRtop")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRtop")]), int(txtFile.topborder[0])),(0,0,255),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRbottom")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRbottom")]), int(txtFile.bottomborder[0])),(0,0,255),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLtop")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLtop")]), int(txtFile.topborder[0])),(0,0,255),2)        
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLbottom")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLbottom")]), int(txtFile.bottomborder[0])),(0,0,255),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRtop")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRtop")]), int(txtFile.topborder[0])),(255,0,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRbottom")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRbottom")]), int(txtFile.bottomborder[0])),(255,0,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLtop")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLtop")]), int(txtFile.topborder[0])),(255,0,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLbottom")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLbottom")]), int(txtFile.bottomborder[0])),(255,0,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")]), int(txtFile.topborder[0])),(0,250,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddlebottom")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddlebottom")]), int(txtFile.bottomborder[0])),(0,250,0),2)
#
#        if asym == False:
#            cv2.circle(frame, (int(txtFile.leftstimx[0]), int(txtFile.topborder[0])), 3, (0,255,0), -1)
#            cv2.circle(frame, (int(txtFile.leftstimx[0]), int(txtFile.bottomborder[0])), 3, (100,150,0), -1)
#            cv2.circle(frame, (int(txtFile.rightstimx[0]), int(txtFile.topborder[0])), 3, (0,255,0), -1)
#            cv2.circle(frame, (int(txtFile.rightstimx[0]), int(txtFile.bottomborder[0])), 3, (100,150,0), -1) 
#        if asym == True :
#            cv2.circle(frame, (int(txtFile.lefttopstimx[0]), int(txtFile.topborder[0])), 3, (0,255,0), -1)
#            cv2.circle(frame, (int(txtFile.lefttopstimx[0]), int(txtFile.bottomborder[0])), 3, (100,150,0), -1)
#            cv2.circle(frame, (int(txtFile.rightbottomstimx[0]), int(txtFile.topborder[0])), 3, (0,255,0), -1)
#            cv2.circle(frame, (int(txtFile.rightbottomstimx[0]), int(txtFile.bottomborder[0])), 3, (100,150,0), -1) 
#
#        cv2.imshow('great_window', frame)
#
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("leftheadx")]),int(final4.iloc[indexpic, final4.columns.get_loc("leftheady")])), 3, (255,255,255), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("rightheadx")]),int(final4.iloc[indexpic, final4.columns.get_loc("rightheady")])), 3, (255,255,255), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("topheadx")]),int(final4.iloc[indexpic, final4.columns.get_loc("topheady")])), 3, (255,255,255), -1)
#    
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]),int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])), 3, (0,255,0), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("frontalRX")]),int(final4.iloc[indexpic, final4.columns.get_loc("frontalRY")])), 3, (255,0,0), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("frontalLX")]),int(final4.iloc[indexpic, final4.columns.get_loc("frontalLY")])), 3, (255,100,0), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("blindRX")]),int(final4.iloc[indexpic, final4.columns.get_loc("blindRY")])), 3, (0,100,255), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("blindLX")]),int(final4.iloc[indexpic, final4.columns.get_loc("blindLY")])), 3, (0,0,255), -1)
#    
#       
#        
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")]),int(txtFile.topborder[0])), 3, (0,100,255), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("blindLX")]),int(final4.iloc[indexpic, final4.columns.get_loc("blindLY")])), 3, (0,0,255), -1)
#
#        
#        # show frame on window
#        cv2.imshow('great_window', frame)
#                        

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
import pandas as pd


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
    if (asym==False) :
        stim = final4["stimx"]
    if (asym==True):
        stim = final4["stimbottomx"]
        
    # Give name to variable to make the next step easier to read and understand :    
    frontalR = final4["interceptfrontalRbottom"]
    frontalL = final4["interceptfrontalLbottom"]
    blindR = final4["interceptblindRbottom"]
    blindL = final4["interceptblindLbottom"]
    middle = final4['interceptmiddlebottom']
    
    # SPECIAL CASE : only frontal    
    final4['frontalbottom'] = np.where( ((np.isnan(frontalL)==False) & (np.isnan(frontalR)==False) & (frontalR<stim) & (frontalL>stim)) | ((np.isnan(frontalR)==False) & (np.isnan(frontalL)==True) & (frontalR<stim)) | ((np.isnan(frontalL)==False) & (np.isnan(frontalR)==True) & (frontalL>stim)), 1, final4['frontalbottom'])

    # SPECIAL CASE : only blind     
    final4['blindbottom'] = np.where( ((np.isnan(blindL)==True) & (np.isnan(blindR)==False) & (blindR>stim)) | ((np.isnan(blindR)==True) & (np.isnan(blindL)==False) & (blindL<stim)) | ((np.isnan(blindR)==False) & (np.isnan(blindL)==False) & (blindL<stim) & (blindR>stim)), 1, final4['blindbottom'])

    # SPECIAL CASE : only lateral-right           
    final4['lateralRightbottom'] = np.where( ((np.isnan(frontalR)== False) & (frontalR>stim) & ((blindR<stim)|(np.isnan(blindR)== True))) | ((np.isnan(blindR)== False) & (blindR<stim) & ((frontalR>stim)|(np.isnan(frontalR)== True))) , 1, final4['lateralRightbottom'])
                                                
    # SPECIAL CASE : only lateral-left                 
    final4['lateralLeftbottom'] = np.where( ((np.isnan(frontalL)== False) & (frontalL<stim) & ((blindL>stim)|(np.isnan(blindL)== True))) | ((np.isnan(blindL)== False) & (blindL>stim) & ((frontalL<stim)|(np.isnan(frontalL)== True))), 1, final4['lateralLeftbottom'])
                                            
    # check if error : if not, this column is supposed to be always equal to 1
    final4['sumallbottom']= final4['blindbottom'] + final4['frontalbottom'] + final4['lateralRightbottom'] + final4['lateralLeftbottom']
    
    # lateral without frontal
    final4['LeftALLbottom']  = np.where( ((np.isnan(middle) == False) & (middle<stim) & (final4['blindbottom'] !=1)) | ((np.isnan(middle) == True) & (np.isnan(blindL) == False) & (blindL>stim)), 1, final4['LeftALLbottom'])
    
    final4['RightALLbottom']  = np.where( ((np.isnan(middle) == False) & (middle>stim) & (final4['blindbottom'] !=1)) | ((np.isnan(middle) == True) & (np.isnan(blindR) == False) & (blindR<stim)), 1, final4['RightALLbottom'])

    return final4

# compute visual fields in the top side
def visual_fields_top(txtFile, final4, asym):
    
    # find stim according to conditions
    if (asym==False) :
        stim = final4["stimx"]
    if (asym==True):
        stim = final4["stimtopx"]

    # Give name to variable to make the next step easier to read and understand :    
    frontalR = final4["interceptfrontalRtop"]
    frontalL = final4["interceptfrontalLtop"]
    blindR = final4["interceptblindRtop"]
    blindL = final4["interceptblindLtop"]
    middle = final4['interceptmiddletop']

    
    # SPECIAL CASE : only frontal    
    final4['frontaltop'] = np.where( ((np.isnan(frontalL)==False) & (np.isnan(frontalR)==False) & (frontalR>stim) & (frontalL<stim)) | ((np.isnan(frontalR)==True) & (np.isnan(frontalL)==False) & (frontalL<stim)) | ((np.isnan(frontalR)==True) & (np.isnan(frontalL)==False) & (frontalR>stim)), 1, final4['frontaltop'])

    # SPECIAL CASE : only blind     
    final4['blindtop'] = np.where( ((np.isnan(blindL)==True) & (np.isnan(blindR)==False) & (blindR<stim)) | ((np.isnan(blindR)==True) & (np.isnan(blindL)==False) & (blindL > stim)) | ((np.isnan(blindR)==False) & (np.isnan(blindL)==False) & (blindL>stim) & (blindR<stim)), 1, final4['blindtop'])

    # SPECIAL CASE : only lateral-right           
    final4['lateralRighttop'] = np.where( ((np.isnan(frontalR)== False) & (frontalR<stim) & ((blindR>stim)|(np.isnan(blindR)== True))) | ((np.isnan(blindR)== False) & (blindR>stim) & ((frontalR<stim)|(np.isnan(frontalR)== True))), 1, final4['lateralRighttop'])
    
    # SPECIAL CASE : only lateral-left                 
    final4['lateralLefttop'] = np.where( ((np.isnan(frontalL)== False) & (frontalL>stim) & ((blindL<stim)|(np.isnan(blindL)== True))) | ((np.isnan(blindL)== False) & (blindL<stim) & ((frontalL>stim)|(np.isnan(frontalL)== True))), 1, final4['lateralLefttop'])

   
    # check if error : if not, this column is supposed to be always equal to 1
    final4['sumalltop']= final4['blindtop'] + final4['frontaltop'] + final4['lateralRighttop'] + final4['lateralLefttop']
    
    # lateral without frontal
    final4['RightALLtop']  = np.where( ((np.isnan(middle) == False) & (middle<stim) & (final4['blindtop'] !=1)) | ((np.isnan(middle) == True) & (np.isnan(blindR) == False) & (blindR>stim)), 1, final4['RightALLtop'])
    
    final4['LeftALLtop']  = np.where( ((np.isnan(middle) == False) & (middle>stim)& (final4['blindtop'] !=1)) | ((np.isnan(middle) == True) & (np.isnan(blindL) == False) & (blindL<stim)), 1, final4['LeftALLtop'])    
  
    return final4



## create data points to determinate visual fields
def create_visual_fields(txtFile, final4, frontalangle, lateralangle, cap, numbframes, asym, problem, resp_gofast) :    
    import interface
    ## create data points to determinate visual fields
    # create column for point between the eyes : x and y
    final4['betweeneyesX'] = (final4['leftheadx'] + final4['rightheadx'])/2
    final4['betweeneyesY'] = (final4['leftheady'] + final4['rightheady'])/2
    
    #rotate point created with 16.5 degrees difference (binoc vision)
    final4['frontalRX'], final4['frontalRY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'], math.radians(frontalangle))
    final4['frontalLX'], final4['frontalLY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'], math.radians(-frontalangle))
    
    #rotate point created with 27 degrees difference (blind vision)
    final4['blindRX'], final4['blindRY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'],  math.radians(lateralangle))
    final4['blindLX'], final4['blindLY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'],  math.radians(-lateralangle))

    
    ######### ok
    #prop = (txtFile.bottomborder[0] - txtFile.topborder[0]) / 10

    #subdf_right = final4[ (final4['betweeneyesX'] > final4['stimx']) & ((final4['betweeneyesY'] < (final4['stimy'] + prop)) &  (final4['betweeneyesY'] > (final4['stimy'] - prop)))   ]
    #subdf_left = final4[ (final4['betweeneyesX'] < final4['stimx']) & ((final4['betweeneyesY'] < (final4['stimy'] + prop)) &  (final4['betweeneyesY'] > (final4['stimy'] - prop)))   ]
    final4['myindex'] = range(len(final4))
    subdf_top = final4[final4['betweeneyesY'] > final4['stimy']]
    subdf_bottom = final4[final4['betweeneyesY'] < final4['stimy']]
    subdf_nan = final4[final4['betweeneyesY'].isna()]

    #straight line between-the-eyes-point and top head y
    subdf_top['m'] = slope(subdf_top['topheadx'], subdf_top['topheady'], subdf_top['betweeneyesX'], subdf_top['betweeneyesY'])
    subdf_top['c'] = yintercept(subdf_top['betweeneyesX'], subdf_top['betweeneyesY'], subdf_top['m'])
    subdf_bottom['m'] = slope(subdf_bottom['topheadx'], subdf_bottom['topheady'], subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'])
    subdf_bottom['c'] = yintercept(subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'], subdf_bottom['m'])
    subdf_top['interceptmiddletop'] = np.where((subdf_top['topheady']<subdf_top['betweeneyesY']), (subdf_top['stimy'] - subdf_top['c'])/subdf_top['m'],  np.NaN)
    subdf_bottom['interceptmiddlebottom'] = np.where((subdf_bottom['topheady']>subdf_bottom['betweeneyesY']), (subdf_bottom['stimy'] - subdf_bottom['c'])/subdf_bottom['m'], np.NaN)
 
    #straight line between-the-eyes-point and FRONTAL-vision-RIGHT point
    subdf_top['m'] = slope(subdf_top['frontalRX'], subdf_top['frontalRY'], subdf_top['betweeneyesX'], subdf_top['betweeneyesY'])
    subdf_top['c'] = yintercept(subdf_top['betweeneyesX'], subdf_top['betweeneyesY'], subdf_top['m'])
    subdf_bottom['m'] = slope(subdf_bottom['frontalRX'], subdf_bottom['frontalRY'], subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'])
    subdf_bottom['c'] = yintercept(subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'], subdf_bottom['m'])
    subdf_top['interceptfrontalRtop'] = np.where((subdf_top['frontalRY']<subdf_top['betweeneyesY']), (subdf_top['stimy'] - subdf_top['c'])/subdf_top['m'],  np.NaN)
    subdf_bottom['interceptfrontalRbottom'] = np.where((subdf_bottom['frontalRY']>subdf_bottom['betweeneyesY']), (subdf_bottom['stimy'] - subdf_bottom['c'])/subdf_bottom['m'], np.NaN)
    
    #straight line between-the-eyes-point and FRONTAL-vision-LEFT point
    subdf_top['m'] = slope(subdf_top['frontalLX'], subdf_top['frontalLY'], subdf_top['betweeneyesX'], subdf_top['betweeneyesY'])
    subdf_top['c'] = yintercept(subdf_top['betweeneyesX'], subdf_top['betweeneyesY'], subdf_top['m'])
    subdf_bottom['m'] = slope(subdf_bottom['frontalLX'], subdf_bottom['frontalLY'], subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'])
    subdf_bottom['c'] = yintercept(subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'], subdf_bottom['m'])
    subdf_top['interceptfrontalLtop'] = np.where((subdf_top['frontalLY']<subdf_top['betweeneyesY']), (subdf_top['stimy'] - subdf_top['c'])/subdf_top['m'], np.NaN)
    subdf_bottom['interceptfrontalLbottom'] = np.where((subdf_bottom['frontalLY']>subdf_bottom['betweeneyesY']), (subdf_bottom['stimy'] - subdf_bottom['c'])/subdf_bottom['m'], np.NaN)
    
    #straight line between-the-eyes-point and BLIND-vision-RIGHT point
    subdf_top['m'] = slope(subdf_top['blindRX'], subdf_top['blindRY'], subdf_top['betweeneyesX'], subdf_top['betweeneyesY'])
    subdf_top['c'] = yintercept(subdf_top['betweeneyesX'], subdf_top['betweeneyesY'], subdf_top['m'])
    subdf_bottom['m'] = slope(subdf_bottom['blindRX'], subdf_bottom['blindRY'], subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'])
    subdf_bottom['c'] = yintercept(subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'], subdf_bottom['m'])
    subdf_top['interceptblindRtop'] = np.where((subdf_top['blindRY']<subdf_top['betweeneyesY']), (subdf_top['stimy'] - subdf_top['c'])/subdf_top['m'], np.NaN)
    subdf_bottom['interceptblindRbottom'] = np.where((subdf_bottom['blindRY']>subdf_bottom['betweeneyesY']), (subdf_bottom['stimy'] - subdf_bottom['c'])/subdf_bottom['m'], np.NaN)
    
    #straight line between-the-eyes-point and BLIND-vision-LEFT point
    subdf_top['m'] = slope(subdf_top['blindLX'], subdf_top['blindLY'], subdf_top['betweeneyesX'], subdf_top['betweeneyesY'])
    subdf_top['c'] = yintercept(subdf_top['betweeneyesX'], subdf_top['betweeneyesY'], subdf_top['m'])
    subdf_bottom['m'] = slope(subdf_bottom['blindLX'], subdf_bottom['blindLY'], subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'])
    subdf_bottom['c'] = yintercept(subdf_bottom['betweeneyesX'], subdf_bottom['betweeneyesY'], subdf_bottom['m'])
    subdf_top['interceptblindLtop'] = np.where((subdf_top['blindLY']<subdf_top['betweeneyesY']), (subdf_top['stimy'] - subdf_top['c'])/subdf_top['m'], np.NaN)
    subdf_bottom['interceptblindLbottom'] = np.where((subdf_bottom['blindLY']>subdf_bottom['betweeneyesY']), (subdf_bottom['stimy'] - subdf_bottom['c'])/subdf_bottom['m'], np.NaN)
    
    
    ############################
    
    
    # find visual fields for BOTTOM #
    subdf_bottom['frontalbottom'] = 0
    subdf_bottom['blindbottom']  = 0
    subdf_bottom['lateralLeftbottom']  = 0
    subdf_bottom['lateralRightbottom']  = 0  
    subdf_bottom['LeftALLbottom']  = 0
    subdf_bottom['RightALLbottom']  = 0  
    subdf_bottom = visual_fields_bottom(txtFile, subdf_bottom, asym)

    # find visual fields for TOP #
    subdf_top['frontaltop'] = 0
    subdf_top['blindtop']  = 0
    subdf_top['lateralLefttop']  = 0
    subdf_top['lateralRighttop']  = 0
    subdf_top['LeftALLtop']  = 0
    subdf_top['RightALLtop']  = 0
    subdf_top = visual_fields_top(txtFile, subdf_top, asym)
    
    frames = [subdf_bottom, subdf_top, subdf_nan]
    #frames = [subdf_bottom, subdf_top]

    final4 = pd.concat(frames)
    final4 = final4.sort_values(by=['myindex'])
    del final4["myindex"]
       
    # VISUALIZE 
    
    # copy table (useful if problem == True)
    finalgood = final4.copy()
    
    if resp_gofast == "n":
        # ask user if he wants to visualize
        response, numbpic, screen_width, screen_height = interface.visualize_fields_q1()
    
        if response == 'y':
            
            # if problem == True, reduced all dimensions by 2        
            if problem == True :
                final4.iloc[:,2:final4.columns.get_loc("interceptblindLright")] = final4.iloc[:,:final4.columns.get_loc("interceptblindLright")]/2
                txtFile.iloc[:,8:] = txtFile.iloc[:,8:]/2
            
            # ask user to select the number of random frames
            #numbpic = interface.visualize_fields_q2()  
            
            final4 = final4.reset_index()
    
            # numbpic random frames selected
            randompic = random.sample(range(int(final4.frame_number[0]),int(final4.frame_number[-1:])), numbpic)
    
            # visualize for all frames        
            for picnum in randompic :
                indexpic = final4.index[final4['frame_number']==picnum].tolist()[0]
                cap.set(1,picnum); 
                ret, frame = cap.read() 
    
                # print text in each frames
                textprint=list() 
                textprint2=list() 
        
                # print text
                for el in (final4.columns.get_loc("LeftALLbottom"), final4.columns.get_loc("RightALLbottom"), final4.columns.get_loc("blindbottom"), final4.columns.get_loc("frontalbottom"), final4.columns.get_loc("lateralLeftbottom"), final4.columns.get_loc("lateralRightbottom"), final4.columns.get_loc("LeftALLtop"), final4.columns.get_loc("RightALLtop"), final4.columns.get_loc("blindtop"), final4.columns.get_loc("frontaltop"), final4.columns.get_loc("lateralLefttop"), final4.columns.get_loc("lateralRighttop")):
                    if final4.iloc[indexpic, el] != 0 and math.isnan(final4.iloc[indexpic, el])==False:
                        textprint.append(final4.columns[el] + ' ' + str(round(final4.iloc[indexpic, el],3)))

                # print angle
                index_angle_col = final4.columns.get_loc("angle")
                textprint.append(final4.columns[index_angle_col] + ' ' + str(round(final4.iloc[indexpic, index_angle_col])) + ' deg')

                    
                lengthArena = txtFile.arenarightx[0] - txtFile.arenaleftx[0]
                for i in range(0,len(textprint)):
                    starttextpoint1 = txtFile.arenaupy[0] + lengthArena/10
                    cv2.putText(frame, textprint[i], (100,int(starttextpoint1)+(i*30)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
    
                #cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])), 3, (255,0,0), -1)          
                #cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("topheadx")]), int(final4.iloc[indexpic, final4.columns.get_loc("topheady")])), 3, (0,0,255), -1)
                #cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("leftheadx")]), int(final4.iloc[indexpic, final4.columns.get_loc("leftheady")])), 3, (0,255,0), -1)
                #cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("rightheadx")]), int(final4.iloc[indexpic, final4.columns.get_loc("rightheady")])), 3, (0,255,0), -1)
    
    
                 # print visual fields
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRtop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRtop")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(255,0,0),2) # red
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRbottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRbottom")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(255,0,0),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLtop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLtop")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(255,0,0),2)        
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLbottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLbottom")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(255,0,0),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRtop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRtop")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(0, 255, 255),2) # blue
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRbottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRbottom")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(0, 255, 255),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLtop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLtop")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(0, 255, 255),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLbottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLbottom")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(0, 255, 255),2)
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(0, 255, 0),2) # vert
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddlebottom")])== False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddlebottom")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])),(0, 255, 0),2)
                
                # print stimuli borders
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("stimx")])== False:
                    cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("stimx")]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])), 3, (68, 1, 84), -1)
    
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc('betweeneyesX')])==False:
                    cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic,final4.columns.get_loc("stimx")]), int(final4.iloc[indexpic,final4.columns.get_loc("stimy")])),(150, 150, 150),1)
               
                # show frame on window
                cv2.imshow('Random_pictures', frame)
                
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
#        indexpic = 140 
#        picnum = indexpic + txtFile.startingframe[0] 
#        
#        cap.set(1,picnum); 
#        ret, frame = cap.read() 
#        
#        # print text in each frames
#        textprint=list() 
#        textprint.append('index' + str(indexpic))
#        for el in range(final4.columns.get_loc("frontalleft"), final4.columns.get_loc("sumallleft")):
#            if final4.iloc[indexpic, el] != 0:
#                textprint.append(final4.columns[el] + ' ' + str(round(final4.iloc[indexpic, el],3)))
#        for el in range(final4.columns.get_loc("frontalright"), final4.columns.get_loc("sumallright")):
#            if final4.iloc[indexpic, el] != 0:
#                textprint.append(final4.columns[el] + ' ' + str(round(final4.iloc[indexpic, el],3)))
#        
#        for i in range(0,len(textprint)):
#            cv2.putText(frame, textprint[i], (100,150+i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
#        
#        import math
#        # print visual fields
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRtop")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRtop")]), int(txtFile.topborder[0])),(0,0,255),2)
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRbottom")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRbottom")]), int(txtFile.bottomborder[0])),(0,0,255),2)
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLtop")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLtop")]), int(txtFile.topborder[0])),(0,0,255),2)        
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLbottom")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLbottom")]), int(txtFile.bottomborder[0])),(0,0,255),2)
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRtop")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRtop")]), int(txtFile.topborder[0])),(255,0,0),2)
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRbottom")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRbottom")]), int(txtFile.bottomborder[0])),(255,0,0),2)
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLtop")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLtop")]), int(txtFile.topborder[0])),(255,0,0),2)
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLbottom")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLbottom")]), int(txtFile.bottomborder[0])),(255,0,0),2)
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")]), int(txtFile.topborder[0])),(0,250,0),2)
#            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddlebottom")])== False:
#                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddlebottom")]), int(txtFile.bottomborder[0])),(0,250,0),2)
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
#        cv2.circle(frame, (int(txtFile.leftborder[0]), int(txtFile.topstimy[0])), 3, (0,255,0), -1)
#        cv2.circle(frame, (int(txtFile.leftborder[0]), int(txtFile.bottomstimy[0])), 3, (100,150,0), -1)
#        cv2.circle(frame, (int(txtFile.rightborder[0]), int(txtFile.topstimy[0])), 3, (0,255,0), -1)
#        cv2.circle(frame, (int(txtFile.rightborder[0]), int(txtFile.bottomstimy[0])), 3, (100,150,0), -1) 
#        
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")]),int(txtFile.topborder[0])), 3, (0,100,255), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("blindLX")]),int(final4.iloc[indexpic, final4.columns.get_loc("blindLY")])), 3, (0,0,255), -1)
#
#        
#        # show frame on window
#        cv2.imshow('great_window', frame)
#                

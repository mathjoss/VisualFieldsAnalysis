# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 14:54:18 2019

@author: mathilde.josserand
"""
import sys
import pandas as pd
import cv2
import numpy as np
import tkinter
import tkinter.ttk
from tkinter import filedialog
import shutil
import os


sys.path.append('modules/')


# import all the subfiles
import interface
import step1
import step2
import step3
import step4_lr_fixstim
import step4_bt_fixstim
import step4_lr_movstim
import step4_bt_movstim

# precomplete cases
if 'animal_type' in locals() or 'animal_type' in globals():
    pre_chick = animal_type
else:
    pre_chick = "chick"

if 'orientation' in locals() or 'orientation' in globals():
    pre_orient = orientation
else:
    pre_orient = "bt"

if 'pathdlc' in locals() or 'pathdlc' in globals():
    pre_dlc = pathdlc
else:
    pre_dlc = "No folder path selected yet"

if 'pathvideo1' in locals() or 'pathvideo1' in globals():
    pre_video = pathvideo1
else:
    pre_video = "No folder path selected yet"

if 'pathvideoproblem' in locals() or 'pathvideoproblem' in globals():
    pre_video2 = pathvideoproblem
else:
    pre_video2 = "No folder path selected yet"

if 'excelfile' in locals() or 'excelfile' in globals():
    pre_excel = excelfile
else:

    pre_excel = "No file path selected yet"

if 'problem' in locals() or 'problem' in globals():
    pre_problem = problem
else:
    pre_problem = False

if 'videoname' in locals() or 'videoname' in globals():
    pre_vidname = videoname
else:
    pre_vidname = "fish%s.avi"
    
if 'movfix' in locals() or 'movfix' in globals():
    pre_mov = movfix
else:
    pre_mov = 0

if 'asym' in locals() or 'asym' in globals():
    pre_asym = asym
else:
    pre_asym = False

if 'area1' in locals() or 'area1' in globals():
    pre_area1 = area1
else:
    pre_area1 = 10

if 'area2' in locals() or 'area2' in globals():
    pre_area2 = area2
else:
    pre_area2 = 30
    
if 'area3' in locals() or 'area3' in globals():
    pre_area3 = area3
else:
    pre_area3 = 50
    
if 'area4' in locals() or 'area4' in globals():
    pre_area4 = area4
else:
    pre_area4 = 30

if 'area5' in locals() or 'area5' in globals():
    pre_area5 = area5
else:
    pre_area5 = 10
  
if 'frontalangle' in locals() or 'frontalangle' in globals():
    pre_front = frontalangle
else:
    pre_front = 15

if 'lateralangle' in locals() or 'lateralangle' in globals():
    pre_lat = lateralangle
else:
    pre_lat = 150
 
if 'numbframes' in locals() or 'numbframes' in globals():
    pre_groupby = rec
else:
    pre_groupby = 2

if 'animal_ID' in locals() or 'animal_ID' in globals():
    pre_anID = animal_ID
else:
    pre_anID = "1 3 5.1 5.2"

if 'thresh' in locals() or 'thresh' in globals():
    pre_thres = thresh
else:
    pre_thres = 3

    
# take all information from user
animal_type, orientation, pathdlc, pathvideo1, problem, pathvideoproblem, excelfile, videoname, movfix, asym, area1, area2, area3, area4, area5, frontalangle, lateralangle, numbframes, animal_ID, thresh = interface.ask_parameters(pre_chick, pre_orient, pre_dlc, pre_video, pre_video2, pre_problem, pre_excel, pre_vidname, pre_mov, pre_asym, pre_area1, pre_area2, pre_area3, pre_area4, pre_area5, pre_front, pre_lat, pre_groupby, pre_anID, pre_thres)

rec = numbframes

if pathdlc =='':
    pathdlc= pre_dlc
else:
    pathdlc = pathdlc + '/'
    
if pathvideo1 =='':
    pathvideo1= pre_video

if pathvideoproblem =='':
    pathvideoproblem= pre_video2

if excelfile =='':
    excelfile= pre_excel
# path video        
pathvideo = pathvideo1 + '/' + videoname

# path dlc

# path folder where folders file and results will be included
pathgeneral = os.path.dirname(pathdlc)

# path folder files
pathfile = pathgeneral + '/data_files'
if os.path.isdir(pathfile) == False and pathgeneral != "":
    os.mkdir(pathfile) # create new folder only when the pathdlc has been set

# path folder results
finaloutputpath = pathgeneral + '/results'
if os.path.isdir(finaloutputpath) == False and pathgeneral != "":
    os.mkdir(finaloutputpath) # create new folder

# path of videos if problem
if problem == True :
    pathvideoconverted = pathvideoproblem + '/' + videoname
else:
    pathvideoconverted = pathvideo

# split ID list
IDList = animal_ID.split(' ')

# read excel file
try:
    input_xls = pd.ExcelFile(excelfile)
except:
    interface.error_excel_file(excelfile)
    sys.exit()

ID = IDList[0]

try:
    inputDlc = pd.read_csv(pathdlc + animal_type + '%s_dlc.csv' %ID, sep=',')  
except:
    interface.error_dlc_file(pathdlc, animal_type, ID)
    sys.exit()

cap = cv2.VideoCapture(pathvideo %ID)
success,frame=cap.read()

if success==False :
    interface.error_video(pathvideo, ID)
    sys.exit()   

# run steps
for ID in IDList :
    print('\n ***********  analysis of ' + animal_type + ' ' + str(ID) + ' ************')
    
    # read video
    cap = cv2.VideoCapture(pathvideo %ID)
    camarche = 0
    # if user want to group by seconds, compute the framerate of the video
    framerate = int(cap.get(cv2.CAP_PROP_FPS))
    # if frame rate is too high, error: ask user what the real framerate is
    if framerate > 80:
        print('problem with encoding of the video : too high frame rate perceived')
        framerate = int(input('write the framerate of the video : '))
    
    if numbframes ==2:
        numbframes= framerate
    ###### STEP 1 : create new file with arena borders data and 
    if orientation =='lr' :
        step1.create_new_file_lr(cap, ID, input_xls, animal_type, pathfile, movfix, asym, framerate) # change the fact that we write manually those values
    elif orientation == 'bt':
        step1.create_new_file_bt(cap, ID, input_xls, animal_type, pathfile, movfix, asym, framerate) # change the fact that we write manually those values

    # read txtFile
    txtFile = pd.read_csv(pathfile + '/' + animal_type + '%s.csv' %ID, sep=',')
    txtFile.columns = map(str.lower, txtFile.columns)
    
    # readDeeplabcut file
    inputDlc = pd.read_csv(pathdlc + animal_type + '%s_dlc.csv' %ID, sep=',')
    twofirstrows = inputDlc.iloc[:2]
    inputDlc = inputDlc.iloc[2:]
    
    # convert all data to numeric in DLC file
    for el in list(inputDlc) :
        inputDlc[el] = pd.to_numeric(inputDlc[el]) 
    
    # create new columns name
    twofirstrows = twofirstrows.transpose()   
    if (asym==True) & (movfix ==1):
        for row in range(twofirstrows.shape[0]):
            if (("stim" in str(twofirstrows.iloc[row,0].lower())) & ("left" in str(twofirstrows.iloc[row,0].lower()))) == True :
                twofirstrows.iloc[row,0] = 'stimleft'
            if (("stim" in str(twofirstrows.iloc[row,0].lower())) & ("right" in str(twofirstrows.iloc[row,0].lower()))) == True :
                twofirstrows.iloc[row,0] = 'stimright' 
               
    if (asym==False) & (movfix ==1):
        for row in range(twofirstrows.shape[0]):
            if ("stim" in str(twofirstrows.iloc[row,0].lower())) == True :
                twofirstrows.iloc[row,0] = 'stim'
    twofirstrows['listcolumns'] = twofirstrows[0] + twofirstrows[1]
    columlist = map(str.lower, twofirstrows['listcolumns'])
    columlist = [w.replace('bodypartscoords', 'frame_number') for w in columlist]
    inputDlc = inputDlc.set_axis(columlist, axis=1, inplace=False)
    inputDlc.columns = map(str.lower, inputDlc.columns)
    
     # Remove the frame we are not interested in
    trialFrames = inputDlc[txtFile.startingframe.iloc[0]:txtFile.endingframe.iloc[0]+1]

    # Create index from 1 to lenght of the dataframe
    trialFrames = trialFrames.reset_index() 
    
    ####### STEP 2 : check errors in Deeplabcut file  
    # read video
    cap = cv2.VideoCapture(pathvideo %ID)
    # check errors and return table with NAN
    trialFrames, trialFrames_for_loc, frame_number = step2.check_errors(cap, trialFrames, txtFile, orientation, thresh, movfix, asym)

    
    ######## STEP 3 : compute location
    if orientation == 'lr' :
        trialFrames, final4 = step3.find_location_lr(trialFrames, trialFrames_for_loc, txtFile, area1, area2, area3, area4, area5, numbframes)
    elif orientation =='bt' :
        trialFrames, final4 = step3.find_location_bt(trialFrames, trialFrames_for_loc, txtFile, area1, area2, area3, area4, area5, numbframes)
       
        
    ######## STEP 4 : compute visual fields    
    if problem == True :
        cap = cv2.VideoCapture(pathvideoconverted %ID) # read video converted
        
    if (orientation == 'lr') & (movfix == 0):
        final4 = step4_lr_fixstim.create_visual_fields(txtFile, final4, frontalangle, lateralangle, cap, numbframes, asym, problem)
    elif (orientation == 'bt')  & (movfix == 0):
        final4 = step4_bt_fixstim.create_visual_fields(txtFile, final4, frontalangle, lateralangle, cap, numbframes, asym, problem)
    elif (orientation == 'lr')  & (movfix == 1):
        final4 = step4_lr_movstim.create_visual_fields(txtFile, final4, frontalangle, lateralangle, cap, numbframes, asym, problem)
    elif (orientation == 'bt')  & (movfix == 1):
        final4 = step4_bt_movstim.create_visual_fields(txtFile, final4, frontalangle, lateralangle, cap, numbframes, asym, problem)
        
        
    ###### STEP 6 : prepare final table   
    final5 = final4.copy()  
    
    # remove unuseful columns    
    if orientation == 'lr':
        final5 = final5[['leftheadx', 'distanceMoved','LEFTCLOSE', 'LEFT', 'CENTER', 'RIGHT', 'RIGHTCLOSE', 'frontalleft', 'blindleft', 'lateralLeftleft', 'lateralRightleft', 'LeftALLleft', 'RightALLleft', 'frontalright', 'blindright', 'lateralLeftright', 'lateralRightright', 'LeftALLright', 'RightALLright']]        
    elif orientation == 'bt':
        final5 = final5[['leftheadx','distanceMoved','TOPCLOSE', 'TOP', 'CENTER', 'BOTTOM', 'BOTTOMCLOSE', 'frontalbottom', 'blindbottom', 'lateralLeftbottom', 'lateralRightbottom', 'LeftALLbottom', 'RightALLbottom', 'frontaltop', 'blindtop', 'lateralLefttop', 'lateralRighttop', 'LeftALLtop', 'RightALLtop']]        
    
    # replace all nan in line
    final5.loc[final5.isnull().any(axis=1), :] = np.nan
    final5["leftheadx"].isna().sum() / len(final5) *100
    
    # rewrite the position columns with NAN
    if orientation == 'lr':
        final5['LEFTCLOSE'] = final4['LEFTCLOSE']
        final5['LEFT'] = final4['LEFT']
        final5['CENTER'] = final4['CENTER']
        final5['RIGHT'] = final4['RIGHT']
        final5['RIGHTCLOSE'] = final4['RIGHTCLOSE']

    
    elif orientation == 'bt':
        final5['TOPCLOSE'] = final4['TOPCLOSE']
        final5['TOP'] = final4['TOP']
        final5['CENTER'] = final4['CENTER']
        final5['BOTTOM'] = final4['BOTTOM']
        final5['BOTTOMCLOSE'] = final4['BOTTOMCLOSE']
    
    final5['distanceMoved'] = final4['distanceMoved']
    final5['index_nan_no_stim'] = final4['index_nan_no_stim']
    
    # re-integrate the frame_number column
    final5.insert(0, column = 'frame_number', value = frame_number)
    
    # Create the seconds column for each trial
    final5['seconds'] = 1
    groupSize = numbframes
    for rowIndex in range(1,final5.shape[0]):
        final5.loc[rowIndex, 'seconds'] = np.floor((final5.frame_number[rowIndex] - final5.frame_number.loc[0])/groupSize)+1
    
    # group by seconds if needed
    nannumber = []
    nannumber_nostim = []
    if numbframes > 1:
        for sec in range(int(final5['seconds'].min()), int(final5['seconds'].max())) :
            nannumber.append((final5.loc[final5['seconds'] == sec]['leftheadx'].isnull().sum())/numbframes)
            nannumber_nostim.append((final5.loc[final5['seconds'] == sec]['index_nan_no_stim'].isnull().sum())/numbframes)
        final5 = final5.groupby('seconds').sum()
    else:
        # if not group by second, then the column "second" shall be renamed "frames" :
        final5.rename(columns={'seconds':'frames'}, inplace=True)

    # round values in final table
    final5 = round(final5, 3)
    
    # add info from text file
    final5 = pd.concat([txtFile, final5], axis=1)
    
    for nbcol in range(0,(final5.columns.get_loc("startingframe")+2)):
        final5[final5.columns[nbcol]] = final5[final5.columns[nbcol]].iloc[0]
      
#    final5.id = final5.id.iloc[0]
#    final5.sex = final5.sex.iloc[0]
#    final5.condition = final5.condition.iloc[0]
#    final5.trial = final5.trial.iloc[0]
#    final5.object = final5.object.iloc[0]
#    final5.position_object = final5.position_object.iloc[0]
#    final5.startingframe = final5.startingframe.iloc[0]
#    final5.endingframe = final5.endingframe.iloc[0]

    # remove all the other non needed columns
    if orientation == 'lr':
        final5 = final5.drop(['leftheadx', 'frame_number','topleftx', 'toplefty', 'toprightx', 'toprighty', 'bottomleftx', 'bottomlefty', 'bottomrightx', 'bottomrighty', 'leftborder', 'rightborder'], axis=1)
    elif orientation == 'bt':
        final5 = final5.drop(['leftheadx','frame_number','topleftx', 'toplefty', 'toprightx', 'toprighty', 'bottomleftx', 'bottomlefty', 'bottomrightx', 'bottomrighty', 'topborder', 'bottomborder'], axis=1)
        
    if (movfix == 0)  & (orientation == 'bt') & (asym == False):
        final5 = final5.drop(['leftstimx', 'leftstimy', 'rightstimx', 'rightstimy'], axis=1)
    elif (movfix == 0)  & (orientation == 'bt') & (asym == True):
        final5 = final5.drop(['lefttopstimx', 'lefttopstimy', 'righttopstimx', 'righttopstimy', 'leftbottomstimx', 'leftbottomstimy', 'rightbottomstimx', 'rightbottomstimy'], axis=1)
    elif (movfix == 0) & (orientation == 'lr') & (asym==False) :
        final5 = final5.drop(['bottomstimx', 'bottomstimy', 'topstimx', 'topstimy'], axis=1)
    elif (movfix == 0) & (orientation == 'lr') & (asym==True) :
        final5 = final5.drop(['bottomleftstimx', 'bottomleftstimy', 'topleftstimx', 'topleftstimy', 'bottomrightstimx', 'bottomrightstimy', 'toprightstimx', 'toprightstimy'], axis=1)
    
    if numbframes > 1:
        final5 = final5.reset_index() 
        final5 = final5.rename(index=str, columns={"index": "seconds"})
    
    #delete the first row and the last one
    final5 = final5.iloc[1:]
    final5.drop(final5.tail(1).index,inplace=True)
    
    # add nan columns
    if numbframes != 1:
        final5['nan'] = nannumber  
        final5['nan_nostim'] = nannumber_nostim  
    
    # write csv
    final5.to_csv(finaloutputpath + '/' + animal_type + '%s.csv' %ID, index = False)


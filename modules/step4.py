# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 21:29:44 2021

@author: Mathilde JOSSERAND
"""


## CREATE ANGLE STIMULUS
import numpy as np

def compute_angle_bt(txtFile, final4, movfix, asym) :    
    
    # check whether stimulus in on the top or bottom if asym=False
    if asym==False and movfix == 0:
        if abs(txtFile.topborder[0] - txtFile.leftstimy[0]) < abs(txtFile.bottomborder[0] - txtFile.leftstimy[0]):             
            side="top"
        else:
            side="bottom"
    elif asym == False and movfix == 1:
        if abs(txtFile.topborder[0] - final4['stimy'][0]) < abs(txtFile.bottomborder[0] - final4['stimy'][0]):             
            side="top"
        else:
            side="bottom"
    
    elif asym == True:
        side="both"
                    
    # create column for point between the eyes : x and y
    final4['betweeneyesX'] = (final4['leftheadx'] + final4['rightheadx'])/2
    final4['betweeneyesY'] = (final4['leftheady'] + final4['rightheady'])/2
    
    # 2 conditions whether there is one or two stimulus
    if asym==False:
        
        # find center stimulus
        if movfix==0:
            center_stim_x = (txtFile.leftstimx + txtFile.rightstimx)/2
            if side == "top":                    
                center_stim_y = txtFile.topborder[0]
            elif side == "bottom":
                center_stim_y = txtFile.bottomborder[0]
            final4['center_stim_x'] = int(center_stim_x)
            final4['center_stim_y'] = int(center_stim_y)
        elif movfix == 1:
            final4['center_stim_x'] = final4['stimx']
            final4['center_stim_y'] = final4['stimy']

        # compute distance between eye and stim, eye and head, and head and stim
        final4['length_eyestim'] = np.sqrt((final4['betweeneyesX'] - final4['center_stim_x'])**2 + (final4['betweeneyesY'] - final4['center_stim_y'])**2)
        final4['length_eyehead'] = np.sqrt((final4['betweeneyesX'] - final4['topheadx'])**2  + (final4['betweeneyesY'] - final4['topheady'])**2)
        final4['length_stimhead'] = np.sqrt((final4['center_stim_x'] - final4['topheadx'])**2 + (final4['center_stim_y'] - final4['topheady'])**2)
        
        # compute the angle and convert it from radians to degrees
        final4['angle'] = np.arccos((final4['length_eyestim']**2 + final4['length_eyehead']**2 - final4['length_stimhead']**2) / (2 * final4['length_eyestim'] * final4['length_eyehead']))
        final4['angle'] = np.degrees(final4['angle'])
        
        final4 = final4.drop(['center_stim_x', 'center_stim_y', 'length_eyestim', 'length_eyehead', 'length_stimhead'], axis=1)
    
    elif asym==True:
        # same steps as before but separately with the top and bottom stimuli
        if movfix==0:
            center_stim_x_bottom = (txtFile.leftbottomstimx + txtFile.rightbottomstimx)/2
            center_stim_y_bottom = txtFile.bottomborder[0]
            center_stim_x_top = (txtFile.lefttopstimx + txtFile.righttopstimx)/2
            center_stim_y_top = txtFile.topborder[0]            
            final4['center_stim_x_bottom'] = int(center_stim_x_bottom)
            final4['center_stim_y_bottom'] = int(center_stim_y_bottom)
            final4['center_stim_x_top'] = int(center_stim_x_top)
            final4['center_stim_y_top'] = int(center_stim_y_top)
        
        elif movfix == 1:
            final4['center_stim_x_top'] = final4['stimtopx']
            final4['center_stim_y_top'] = final4['stimtopy']
            final4['center_stim_x_bottom'] = final4['stimbottomx']
            final4['center_stim_y_bottom'] = final4['stimbottomy']
            
        final4['length_eyehead'] = np.sqrt((final4['betweeneyesX'] - final4['topheadx'])**2  + (final4['betweeneyesY'] - final4['topheady'])**2)
        final4['length_eyestimbottom'] = np.sqrt((final4['betweeneyesX'] - final4['center_stim_x_bottom'])**2 + (final4['betweeneyesY'] - final4['center_stim_y_bottom'])**2)
        final4['length_stimbottomhead'] = np.sqrt((final4['center_stim_x_bottom'] - final4['topheadx'])**2 + (final4['center_stim_y_bottom'] - final4['topheady'])**2)
        final4['length_eyestimtop'] = np.sqrt((final4['betweeneyesX'] - final4['center_stim_x_top'])**2 + (final4['betweeneyesY'] - final4['center_stim_y_top'])**2)
        final4['length_stimtophead'] = np.sqrt((final4['center_stim_x_top'] - final4['topheadx'])**2 + (final4['center_stim_y_top'] - final4['topheady'])**2)
        
        final4['angle_stimbottom'] = np.arccos((final4['length_eyestimbottom']**2 + final4['length_eyehead']**2 - final4['length_stimbottomhead']**2) / (2 * final4['length_eyestimbottom'] * final4['length_eyehead']))
        final4['angle_stimbottom'] = np.degrees(final4['angle_stimbottom'])
        final4['angle_stimtop'] = np.arccos((final4['length_eyestimtop']**2 + final4['length_eyehead']**2 - final4['length_stimtophead']**2) / (2 * final4['length_eyestimtop'] * final4['length_eyehead']))
        final4['angle_stimtop'] = np.degrees(final4['angle_stimtop'])
        
        final4 = final4.drop(['center_stim_x_bottom', 'center_stim_y_bottom', 'center_stim_x_top', 'center_stim_y_top', 'length_eyehead', 'length_eyestimbottom', 'length_eyestimtop', 'length_stimbottomhead', "length_stimtophead"], axis=1)

        return final4
    
def compute_angle_lr(txtFile, final4, movfix, asym) :    
    
    #check whether stimulus in on the left or right if asym=False
    if asym==False and movfix == 0:
        if abs(txtFile.leftborder[0] - txtFile.topstimx[0]) < abs(txtFile.rightborder[0] - txtFile.topstimx[0]):             
            side="left"
        else:
            side="right"

    elif asym == False and movfix == 1:
        if abs(txtFile.leftborder[0] - final4['stimx'][0]) < abs(txtFile.rightborder[0] - final4['stimx'][0]):             
            side="left"
        else:
            side="right"
    elif asym == True:
        side="both"   
        
    # create column for point between the eyes : x and y
    final4['betweeneyesX'] = (final4['leftheadx'] + final4['rightheadx'])/2
    final4['betweeneyesY'] = (final4['leftheady'] + final4['rightheady'])/2
    
    # 2 conditions whether there is one or two stimulus
    if asym==False:
        
        # find center stimulus
        if movfix==0:
            center_stim_y = (txtFile.topstimy + txtFile.bottomstimy)/2
            if side == "left":
                center_stim_x = txtFile.leftborder
            elif side == "right":
                center_stim_x = txtFile.rightborder
            final4['center_stim_x'] = int(center_stim_x)
            final4['center_stim_y'] = int(center_stim_y)
            
        elif movfix == 1:
            final4['center_stim_x'] = final4['stimx']
            final4['center_stim_y'] = final4['stimy']

        # compute distance between eye and stim, eye and head, and head and stim
        final4['length_eyestim'] = np.sqrt((final4['betweeneyesX'] - final4['center_stim_x'])**2 + (final4['betweeneyesY'] - final4['center_stim_y'])**2)
        final4['length_eyehead'] = np.sqrt((final4['betweeneyesX'] - final4['topheadx'])**2  + (final4['betweeneyesY'] - final4['topheady'])**2)
        final4['length_stimhead'] = np.sqrt((final4['center_stim_x'] - final4['topheadx'])**2 + (final4['center_stim_y'] - final4['topheady'])**2)
        
        # compute the angle and convert it from radians to degrees
        final4['angle'] = np.arccos((final4['length_eyestim']**2 + final4['length_eyehead']**2 - final4['length_stimhead']**2) / (2 * final4['length_eyestim'] * final4['length_eyehead']))
        final4['angle'] = np.degrees(final4['angle'])
        
        final4 = final4.drop(['center_stim_x', 'center_stim_y', 'length_eyestim', 'length_eyehead', 'length_stimhead'], axis=1)
    
    elif asym==True:
        
        if movfix==0:
            center_stim_x_left = txtFile.leftborder
            center_stim_y_left = (txtFile.topleftstimy + txtFile.bottomleftstimy)/2
            center_stim_x_right = txtFile.rightborder
            center_stim_y_right = (txtFile.toprightstimy + txtFile.bottomrightstimy)/2
    
            final4['center_stim_x_left'] = int(center_stim_x_left)
            final4['center_stim_y_left'] = int(center_stim_y_left)
            final4['center_stim_x_right'] = int(center_stim_x_right)
            final4['center_stim_y_right'] = int(center_stim_y_right)
        
        elif movfix == 1:
            final4['center_stim_x_left'] = final4['stimleftx']
            final4['center_stim_y_left'] = final4['stimlefty']
            final4['center_stim_x_right'] = final4['stimrightx']
            final4['center_stim_y_right'] = final4['stimrighty']
            
        final4['length_eyehead'] = np.sqrt((final4['betweeneyesX'] - final4['topheadx'])**2  + (final4['betweeneyesY'] - final4['topheady'])**2)
        final4['length_eyestimleft'] = np.sqrt((final4['betweeneyesX'] - final4['center_stim_x_left'])**2 + (final4['betweeneyesY'] - final4['center_stim_y_left'])**2)
        final4['length_stimlefthead'] = np.sqrt((final4['center_stim_x_left'] - final4['topheadx'])**2 + (final4['center_stim_y_left'] - final4['topheady'])**2)
        final4['length_eyestimright'] = np.sqrt((final4['betweeneyesX'] - final4['center_stim_x_right'])**2 + (final4['betweeneyesY'] - final4['center_stim_y_right'])**2)
        final4['length_stimrighthead'] = np.sqrt((final4['center_stim_x_right'] - final4['topheadx'])**2 + (final4['center_stim_y_right'] - final4['topheady'])**2)
        
        final4['angle_stimleft'] = np.arccos((final4['length_eyestimleft']**2 + final4['length_eyehead']**2 - final4['length_stimlefthead']**2) / (2 * final4['length_eyestimleft'] * final4['length_eyehead']))
        final4['angle_stimleft'] = np.degrees(final4['angle_stimleft'])
        final4['angle_stimright'] = np.arccos((final4['length_eyestimright']**2 + final4['length_eyehead']**2 - final4['length_stimrighthead']**2) / (2 * final4['length_eyestimright'] * final4['length_eyehead']))
        final4['angle_stimright'] = np.degrees(final4['angle_stimright'])
        
        final4 = final4.drop(['center_stim_x_left', 'center_stim_y_left', 'center_stim_x_right', 'center_stim_y_right', 'length_eyehead', 'length_eyestimleft', 'length_eyestimright', 'length_stimlefthead', "length_stimrighthead"], axis=1)

        return final4
    
def compute_angle_cen(txtFile, final4, movfix, asym) :    
    
    # create column for point between the eyes : x and y
    final4['betweeneyesX'] = (final4['leftheadx'] + final4['rightheadx'])/2
    final4['betweeneyesY'] = (final4['leftheady'] + final4['rightheady'])/2
    
    # 2 conditions whether there is one or two stimulus
    if asym==False:
        
        # find center stimulus
        if movfix==0:
            # center_stim_x = (txtFile.leftStimX + txtFile.rightStimX)/2
            # center_stim_y = (txtFile.leftStimY + txtFile.rightStimY)/2
            # final4['center_stim_x'] = int(center_stim_x)
            # final4['center_stim_y'] = int(center_stim_y)
            final4['center_stim_x'] = int(txtFile.stimx)
            final4['center_stim_y'] = int(txtFile.stimy)
        elif movfix == 1:
            final4['center_stim_x'] = final4['stimx']
            final4['center_stim_y'] = final4['stimy']

        # compute distance between eye and stim, eye and head, and head and stim
        final4['length_eyestim'] = np.sqrt((final4['betweeneyesX'] - final4['center_stim_x'])**2 + (final4['betweeneyesY'] - final4['center_stim_y'])**2)
        final4['length_eyehead'] = np.sqrt((final4['betweeneyesX'] - final4['topheadx'])**2  + (final4['betweeneyesY'] - final4['topheady'])**2)
        final4['length_stimhead'] = np.sqrt((final4['center_stim_x'] - final4['topheadx'])**2 + (final4['center_stim_y'] - final4['topheady'])**2)
        
        # compute the angle and convert it from radians to degrees
        final4['angle'] = np.arccos((final4['length_eyestim']**2 + final4['length_eyehead']**2 - final4['length_stimhead']**2) / (2 * final4['length_eyestim'] * final4['length_eyehead']))
        final4['angle'] = np.degrees(final4['angle'])
        
        final4 = final4.drop(['center_stim_x', 'center_stim_y', 'length_eyestim', 'length_eyehead', 'length_stimhead'], axis=1)
    
    elif asym==True:
        
        if movfix==0:
            center_stim_x_1 = (txtFile.left1StimX + txtFile.right1StimX)/2
            center_stim_y_1 = (txtFile.left1StimY + txtFile.right1StimY)/2
            center_stim_x_2 = (txtFile.left2StimX + txtFile.right2StimX)/2
            center_stim_y_2 = (txtFile.left2StimY + txtFile.right2StimY)/2
            
            final4['center_stim_x_1'] = int(center_stim_x_1)
            final4['center_stim_y_1'] = int(center_stim_y_1)
            final4['center_stim_x_2'] = int(center_stim_x_2)
            final4['center_stim_y_2'] = int(center_stim_y_2)
        
        elif movfix == 1:
            final4['center_stim_x_1'] = final4['stim1x']
            final4['center_stim_y_1'] = final4['stim1y']
            final4['center_stim_x_2'] = final4['stim2x']
            final4['center_stim_y_2'] = final4['stim2y']
            
        final4['length_eyehead'] = np.sqrt((final4['betweeneyesX'] - final4['topheadx'])**2  + (final4['betweeneyesY'] - final4['topheady'])**2)
        final4['length_eyestim1'] = np.sqrt((final4['betweeneyesX'] - final4['center_stim_x_1'])**2 + (final4['betweeneyesY'] - final4['center_stim_y_1'])**2)
        final4['length_stim1head'] = np.sqrt((final4['center_stim_x_1'] - final4['topheadx'])**2 + (final4['center_stim_y_1'] - final4['topheady'])**2)
        final4['length_eyestim2'] = np.sqrt((final4['betweeneyesX'] - final4['center_stim_x_2'])**2 + (final4['betweeneyesY'] - final4['center_stim_y_2'])**2)
        final4['length_stim2head'] = np.sqrt((final4['center_stim_x_2'] - final4['topheadx'])**2 + (final4['center_stim_y_2'] - final4['topheady'])**2)
        
        final4['angle_stim1'] = np.arccos((final4['length_eyestim1']**2 + final4['length_eyehead']**2 - final4['length_stim1head']**2) / (2 * final4['length_eyestim1'] * final4['length_eyehead']))
        final4['angle_stim1'] = np.degrees(final4['angle_stim1'])
        final4['angle_stim2'] = np.arccos((final4['length_eyestim2']**2 + final4['length_eyehead']**2 - final4['length_stim2head']**2) / (2 * final4['length_eyestim2'] * final4['length_eyehead']))
        final4['angle_stim2'] = np.degrees(final4['angle_stim2'])
        
        final4 = final4.drop(['center_stim_x_1', 'center_stim_y_1', 'center_stim_x_2', 'center_stim_y_2', 'length_eyehead', 'length_eyestim1', 'length_eyestim2', 'length_stim1head', "length_stim2head"], axis=1)

        return final4
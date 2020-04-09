# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 14:09:21 2019

@author: mathilde.josserand
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
from os import listdir
from os.path import isfile, join

# path of the folder containing the videos
pathvideos = 'C:/Users/mathilde.josserand/Desktop/davide/Newvideo_fish/'
## ATTENTION : in this folder, you need to have only the videos you want to merge, and nothing else !
# The videos in this folder can be in any format : avi, mp4 ....

# name and path of the output file
pathoutput = "C:/Users/mathilde.josserand/Desktop/davide/Newvideo_fish/outputvideonew.mp4"
## ATTENTION : it has to be in mp4 format !

# will list all files in the folder
onlyfiles = [f for f in listdir(pathvideos) if isfile(join(pathvideos, f))]

# initialize the ouput video "final_clip" with the first video
path = pathvideos + onlyfiles[0]
final_clip = VideoFileClip(path)

# incrementing videos to the output video
for el in onlyfiles[1:] :
    path = pathvideos + el
    clip = VideoFileClip(path)
    final_clip = concatenate_videoclips([final_clip,clip], method='compose')

# write the ouput file
final_clip.write_videofile(pathoutput, audio = False)


## NOTE : if you get this error message :  "OSError: [WinError 6] The handle is invalid", you just need to restart again Spyder
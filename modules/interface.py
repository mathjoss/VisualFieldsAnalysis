# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 11:26:41 2019

@author: mathilde.josserand
"""

import tkinter
import tkinter.ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from win32api import GetSystemMetrics


dlc= ''
video =''
video2=''
pathexcel=''

# function to center window in the screen
def center(win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
     

def ask_parameters(pre_chick, pre_orient, pre_dlc, pre_video, pre_video2, pre_problem, pre_excel, pre_vidname, pre_mov, pre_asym, pre_area1, pre_area2, pre_area3, pre_area4, pre_area5, pre_front, pre_lat, pre_groupby, pre_anID, pre_thres):

    # --------------------------- 
    # CREATE WINDOWS AND FRAMES
    # -----------------------------
    
    # function to quit the window after selecting OK button
    def quit_program():
        root_window.destroy()

    # open window
    root_window = tkinter.Tk()
    root_window.title("VF analysis: step1.")       
    root_window.configure(bg="white")
    
    root_window.geometry(str(GetSystemMetrics(0))+"x"+str(GetSystemMetrics(1)))

    
    # create frame
    frame=tkinter.ttk.Frame(root_window, width=400, height=200)
    frame['borderwidth'] = 1
    frame['relief'] = 'sunken'
    frame.grid(column=0, row=1, padx=40, pady=10, sticky=(tkinter.W, tkinter.N, tkinter.E))
    
#    # create frame1
#    frame1=tkinter.ttk.Frame(root_window, width=400, height=200)
#    frame1['borderwidth'] = 1
#    frame1['relief'] = 'sunken'
#    frame1.grid(column=0, row=2, padx=40, pady=10, sticky=(tkinter.W, tkinter.N, tkinter.E))
#    
#    # create frame2
#    frame2=tkinter.ttk.Frame(root_window, width=400, height=200)
#    frame2['borderwidth'] = 1
#    frame2['relief'] = 'sunken'
#    frame2.grid(column=0, row=3, padx=40, pady=10, sticky=(tkinter.W, tkinter.N, tkinter.E))
    
    # create frame3
    frame3=tkinter.ttk.Frame(root_window, width=400, height=200)
    frame3['borderwidth'] = 1
    frame3['relief'] = 'sunken'
    frame3.grid(column=1, row=1, padx=40, pady=10, sticky=(tkinter.W, tkinter.N, tkinter.E))
    
#    # create frame4
#    frame4=tkinter.ttk.Frame(root_window, width=400, height=200)
#    frame4['borderwidth'] = 1
#    frame4['relief'] = 'sunken'
#    frame4.grid(column=1, row=2, padx=40, pady=10, sticky=(tkinter.W, tkinter.N, tkinter.E))
#    
#    # create frame5
#    style = tkinter.ttk.Style()
#    style.configure("BW.TLabel", foreground="black", background="white")
#    frame5=tkinter.ttk.Frame(root_window, width=400, height=200, style="BW.TLabel")
#    frame5['borderwidth'] = 0
#    frame5['relief'] = 'flat'
#    frame5.grid(column=1, row=3, padx=40, pady=10, sticky=(tkinter.W, tkinter.N, tkinter.E))
    
    
    # --------------------------- 
    # PRESENTATION 
    # -----------------------------
    
    #label = tkinter.ttk.Label(frame0, text='VISUAL FIELD ANALYSIS PROGRAM', font = 'Helvetica 12 bold', style = "BW.TLabel")
    #label.grid(column=0, row=0, pady=10, padx=2, sticky=(tkinter.N))
    

    
    # --------------------------- 
    # ANIMAL TYPE     
    # -----------------------------
    
    # Create label zone
    first_window_label = tkinter.ttk.Label(frame, text='Write animal type : chick, fish...' )
    first_window_label.grid(column=0, row=0, pady=10, padx=2, sticky=(tkinter.N))
   
    # Create the entry buttong 
    name = tkinter.StringVar(frame, value=pre_chick) # Value saved here
    first_window_entry = tkinter.Entry(frame, width=10, textvariable=name)
    first_window_entry.grid(column=1, row=0, pady=10, padx=2, sticky=(tkinter.N))
    
        
    # --------------------------- 
    # PATH DLC 
    # -----------------------------
    

    # Create zone where arborescence will print
    def browse_button_dlc():
        global dlc
        dlc = filedialog.askdirectory()
        pathlabel.config(text=dlc)
    
    #print(pre_dlc)
    pathlabel = tkinter.Label(frame, text = pre_dlc, font = 'Helvetica 7')
    pathlabel.grid(column=2, row=1, pady=10, padx=10, sticky=(tkinter.N))
   
    # Create label zone
    third_window_label = tkinter.ttk.Label(frame, text='Select path of DLC files folder')
    third_window_label.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    
    # Create Browse button
    third_window_button = tkinter.Button(frame, text="Browse", command=browse_button_dlc)
    third_window_button.grid(column=1, row=1, pady=10, padx=10, sticky=(tkinter.N))    
    #pathlabel.config(text=dlc)

    # --------------------------- 
    # PATH video 
    # -----------------------------
    
    def browse_button_vid():
        global video
        video = filedialog.askdirectory()
        pathlabel2.config(text=video)
       
    def browse_button_vid2():
        global video2
        video2 = filedialog.askdirectory()
        pathlabel3.config(text=video2)
    
    # Create zone where arborescence will print
    pathlabel2 = tkinter.Label(frame, text = pre_video, font = 'Helvetica 7')
    pathlabel2.grid(column=2, row=2, pady=10, padx=10, sticky=(tkinter.N))
    
    # Create label zone
    window4_label = tkinter.ttk.Label(frame, text='Select path for videos files folder')
    window4_label.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))  
    
    # Create Browse button
    window4_button = tkinter.Button(frame, text="Browse", command=browse_button_vid)
    window4_button.grid(column=1, row=2, pady=10, padx=10, sticky=(tkinter.N))
    
    # Create label: if problem  video
    fifteenth_window_label = tkinter.ttk.Label(frame, text='Have you experienced the problem with too heavy videos?')
    fifteenth_window_label.grid(column=0, row=3, pady=10, padx=10, sticky=(tkinter.N))
    
    # Create button: yes or no
    problem = tkinter.BooleanVar(frame, value = pre_problem)
    fifteenth_window_radiobutton1 = tkinter.Radiobutton(frame, text="Yes", padx = 20, variable=problem, value=True)
    fifteenth_window_radiobutton1.grid(column=1, row=3, pady=10, padx=10, sticky=(tkinter.N))
    fifteenth_window_radiobutton2 = tkinter.Radiobutton(frame, text="No", padx = 20,  variable=problem, value=False)
    fifteenth_window_radiobutton2.grid(column=2, row=3, pady=10, padx=10, sticky=(tkinter.N))
    
    # If problem, do same process as before
    pathlabel3 = tkinter.Label(frame, text = pre_video2, font = 'Helvetica 7')
    pathlabel3.grid(column=2, row=4, pady=10, padx=10, sticky=(tkinter.N))    
    fifteenth_window_label = tkinter.ttk.Label(frame, text='If yes, select path with reduced videos. If no, leave it empty.')
    fifteenth_window_label.grid(column=0, row=4, pady=10, padx=10, sticky=(tkinter.N))
    fifteenth_window_button = tkinter.Button(frame, text="Browse", command=browse_button_vid2)
    fifteenth_window_button.grid(column=1, row=4, pady=10, padx=10, sticky=(tkinter.N))
    
    # --------------------------- 
    # NAME video 
    # -----------------------------
    
    # Create labels
    twelvth_window_label = tkinter.ttk.Label(frame, text='Write your video names, and replace the number by %s')
    twelvth_window_label.grid(column=0, row=6, pady=10, padx=10, sticky=(tkinter.N))
    twelvth_window_label = tkinter.ttk.Label(frame, text='Example: if your videos are called fish1.avi, fish2.avi... write: fish%s.avi')
    twelvth_window_label.grid(column=0, row=7, pady=10, padx=10, sticky=(tkinter.N))
    
    # Create the entry button
    namevideos=tkinter.StringVar(root_window, value= pre_vidname) # Value saved here
    twelvth_window_entry = tkinter.Entry(frame, width=15, textvariable=namevideos)
    twelvth_window_entry.grid(column=1, row=7, pady=10, padx=10, sticky=(tkinter.N))
    
    # --------------------------- 
    # PATH excel 
    # -----------------------------
    
    def browse_file():
        global pathexcel
        pathexcel = filedialog.askopenfilename()
        pathlabel4.config(text=pathexcel)
  
     # Create label where arborescence will print
    pathlabel4 = tkinter.Label(frame, text = pre_excel, font = 'Helvetica 7')
    pathlabel4.grid(column=2, row=11, pady=10, padx=10, sticky=(tkinter.N))
    
    # Create label
    window_label = tkinter.ttk.Label(frame, text='Select excel file')
    window_label.grid(column=0, row=11, pady=10, padx=10, sticky=(tkinter.N))
    
    # Create browse button
    window_button = tkinter.Button(frame, text="Browse", command=browse_file)
    window_button.grid(column=1, row=11, pady=10, padx=10, sticky=(tkinter.N))
    
    
    
    # --------------------------- 
    # STIMULI PART
    # -----------------------------    
    
    # label introduction
    #lab = tkinter.ttk.Label(frame1, text='PART 2: Stimulus information.')
    #lab.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))

    # label first question
    second_label = tkinter.ttk.Label(frame, text='On which side of the apparatus are/is the stimuli?')
    second_label.grid(column=0, row=12, pady=10, padx=10, sticky=(tkinter.N))

    # Create the button
    orientation = tkinter.StringVar(frame, value= pre_orient)
    second_radiobutton1 = tkinter.Radiobutton(frame, text="Bottom and/or top", padx = 20, variable=orientation, value='bt')
    second_radiobutton1.grid(column=1, row=12, pady=10, padx=10, sticky=(tkinter.N))
    second_radiobutton2 = tkinter.Radiobutton(frame, text="Left and/or right", padx = 20,  variable=orientation, value='lr')
    second_radiobutton2.grid(column=2, row=12, pady=10, padx=10, sticky=(tkinter.N))
    
    # print image
    imgg = Image.open("pictures/orientation.png")
    imgg = imgg.resize((300, 150), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(imgg)
    panel =  tkinter.ttk.Label(frame, image = img)
    panel.grid(column=0, row=13, pady=10, padx=10, sticky=(tkinter.N))
    
    
    #label second question
    window_label1 = tkinter.ttk.Label(frame, text='Is/are the stimuli fixed or moving ?')
    window_label1.grid(column=0, row=14, pady=10, padx=10, sticky=(tkinter.N))
    mov = tkinter.IntVar(frame, value = pre_mov)
    
    # Button second question
    window_radiobutton1 = tkinter.Radiobutton(frame, text="fixed", padx = 20, variable=mov, value=0)
    window_radiobutton1.grid(column=1, row=14, pady=10, padx=10, sticky=(tkinter.N))
    window_radiobutton2 = tkinter.Radiobutton(frame, text="moving and tracked by deeplabcut", padx = 20,  variable=mov, value=1)
    window_radiobutton2.grid(column=2, row=14, pady=10, padx=10, sticky=(tkinter.N))

    # label third question 
    window_label2 = tkinter.ttk.Label(frame, text='\n Is there 1 stimulus on one side or 2 stimuli on both side ?')
    window_label2.grid(column=0, row=15, pady=10, padx=10, sticky=(tkinter.N))
    
    # Button third question
    asym = tkinter.BooleanVar(frame, value = pre_asym)
    window2_radiobutton1 = tkinter.Radiobutton(frame, text="1 stimulus", padx = 20, variable=asym, value=False)
    window2_radiobutton1.grid(column=1, row=15, pady=10, padx=10, sticky=(tkinter.N))
    window2_radiobutton2 = tkinter.Radiobutton(frame, text="2 stimuli", padx = 20,  variable=asym, value=True)
    window2_radiobutton2.grid(column=2, row=15, pady=10, padx=10, sticky=(tkinter.N))
    
    # --------------------------- 
    # START EXPERIMENT
    # -----------------------------    
    
    # label first question
    eleventh_window_label = tkinter.ttk.Label(frame, text='Do you want to group your frames by seconds?')
    eleventh_window_label.grid(column=0, row=16, pady=10, padx=10, sticky=(tkinter.N))

    # Create the button
    groupbyframe = tkinter.IntVar(frame, value = pre_groupby)
    eleventh_window_radiobutton1 = tkinter.Radiobutton(frame, text="Yes", padx = 20, variable=groupbyframe, value=2)
    eleventh_window_radiobutton1.grid(column=1, row=16, pady=10, padx=10, sticky=(tkinter.N))
    eleventh_window_radiobutton2 = tkinter.Radiobutton(frame, text="No", padx = 20,  variable=groupbyframe, value=1)
    eleventh_window_radiobutton2.grid(column=2, row=16, pady=10, padx=10, sticky=(tkinter.N))

    
    # label second questions
    thirteenth_window_label = tkinter.ttk.Label(frame, text='Write all the ID of the animals you want to analyze, separated by a space')
    thirteenth_window_label.grid(column=0, row=17, pady=10, padx=10, sticky=(tkinter.N))
    thirteenth_window_label = tkinter.ttk.Label(frame, text='Example: to analyze chick 1, 3, 5.1 and 5.2, write : 1 3 5.1 5.2')
    thirteenth_window_label.grid(column=0, row=18, pady=10, padx=10, sticky=(tkinter.N))
   
    # Create the button 
    animal_ID=tkinter.StringVar(frame, value = pre_anID) # Value saved here
    thirteenth_window_entry = tkinter.Entry(frame, width=15, textvariable=animal_ID)
    thirteenth_window_entry.grid(column=1, row=17, pady=10, padx=10, sticky=(tkinter.N))
    
    # label third question
    fourteenth_window_label = tkinter.ttk.Label(frame, text='Write the threshold for detecting outliers (Recommended : 3)')
    fourteenth_window_label.grid(column=0, row=18, pady=10, padx=10, sticky=(tkinter.N))
    
    # button third question
    threshold=tkinter.IntVar(root_window, value= pre_thres) # Value saved here
    fourteenth_window_entry = tkinter.Entry(frame, width=10, textvariable=threshold)
    fourteenth_window_entry.grid(column=1, row=18, pady=10, padx=10, sticky=(tkinter.N))
    
    
    # --------------------------- 
    # AREAS
    # -----------------------------    
    
    
    ninth_window_label1 = tkinter.ttk.Label(frame3, text='write first area length')
    ninth_window_label1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    area1= tkinter.IntVar(root_window, value= pre_area1) # Value saved here
    ninth_window_entry1 = tkinter.Entry(frame3, width=10, textvariable=area1)
    ninth_window_entry1.grid(column=1, row=0, pady=10, padx=10, sticky=(tkinter.N))
    
    ninth_window_label2 = tkinter.ttk.Label(frame3, text='write second area length')
    ninth_window_label2.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    area2=tkinter.IntVar(root_window, value=pre_area2) # Value saved here
    ninth_window_entry2 = tkinter.Entry(frame3, width=10, textvariable=area2)
    ninth_window_entry2.grid(column=1, row=1, pady=10, padx=10, sticky=(tkinter.N))
    
    ninth_window_label3 = tkinter.ttk.Label(frame3, text='write third area length')
    ninth_window_label3.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))
    area3=tkinter.IntVar(root_window, value=pre_area3) # Value saved here
    ninth_window_entry3 = tkinter.Entry(frame3, width=10, textvariable=area3)
    ninth_window_entry3.grid(column=1, row=2, pady=10, padx=10, sticky=(tkinter.N))
    
    ninth_window_label4 = tkinter.ttk.Label(frame3, text='write fourth area length')
    ninth_window_label4.grid(column=0, row=3, pady=10, padx=10, sticky=(tkinter.N))
    area4=tkinter.IntVar(root_window, value=pre_area4) # Value saved here
    ninth_window_entry4 = tkinter.Entry(frame3, width=10, textvariable=area4)
    ninth_window_entry4.grid(column=1, row=3, pady=10, padx=10, sticky=(tkinter.N))
    
    ninth_window_label5 = tkinter.ttk.Label(frame3, text='write fifth area length')
    ninth_window_label5.grid(column=0, row=4, pady=10, padx=10, sticky=(tkinter.N))
    area5=tkinter.IntVar(root_window, value=pre_area5) # Value saved here
    ninth_window_entry5 = tkinter.Entry(frame3, width=10, textvariable=area5)
    ninth_window_entry5.grid(column=1, row=4, pady=10, padx=10, sticky=(tkinter.N))
    
    imgg = Image.open("pictures/areas.png")
    imgg = imgg.resize((309, 200), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(imgg)
    panel2 =  tkinter.ttk.Label(frame3, image = img2)
    panel2.grid(column=0, row=5, pady=10, padx=10, sticky=(tkinter.N))
    
    # --------------------------- 
    # Visual fields
    # -----------------------------    
    
    tenth_window_label1 = tkinter.ttk.Label(frame3, text='Write frontal angle for the animal (for ex, 16 for the fish).')
    tenth_window_label1.grid(column=0, row=6, pady=10, padx=10, sticky=(tkinter.N))
    frontalangle=tkinter.IntVar(frame3, value=pre_front) # Value saved here
    tenth_window_entry1 = tkinter.Entry(frame3, width=10, textvariable=frontalangle)
    tenth_window_entry1.grid(column=1, row=6, pady=10, padx=10, sticky=(tkinter.N))
    
    tenth_window_label2 = tkinter.ttk.Label(frame3, text='write lateral angle for the animal (for ex, 150 for the fish)')
    tenth_window_label2.grid(column=0, row=7, pady=10, padx=10, sticky=(tkinter.N))
    lateralangle=tkinter.IntVar(frame3, value=pre_lat) # Value saved here
    tenth_window_entry2 = tkinter.Entry(frame3, width=10, textvariable=lateralangle)
    tenth_window_entry2.grid(column=1, row=7, pady=10, padx=10, sticky=(tkinter.N))
 
    imgg = Image.open("pictures/angle.png")
    imgg = imgg.resize((176, 250), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(imgg)
    panel3 =  tkinter.ttk.Label(frame3, image = img3)
    panel3.grid(column=0, row=8, pady=10, padx=10, sticky=(tkinter.N))
    
    


    # --------------------------- 
    # Let's start!
    # -----------------------------    
    
    first_window_quit_button = tkinter.Button(frame3, text = "Let's start !", command = quit_program, bg="tomato" , justify='center', height = 2, width = 20, font = ("Helvetica", 12) )
    first_window_quit_button.grid(column = 0, row=9, pady=10, sticky=(tkinter.N))


    # center window
    center(root_window)
    
    # close process
    root_window.mainloop()
    
    # get the value of the variable 
    animal_type = name.get()
    orientation = orientation.get()
    pathdlc = dlc

    pathvideo1 = video
    problem = problem.get()
    pathvideoproblem =  video2
    excelfile = pathexcel

    videoname = namevideos.get()
    movfix = mov.get()
    asym =  asym.get()
    area1 = area1.get()
    area2 = area2.get()
    area3 = area3.get()
    area4 = area4.get()
    area5 = area5.get()
    frontalangle = frontalangle.get()
    lateralangle = lateralangle.get()
    numbframes = groupbyframe.get()
    animal_ID = animal_ID.get()
    thresh = threshold.get()
    
    return animal_type, orientation, pathdlc, pathvideo1, problem, pathvideoproblem, excelfile, videoname, movfix, asym, area1, area2, area3, area4, area5, frontalangle, lateralangle, numbframes, animal_ID, thresh

# same indication for all other tkinter windows
    
def error_excel_file(pathexcelfile):
    def quit_program():
        root_window.destroy()

    
    root_window = tkinter.Tk()
    frame=tkinter.ttk.Frame(root_window, width=800, height=400)
    frame['borderwidth'] = 2
    frame['relief'] = 'sunken'
    
    frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
    

    label1 = tkinter.ttk.Label(frame, text='The program can not find the excel file you mentionned. Are you sure that: ')
    label1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    
    label2 = tkinter.ttk.Label(frame, text=pathexcelfile)
    label2.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    
    label3 = tkinter.ttk.Label(frame, text=' actually exist? And is it an excel file? Rerun the program and change this value. ')
    label3.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))

    second_window_next_button = tkinter.Button(frame, text = "OK", command = quit_program)
    second_window_next_button.grid(column=0, row=3, pady=10, sticky=(tkinter.N))
    center(root_window)
    root_window.mainloop()


def error_video(pathvideo, ID):
    def quit_program():
        root_window.destroy()

    
    root_window = tkinter.Tk()
    frame=tkinter.ttk.Frame(root_window, width=800, height=400)
    frame['borderwidth'] = 2
    frame['relief'] = 'sunken'
    
    frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
    

    label1 = tkinter.ttk.Label(frame, text='The program can not find the videos you mentionned. You said the videos are in this path: ')
    label1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    
    style = tkinter.ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")
    label2 = tkinter.ttk.Label(frame, text=pathvideo, style="BW.TLabel")
    label2.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    
    label3 = tkinter.ttk.Label(frame, text=' And for the first video you want to analyze, %s is being replaced by the value: ')
    label3.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))
    
    label4 = tkinter.ttk.Label(frame, text=ID,  style="BW.TLabel")
    label4.grid(column=0, row=3, pady=10, padx=10, sticky=(tkinter.N))
    
    label5 = tkinter.ttk.Label(frame, text=' Are you sure that this video actually exist? Rerun the program and change either the video path, the video name or the animal ID.')
    label5.grid(column=0, row=4, pady=10, padx=10, sticky=(tkinter.N))

    second_window_next_button = tkinter.Button(frame, text = "OK", command = quit_program)
    second_window_next_button.grid(column=0, row=5, pady=10, sticky=(tkinter.N))
    center(root_window)
    root_window.mainloop()


def error_dlc_file(pathdlc, animal_type, ID):
    def quit_program():
        root_window.destroy()

    
    root_window = tkinter.Tk()
    frame=tkinter.ttk.Frame(root_window, width=800, height=400)
    frame['borderwidth'] = 2
    frame['relief'] = 'sunken'
    
    frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
    

    label1 = tkinter.ttk.Label(frame, text='The program can not find the dlc files you mentionned. You said the files are in this path: ')
    label1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    
    style = tkinter.ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")
    label2 = tkinter.ttk.Label(frame, text=pathdlc, style="BW.TLabel")
    label2.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    
    label3 = tkinter.ttk.Label(frame, text=' You select animal_type as being: ')
    label3.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))
    
    label4 = tkinter.ttk.Label(frame, text=animal_type,  style="BW.TLabel")
    label4.grid(column=0, row=3, pady=10, padx=10, sticky=(tkinter.N))
    
    label5 = tkinter.ttk.Label(frame, text=' And the first animal ID is: ')
    label5.grid(column=0, row=4, pady=10, padx=10, sticky=(tkinter.N))
    
    label6 = tkinter.ttk.Label(frame, text=ID,  style="BW.TLabel")
    label6.grid(column=0, row=5, pady=10, padx=10, sticky=(tkinter.N))
    
    label7 = tkinter.ttk.Label(frame, text=' So the program looked for this file : ')
    label7.grid(column=0, row=6, pady=10, padx=10, sticky=(tkinter.N))
    
    label8 = tkinter.ttk.Label(frame, text=(pathdlc + animal_type + ID + "_dlc.csv"),  style="BW.TLabel")
    label8.grid(column=0, row=7, pady=10, padx=10, sticky=(tkinter.N))
      
    label9 = tkinter.ttk.Label(frame, text=' Does it exist? Rerun the program and change either the dlc file path, the animal_type, the animal ID or the name of your dlc files.')
    label9.grid(column=0, row=8, pady=10, padx=10, sticky=(tkinter.N))

    second_window_next_button = tkinter.Button(frame, text = "OK", command = quit_program)
    second_window_next_button.grid(column=0, row=9, pady=10, sticky=(tkinter.N))
    center(root_window)
    root_window.mainloop()

def check_errors_q1(errors_distance_percent):

    def quit_program():
        root_window.destroy()

    
    root_window = tkinter.Tk()
    frame=tkinter.ttk.Frame(root_window, width=800, height=400)
    frame['borderwidth'] = 2
    frame['relief'] = 'sunken'
    frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
    texttoshow = str(round(errors_distance_percent,2)) + ' % is the percentage of rows that will be counted as NAN by Visual Field analysis program.'
    label1 = tkinter.ttk.Label(frame, text=texttoshow)
    label1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    
    label2 = tkinter.ttk.Label(frame, text=' Do you want to see frames that were considered as outlier by the program?')
    label2.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    
    resp = tkinter.StringVar()
    second_window_radiobutton1 = tkinter.Radiobutton(frame, text="yes", padx = 20, variable=resp, value='y')
    second_window_radiobutton1.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))
    second_window_radiobutton2 = tkinter.Radiobutton(frame, text="no", padx = 20,  variable=resp, value='n')
    second_window_radiobutton2.grid(column=0, row=3, pady=10, padx=10, sticky=(tkinter.N))
    
    label3 = tkinter.ttk.Label(frame, text=' After checking the frames: if you think that the program should have not classified these frames in NaN, abort the program and increase threshold value.')
    label3.grid(column=0, row=4, pady=10, padx=10, sticky=(tkinter.N))

    second_window_next_button = tkinter.Button(frame, text = "OK", command = quit_program)
    second_window_next_button.grid(column=0, row=5, pady=10, sticky=(tkinter.N))
    center(root_window)
    root_window.mainloop()
    resp= resp.get()
    
    return resp

def check_errors_q2(errors_total_percent):

    def quit_program():
        root_window.destroy()
    
    root_window = tkinter.Tk()
    frame2=tkinter.ttk.Frame(root_window, width=800, height=400)
    frame2['borderwidth'] = 2
    frame2['relief'] = 'sunken'
    frame2.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
    texttoshow2= str(round(errors_total_percent,2)) + ' % is the total percentage of rows that will be counted as NAN. It includes:'
    label1 = tkinter.ttk.Label(frame2, text=texttoshow2)
    label1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    
    label2 = tkinter.ttk.Label(frame2, text=" - frames removed by Visual Field Analysis program (which you checked)")
    label2.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    
    label3 = tkinter.ttk.Label(frame2, text=" - frames where likelihood < 0.9 according to Deeplabcut")
    label3.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))
    
    label4 = tkinter.ttk.Label(frame2, text=" - frames where no stimuli is present (if stimuli is moving and tracked by deeplabcut)")
    label4.grid(column=0, row=3, pady=10, padx=10, sticky=(tkinter.N))
    
    label5 = tkinter.ttk.Label(frame2, text=" Do you want to continue? ")
    label5.grid(column=0, row=4, pady=10, padx=10, sticky=(tkinter.N))
    
    resp2 = tkinter.StringVar()
    window_radiobutton1 = tkinter.Radiobutton(frame2, text="yes", padx = 20, variable=resp2, value='y')
    window_radiobutton1.grid(column=0, row=5, pady=10, padx=10, sticky=(tkinter.N))
    window_radiobutton2 = tkinter.Radiobutton(frame2, text="no", padx = 20,  variable=resp2, value='n')
    window_radiobutton2.grid(column=0, row=6, pady=10, padx=10, sticky=(tkinter.N))
    window_next_button = tkinter.Button(frame2, text = "OK", command = quit_program)
    window_next_button.grid(column=0, row=7, pady=10, sticky=(tkinter.N))
    center(root_window)
    root_window.mainloop()
    resp2= resp2.get()
    
    return resp2

def visualize_fields_q1():

    def quit_program():
        root_window.destroy()
        
    root_window = tkinter.Tk()
    frame=tkinter.ttk.Frame(root_window, width=800, height=400)
    frame['borderwidth'] = 2
    frame['relief'] = 'sunken'
    frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
    texttoshow = 'Do you want to randomly check pictures to see if the visual fields are correct?'
    label1 = tkinter.ttk.Label(frame, text=texttoshow)
    label1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    
    response = tkinter.StringVar()
    second_window_radiobutton1 = tkinter.Radiobutton(frame, text="Yes", padx = 20, variable=response, value='y')
    second_window_radiobutton1.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    second_window_radiobutton2 = tkinter.Radiobutton(frame, text="No", padx = 20,  variable=response, value='n')
    second_window_radiobutton2.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))
    second_window_next_button = tkinter.Button(frame, text = "OK", command = quit_program)
    second_window_next_button.grid(column=0, row=3, pady=10, sticky=(tkinter.N))
    center(root_window)
    root_window.mainloop()
    response= response.get()
    
    return response

def visualize_fields_q2():

    def quit_program():
        root_window.destroy()
        
    root_window = tkinter.Tk()
    frame3=tkinter.ttk.Frame(root_window, width=800, height=400)
    frame3['borderwidth'] = 2
    frame3['relief'] = 'sunken'
    frame3.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
    texttoshow = 'How many frames do you want to visualize?'
    label2 = tkinter.ttk.Label(frame3, text=texttoshow)
    label2.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))

    numbpic = tkinter.IntVar()
    entry = tkinter.Entry(frame3, width=10, textvariable=numbpic)
    entry.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    button = tkinter.Button(frame3, text = "OK", command = quit_program)
    button.grid(column=0, row=2, pady=10, sticky=(tkinter.N))
    center(root_window)
    root_window.mainloop()
    numbpic= numbpic.get()
    return numbpic
        
def visualize_fields_q3():

    def quit_program():
        root_window.destroy()
        
    root_window = tkinter.Tk()
    frame2=tkinter.ttk.Frame(root_window, width=800, height=400)
    frame2['borderwidth'] = 2
    frame2['relief'] = 'sunken'
    frame2.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
    texttoshow2='Do you want to continue and analyze the next animal ?'
    label1 = tkinter.ttk.Label(frame2, text=texttoshow2)
    label1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    
    resp = tkinter.StringVar()
    window_radiobutton1 = tkinter.Radiobutton(frame2, text="Yes", padx = 20, variable=resp, value='y')
    window_radiobutton1.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    window_radiobutton2 = tkinter.Radiobutton(frame2, text="No", padx = 20,  variable=resp, value='n')
    window_radiobutton2.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))
    window_next_button = tkinter.Button(frame2, text = "OK", command = quit_program)
    window_next_button.grid(column=0, row=3, pady=10, sticky=(tkinter.N))
    center(root_window)
    root_window.mainloop()
    resp= resp.get()
    
    return resp

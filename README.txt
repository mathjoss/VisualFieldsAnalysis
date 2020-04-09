This program uses outputs from DeepLabCut (http://www.mousemotorlab.org/deeplabcut and https://github.com/AlexEMG/DeepLabCut) to compute visual fields used by an animal toward a stimulus.

From the body positions 'LeftHead', 'RightHead' and 'TopHead' obtained by DeepLabCut, it computes the visual fields (frontal view, blind view, lateral right view or lateral left view). It also indicates the position of the animal in the apparatus.

If you want more info and explanation, please read the article with the full protocol.

Before using this program:
- organize your files: gather the videofiles in a folder, the DLC output files in an other folder. 
- complete a excel document with starting and ending time of the experiment, one sheet per animal (see example in example/example.xlsx)
- write coherent name for your files: only the number of the animal must change between the files


*------------------*

REQUIREMENTS
Python (only >3 tested)  with pandas, matplotlib, cv2, numpy, tkinter, random, math functions


*------------------*

INSTALLATION
1. Download all functions and files available on github from https://github.com/mathjoss/VF_analysis.git

2. Run main_coordinator.py 


*-------------------*

INSTRUCTIONS FOR OPERATION

1. Read more info from http://www.mousemotorlab.org/deeplabcut if you want to understand more about DeepLabCut and the output generated.

2. Write inside an excel file (same format as the excel file animals_excel_sheet.xlsx) the columns information you need: Start (min) and Stop(min) required

3. Add videos to a folder with same name format : for example, chick11.1, chick11.2, chick12.1 ... (avoid changing names like chick1, new_chick2)

4. Add DeepLabCut files to a folder and rename them to AnimalNUMBER_dlc (for example: chick11.1_dlc, chick11.2_dlc ...)

5. Create two empty folders : files and results

6. Run main_coordinator


*--------------------*

FILES/FOLDER EXPLANATION

1. main_coordinator : main file coordinating all functions

2. merge_video.py: additional python file allowing you to merge multiple videos in one single video (can be used in order to select representative set of frames from multiple videos in DeepLabCut)

3. modules: python files necessary for the coding.
- interface : open tkinter window to interact with the user
- step1 : find position of the arena corners and stimulus (if needed)
- step2 : find errors in DLC tracking and visualize errors
- step3 : find location of the animal in different areas
- step4_bt_fixstim : find visual fields used for an apparatus orientation in Bottom/Top position and for a large fixed stimulus indicated in step1
- step4_bt_movstim : find visual fields used for an apparatus orientation in Bottom/Top position and for a moving stimulus tracked by DLC
- step4_lr_fixstim : find visual fields used for an apparatus orientation in Left/Right position and for a large fixed stimulus indicated in step1
- step4_lr_movstim : find visual fields used for an apparatus orientation in Bottom/Top position and for a moving stimulus tracked by DLC

4. pictures: pictures that will be printed out in the interface

5. Example: example folder, which contain:
- a folder videos, with video of chick 1 and 2
- results_dlc, with csv output file for chick 1 and 2.
Inside this folder, two other folders are created from Visual Fields Analysis program: one folder with the results, and one folder with additionnal data on videos.
- manual comparaison folder just contains example of Visual Fields Analysis program output
- example.xslx is the excel file containing the information for chick 1 and 2, in two different sheets. You should complete that excel file while running the program. Only ID, start (min), stop (min) are essential to complete. The others columns are not necessary.



** Excel document animals_excel_sheet.xlsx : example of how data should be written
** orientation.png : image used for user interface


CONTACT mathilde.josserand@gmail.com or bastien.lemaire@unitn.it with any questions

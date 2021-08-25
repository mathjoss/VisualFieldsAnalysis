This program uses outputs from DeepLabCut (http://www.mousemotorlab.org/deeplabcut and https://github.com/AlexEMG/DeepLabCut) to compute visual fields used by an animal toward a stimulus.

From the body positions 'LeftHead', 'RightHead' and 'TopHead' obtained by DeepLabCut, it computes the visual fields (frontal view, blind view, lateral right view or lateral left view). It also indicates the position of the animal in the apparatus, how much the animal moved inside the apparatus, and the angle of the head toward the stimulus.

If you want more info and explanation, please read the article with the full protocol.

Before using this program:
- organize your files: gather the videofiles in a folder, the DLC output files in an other folder. 
- complete a excel document with starting and ending time of the experiment, one sheet per animal (see example in example/example.xlsx)
- write coherent name for your files: only the animal ID must change between the files


*------------------*

REQUIREMENTS
Python (only >3 tested)  with pandas, matplotlib, opencv, numpy, xlrd
To help you with these packages, a yaml file is available. See part "Installation" for more information.


*------------------*

INSTALLATION

For the skilled computer scientist:
1. Download all functions and files available on github from https://github.com/mathjoss/VisualFieldsAnalysis.git
2. Download the packages mentionned in the Requirements above
3. Run main_coordinator.py 

For someone not familiar with programming but WITH ANACONDA INSTALLED, follow these steps:
1. Download all functions and files available on github from https://github.com/mathjoss/VisualFieldsAnalysis.git
2. Copy paste the file "VisualFieldAnalysis.yaml" inside your "home" folder. This folder is usually the one when you go one step backward in the tree structure from your Documents. In other terms, go in your disk "C:/", select your user name if there are several user, and then paste the file near the folders "Documents", "Downloads",...
3. Open the terminal (command prompt). How to open it depends on your operating system. You will easily find it on Google.
4. write "conda env create -f VFA.yaml" and press enter. It will take several minutes.
5. When it is done, write "conda activate VisualFieldAnalysis" and press enter.
6. Then write "spyder". It will open a new console.
7. Open the file "main_coordinator" in spyder, and then press the button "Run" which look like a green "play" arrow.
8. Normally, a new window opens! VisualFieldAnalysis is installed. Then, refer to the protocol for how to use it.

For someone not familiar with programming but without anaconda:
1- Download Anaconda. It is really cool and free, and easy to use. To download it go to: https://www.anaconda.com/products/individual and download it according to your operating system.
2- Then, follow the previous steps :)


*-------------------*

INSTRUCTIONS FOR OPERATION

1. Read more info from http://www.mousemotorlab.org/deeplabcut if you want to understand more about DeepLabCut and the output generated.

2. Write inside an excel file (same format as the excel file example.xlsx in Example folder) the columns information you need: ID, Start (min) and Stop(min) required (other columns optional)

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

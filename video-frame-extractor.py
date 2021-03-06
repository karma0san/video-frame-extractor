import os
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import subprocess

root = Tk()
root.title('Image extractor')

# variables for section 1: Loading files section
filenamespath_list = [] # List to store filenamespath

# variables for section 2: Extraction options
images_options = ['png', 'jpg'] # options for output images
digit_options = ['1', '2', '3'] # options for digit for the filenames

fps = IntVar() # Integer variable for frames per seconds
fps.set(5) # Default integer variable for frames per seconds

image_output_selection = StringVar() # string variable for image output selection
image_output_selection.set(images_options[0]) # default selection for image output option

digit_number_selection = IntVar() # integer variable for digit number selection
digit_number_selection.set(digit_options[1]) # default selection for digit number

## functions for section 1: Loading files section
def loadFiles():
    global filenamespath_list

    clear() # clear the texts first if there is any

    # Load the video files
    root.filenames =  filedialog.askopenfilenames(title = "Select file", filetypes = (("mp4","*.mp4"),("avi","*.avi"),("mov","*.mov"))) 

    filenamespath_list = list(root.filenames) # List to store filepaths

    filenames_list = [] # List to store filenames

    # Makes each line for the paths
    filenamespath = '\n'.join([i for i in filenamespath_list])
    
    # update file list label
    file_list.insert(END, filenamespath) # insert texts on text box
    file_list.configure(state = 'disabled') # create text read only
    file_list.grid(row = 0, column = 1)


def clear():
    file_list.configure(state = 'normal') # set back the state of text box to normal
    file_list.delete("1.0", "end") # clear the textbox
    filenamespath_list = [] # List to store filepaths
    filenames_list = [] # List to store filenames


## functions for section 3: Start the extraction
def execution(fps, image_output_selection, digit_number_selection, filenamespath_list):
    path = os.getcwd() # Get current working directory
    ffmpeg_plugin_path = path + "\\bin\\ffmpeg.exe" # path to plugin

    # Filename with path (without extensions)
    for filenamespath in filenamespath_list:
        filename = Path(filenamespath).stem # Extract filename from file path
        filename_with_path = filenamespath[0:-4] # Extract file path without extensions
        if os.path.isdir(filename_with_path) == False:
            os.mkdir(filename_with_path)
        subprocess.run([ffmpeg_plugin_path, '-i', filenamespath, '-r', str(fps), filename_with_path + '/' + filename + '_%0' + str(digit_number_selection) + 'd.' + image_output_selection]) # command to extract the images

def start():
    if image_output_selection.get() == 'jpg':
        image_output_response = messagebox.askyesno('Warning', 'You have chosen jpg as an output, the output images quality might be depreciated. Would you like to proceed?')
        if image_output_response == 1:
            final_response = messagebox.askyesno('Is this selection correct?',
                            'Number of frames = ' + str(fps.get()) + '\n'
                            'Output format = ' + image_output_selection.get() + '\n'
                            'Number of digits to suffix = ' + str(digit_number_selection.get()) + '\n')
            if final_response == 1:
                execution(fps.get(), image_output_selection.get(), digit_number_selection.get(), filenamespath_list)
    else:
        final_response = messagebox.askyesno('Is this selection correct?',
                            'Number of frames = ' + str(fps.get()) + '\n'
                            'Output format = ' + image_output_selection.get() + '\n'
                            'Number of digits to suffix = ' + str(digit_number_selection.get()) + '\n')
        if final_response == 1:
            execution(fps.get(), image_output_selection.get(), digit_number_selection.get(), filenamespath_list)


##-------------------------------------------------------------------------------
# Section 1: Loading files section
loading_frame = LabelFrame(root, text = 'load your files')
loading_frame.pack(padx = 5, pady = 5)

# Textbox to show the selected videos
file_list = Text(loading_frame, padx = 15, pady = 15, bd = 1, width = 50, height = 8)
file_list.grid(row = 0, column = 1)

# Adding scroll bar to the text box
scroll_bar = Scrollbar(loading_frame, orient = 'vertical', command = file_list.yview)
file_list.config(yscrollcommand = scroll_bar.set)
file_list.grid(row = 0, column = 1, sticky = NSEW)

# button for loading videos
button_load = Button(loading_frame, text = 'Load', padx = 40, pady = 20, command = loadFiles)
button_load.grid(row = 1, column = 0, padx = 5, pady = 5)

# button for clearing the loaded files
button_clear = Button(loading_frame, text = 'Clear', padx = 40, pady = 20, command = clear)
button_clear.grid(row = 1, column = 2, padx = 5, pady = 5)


##-----------------------------------------------------------
# Section 2: Extraction options
options_frame = LabelFrame(root, text = 'select your options', padx = 80, pady = 20)
options_frame.pack(padx = 5, pady = 5)

# Number of frames per second
Label(options_frame, text = 'Frames per second', padx = 40, pady = 30, bd = 1).grid(row = 0, column = 0)
fps_number = Entry(options_frame, text = "Enter desired fps", textvariable = fps, width = 5, justify = 'center')
fps_number.grid(row = 1, column = 0)

# Select desired output format
Label(options_frame, text = 'Output Image', padx = 40, pady = 30, bd = 1).grid(row = 0, column = 1)
image_output = OptionMenu(options_frame, image_output_selection, *images_options)
image_output.grid(row = 1, column = 1)

# Numbers of digit after the exported frame name
Label(options_frame, text = 'Number of digits to suffix', padx = 40, pady = 30, bd = 1).grid(row = 0, column = 2)
digit_number = OptionMenu(options_frame, digit_number_selection, *digit_options)
digit_number.grid(row = 1, column = 2)


##-----------------------------------------------------------------------------------------
# Section 3: Start the extraction
execution_frame = LabelFrame(root, text = 'Start the extraction', padx = 50, pady = 20)
execution_frame.pack(padx = 5, pady = 5)

button_start = Button(execution_frame, text = 'Start', padx = 40, pady = 20, command = start)
button_start.grid(row = 0, column = 0)


root.mainloop()
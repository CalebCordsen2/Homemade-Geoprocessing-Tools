"""
Author: Caleb Cordsen
Date 3/2/2023

Description: This is the main loop to run my custom geoprocessing tools.
"""
import sys
import buffer
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import ImageTk

## Followed tkinter tutorial from this page https://www.youtube.com/watch?v=5qOnzF7RsNA&t=1227s
def clean_page(frame):
    '''
    Parameters
    ----------
    frame : Frame
        This is a tkinter frame that this function takes in.

    Returns
    -------
    None.
    
    Description:
        This function looks through the widgets currenlty existing on a frame and gets rid of them
        in order to efficiently clean up the page and switch to new ones.
    '''
    # Loop through the widgets in the inputted frame and destroy them
    for widget in frame.winfo_children():
        widget.destroy()

def load_main():
    '''
    Returns
    -------
    None.
    
    Description:
        This function loads the home page of the GUI for Caleb's Geoprocessing Tools. It takes no 
        inputs and returns nothing.
    '''
    # Clean up both the buffer and clip 
    clean_page(bufferPage)
    clean_page(clipPage)
    clean_page(batchBufferPage)
    # Raise the mainPage frame
    mainPage.tkraise()
    mainPage.pack_propagate(False)
    # Display the logo and pack it in
    logo = ImageTk.PhotoImage(file="Images/CalebLogo.png")
    logo_widg = Label(mainPage,image=logo,bg=bgcl)
    logo_widg.image = logo
    logo_widg.pack()
    # Display text that says to select an option
    Label(mainPage,
          text="Please Select an Option Below",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",20)
          ).pack()
    # Load a button that takes you to the clip tool
    Button(mainPage,
           text="Clip Tool",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:clip_page()
           ).pack(pady=20)
    # Load a button that takes you to the singular buffer page
    Button(mainPage,
           text="Singular Buffer Tool",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:buffer_page()
           ).pack()
    # Load a button that takes you to the batch buffer page
    Button(mainPage,
           text="Batch Buffer Tool",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:batchBuffer_page()
           ).pack(pady=20)
    
def buffer_page():
    '''
    Returns
    -------
    None.
    
    Description:
        This function loads the singuler buffer page of the GUI for Caleb's Geoprocessing Tools. It takes no 
        inputs and returns nothing.
    '''
    # Clean the mainPage and raise the bufferPage frame
    clean_page(mainPage)
    bufferPage.tkraise()
    bufferPage.pack_propagate(False)
    
    # Pack in a label that displays a welcome message
    Label(bufferPage,
          text="Welcome to the Buffer Tool!",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",20)
          ).pack()
    # Pack in a label that says to fill out the information below
    Label(bufferPage,
          text="Please fill out the information below!",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",17)
          ).pack(pady=20)
    
    # Create a variable within the buffer page function outDIR that stores
    # the output directory for buffer to be saved to. Set to None to start
    outDIR = None
    def browse_outputDIR(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function prompts the user to select a file directory. It stores the path in outDIR and updates
            a label on the buffer page to show that selected file directory.
        '''
        # bring in outDIR variable
        nonlocal outDIR
        # Get the file directory
        file_name = askdirectory()
        # Set the label text to the selected file and set outDIR to file_name
        label1.config(text="Selected output directory: "+file_name)
        outDIR = file_name
    # Pack a button that prompts the user to select the output directory. On click it calls browse_outputDIR
    Button(bufferPage,
           text="Please Select a Output Directory",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:browse_outputDIR(outLbl)
           ).pack()
    # Pack a label that starts blank but will update based on outputDIR input
    outLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    outLbl.pack()
    
    # Create a variable within the buffer page function inputFile that stores
    # the input shape file. Set to None to start
    inputFile = None
    def browse_inputShape(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function prompts the user to select a input file. It stores the path in inputFile and updates
            a label on the buffer page to show that selected file.
        '''
        # Bring in inputFile variable
        nonlocal inputFile
        # Get the file
        file_name = askopenfilename(filetypes=[("Shape Files","*.shp")])
        # Set the label text to selected file and set inputFile to that path
        label1.config(text="Selected input file: "+file_name)
        inputFile = file_name
    # Pack in a button that will prompt user to input shape by calling above function
    Button(bufferPage,
           text="Please Select a Input Shape File",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:browse_inputShape(inputLbl)
           ).pack()
    # Create a blank label that will update on the above button press
    inputLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    inputLbl.pack()
    
    # Create a text field for the user to enter a output file name
    outputFileNameEntry = Entry(bufferPage,width=50)
    outputFileNameEntry.insert(END,"Please enter an output file name here. Must end in .shp")
    outputFileNameEntry.pack()
    # Make a variable outFileName that will store the outFileName.
    outFileName = None
    def submitOutFile(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function will submit a file name from a text field to a label and update outFileName
        '''
        # Bring in the outFileName variable
        nonlocal outFileName
        # Only allow .shp file extensions. Update the label text to error if not
        if(outputFileNameEntry.get()[-4:]!='.shp'):
            label1.config(text='Sorry but you need to submit a .shp file name!')
        else:
            # Set the outFileName and label text to the user input
            outFileName = outputFileNameEntry.get()
            label1.config(text="Inputted file name: "+outputFileNameEntry.get())
    # Load a submit button that calls above function on click
    Button(bufferPage,
           text="Submit file name",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:submitOutFile(outFileLbl)
           ).pack()  
    # Pack a blank label that will update on above button push
    outFileLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    outFileLbl.pack()
    
    # Create an entry field for users to enter the buffer size
    bufferSizeEntry = Entry(bufferPage,width=50)
    bufferSizeEntry.insert(END,"Please Enter a Buffer Size Here!")
    bufferSizeEntry.pack()
    # Create a variable to store the bufferSize and start at None
    actualBufferSize = None
    def submitSize(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function will submit a buffer size from a text field to a label and update actualBufferSize
        '''
        # Bring in actualBufferSize variable
        nonlocal actualBufferSize
        try:
            # Try converting the text inputted to a float. Put it in actualBufferSize and update label text
            strBuffSize = bufferSizeEntry.get()
            actualBufferSize = float(strBuffSize)
            label1.config(text="Inputted buffer size: "+bufferSizeEntry.get())
        except:
            # If the conversion to float failed, update the label to a error message
            label1.config(text="That is not a valid number! Try again!")
    # Pack a submit button that calls the above function on click
    Button(bufferPage,
           text="Submit buffer size.",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:submitSize(buffSizeLbl)
           ).pack()  
    # Pack a blank label that will update on the above button push
    buffSizeLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    buffSizeLbl.pack()
    
    # Set up a drop down menu for units with various unit options
    currentUnitClick = StringVar()
    currentUnitClick.set("")
    bufferUnitEntry = OptionMenu(bufferPage,currentUnitClick,"meters","kilometers","decimeters","centimeters","millimeters","miles","yards","feet","inches","nautical miles")
    bufferUnitEntry.pack()
    # Set up a None bufferUnit variable
    bufferUnit = None
    def submitUnit(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function submits the current dropdown menu selection for units.
        '''
        # Bring in the bufferUnit variable
        nonlocal bufferUnit
        # Check if the currentUnit selected has an actual unit selected. If it does proceed
        if(currentUnitClick.get()!=""):
            # Get the buffer unit and store in bufferUnit and then update label
            bufferUnit = currentUnitClick.get()
            label1.config(text="Inputted buffer unit: "+bufferUnit)
        else:
            # If no unit was selected update label to say so
            label1.config(text="You have not selected a unit type!")
    # Pack a button that will submit the unit using function above
    Button(bufferPage,
           text="Submit buffer unit.",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:submitUnit(buffUnitLbl)
           ).pack()  
    # Pack a label that will update on the above button push
    buffUnitLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    buffUnitLbl.pack()
    
    def runBuffer(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function runs the buffer based on inputs and updates label based on outcome of buffer.
        '''
        # Check to make sure that there is inputs for all required fields. If not, update the label saying to fill out info
        if(actualBufferSize == None or outFileName == None or inputFile == None or outDIR == None or outDIR=='' or inputFile=='' or bufferUnit==None):
            label1.config(text="Please provide valid information to the forms above!")
        else:
            # If all information is there set the label to the return message from running the buffer on inputs
            label1.config(text=buffer.bufferMain(outDIR,inputFile,outFileName,actualBufferSize,bufferUnit))
    # Pack a button that runs the buffer using above function
    Button(bufferPage,
           text="Run Buffer",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:runBuffer(runBuffLbl)
           ).pack()
    # Pack a blank label that updates based on above button
    runBuffLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    runBuffLbl.pack()
    # Pack a button that will take users back to main menu by calling load_main()
    Button(bufferPage,
           text="Back to Main Menu",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:load_main()
           ).pack()

def batchBuffer_page():
    '''
    Returns
    -------
    None.
    
    Description:
        This function loads the batch buffer page of the GUI for Caleb's Geoprocessing Tools. It takes no 
        inputs and returns nothing.
    '''
    # Clean the mainPage and raise the bufferPage frame
    clean_page(mainPage)
    batchBufferPage.tkraise()
    batchBufferPage.pack_propagate(False)
    
    # Pack in a label that displays a welcome message
    Label(batchBufferPage,
          text="Welcome to the Batch Buffer Tool!",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",20)
          ).pack()
    # Pack in a label that says to fill out the information below
    Label(batchBufferPage,
          text="Please fill out the information below!",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",17)
          ).pack(pady=20)
    
    # Create a variable within the buffer page function outDIR that stores
    # the output directory for buffer to be saved to. Set to None to start
    outDIRs = []
    def browse_outputDIR(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function prompts the user to select a file directory. It stores the path in outDIRs and updates
            a label on the buffer page to show the current list size
        '''
        # bring in outDIRs variable
        nonlocal outDIRs
        # Get the file directory
        file_name = askdirectory()
        # Set the label text to the selected file and append file_name to outDIRs
        outDIRs.append(file_name)
        label1.config(text="Current directory list size: "+str(len(outDIRs)))
    # Pack a button that prompts the user to select the output directory. On click it calls browse_outputDIR
    Button(batchBufferPage,
           text="Add a Output Directory For Processing",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:browse_outputDIR(outLbl)
           ).pack()
    # Pack a label that starts blank but will update based on outputDIR input
    outLbl = Label(batchBufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    outLbl.pack()
    
    # Create a variable within the buffer page function inputFile that stores
    # the input shape file. Set to None to start
    inputFiles = []
    def browse_inputShape(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function prompts the user to select a input file. It stores the path in inputFiles and updates
            a label on the buffer page to show the current list size
        '''
        # Bring in inputFiles variable
        nonlocal inputFiles
        # Get the file
        file_name = askopenfilename(filetypes=[("Shape Files","*.shp")])
        # Append to inputFiles the file_name
        inputFiles.append(file_name)
        # Set the label text to selected file and set inputFile to that path
        label1.config(text="Current input file list size: "+str(len(inputFiles)))
    # Pack in a button that will prompt user to input shape by calling above function
    Button(batchBufferPage,
           text="Add a Input Shape File For Processing",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:browse_inputShape(inputLbl)
           ).pack()
    # Create a blank label that will update on the above button press
    inputLbl = Label(batchBufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    inputLbl.pack()
    
    # Create a text field for the user to enter a output file name
    outputFileNameEntry = Entry(batchBufferPage,width=50)
    outputFileNameEntry.insert(END,"Please enter an output file name here. Must end in .shp")
    outputFileNameEntry.pack()
    # Make a variable outFileName that will store the outFileName.
    outFileNames = []
    def submitOutFile(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function will append a filename to outFileNames and display current list size
        '''
        # Bring in the outFileNames variable
        nonlocal outFileNames
        # Only allow .shp file extensions. Update the label text to error if not
        if(outputFileNameEntry.get()[-4:]!='.shp'):
            label1.config(text='Sorry but you need to submit a .shp file name!')
        else:
            # Append user input to outFileNames and update label to show list size
            outFileNames.append(outputFileNameEntry.get())
            label1.config(text="Current output file name list size: "+str(len(outFileNames)))
    # Load a submit button that calls above function on click
    Button(batchBufferPage,
           text="Add a File Name For Processing",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:submitOutFile(outFileLbl)
           ).pack()  
    # Pack a blank label that will update on above button push
    outFileLbl = Label(batchBufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    outFileLbl.pack()
    
    # Create an entry field for users to enter the buffer size
    bufferSizeEntry = Entry(batchBufferPage,width=50)
    bufferSizeEntry.insert(END,"Please Enter a Buffer Size Here!")
    bufferSizeEntry.pack()
    # Create a variable to store the bufferSize and start at None
    actualBufferSizes = []
    def submitSize(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function will submit a buffer size from a text field, update a label and append to actualBufferSizes
        '''
        # Bring in actualBufferSizes variable
        nonlocal actualBufferSizes
        try:
            # Try converting the text inputted to a float. Append to actualBufferSizes and update label text to size of list
            strBuffSize = bufferSizeEntry.get()
            actualBufferSize = float(strBuffSize)
            actualBufferSizes.append(actualBufferSize)
            label1.config(text="Current buffer size list size: "+str(len(actualBufferSizes)))
        except:
            # If the conversion to float failed, update the label to a error message
            label1.config(text="That is not a valid number! Try again!")
    # Pack a submit button that calls the above function on click
    Button(batchBufferPage,
           text="Add a Buffer Size For Processing",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:submitSize(buffSizeLbl)
           ).pack()  
    # Pack a blank label that will update on the above button push
    buffSizeLbl = Label(batchBufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    buffSizeLbl.pack()
    
    # Set up a drop down menu for units with various unit options
    currentUnitClick = StringVar()
    currentUnitClick.set("")
    bufferUnitEntry = OptionMenu(batchBufferPage,currentUnitClick,"meters","kilometers","decimeters","centimeters","millimeters","miles","yards","feet","inches","nautical miles")
    bufferUnitEntry.pack()
    # Set up a None bufferUnit variable
    bufferUnits = []
    def submitUnit(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function submits the current dropdown menu selection for units, appending to bufferUnits and updating a label.
        '''
        # Bring in the bufferUnit variable
        nonlocal bufferUnits
        # Check if the currentUnit selected has an actual unit selected. If it does proceed
        if(currentUnitClick.get()!=""):
            # Get the buffer unit and store in bufferUnit and then update label
            bufferUnit = currentUnitClick.get()
            bufferUnits.append(bufferUnit)
            label1.config(text="Current unit list size: "+str(len(bufferUnits)))
        else:
            # If no unit was selected update label to say so
            label1.config(text="You have not selected a unit type!")
    # Pack a button that will submit the unit using function above
    Button(batchBufferPage,
           text="Add a Buffer Unit For Processing",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:submitUnit(buffUnitLbl)
           ).pack()  
    # Pack a label that will update on the above button push
    buffUnitLbl = Label(batchBufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    buffUnitLbl.pack()
    
    def runBuffer(label1):
        '''
        Parameters
        ----------
        label1 : A tkinter label
            A tkinter label to change

        Returns
        -------
        None.
        
        Description:
            This function runs a batch buffer based on inputs and updates label based on outcome of batch buffer.
        '''
        # Check to make sure that there is inputs for all required fields. If not, update the label saying to fill out info
        if(len(outDIRs)!=len(inputFiles) or len(inputFiles)!=len(outFileNames) or len(outFileNames)!=len(actualBufferSizes) or len(actualBufferSizes)!=len(bufferUnits)):
            label1.config(text="All input lists must be the same size!")
        elif(len(outDIRs)==0 or len(inputFiles)==0 or len(outFileNames)==0 or len(actualBufferSizes)==0 or len(bufferUnits)==0):
            label1.config(text="All lists must be of at least size 1!")
        else:
            # If all information is there set the label to the return message from running the buffer on inputs
            label1.config(text=buffer.batchBuffer(outDIRs,inputFiles,outFileNames,actualBufferSizes,bufferUnits))
    # Pack a button that runs the buffer using above function
    Button(batchBufferPage,
           text="Run Batch Buffer",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:runBuffer(runBuffLbl)
           ).pack()
    # Pack a blank label that updates based on above button
    runBuffLbl = Label(batchBufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    runBuffLbl.pack()
    # Pack a button that will take users back to main menu by calling load_main()
    Button(batchBufferPage,
           text="Back to Main Menu",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:load_main()
           ).pack()

def clip_page():
    clean_page(mainPage)
    clipPage.tkraise()
    clipPage.pack_propagate(False)
    Label(clipPage,
          text="Welcome to the Clip Tool!",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",20)
          ).pack()
    logo = ImageTk.PhotoImage(file="Images/UnderConstruction.png")
    logo_widg = Label(clipPage,image=logo,bg=bgcl)
    logo_widg.image = logo
    logo_widg.pack()
    Button(clipPage,
           text="Back to Main Menu",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:load_main()
           ).pack()
    
# Center and name window
# Code for centering window inspired by https://coderslegacy.com/tkinter-center-window-on-screen/
root = Tk()
root.title("Caleb's Geoprocessing Tools")
width = 600 # Width 
height = 600 # Height
screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight() # Height of the screen
# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))

bgcl = "#990066"

# Need a function to order points in a clockwise form
mainPage = Frame(root,width=600,height=600,bg=bgcl)
mainPage.grid(row=0,column=0)
bufferPage = Frame(root,width=600,height=600,bg=bgcl)
bufferPage.grid(row=0,column=0)
batchBufferPage = Frame(root,width=600,height=600,bg=bgcl)
batchBufferPage.grid(row=0,column=0)
clipPage = Frame(root,width=600,height=600,bg=bgcl)
clipPage.grid(row=0,column=0)

load_main()

root.mainloop()
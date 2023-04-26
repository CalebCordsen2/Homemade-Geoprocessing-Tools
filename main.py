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
    for widget in frame.winfo_children():
        widget.destroy()

def load_main():
    clean_page(bufferPage)
    clean_page(clipPage)
    mainPage.tkraise()
    mainPage.pack_propagate(False)
    logo = ImageTk.PhotoImage(file="Images/CalebLogo.png")
    logo_widg = Label(mainPage,image=logo,bg=bgcl)
    logo_widg.image = logo
    logo_widg.pack()
    Label(mainPage,
          text="Please Select an Option Below",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",20)
          ).pack()
    Button(mainPage,
           text="Clip Tool",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:clip_page()
           ).pack(pady=20)
    Button(mainPage,
           text="Buffer Tool",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:buffer_page()
           ).pack()
    
def buffer_page():
    
    clean_page(mainPage)
    bufferPage.tkraise()
    bufferPage.pack_propagate(False)
    
    Label(bufferPage,
          text="Welcome to the Buffer Tool!",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",20)
          ).pack()
    Label(bufferPage,
          text="Please fill out the information below!",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",17)
          ).pack(pady=20)
    
    outDIR = None
    def browse_outputDIR(label1):
        nonlocal outDIR
        file_name = askdirectory()
        label1.config(text="Selected output directory: "+file_name)
        outDIR = file_name
    Button(bufferPage,
           text="Please Select a Output Directory",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:browse_outputDIR(outLbl)
           ).pack()
    outLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    outLbl.pack()
    
    
    inputFile = None
    def browse_inputShape(label1):
        nonlocal inputFile
        file_name = askopenfilename(filetypes=[("Shape Files","*.shp")])
        label1.config(text="Selected input file: "+file_name)
        inputFile = file_name
    Button(bufferPage,
           text="Please Select a Input Shape File",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:browse_inputShape(inputLbl)
           ).pack()
    inputLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    inputLbl.pack()
    
    outputFileNameEntry = Entry(bufferPage,width=50)
    outputFileNameEntry.insert(END,"Please enter an output file name here. Must end in .shp")
    outputFileNameEntry.pack()
    outFileName = None
    def submitOutFile(label1):
        nonlocal outFileName
        if(outputFileNameEntry.get()[-4:]!='.shp'):
            label1.config(text='Sorry but you need to submit a .shp file name!')
        else:
            outFileName = outputFileNameEntry.get()
            label1.config(text="Inputted file name: "+outputFileNameEntry.get())
    Button(bufferPage,
           text="Submit file name",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:submitOutFile(outFileLbl)
           ).pack()  
    outFileLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    outFileLbl.pack()
    
    bufferSizeEntry = Entry(bufferPage,width=50)
    bufferSizeEntry.insert(END,"Please Enter a Buffer Size Here!")
    bufferSizeEntry.pack()
    actualBufferSize = None
    def submitSize(label1):
        nonlocal actualBufferSize
        try:
            strBuffSize = bufferSizeEntry.get()
            actualBufferSize = float(strBuffSize)
            label1.config(text="Inputted buffer size: "+bufferSizeEntry.get())
        except:
            label1.config(text="That is not a valid number! Try again!")
    Button(bufferPage,
           text="Submit buffer size.",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:submitSize(buffSizeLbl)
           ).pack()  
    buffSizeLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    buffSizeLbl.pack()
    
    currentUnitClick = StringVar()
    currentUnitClick.set("")
    bufferUnitEntry = OptionMenu(bufferPage,currentUnitClick,"meters","kilometers","decimeters","centimeters","millimeters","miles","yards","feet","inches","nautical miles")
    bufferUnitEntry.pack()
    bufferUnit = None
    def submitUnit(label1):
        nonlocal bufferUnit
        if(currentUnitClick.get()!=""):
            bufferUnit = currentUnitClick.get()
            label1.config(text="Inputted buffer unit: "+bufferUnit)
        else:
            label1.config(text="You have not selected a unit type!")
    Button(bufferPage,
           text="Submit buffer unit.",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:submitUnit(buffUnitLbl)
           ).pack()  
    buffUnitLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    buffUnitLbl.pack()
    
    def runBuffer(label1):
        if(actualBufferSize == None or outFileName == None or inputFile == None or outDIR == None or outDIR=='' or inputFile=='' or bufferUnit==None):
            label1.config(text="Please provide valid information to the forms above!")
        else:
            label1.config(text=buffer.bufferMain(outDIR,inputFile,outFileName,actualBufferSize,bufferUnit))
    Button(bufferPage,
           text="Run Buffer",
           font=("TkMenuFont",14),
           bg='#CCCCFF',
           fg='#000066',
           cursor='hand2',
           command = lambda:runBuffer(runBuffLbl)
           ).pack()
    runBuffLbl = Label(bufferPage,
          text="",
          bg=bgcl,
          fg="white",
          font=("TkMenuFont",9)
          )
    runBuffLbl.pack()
    Button(bufferPage,
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
clipPage = Frame(root,width=600,height=600,bg=bgcl)
clipPage.grid(row=0,column=0)

load_main()

root.mainloop()
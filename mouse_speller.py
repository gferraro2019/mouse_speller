"""
The purpose of this script is to show letters on the main screen and to enable a speller that prononce them every time a cursor is hovering the rectangle
related to each letter. The languange of the speller can be changedtrough its proper parameter.

Autorh: Giuseppe Ferraro
mail: giuseppe.ferraro@isae-supaero.fr
"""  

import cv2 
from ctypes import windll, Structure, c_long, byref
from gtts import gTTS
from multiprocessing import Process
import numpy as np
import os
import os.path as op
import pandas as pd
import playsound
import time 
import tkinter

class AOI():
    """This class defines an object called AOI (Area of Interest). It has features like:
    
    a letter;
    a shape defined by x and y coordinates (start point and end point);
    a border;
    a color of the border;
    a thickness for the border;
    a background color;
    a center.

    Returns:
        AOI: an object called AOI (Area of Interest).
    """
    letter = ""
    start_point = ()
    end_point = ()
    #  Blue color in BGR
    border_color = (255, 0, 0)
    background_color = ()
    font_color = ()
    #  Line thickness of 2 px
    border_thickness = 2
    
    def __init__(self,letter,x1,y1,x2,y2,bkg_color,font_color):
        self.letter = letter
        self.start_point = (x1,y1)
        self.end_point = (x2,y2)
        self.background_color = bkg_color
        self.font_color = font_color
    
    def center(self):
        return (int(self.end_point[0]/2),int(self.end_point[1]/2))

class POINT(Structure):
    """This class defines a point in the screen

    Args:
        Structure (POINT): a point in the screen identified by its x and y coordinates
    """
    _fields_ = [("x", c_long), ("y", c_long)]
    
def random_color():
    """This function generates a random color in RGB

    Returns:
        tuple: (R,G,B)
    """
    color =[0,0,0]
    for i in range(3):
        color[i] = np.random.randint(0,255)
    return tuple(color)

def load_colors(file_path):
    """This function reads color from a csv file that reports the color in RGB shape and loads them in BGR shape for CV2 library.
    Also it reads the color to use for the font ("b" stands for black, "w" for white).

    Args:
        file_path (str): the file path of the .csv file to use

    Returns:
        bg_colors (list(tuple)): list of the background colors to use for each AOI
        font_clors (list(str)): list of the font colors to use for each letter in the AOI
    """

    columns_names = ['R_background','G_background','B_background','intesity','R_font','G_font','B_font',]
    df = pd.read_csv(file_path, names=columns_names)# , usecols=columns_names)
    
    bg_colors = []
    font_colors = []

    for i in range(len(df)):
        r_bg,g_bg,b_bg,a_bg,r_font,g_font,b_font = df.loc[i]
        # stores the color in BGR shape
        bg_colors.append((int(b_bg),int(g_bg),int(r_bg)))
        font_colors.append((int(b_font),int(g_font),int(r_font)))

    return bg_colors, font_colors

def load_letters(file_path):
    with open(file_path) as file:
        data = file.read()
        
        letters = data.split("\n"
                             )
    return letters
        

def speak(text):
    """This function generates the audio file to be reproduce from the speller

    Args:
        text (str): text to be reproduce in the audio file
    """
    #  change the lang pamter for other languages
    tts = gTTS(text=text, lang='fr')

    filename = "abc1.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def queryMousePosition():
    """Thi function reads the mouse position in the current screen.

    Returns:
        position (dict): a dictionary containing the x and y coordinates.
    """
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

def getAOI(position, AOIs):
    """This function get the Area Of Interest (AOI) that the mouse is currently hovering.

    Args:
        position (dict): a dictionary containing the x and y coordinates.
        AOIs (list(AOI)): the list of all the existing AOI in the current screen.
         
     Returns:
        aoi (str): the letter of the current AOI that the mouse is hovering.
    """
    x = position["x"]
    y = position["y"]
#      print(x,y)
    aoi = "out"
    for l in AOIs:
        a = AOIs[l]
#          print(a.start_point,a.end_point)
        if(x>=a.start_point[0] and x<a.end_point[0] and y>=a.start_point[1] and y< a.end_point[1]):
            aoi= a.letter
            # print("AOI is: ",aoi)
            break

    return aoi

def speller(AOIs):
    """This function is spelling the letter of the current AOI. This function is executed in seperate process for making possible to
    spell the letters while the table of AOIs is showed in another indipendent process. 

    Args:
        AOIs (list(AOI)): the list of all the existing AOI in the current screen.
    """
    prevAOI = "start"
    currAOI = "start"
    timer = 0.300
    while(True):
        pos = queryMousePosition()
        currAOI = getAOI(pos,AOIs)

        if(currAOI!=prevAOI):
            if(currAOI!="out" ):
                t0=time.time()       
            prevAOI = currAOI

        if(currAOI!="out" and currAOI==prevAOI and time.time()-t0 >=timer):
            speak(currAOI)
            t=time.time()-t0
            print(currAOI,"\t",t,"\t",pos,"\t",AOIs[currAOI].center())
            t0 = time.time()

def showTable(AOIs,h_interspace,v_interspace,rectangle_width,rectangle_heigth,screen_width,screen_heigth):
    """This function is showing the table containg the letters. This function is executed in seperate process for making possible to
    show the letters and AOIs while the letters of the AOIs are spelled in another indipendent process. 

    Args:
        AOIs (list(AOI)): the list of all the existing AOI in the current screen.
        h_interspace (int): horizontal space in-between two rectangles(AOIs)
        v_interspace (int): vertical space in-between two rectangles(AOIs)
        rectangle_width (int): the width mesuread in pixels of a rectangle(aoi)
        rectangle_heigth (int): the height mesuread in pixels of a rectangle
        screen_width (int): the width mesuread in pixels of the screen resolution
        screen_heigth (int): the heigth mesuread in pixels of the screen resolution
    """
    #  Create a black image
    img = np.zeros((screen_heigth,screen_width,3), np.uint8)

    for letter in AOIs:
        aoi = AOIs[letter]
        img = cv2.rectangle(img,aoi.start_point,aoi.end_point,aoi.background_color,-1)
        img = cv2.putText(img, letter, (aoi.end_point[0]-h_interspace-int(rectangle_width/2),aoi.end_point[1]+int(v_interspace/2)-int(rectangle_heigth/2)) , cv2.FONT_HERSHEY_TRIPLEX, 2, aoi.font_color, 5)

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("window", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Reads the screen resolution
    root = tkinter.Tk()
    root.withdraw()
    screen_width, screen_heigth = root.winfo_screenwidth(), root.winfo_screenheight()
    
    # Creates a dictionary of AOIs
    AOIs = {}
    
    # List of letters for the AOIs
    # letters = ["a","i","s","o","l",
    #            "r","c","e","n","m",
    #            "t","j/ge","d","p","v",
    #            u"é","u","f/ph","ch","b"]
    
    # Specify here a different path and/or filename
    path = r""
    file_name_letters = "letters.txt"
    file_name_colors = "color_backgrounds_and_letters.csv"
    file_path_letters = op.join(path,file_name_letters)
    file_path_colors = op.join(path,file_name_colors)
    
    # List of letters for the AOIs
    letters = load_letters(file_path_letters)
    
    # Loading colors for background of the rectabgles and the font of the letter
    backgorund_colors, font_colors = load_colors(file_path_colors)

    resolution = (screen_width,screen_heigth)
    
    # Horizontal space in pixels between two AOIs
    h_interspace = 30
    
    # Vertical space in pixels between two AOIs
    v_interspace = 20
    
    n_letters_row = 5
    n_letters_col = 4
    rectangle_width = int((resolution[0] - (n_letters_row + 1)*h_interspace)/n_letters_row)
    rectangle_heigth =int((resolution[1] - (n_letters_col + 1)*v_interspace)/n_letters_col)

    # Creates list of coordinates of the AOIs
    coordinates = []
    
    # Creates the coordinates for the AOIs dynamically
    tmp_y2=0
    for j in range(n_letters_col):
        tmp_x2 =0
        tmp_y1 = tmp_y2 + v_interspace
        for k in range(n_letters_row):
            tmp_x1 = tmp_x2 + h_interspace
            tmp_x2 = tmp_x1 + rectangle_width 
            tmp_y2 = tmp_y1 + rectangle_heigth 
            coordinates.append((tmp_x1,tmp_y1,tmp_x2,tmp_y2))

    # Updates the dictionary of the AOIs
    for i,l in enumerate(letters):
        AOIs[l] = AOI(l,coordinates[i][0],coordinates[i][1],coordinates[i][2],coordinates[i][3],backgorund_colors[i],font_colors[i])    

    print(coordinates)
    
    # Executes 2 indipendent processes: one for showing the tables of letters and the other for spelling the letters of the current AOI 
    p1 = Process(target=showTable, args=(AOIs,h_interspace,v_interspace,rectangle_width,rectangle_heigth,screen_width,screen_heigth))
    p2 = Process(target=speller, args=(AOIs,))
    p1.start()
    p2.start()




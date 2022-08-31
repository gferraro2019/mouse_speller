Mouse Speller
====

This project aims to show in a full-screen mode a matrix of letters included in colored rectangles.
Once the cursor of the mouse is hovering each rectangle the speller will pronounce the letter contained in that rectangle.
It can be used in combination with an eye-tracker, using this latter to control the cursor of the mouse.

Because this project wast developed to be used with ET the rectangle are defined as Areas of Interest (AOIs).

Use the files "letters.txt" and "color_backgrounds_and_letters.csv" to set respectively the letters/symbols/words to plot inside the rectangles and its background color and font color.

## Defining Letters/Symbols/Words
For inserting a letter/symbol/word in "letters.txt" you just need to type it in the line a pressing enter to add the special charcter "\n". Everything is in a single line will be plotted in the rectangle.

## Definig Colors for the Background of the rectangles and for the font.
For defining the colors to be used as background colors for the rectangles and font colorsi through "color_backgrounds_and_letters.csv" "letters.txt" you just need to type it in the line a pressing enter to add the special charcter "\n". Everything is in a single line will be plotted in the rectangle.

Each line reports in the order the rgba for backgound color of the rectangle and then the rgb for the font color. Remeber that in the file color must be saved in RGB order and then will be automatic traduced in BGR for cv2 library.
     
i.e the first line in "color_backgrounds_and_letters.csv" file reports the values: 243,237,249,255,0,0,0 respectively 'R','G','B','a' for the background color of the rectangle and then the'R','G','B' for the font color.


## Contents

[Dependencies](#dependencies)  
[Installation](#installation)  
[Example usage](#example-usage)  
[Help](#help)

## Dependencies
* cv2
* ctypes
* gtts
* multiprocessing
* numpy
* os
* pandas
* playsound
* time 
* tkinter


## Installation
All dependecy can be install through the requirements.txt file with the command: pip install -r requirements.txt

## Example Usage
python mouse_speller.py

![matrix of letters to spell](https://github.com/gferraro2019/mouse_speller/blob/main/example.png?raw=true)


## Help
For any modification or further explanation please feel free to reach me out at:
giuseppe.ferraro@isae-suapero.fr



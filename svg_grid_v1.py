#Create an SVG file of an stadnard paper siez and populate with a flex
#grid ready to polutae with text and data

#paper sizes
#A4 = 210mm x 297mm
#A2 = 420mm x 594mm
#B2 = 500mm x 707mm

import csv
from helpers import *

#GRID ONSTANTS

DOC_WIDTH = 500
DOC_HEIGHT = 707

GAPS = 2 #gaps between boxes

BOX_HEIGHT = 50 #text box height

TEXT_BOX_W = 5 #text box width
PLOT_BOX_W = DOC_WIDTH - TEXT_BOX_W - (GAPS*3) # plot box width
#-----------------------------------------------------------------------

#DATA CONSTANTS
X_SCALE_FACTOR = 0.011
Y_SCALE_FACTOR = 0.05

X_FRAME_OFFSET = 5
Y_FRAME_OFFSET = 11

TEXT_COLOUR = "darkslategray"
TEXT_SPACING = 2.5
FONT_SIZE = 2.3

LINE_WEIGHT = 0.25


#-----------------------------------------------------------------------

#array for storing all the svg paths
grids = []

for i in range(12):

    data = openFile('../ForecastDataSets/Newlyn2020.csv', i+1)
    svg_paths = createSVG(data[0], data[1], X_SCALE_FACTOR, Y_SCALE_FACTOR,  X_FRAME_OFFSET, Y_FRAME_OFFSET, TEXT_SPACING, FONT_SIZE, TEXT_COLOUR, LINE_WEIGHT)
   
    #calculate the vertical spacing bewteen the rows.
    y_coord = (i*(BOX_HEIGHT + GAPS)) + GAPS
    
    #create svg strings for the text box and plot box.
    # plot box will always fill the space regardless of text box width.
    text_grid = '<rect x="{}" y="{}" width="{}" height="{}" stroke="black" stroke-width="0.25px" fill="none"/>'.format(GAPS, y_coord, TEXT_BOX_W, BOX_HEIGHT)
    grid = '<rect x="{}" y="{}" width="{}" height="{}" stroke="black" stroke-width="0.25px" fill="none"/>'.format(TEXT_BOX_W + (GAPS*2), y_coord, PLOT_BOX_W, BOX_HEIGHT)     
    nested_svg_open = '<svg x="{}" y="{}">\n'.format(0 + (GAPS*2), y_coord)
    nest_svg_close = '</svg>\n'
    
    #add new lines of svg to the grid array
    grids.append(text_grid)
    grids.append(grid)
    grids.append(nested_svg_open)

    for path in svg_paths:
        grids.append(path + '\n')
    
    grids.append(nest_svg_close)




#open a file and start wirting svg string to it.
f = open("svg_grid2.html", "w")

#Opening SVG tag. Width and Height in absolute(mm) units.
#Viewbox units set to same to ensure stuff on screen is correct and it prints OK.
f.write('<svg width="{}mm" height="{}mm" version="1.1" viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg">\n'.format(DOC_WIDTH, DOC_HEIGHT, DOC_WIDTH, DOC_HEIGHT))

#Black border for testing, remove later.
f.write('<rect x="0" y="0" width="{}" height="{}" stroke="red" stroke-width="0.25px" fill="none"/>\n'.format(DOC_WIDTH, DOC_HEIGHT))

for i in range(len(grids)):
    f.write(grids[i] + '\n')

f.write('</svg>')

f.close()
print("end")
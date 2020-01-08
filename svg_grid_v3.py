#Create an SVG file of an stadnard paper siez and populate with a flex
#grid ready to polutae with text and data

#paper sizes
#A4 = 210mm x 297mm
#A2 = 420mm x 594mm
#B2 = 500mm x 707mm

import csv
from helpers import *

#-----------------------------------------------------------------------
#DOC GRID CONSTANTS
DOC_WIDTH = 500                     # Main SVG doc size   
DOC_HEIGHT = 707                    # Main SVG doc size
GAPS = 0                           #gaps between boxes
BOX_HEIGHT = 50                     #text box height
TEXT_BOX_W = 10                      #text box width
PLOT_BOX_W = DOC_WIDTH - TEXT_BOX_W - (GAPS*3) # plot box width
GRID_COLOUR = "#2E6A8D"              #grid colour fill
GRID_WEIGHT = 1
GRID_LINE_COLOUR = "#2E6A8D"

#-----------------------------------------------------------------------
#DATA PLOT CONSTANTS
X_SCALE_FACTOR = 0.0105              # X-scale of curve plot
Y_SCALE_FACTOR = 0.05               # Y-scale of curve plot
X_FRAME_OFFSET = 2                  #move the curve plot around inside the grid box (LEFT/RIGHT)
Y_FRAME_OFFSET = 10                  #move the curve plot around inside the grid box (UP/DOWN)
TEXT_COLOUR = "white"               #Text colour
TEXT_SPACING = 2.5                  #Text line height bewteen TIME/HEIGHT/DAY
FONT_FAMILY = "monospace"           #Font family
FONT_SIZE = 2                       #Font size
LINE_WEIGHT = 0.25                  #Line wieght, stroke.
LINE_COLOUR = "white"               #Line colour

#-----------------------------------------------------------------------

#array for storing all the svg paths
grids = []
month_text = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

for i in range(12):

    data = openFile('../ForecastDataSets/Newlyn2020.csv', i+1)
    svg_paths = createSVG(data[0], data[1], X_SCALE_FACTOR, Y_SCALE_FACTOR,  X_FRAME_OFFSET, Y_FRAME_OFFSET, TEXT_SPACING, FONT_FAMILY, FONT_SIZE, TEXT_COLOUR, LINE_WEIGHT, LINE_COLOUR)
   
    #calculate the vertical spacing bewteen the rows.
    y_coord = (i*(BOX_HEIGHT + GAPS)) + GAPS
    
    #create svg strings for the text box and plot box.
    # plot box will always fill the space regardless of text box width.
    text_grid = '<rect x="{}" y="{}" width="{}" height="{}" stroke="{}" stroke-width="{}" fill="{}"/>\n'.format(GAPS, y_coord, TEXT_BOX_W, BOX_HEIGHT, GRID_LINE_COLOUR, GRID_WEIGHT, GRID_COLOUR)

    text_month = '<text x="{}" y="{}" dx="0" dy="0" transform="rotate(90, {}, {})" text-anchor="middle" dominant-baseline="central" font-size="5" fill="white" >{}</text>\n'.format(GAPS + (TEXT_BOX_W/2), (BOX_HEIGHT/2) + y_coord, GAPS + (TEXT_BOX_W/2),(BOX_HEIGHT/2) + y_coord, month_text[i].upper())


    #TODO . code for the vetical rotated month text goes here...
    
    grid = '<rect x="{}" y="{}" width="{}" height="{}" stroke="{}" stroke-width="{}" fill="{}"/>\n'.format(TEXT_BOX_W + (GAPS*2), y_coord, PLOT_BOX_W, BOX_HEIGHT,GRID_LINE_COLOUR, GRID_WEIGHT, GRID_COLOUR)     
    nested_svg_open = '<svg x="{}" y="{}">\n'.format(TEXT_BOX_W + (GAPS*2), y_coord)
    nest_svg_close = '</svg>\n'
    
    #add new lines of svg to the grid array
    grids.append(text_grid)
    grids.append(text_month)
    grids.append(grid)
    grids.append(nested_svg_open)

    for path in svg_paths:
        grids.append(path + '\n')
    
    grids.append(nest_svg_close)




#open a file and start wirting svg string to it.
f = open("poster1.svg", "w")

#Opening SVG tag. Width and Height in absolute(mm) units.
#Viewbox units set to same to ensure stuff on screen is correct and it prints OK.
f.write('<svg width="{}mm" height="{}mm" version="1.1" viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg">\n'.format(DOC_WIDTH, DOC_HEIGHT, DOC_WIDTH, DOC_HEIGHT))

#Black border for testing, remove later.
f.write('<rect x="0" y="0" width="{}" height="{}" stroke="red" stroke-width="0.25px" fill="none"/>\n'.format(DOC_WIDTH, DOC_HEIGHT))

for i in range(len(grids)):
    f.write(grids[i])

f.write('</svg>')

f.close()
print("end")
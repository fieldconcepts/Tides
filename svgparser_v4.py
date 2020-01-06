#Loads a tidal forecast data set from csv file and converts points to an SVG in html format
#ready to view inside browser.

import csv
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt

#constant scale factors and offsets
X_SCALE_FACTOR = 0.03
Y_SCALE_FACTOR = 0.1

X_FRAME_OFFSET = 20
Y_FRAME_OFFSET = 40

SPACING = 120
COLOUR = "darkslategray"
TEXT_SPACING = 7

YEAR = []

for j in range(12):

    print(j+1)
    #open the forecast dataset and skip headers
    with open('../ForecastDataSets/Newlyn2020.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)  # skip the headers

        time = []
        height = []

        #loop throughthe file
        for row in csv_reader:

            #parse in the datetimes and append to new datetime array
            temp = datetime.strptime(row[0], "%Y-%m-%d %H:%M")

            if temp.month == j+1:
                time.append(temp)
                height.append(float(row[1]))

    #find mid tide
    midtide = (height[0] + height[1])/2


    #create timedeltas
    deltas = []

    for i in range(len(time)):
        delta = time[i] - time[0]
        delta_mins = delta.total_seconds() / 60
        delta_mins = delta_mins * X_SCALE_FACTOR
        deltas.append(int(delta_mins))


    #convert heights to integers
    points = []

    for i in range(len(height)):
        point = int(100 * height[i])
        point = point* Y_SCALE_FACTOR
        points.append(point)


    #inverse datapoints
    points_inverse = []
    for i in range(len(points)):
        points_inverse.append(points[i] * -1)



    #create boundary box for plot
    upper_bound = 0 + Y_FRAME_OFFSET + (SPACING * j)
    lower_bound = max(points_inverse) - min(points_inverse) + Y_FRAME_OFFSET + (SPACING * j)

    svg_line1 = '<line x1="0" y1="{}" x2="2000" y2="{}" style="stroke:red ;stroke-width:1" />'.format(lower_bound, lower_bound)
    svg_line2 = '<line x1="0" y1="{}" x2="2000" y2="{}" style="stroke:red ;stroke-width:1" />'.format(upper_bound, upper_bound)


    #create svg file structure strings
    svg_paths = []

    for i in range(len(points_inverse)-1):

        #point1 X and Y coords
        p1_x = int(deltas[i]) + X_FRAME_OFFSET
        p1_y = int(points_inverse[i]) - min(points_inverse) + Y_FRAME_OFFSET + (SPACING * j)

        #point 1 X and Y coords
        p2_x = int(deltas[i+1]) + X_FRAME_OFFSET 
        p2_y = int(points_inverse[i+1]) - min(points_inverse) + Y_FRAME_OFFSET + (SPACING * j)

        #calc to find bezier midpoint, should be relatively consistant
        curve = (p2_x - p1_x) / 2

        #bezeier 1 X and Y coords
        b1_x = p1_x + curve
        b1_y = p1_y

        #bezier 2 X and Y coords
        b2_x = p2_x - curve
        b2_y = p2_y

        #create a formatted svg path string and append to an array
        svg_path = '<path d="M{},{} C{},{} {},{} {},{}" stroke="red" stroke-width="1" stroke-linecap="round" fill="none"/>'.format(p1_x,p1_y,b1_x,b1_y,b2_x,b2_y,p2_x,p2_y)


        #create a formatted svg text  HEIGHT string and append to an array
        if height[i] > midtide:
            text_height_offset = -6
            text_time_offset = text_height_offset - TEXT_SPACING
            text_date_offset = text_time_offset - TEXT_SPACING
        elif height[i] < midtide:
            text_height_offset = 10
            text_time_offset = text_height_offset + TEXT_SPACING
            text_date_offset = text_time_offset + TEXT_SPACING
        
        svg_text_height = '<text x="{}" y="{}" dx="-5" dy="{}" style="fill:{}; font: italic 6px sans-serif;" font-weight="bold">{:.1f}</text>'.format(p1_x, p1_y, text_height_offset, COLOUR, height[i])
        svg_text_time = '<text x="{}" y="{}" dx="-10" dy="{}" style="fill:{}; font: italic 6px sans-serif;" >{}</text>'.format(p1_x, p1_y, text_time_offset, COLOUR, time[i].strftime('%H:%M'))
        svg_text_date = '<text x="{}" y="{}" dx="-10" dy="{}" style="fill:{}; font: italic 6px sans-serif;" >{}</text>'.format(p1_x, p1_y, text_date_offset, COLOUR, time[i].strftime('%a%-d'))
        #append strings to svg array
        svg_paths.append(svg_path)
        svg_paths.append(svg_text_height)
        svg_paths.append(svg_text_time)
        svg_paths.append(svg_text_date)

    #manually add a final text item to last point
    if height[-1] > midtide:
        text_height_offset_last = -6
        text_time_offset_last = text_height_offset_last - TEXT_SPACING
        text_date_offset_last = text_time_offset_last - TEXT_SPACING
    elif height[-1] < midtide:
        text_height_offset_last = 10
        text_time_offset_last = text_height_offset_last + TEXT_SPACING
        text_date_offset_last = text_time_offset_last + TEXT_SPACING

    p1_x_last = int(deltas[-1]) + X_FRAME_OFFSET
    p1_y_last = int(points_inverse[-1]) - min(points_inverse) + Y_FRAME_OFFSET + (SPACING * j)
    svg_text_height_last = '<text x="{}" y="{}" dx="-5" dy="{}" style="fill:{}; font: italic 6px sans-serif;" >{:.1f}</text>'.format(p1_x_last, p1_y_last, text_height_offset_last, COLOUR, height[-1])
    svg_text_time_last = '<text x="{}" y="{}" dx="-10" dy="{}" style="fill:{}; font: italic 6px sans-serif;" >{}</text>'.format(p1_x_last, p1_y_last, text_time_offset_last, COLOUR, time[-1].strftime('%H:%M'))
    svg_text_date_last = '<text x="{}" y="{}" dx="-10" dy="{}" style="fill:{}; font: italic 6px sans-serif;" >{}</text>'.format(p1_x_last, p1_y_last, text_date_offset_last, COLOUR, time[-1].strftime('%a%-d'))   
        
    #append final point text and upper lower bound lines
    svg_paths.append(svg_text_height_last)
    svg_paths.append(svg_text_time_last)
    svg_paths.append(svg_text_date_last)
    #svg_paths.append(svg_line1) #BOUNDARY LINES
    #svg_paths.append(svg_line2) #BOUNDARY LINES

    YEAR.append(svg_paths)
    

#output the paths to an svg and save as a html file ready to view in browser
f = open("svg_output2.html", "w")
f.write('<!DOCTYPE html>' + '\n' + '<html>' + '\n' + '<body>' + '\n' + '<svg height="1600" width="2000">' + '\n')

for k in range(len(YEAR)):
    for path in YEAR[k]:
            f.write(path + '\n')

f.write('</svg>' + '\n' + '</body>' + '\n' + '</html>')
f.close()

print("end")

#fig, ax = plt.subplots()
#ax.plot(january_deltas, january_points)
#plt.show()
    



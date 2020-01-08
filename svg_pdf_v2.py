from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

drawing = svg2rlg("poster1.svg")
renderPDF.drawToFile(drawing, "poster1.pdf")

print("end")

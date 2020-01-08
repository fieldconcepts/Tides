from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

drawing = svg2rlg("poster_test_1.svg")
renderPDF.drawToFile(drawing, "file2.pdf")
renderPM.drawToFile(drawing, "file2.png", fmt="PNG")

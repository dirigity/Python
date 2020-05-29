from appJar import gui
import random
def modifyScale():
    app.setMessage("Output", str(app.getAllScales()))


def randomize():
    app.openFrame("SlidersFrame")
    for i in range(DimensionN):           
        app.setScale(str(i), 100*random.random(), callFunction=True)
    app.stopFrame()


app = gui("Interface")

app.setFont(14)

app.startFrame("SlidersFrame", row=0, column=0)
DimensionN = 5
for i in range(DimensionN):   
    app.addLabelScale(str(i))     
    app.setScaleChangeFunction(str(i),modifyScale)
app.stopFrame()
app.startFrame("OutputFrame",row=0,column=1)
app.addMessage("Output", "")
app.setMessageWidth("Output", 100)

app.stopFrame()

app.addButton("Randomize", randomize)

randomize()
app.go()
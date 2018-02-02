from appJar import gui
import time
import lazylights
import binascii

def press(name):
    
    global bulbs
    
    print(name, "button pressed")
    #app.setLabel("lbl1","Pressed " + str(count) + " Times")
    
    if (name == "Exit") :
        app.stop()
    if (name == "Find Bulbs") :
        
        bulbs = lazylights.find_bulbs()
        print (bulbs)
    elif (name == "On") :
        app.warn("ON")
        app.setImage("Light","bulb_on.gif")
        lazylights.set_power(bulbs, True)
    elif (name == "Off"):
        app.warn("OFF")
        app.setImage("Light","bulb_off.gif")
        lazylights.set_power(bulbs, False)


app = gui("Lights")

app.addLabel("lbl1", "LIFX Controller")
app.addButton("Find Bulbs",press)
app.setBg("white")
#app.setFg("white")
app.setFont(16)

app.addImage("Light","bulb_off.gif")
app.addButtons(["On","Off"],press)
app.addButton("Exit",press)

bulbs = lazylights.find_bulbs()
print (bulbs)
app.go()

app.warn("App Ended")




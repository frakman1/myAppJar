from appJar import gui
import time
import lazylights
import binascii
import lifxlan 

bulbs = 0
selected_bulb = 0

def listChanged():
    details = str(0)
    app.setTextArea("Result", "Loading bulb details")
    selected =  (app.getOptionBox("LIFX Bulbs"))#;print("selected: ",selected)
    global bulbs
    global selected_bulb
    for bulb in bulbs:
        if (bulb.get_label() == selected):
            try:
                details =str(bulb)
                selected_bulb = bulb
                break
            except Exception as e:
                print ("Ignoring error: ", str(e))
                app.errorBox("Error", str(e))
                
    
    app.clearTextArea("Result")
    app.setTextArea("Result", details)
    if "Power: On" in details:
        print ("BULB is ON")
        app.setButtonImage("Light","bulb_on.gif")
    elif "Power: Off" in details:
        print ("BULB is OFF ")
        app.setButtonImage("Light","bulb_off.gif")
        

def finder():
    global bulbList
    bulbList.clear()
    try:
        global bulbs
        lan = lifxlan.LifxLAN(3)
        bulbs = lan.get_lights()
        #print(bulbs[0].label) 
        if len(bulbs) < 1:
            app.errorBox("Error", "No bulbs found. Please try again.")
            app.setLabelBg("lbl2","gray")
            app.setLabel("lbl2", "Found 0 bulbs")
            return
        else:
            app.setLabelBg("lbl2","green")
        
        app.setLabel("lbl2", "Found "+str(len(bulbs))+" bulbs")
        for bulb in bulbs:
            print(bulb.get_label()) 
            bulbList.append(bulb.get_label())
        app.changeOptionBox("LIFX Bulbs", bulbList)
    
    except Exception as e:
        print ("Ignoring error:", str(e))
        app.setLabelBg("lbl2","gray")
        app.setLabel("lbl2", "Found 0 bulbs")
        app.errorBox("Error", str(e)+"\n\nPlease try again. If you keep getting this error. Try restarting the app")
        
    print ("finder() Ended")

def press(name):
    global bulbs
    
    print(name, "button pressed")
    
    if (name == "Find Bulbs") :
        finder()
    elif (name == "Light") :
        print("selected: ",selected_bulb.get_label())
        print("Power is Currently: {}".format(selected_bulb.get_power()))
        onOff = selected_bulb.get_power()
        selected_bulb.set_power(not selected_bulb.get_power(), duration=0, rapid=True)
        if (onOff == 0):
            selected_bulb.set_power(True, duration=0, rapid=True)
            app.setButtonImage("Light","bulb_on.gif") ;# print("PowerOn")
        else:
            selected_bulb.set_power(False, duration=0, rapid=True)
            app.setButtonImage("Light","bulb_off.gif"); #print("PowerOff")
        
        listChanged()



bulbList = ["-None-          "]

app = gui("LIFX Controller")
app.setStretch("both")
app.setResizable(True)
app.setFont(12)

app.setSticky("nw")

app.startLabelFrame("", 0,0,2)
app.addButton("Find Bulbs",press,0,0)
app.addLabel("lbl2"," ",0,1)
app.setLabelBg("lbl2","gray")
app.addOptionBox("LIFX Bulbs",bulbList,1,0)
app.setOptionBoxChangeFunction("LIFX Bulbs", listChanged)
app.addImageButton("Light", press, "bulb_off.gif",align="center")
app.stopLabelFrame()


app.setSticky("news")
app.addScrolledTextArea("Result",2,0,5,23)


app.go()

app.warn("App Ended")




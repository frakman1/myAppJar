from appJar import gui
import time
import binascii
import lifxlan 
import colorsys
from colour import Color
import math
import sys
from time import sleep
from lifxlan import BLUE, CYAN, GREEN, ORANGE, PINK, PURPLE, RED, YELLOW


EXPECTED_BULBS = 2

bulbs = 0
selected_bulb = 0
details = str(0)
gSelectAll = False
lan = 0
gExpectedBulbs = 0
test_string = """

"""

def selectAllPressed (name):
    global gSelectAll
    gSelectAll = app.getCheckBox("Select All")
    #print("gSelectAll:",gSelectAll)

def expectedPressed (name):
    global gExpectedBulbs
    gExpectedBulbs = app.getSpinBox("Expected Bulbs")
    #print("gExpectedBulbs:",gExpectedBulbs)

    
def rgb_to_hsv(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d/high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return h, s, v
    
    
def hsv_to_rgb(h, s, v):
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i%6)]

    return r, g, b


def listChanged():
    app.clearTextArea("Result");
    app.setTextArea("Result", "Loading bulb details")
    selected =  (app.getOptionBox("LIFX Bulbs"))#;print("selected: ",selected)
    global bulbs
    global selected_bulb
    global details
    try:
        for bulb in bulbs:
            if (bulb.label == selected):
                #print("Found selected bulb")
                selected_bulb = bulb
                details =str(selected_bulb)
                #print(details)
                #print("breaking")
                break
    except Exception as e:
        print ("Ignoring error: ", str(e))
        app.errorBox("Error", str(e))
        return
                
    
    app.clearTextArea("Result")
    app.setTextArea("Result", details)
    
    if "Power: On" in details:
        #print ("BULB is ON")
        app.setButtonImage("Light","bulb_on.gif")
    elif "Power: Off" in details:
        #print ("BULB is OFF ")
        app.setButtonImage("Light","bulb_off.gif")
    app.setButton ( "Light", "Toggle" )    
    app.showButton("Light")
    color = bulb.get_color();#print(color[0],color[1],color[2]); 
    h = color[0]/65535.0;#print("h:",h)
    s = color[1]/65535.0;#print("s:",s)
    v = color[2]/65535.0;#print("v:",v)

    rgb1= hsv_to_rgb(h,s,v);#print("rgb1:",rgb1)
    c = Color(rgb=(rgb1[0], rgb1[1], rgb1[2])) 
    #print("c:",c)
    app.setLabelBg("bulbcolor", c.hex_l)
    
    

    
        

def finder():
    global bulbList
    global lan
    bulbList.clear()
    bulbList.append("-Select Bulb-")
    try:
        global bulbs
        lan = lifxlan.LifxLAN(int(gExpectedBulbs) if int(gExpectedBulbs) != 0 else None)
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
            #print(".get_label()",bulb.get_label()) 
            #print(".label:",bulb.label)
            bulbList.append(bulb.get_label())
        app.changeOptionBox("LIFX Bulbs", bulbList)
        app.showButton ( "Pick Color" )
    
    except Exception as e:
        print ("Ignoring error:", str(e))
        app.setLabelBg("lbl2","gray")
        app.setLabel("lbl2", "Found 0 bulbs")
        app.errorBox("Error", str(e)+"\n\nPlease try again. If you keep getting this error. Try restarting the app")
        
    print ("finder() Ended")

def press(name):
    global bulbs
    global details
    global gSelectAll
    global lan
    
    #print(name, "button pressed")
    
    if (name == "Find Bulbs") :
        finder()
    elif (name == "All Off"):
        if len(bulbs) < 1:
            return
        lan.set_power_all_lights(False, rapid=True)
    elif (name == "All On"):
        if len(bulbs) < 1:
            return
        lan.set_power_all_lights(True, rapid=True)
        
    elif (name == "Pick Color") :
        pickedColor = app.colourBox(colour="#FFFFFF")
        app.setLabelBg("bulbcolor", pickedColor)
        #print("pickedColor:",pickedColor)
        if pickedColor == None:
            return
        c = Color(str(pickedColor))
        hsv = rgb_to_hsv(c.red,c.green,c.blue)
        #print("hsv:",hsv)
        bulbHSBK = [hsv[0]*65535.0,hsv[1]*65535.0,hsv[2]*65535.0,3500]
        print ("bulbHSBK:",bulbHSBK)
        if gSelectAll:
            lan.set_color_all_lights(bulbHSBK, duration=0, rapid=False)
            
        elif selected_bulb:
            #print("sending color",hsv)
            selected_bulb.set_color(bulbHSBK, duration=0, rapid=False)
        else:
            app.errorBox("Error", "Error. No bulb was selected. Please select a bulb from the pull-down menu (or tick the 'Select All' checkbox) and try again.")
            
    elif (name == "Light") :
        #print("selected: ",selected_bulb.label)
        #print("Power is Currently: {}".format(selected_bulb.power_level))
        onOff = selected_bulb.power_level; print
        #selected_bulb.set_power(not selected_bulb.get_power(), duration=0, rapid=True)
        if "Power: Off" in details:
            selected_bulb.set_power(65535, duration=0, rapid=False)
            app.setButtonImage("Light","bulb_on.gif");#print("PowerOn");
            details = details.replace("Power: Off", "Power: On"); 
            app.clearTextArea("Result")
            app.setTextArea("Result", details)
            
        else:
            selected_bulb.set_power(0, duration=0, rapid=False)
            app.setButtonImage("Light","bulb_off.gif");#print("PowerOff");
            details = details.replace("Power: On", "Power: Off"); #print("details:\n",details)
            app.clearTextArea("Result")
            app.setTextArea("Result", details)
            
        app.setButton ( "Light", "Toggle" )
        app.showButton("Light")
        
        
        #listChanged()

def rainbow_press(name):
    print("Discovering lights...")
    lan = lifxlan.LifxLAN(EXPECTED_BULBS)
    print("lifx-type:",type(lan))
    original_colors = lan.get_color_all_lights()
    original_powers = lan.get_power_all_lights()

    print("Turning on all lights...")
    lan.set_power_all_lights(True)
    sleep(1)

    print("Flashy fast rainbow")
    rainbow(lan, 0.4)

    print("Smooth slow rainbow")
    #rainbow(lan, 1, smooth=True)

    print("Restoring original color to all lights...")
    for light in original_colors:
        light.set_color(original_colors[light])

    sleep(1)

    print("Restoring original power to all lights...")
    for light in original_powers:
        light.set_power(original_powers[light])

def rainbow(lan, duration_secs=0.5, smooth=False):
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
    transition_time_ms = duration_secs*1000 if smooth else 500
    rapid = True if duration_secs < 1 else False
    for i in range(0,3):
        for color in colors:
            lan.set_color_all_lights(color, transition_time_ms, rapid)
            sleep(duration_secs)
    
    


bulbList = ["-None-          "]

app = gui("LIFX Controller")
app.setStretch("both")
app.setResizable(True)
app.setFont(12)

app.setSticky("new")

app.startLabelFrame("", 0,0,2)
app.addButton("Find Bulbs",press,0,0)
app.addLabel("lbl2"," ",1,0)
app.setLabelBg("lbl2","white")
app.addOptionBox("LIFX Bulbs",bulbList,2,0)
app.setOptionBoxChangeFunction("LIFX Bulbs", listChanged)
app.addImageButton("Light", press, "bulb_off.gif",align="center")
app.setButton( "Light", "Toggle" )
app.hideButton("Light")
app.addButton("Pick Color", press,1,1)
app.hideButton ( "Pick Color" )
#app.setButtonImage("picker", "colorpicker.gif", align=None)
app.addCheckBox("Select All",0,1)
app.setCheckBoxChangeFunction("Select All", selectAllPressed)
app.startLabelFrame("Bulb Color",3,1,1,2)
app.addLabel("bulbcolor", "", 3, 1, 1, 2)
app.setLabel("bulbcolor"," ")
app.setLabelHeight("bulbcolor", 15)
app.setLabelWidth("bulbcolor", 25) 
app.setLabelBg("bulbcolor", "gray")
app.stopLabelFrame()
app.setSticky("ne")

app.addButton("All Off", press,0,2)
app.addButton("All On",  press,1,2)
app.addButton("All Rainbow", rainbow_press,2,2)
expected_range = list(range(1,20))
app.addLabelSpinBox ( "Expected Bulbs", list(reversed(range(20))), 3,2 )
app.setSpinBox("Expected Bulbs", 2)

app.setSpinBoxChangeFunction("Expected Bulbs", expectedPressed)

app.stopLabelFrame()


app.setSticky("sew")
app.startLabelFrame("Bulb Details",4,0)
app.addScrolledTextArea("Result",3,0)
app.setTextAreaWidth("Result", 75)
app.setTextAreaHeight("Result", 28)
app.setTextArea("Result", test_string)
app.stopLabelFrame()

app.go()

app.warn("App Ended")




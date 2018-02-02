from appJar import gui
import time
import lazylights
import binascii
#------------------------------------------------------------------------------------------------------------
# I use this to manually create a bulb using IP and MAC address.
def createBulb(ip, macString, port = 56700):
    return lazylights.Bulb(b'LIFXV2', binascii.unhexlify(macString.replace(':', '')), (ip,port))
#------------------------------------------------------------------------------------------------------------


def press(name):
    
    
    print(name, "button pressed")
    #app.setLabel("lbl1","Pressed " + str(count) + " Times")
    
    if (name == "Exit") :
        app.stop()
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

app.setBg("white")
#app.setFg("white")
app.setFont(16)

app.addImage("Light","bulb_off.gif")
app.addButtons(["On","Off"],press)
app.addButton("Exit",press)

myBulb1 = createBulb('192.168.1.56','D0:73:D5:03:19:E3')  
myBulb2 = createBulb('192.168.1.156','D0:73:D5:02:39:CB')  
bulbs=[myBulb1, myBulb2]

app.go()

app.warn("App Ended")




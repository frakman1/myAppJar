from appJar import gui
import time



def validate():
    username = app.getEntry("Username")
    password = app.getEntry("Password")
    
    if (username == "frak" and password == "password"):
        app.infoBox("Success", "Valid Password")
        app.setStatusbar("Credentials Accepted")
    else:
        app.errorBox("Error", "Invalid credentials")
        app.setStatusbar("Invalid Credentials. Try Again")
        app.setFocus("Username")


def press(name):
    
    
    print(name, "button pressed")
    #app.setLabel("lbl1","Pressed " + str(count) + " Times")
    
    if (name == "Cancel") :
        app.stop()
    elif (name == "Reset") :
        app.clearEntry("Username")
        app.clearEntry("Password")
        app.setFocus("Username")
    elif (name == "Submit"):
        validate()
        




app = gui("Login")


app.addLabel("lbl1", "Login Window")

app.setBg("green")
app.setFg("white")
app.setFont(16)


#app.addButton("Press Me", press)

app.addLabelEntry("Username")
app.addSecretLabelEntry("Password")
app.addButtons(["Submit","Reset","Cancel"],press)
app.setFocus("Username")
app.addStatusbar()
app.setStatusbar("Enter Credentials")
app.go()

app.warn("App Ended")




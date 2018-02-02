from appJar import gui
import time

count = 5

# define the function blocks
def four():
    print ("You typed four.\n")
    app.setLabelBg("lbl1","blue")

def three():
    print ("You typed three.\n")
    app.setLabelBg("lbl1","green")

def two():
    print ("You typed two.\n")
    app.setLabelBg("lbl1","orange")

def one():
    print ("You typed one.\n")
    app.setLabelBg("lbl1","yellow")

def zero():
    print ("You typed zero.\n")
    app.setLabelBg("lbl1","red")
    
# map the inputs to the function blocks
options = {4 : four,
           3 : three,
           2 : two,
           1 : one,
           0 : zero,
}



def press(name):
    global count
    count -= 1
    print(name, "button pressed")
    app.setLabel("lbl1","Pressed " + str(count) + " Times")
    options[count]()
    if (count == 0) :
        time.sleep(1)
        app.stop()












app = gui("First App")
app.setSize("400x200")
app.setResizable(False)
app.addLabel("lbl1", "Hello World")
app.addLabel("lbl2", "Hello Again")
app.addLabel("lbl3", "Goodbye World")


#app.critical("Hello There")
app.setBg("black")
#app.setFont(20)

app.setLabelBg("lbl1","yellow")
app.setLabelFg("lbl1","red")
app.setLabelBg("lbl2","red")
app.setLabelBg("lbl3","green")

app.addButton("Press Me", press)

app.go()

app.warn("App Ended")




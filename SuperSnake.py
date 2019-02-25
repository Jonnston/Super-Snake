###
#Dominick Johnston
#djohnsto
#Super Snake
#112 Term Project

###
#Code adapted form generic animation code on 112 site



from tkinter import *


# initializes data variable. Model.
def init(data):
    data.rows = 16
    data.cols = 16
    data.cellWidth = data.width/data.cols
    data.cellHeight = data.height/data.rows
    # Snake piece radius. The snake is made of circles, each circle is a 
    # uniform size.
    data.sr = data.cellHeight/2
    data.snake = [[data.sr,data.sr]]
    data.isGameOver = False
    # Direction of movement
    data.dir = 'Down'

def mousePressed(event, data):
    # use event.x and event.y
    pass

# Takes a key input. If it matches one of the four directions, then it sets
# the new direction accordingly and returns true. Otherwise it returns False.
# if we return False, then we continue on in our key press function.
def setDirection(event,data):
    key = event.keysym
    if key == 'Down':
        data.dir = 'Down'
        return True
    elif key == 'Up':
        data.dir = 'Up'
        return True
    elif key == 'Left':
        data.dir = 'Left'
        return True
    elif key == 'Right':
        data.dir = 'Right'
        return True
    return False
    


def keyPressed(event, data):
    if not setDirection(event,data):
        pass

# Moves the snake. Takes the old tail, puts it in front of the current head
# in the direction of motion
def moveSnake(data):
    # Center x and center y of the old head
    oldHeadCX = data.snake[0][0]
    oldHeadCY = data.snake[0][1]
    # Defines center for new head. Use the old center as a basis, then add one
    # square of offset in the correct direction
    newHeadCX = oldHeadCX
    newHeadCY = oldHeadCY
    if data.dir == 'Up':
        newHeadCY -= data.cellHeight
    elif data.dir == 'Down':
        newHeadCY += data.cellHeight
    elif data.dir == 'Left':
        newHeadCX -= data.cellWidth
    elif data.dir == 'Right':
        newHeadCX += data.cellWidth
    oldTail = data.snake.pop()
    oldTail[0] = newHeadCX
    oldTail[1] = newHeadCY
    newHead = oldTail
    data.snake.insert(0,newHead)

def isGameOver(data):
    snakeHead = data.snake[0]
    if not (0 < snakeHead[0] < data.width):
        data.isGameOver = True
    if not (0 < snakeHead[1] < data.height):
        data.isGameOver = True


def timerFired(data):
    # Move the snake
    moveSnake(data)
    # Check if we're out of bounds, set game over if needed.
    isGameOver(data)
    


# Draws the background and the gridlines
def drawBackgound(canvas,data):
    # Draw backgorund
    canvas.create_rectangle(0,0,data.width,data.height,fill='mediumpurple1')
    # Draw lines
    for row in range(1,data.rows):
        x0, x1 = 0, data.width
        y0, y1 = data.cellHeight*row, data.cellHeight*row
        canvas.create_line(x0,y0,x1,y1,fill='gray')
    for col in range(1,data.cols):
        y0, y1 = 0, data.height
        x0, x1 = data.cellHeight*col, data.cellHeight*col
        canvas.create_line(x0,y0,x1,y1,fill='gray')

# Handles all images which appear in the window. View.
def redrawAll(canvas, data):
    drawBackgound(canvas,data)
    # Draw snake
    if not data.isGameOver:
        for segment in data.snake:
            x0, y0 = segment[0] - data.sr, segment[1] - data.sr
            x1, y1 = segment[0] + data.sr, segment[1] + data.sr
            canvas.create_oval(x0,y0,x1,y1,fill='green')
    else:
        x, y = data.width/2, data.height/2
        canvas.create_text(x,y,text='Game over!',font = 'Arial 50')
    

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 200 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 800)
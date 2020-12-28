from tkinter import Tk, Canvas, Label, PhotoImage, Button, Misc, Entry
from time import sleep, time
from random import randint as rand
from re import sub as re_sub, search as re_search
import platform
import winsound

window = Tk()
window.title("T R O N")

# Screen resolution
w = 1920
h = 1080
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2) - (w/2)  # Calculate center
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

if platform.system() == "Windows":
    window.attributes('-fullscreen', True)
elif platform.system() == "Linux":
            window.attributes('-zoomed', True)

# Starting state
player2 = "A I"
gamefiles = []
exitLoop = False
exitLoop2 = False
game = True
loop = True
newGame = False
loadSaved = False
multi = False
sounds = True
fullScreenOn = True

keyUp = "<Up>"
keyDown = "<Down>"
keyLeft = "<Left>"
keyRight = "<Right>"

# Image loading
bike1Right = PhotoImage(file="Images/bikeRight.png").subsample(2, 2)
bike1Left = PhotoImage(file="Images/bikeLeft.png").subsample(2, 2)
bike1Up = PhotoImage(file="Images/bikeUp.png").subsample(2, 2)
bike1Down = PhotoImage(file="Images/bikeDown.png").subsample(2, 2)

explosion13 = PhotoImage(file="Images/explosion1.3.png").subsample(2, 2)
explosion12 = PhotoImage(file="Images/explosion1.2.png").subsample(2, 2)
explosion11 = PhotoImage(file="Images/explosion1.1.png").subsample(2, 2)

explosion23 = PhotoImage(file="Images/explosion2.3.png").subsample(2, 2)
explosion22 = PhotoImage(file="Images/explosion2.2.png").subsample(2, 2)
explosion21 = PhotoImage(file="Images/explosion2.1.png").subsample(2, 2)

bike2Right = PhotoImage(file="Images/bike2Right.png").subsample(2, 2)
bike2Left = PhotoImage(file="Images/bike2Left.png").subsample(2, 2)
bike2Up = PhotoImage(file="Images/bike2Up.png").subsample(2, 2)
bike2Down = PhotoImage(file="Images/bike2Down.png").subsample(2, 2)

wall1 = PhotoImage(file="Images/wall.png").subsample(8, 8)
wall2 = PhotoImage(file="Images/wall2.png").subsample(8, 8)

file = PhotoImage(file="Images/option1.png")
file2 = PhotoImage(file="Images/grid.png")


# Functions
def loadingScreen():
    # Background
    canvas = Canvas(window, width=w, height=h)
    file = PhotoImage(file="Images/loading.png")
    bg_label = Label(window, image=file)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    barBg = Label(window, text=" ", width=138, height=2,
                  bg="#171717", font=("Helvetica 2 bold"))
    barBg.place(x=822, y=620)
    bar = Label(window, text=" ", width=0, height=2,
                bg="#34ebc9", font=("Helvetica 2 bold"))
    bar.place(x=822, y=620)
    canvas.file = file  # Assign it to object or lose bc of garbage collector
    canvas.pack()

    window.update()
    adder = 1
    for i in range(50):
        bar.config(width=adder)
        adder += 2
        sleep(0.04)
        window.update()
    sleep(1)
    for i in range(4):
        bar.config(width=adder)
        adder += 13
        sleep(0.05)
        window.update()
    

def startScreen():
    global canvas, enabled, game, loop, file, sounds
    game = True
    loop = True
    if sounds:
        winsound.PlaySound("Sound/bg.wav", winsound.SND_ASYNC)
    canvas = Canvas(window, width=w, height=h)
    bg_label = Label(window, image=file)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.pack()

    # Buttons
    # Load Game
    btn = Button(window, text="L o a d   G a m e", command=loadGame,
                 width=25, height=2, bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=320)
    # Single Player
    btn = Button(window, text="S i n g l e p l a y e r", command=singlePlayer,
                 width=25, height=2, bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=400)
    # Multiplayer
    btn = Button(window, text="M u l t i p l a y e r", command=multiPlayer,
                 width=25, height=2, bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=480)
    # Settings
    btn = Button(window, text="S e t t i n g s", command=settingsScreen,
                 width=25, height=2, bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=560)
    # Leaderboard
    btn = Button(window, text="L e a d e r b o a r d", command=leaderboard,
                 width=25, height=2, bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=640)
    # Credits
    btn = Button(window, text="C r e d i t s", command=endCredits,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"), pady="5",
                 bd=5, relief="flat")
    btn.place(x=816, y=720)
    # Quit
    btn = Button(window, text="Q u i t", command=closeGame, width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"), pady="5",
                 bd=5, relief="flat")
    btn.place(x=816, y=800)
    # Hack
    btn = Button(window, text="?", command=hackEnable, width=2, height=2,
                 bg="#2794a1", font=("Helvetica 15 bold"), relief="flat")
    btn.place(x=1800, y=900)


def hackEnable():
    global hack, canvas, enabled, sounds
    if hack is True:
        hack = False
        enabledTxt = "Disabled"
        if sounds:
            winsound.PlaySound("Sound/disabled.wav", winsound.SND_ASYNC)
    else:
        hack = True
        enabledTxt = "Enabled"
        if sounds:
            winsound.PlaySound("Sound/hack.wav", winsound.SND_ASYNC)

    enabled = Label(window, text=enabledTxt, bg="black", font=("Helvetica 35"),
                    width=20, height=2, fg="white")
    enabled.place(x=690, y=300)
    window.update()
    sleep(1)  # Display message for 1 second
    enabled.destroy()  # Remove the message from screen
    window.update()
    sleep(2)
    if sounds:
        winsound.PlaySound("Sound/bg.wav", winsound.SND_ASYNC)


def leftKey1(event):
    global direction1, canvas2, bike1, bike1Body, lastMove1
    direction1 = "left"
    canvas2.itemconfig(bike1, image=bike1Left)  # Change the bike direction img
    if lastMove1 == "up":
        # Move bike body to the nose of bike - need to know last move
        canvas2.move(bike1Body, - 30, + 30)
    elif lastMove1 == "down":
        canvas2.move(bike1Body, - 30, - 30)
    else:
        pass
    lastMove1 = "left"


def rightKey1(event):
    global direction1, canvas2, bike1, bike1Body, lastMove1
    direction1 = "right"
    canvas2.itemconfig(bike1, image=bike1Right)
    if lastMove1 == "up":
        canvas2.move(bike1Body, + 30, + 30)
    elif lastMove1 == "down":
        canvas2.move(bike1Body, + 30, - 30)
    else:
        pass
    lastMove1 = "right"


def upKey1(event):
    global direction1, canvas2, bike1, bike1Body, lastMove1
    direction1 = "up"
    canvas2.itemconfig(bike1, image=bike1Up)
    if lastMove1 == "right":
        canvas2.move(bike1Body, - 30, - 30)
    elif lastMove1 == "left":
        canvas2.move(bike1Body, + 30, - 30)
    else:
        pass
    lastMove1 = "up"


def downKey1(event):
    global direction1, canvas2, bike1, bike1Body, lastMove1
    direction1 = "down"
    canvas2.itemconfig(bike1, image=bike1Down)
    if lastMove1 == "right":
        canvas2.move(bike1Body, -30, + 30)
    elif lastMove1 == "left":
        canvas2.move(bike1Body, +30, +30)
    else:
        pass
    lastMove1 = "down"


def leftKey2(event):
    global direction2, canvas2, bike2, bike2Body, lastMove2
    direction2 = "left"
    canvas2.itemconfig(bike2, image=bike2Left)
    if lastMove2 == "up":
        canvas2.move(bike2Body, -30, +30)
    elif lastMove2 == "down":
        canvas2.move(bike2Body, -30, -30)
    else:
        pass
    lastMove2 = "left"


def rightKey2(event):
    global direction2, canvas2, bike2, bike2Body, lastMove2
    direction2 = "right"
    canvas2.itemconfig(bike2, image=bike2Right)
    if lastMove2 == "up":
        canvas2.move(bike2Body, 30, +30)
    elif lastMove2 == "down":
        canvas2.move(bike2Body, 30, -30)
    else:
        pass
    lastMove2 = "right"


def upKey2(event):
    global direction2, canvas2, bike2, bike2Body, lastMove2
    direction2 = "up"
    canvas2.itemconfig(bike2, image=bike2Up)
    if lastMove2 == "left":
        canvas2.move(bike2Body, 30, -30)
    elif lastMove2 == "right":
        canvas2.move(bike2Body, -30, -30)
    else:
        pass
    lastMove2 = "up"


def downKey2(event):
    global direction2, canvas2, bike2, bike2Body, lastMove2
    direction2 = "down"
    canvas2.itemconfig(bike2, image=bike2Down)
    if lastMove2 == "left":
        canvas2.move(bike2Body, 30, 30)
    elif lastMove2 == "right":
        canvas2.move(bike2Body, -30, 30)
    else:
        pass
    lastMove2 = "down"


def overlapping(a, b):
    # if bike body is inside of a wall then return True
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False


# MATCH FUNCTION


def gameArena():
    global file2, direction1, direction2, canvas2, bike1, score1
    global score2, multi, speed, paused, blocks, game, userGame
    global bike2, hack, bike1Body, bike2Body, lastMove1, lastMove2
    global player1, player2, posBike1, posBike2, loadSaved, newGame
    global keyUp, keyDown, keyRight, keyLeft, startTime, endTime, sounds
    paused = False
    direction1 = "right"
    direction2 = "left"
    canvas2 = Canvas(window, width=w, height=h)
    canvas2.pack()
    canvas2.place(x=0, y=0, relwidth=1, relheight=1)
    Misc.lift(canvas2)
    canvas2.create_image(0, 0, anchor="nw", image=file2)

    blocks = []  # List for wall blocks

    # If not in load game then create regular match
    if loadSaved is False:
        bike1 = canvas2.create_image(600, 565, anchor="nw", image=bike1Right)
        bike2 = canvas2.create_image(1200, 565, anchor="nw", image=bike2Left)
        bike1Body = canvas2.create_rectangle(637.5, 602.5, 658.5, 623.5,
                                             fill="", outline="")
        bike2Body = canvas2.create_rectangle(1235.5, 604.5, 1256.5, 625.5,
                                             fill="", outline="")

        # Move body to the nose of bike
        canvas2.move(bike1Body, 30, 0)
        canvas2.lift(bike1Body)
        lastMove1 = "right"
        canvas2.move(bike2Body, -30, 0)
        canvas2.lift(bike2Body)
        lastMove2 = "left"

    if multi is False:
        player2 = "A I"

    # If in load game then get the game data and build
    if loadSaved:
        userSaveFile = open("Game-files/"+userGame)
        dataList = userSaveFile.read().split("\n")

        direction1 = dataList[0]
        direction2 = dataList[1]
        player1 = dataList[2]
        player2 = "A I"

        temp1 = dataList[3]
        tempBike1 = re_sub("[()]", "", temp1)  # Remove brackets
        bike1Coords = tempBike1.split(",")

        temp2 = dataList[4]
        tempBike2 = re_sub("[()]", "", temp2)
        bike2Coords = tempBike2.split(",")

        # The center point of the bike to generate connecting wall
        bike1CentreX = float(bike1Coords[0]) + (float(bike1Coords[2]) -
                                                float(bike1Coords[0])) / 2
        bike1CentreY = float(bike1Coords[1]) + (float(bike1Coords[3]) -
                                                float(bike1Coords[1])) / 2

        bike2CentreX = float(bike2Coords[0]) + (float(bike2Coords[2]) -
                                                float(bike2Coords[0])) / 2
        bike2CentreY = float(bike2Coords[1]) + (float(bike2Coords[3]) -
                                                float(bike2Coords[1])) / 2

        bike1Body = canvas2.create_rectangle(bike1CentreX, bike1CentreY,
                                             bike1CentreX+23, bike1CentreY+23,
                                             fill="", outline="")
        bike2Body = canvas2.create_rectangle(bike2CentreX, bike2CentreY,
                                             bike2CentreX+23, bike2CentreY+23,
                                             fill="", outline="")

        # Which img to use and where to push bike body depends on the direction
        if direction1 == "right":
            bike1 = canvas2.create_image(bike1Coords[0], bike1Coords[1],
                                         anchor="nw", image=bike1Right)
            canvas2.move(bike1Body, 30, 0)
            canvas2.lift(bike1Body)
            lastMove1 = "right"
        elif direction1 == "left":
            bike1 = canvas2.create_image(bike1Coords[0], bike1Coords[1],
                                         anchor="nw", image=bike1Left)
            canvas2.move(bike1Body, -30, 0)
            canvas2.lift(bike1Body)
            lastMove1 = "left"
        elif direction1 == "up":
            bike1 = canvas2.create_image(bike1Coords[0], bike1Coords[1],
                                         anchor="nw", image=bike1Up)
            canvas2.move(bike1Body, 0, -30)
            canvas2.lift(bike1Body)
            lastMove1 = "up"
        else:
            bike1 = canvas2.create_image(bike1Coords[0], bike1Coords[1],
                                         anchor="nw", image=bike1Down)
            canvas2.move(bike1Body, 0, 30)
            canvas2.lift(bike1Body)
            lastMove1 = "down"

        if direction2 == "right":
            bike2 = canvas2.create_image(bike2Coords[0], bike2Coords[1],
                                         anchor="nw", image=bike2Right)
            canvas2.move(bike2Body, 30, 0)
            canvas2.lift(bike2Body)
            lastMove2 = "right"
        elif direction2 == "left":
            bike2 = canvas2.create_image(bike2Coords[0], bike2Coords[1],
                                         anchor="nw", image=bike2Left)
            canvas2.move(bike2Body, -30, 0)
            canvas2.lift(bike2Body)
            lastMove2 = "left"
        elif direction2 == "up":
            bike2 = canvas2.create_image(bike2Coords[0], bike2Coords[1],
                                         anchor="nw", image=bike2Up)
            canvas2.move(bike2Body, 0, -30)
            canvas2.lift(bike2Body)
            lastMove2 = "up"
        else:
            bike2 = canvas2.create_image(bike2Coords[0], bike2Coords[1],
                                         anchor="nw", image=bike2Down)
            canvas2.move(bike2Body, 0, 30)
            canvas2.lift(bike2Body)
            lastMove2 = "down"

        speed = int(dataList[7])

    # Scoreboard text and scores
    txt1 = player1
    canvas2.create_text(600, 60, text=txt1, fill="white",
                        font=("Helvetica 35"))
    txt2 = player2
    canvas2.create_text(1300, 60, text=txt2, fill="white",
                        font=("Helvetica 35"))

    scoreText1 = canvas2.create_text(900, 60, text=str(score1), fill="white",
                                     font=("Helvetica 35"))
    scoreText2 = canvas2.create_text(1023, 60, text=str(score2),
                                     fill="white", font=("Helvetica 35"))

    # Driving Keys
    canvas2.bind(keyLeft, leftKey1)
    canvas2.bind(keyRight, rightKey1)
    canvas2.bind(keyUp, upKey1)
    canvas2.bind(keyDown, downKey1)

    # Useful keys
    canvas2.bind("<Escape>", pause)
    canvas2.bind("<b>", bossKey)

    if multi:  # If multiplayer is enabled assign these keys
        canvas2.bind("<Left>", leftKey2)
        canvas2.bind("<Right>", rightKey2)
        canvas2.bind("<Up>", upKey2)
        canvas2.bind("<Down>", downKey2)

        canvas2.bind("<a>", leftKey1)
        canvas2.bind("<d>", rightKey1)
        canvas2.bind("<w>", upKey1)
        canvas2.bind("<s>", downKey1)

    canvas2.focus_set()  # Focus on keys
    window.update()
    if sounds:
        winsound.PlaySound("Sound/321.wav", winsound.SND_ASYNC)
    sleep(2.5)  # Wait 1 second before the game starts
    if sounds:
        winsound.PlaySound("Sound/bikes.wav", winsound.SND_ASYNC)

    # Variables to add scores later
    add1 = False
    add2 = False

    if paused is False:
        game = True

    if multi is False and loadSaved is False:  # Start stopper in Singleplayer
        startTime = time()

    loadSaved = False  # We do not need to go into loading saved game statement

    # Loop starts
    while game:
        Misc.lift(canvas2)  # Bring canvas to the front
        # bbox finds 4 coordinates of our image canvas.coords finds only 2
        posBike1 = canvas2.bbox(bike1)
        posBike2 = canvas2.bbox(bike2)

        # The center point of the bike to generate wall connecting wall
        bike1CentreX = float(posBike1[0]) + (float(posBike1[2]) -
                                             float(posBike1[0]))/2
        bike1CentreY = posBike1[1] + (posBike1[3]-posBike1[1])/2

        bike2CentreX = float(posBike2[0]) + (float(posBike2[2]) -
                                             float(posBike2[0]))/2
        bike2CentreY = posBike2[1] + (posBike2[3]-posBike2[1])/2

        # Game arena barriers
        if posBike1[0] < 0:
            endTime = startTime
            game = False
            score2 += 1  # Add to bike2 score because bike1 crashed into wall
            canvas2.itemconfig(bike1, image=explosion11)  # Aimation starts
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike1, image=explosion12)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike1, image=explosion13)
            window.update()
            sleep(0.02)
            canvas2.delete(bike1)

        elif posBike2[0] < 0:
            endTime = time()
            game = False
            score1 += 1
            canvas2.itemconfig(bike2, image=explosion21)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike2, image=explosion22)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike2, image=explosion23)
            window.update()
            sleep(0.02)
            canvas2.delete(bike2)

        elif posBike1[1] < 106:
            endTime = startTime
            game = False
            score2 += 1
            canvas2.itemconfig(bike1, image=explosion11)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike1, image=explosion12)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike1, image=explosion13)
            window.update()
            sleep(0.02)
            canvas2.delete(bike1)

        elif posBike2[1] < 106:
            endTime = time()
            game = False
            score1 += 1
            canvas2.itemconfig(bike2, image=explosion21)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike2, image=explosion22)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike2, image=explosion23)
            window.update()
            sleep(0.02)
            canvas2.delete(bike2)

        elif posBike1[2] > 1919:
            endTime = startTime
            game = False
            score2 += 1
            canvas2.itemconfig(bike1, image=explosion11)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike1, image=explosion12)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike1, image=explosion13)
            window.update()
            sleep(0.02)
            canvas2.delete(bike1)

        elif posBike2[2] > 1919:
            endTime = time()
            game = False
            score1 += 1
            canvas2.itemconfig(bike2, image=explosion21)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike2, image=explosion22)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike2, image=explosion23)
            window.update()
            sleep(0.02)
            canvas2.delete(bike2)

        elif posBike1[3] > 1080:
            endTime = startTime
            game = False
            score2 += 1
            canvas2.itemconfig(bike1, image=explosion11)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike1, image=explosion12)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike1, image=explosion13)
            window.update()
            sleep(0.02)
            canvas2.delete(bike1)

        elif posBike2[3] > 1080:
            endTime = time()
            game = False
            score1 += 1
            canvas2.itemconfig(bike2, image=explosion21)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike2, image=explosion22)
            window.update()
            sleep(0.02)
            canvas2.itemconfig(bike2, image=explosion23)
            window.update()
            sleep(0.02)
            canvas2.delete(bike2)

        # BIKE 1 LOGIC

        # Changing direction image and moving it and bike body, generating wall
        if direction1 == "right":
            canvas2.move(bike1, speed, 0)
            canvas2.move(bike1Body, speed, 0)
            blocks.append(canvas2.create_image(bike1CentreX, bike1CentreY,
                                               image=wall1))  # Draws a wall
            canvas2.lift(bike1)  # Bike needs to be over the wall not under
            sleep(0.001)  # Need to wait to move on, game cannot be instant
            window.update()
        elif direction1 == "left":
            canvas2.move(bike1, -speed, 0)
            canvas2.move(bike1Body, -speed, 0)
            blocks.append(canvas2.create_image(bike1CentreX, bike1CentreY,
                                               image=wall1))
            canvas2.lift(bike1)
            sleep(0.001)
            window.update()
        elif direction1 == "up":
            canvas2.move(bike1, 0, -speed)
            canvas2.move(bike1Body, 0, -speed)
            blocks.append(canvas2.create_image(bike1CentreX, bike1CentreY,
                                               image=wall1))
            canvas2.lift(bike1)
            sleep(0.001)
            window.update()
        elif direction1 == "down":
            canvas2.move(bike1, 0, speed)
            canvas2.move(bike1Body, 0, speed)
            blocks.append(canvas2.create_image(bike1CentreX, bike1CentreY,
                                               image=wall1))
            canvas2.lift(bike1)
            sleep(0.001)
            window.update()

        # BIKE 2 LOGIC

        if direction2 == "right":
            canvas2.move(bike2, speed, 0)
            canvas2.move(bike2Body, speed, 0)

            if multi is False:  # If multiplayer, we dont need direction sensor
                # Sensor needs to be ahead of the nose, hence bigger values
                bike2Sensor = canvas2.create_rectangle(bike2CentreX+100,
                                                       bike2CentreY,
                                                       bike2CentreX+108,
                                                       bike2CentreY+8,
                                                       fill="", outline="")

            blocks.append(canvas2.create_image(bike2CentreX, bike2CentreY,
                                               image=wall2))
            canvas2.lift(bike2)
            sleep(0.001)
            window.update()
        elif direction2 == "left":
            canvas2.move(bike2, -speed, 0)
            canvas2.move(bike2Body, -speed, 0)

            if multi is False:
                bike2Sensor = canvas2.create_rectangle(bike2CentreX-100,
                                                       bike2CentreY,
                                                       bike2CentreX-92,
                                                       bike2CentreY+8,
                                                       fill="", outline="")

            blocks.append(canvas2.create_image(bike2CentreX,
                                               bike2CentreY, image=wall2))
            canvas2.lift(bike2)
            sleep(0.001)
            window.update()
        elif direction2 == "up":
            canvas2.move(bike2, 0, -speed)
            canvas2.move(bike2Body, 0, -speed)

            if multi is False:
                bike2Sensor = canvas2.create_rectangle(bike2CentreX,
                                                       bike2CentreY-100,
                                                       bike2CentreX+8,
                                                       bike2CentreY-92,
                                                       fill="", outline="")

            blocks.append(canvas2.create_image(bike2CentreX,
                                               bike2CentreY, image=wall2))
            canvas2.lift(bike2)
            sleep(0.001)
            window.update()
        elif direction2 == "down":
            canvas2.move(bike2, 0, speed)
            canvas2.move(bike2Body, 0, speed)

            if multi is False:
                bike2Sensor = canvas2.create_rectangle(bike2CentreX,
                                                       bike2CentreY+100,
                                                       bike2CentreX+8,
                                                       bike2CentreY+108,
                                                       fill="", outline="")

            blocks.append(canvas2.create_image(bike2CentreX,
                                               bike2CentreY, image=wall2))
            canvas2.lift(bike2)
            sleep(0.001)
            window.update()

        # Bike's physical body position
        posBike1Body = canvas2.bbox(bike1Body)
        posBike2Body = canvas2.bbox(bike2Body)

        if multi is False:  # Get AI bike body position if not in multiplayer
            posBike2Sensor = canvas2.bbox(bike2Sensor)

        for i in range(0, len(blocks)):  # Checking for all blocks
            # If overlaps end
            if hack is False and overlapping(posBike1Body,
                                             canvas2.bbox(blocks[i])):
                endTime = startTime
                game = False  # Exit match loop
                add2 = True  # Since we hit multiple walls, we will add later
                canvas2.itemconfig(bike1, image=explosion11)
                window.update()
                sleep(0.02)
                canvas2.itemconfig(bike1, image=explosion12)
                window.update()
                sleep(0.02)
                canvas2.itemconfig(bike1, image=explosion13)
                window.update()
                sleep(0.02)
                canvas2.delete(bike1)

            if overlapping(posBike2Body, canvas2.bbox(blocks[i])):
                endTime = time()
                game = False
                add1 = True
                canvas2.itemconfig(bike2, image=explosion21)
                window.update()
                sleep(0.02)
                canvas2.itemconfig(bike2, image=explosion22)
                window.update()
                sleep(0.02)
                canvas2.itemconfig(bike2, image=explosion23)
                window.update()
                sleep(0.02)
                canvas2.delete(bike2)

            # Sensor check
            elif multi is False and posBike2Sensor is not None:
                if overlapping(posBike2Sensor, canvas2.bbox(blocks[i])):

                    if direction2 == "right" or direction2 == "left":
                        r = rand(0, 1)  # Choose randomly where to turn
                        if r == 0:
                            upKey2("<Up>")

                        else:
                            downKey2("<Down>")
                        window.update()
                        break

                    elif direction2 == "up" or direction2 == "down":
                        r = rand(0, 1)
                        if r == 0:
                            leftKey2("<Up>")

                        else:
                            rightKey2("<Down>")
                        window.update()
                        break

                # Game arena barriers
                elif posBike2Sensor[0] < 0 or posBike2Sensor[2] > 1919:
                    r = rand(0, 1)
                    if r == 0:
                        upKey2("<Up>")

                    else:
                        downKey2("<Down>")
                    window.update()
                    break
                elif posBike2Sensor[1] < 106 or posBike2Sensor[3] > 1080:
                    r = rand(0, 1)
                    if r == 0:
                        leftKey2("<Up>")

                    else:
                        rightKey2("<Down>")
                    window.update()
                    break

            else:
                continue
    if sounds:
        winsound.PlaySound("Sound/explosion.wav", winsound.SND_ASYNC)
    if add1:
        score1 += 1  # Now we can add

    elif add2:
        score2 += 1

    canvas2.itemconfigure(scoreText1, text=score1)  # Update scoreboard
    canvas2.itemconfigure(scoreText2, text=score2)
    sleep(1)


# MAIN LOOP FUNCTION


def gameLoop():
    global score1, score2, loop, newGame, game, loadGameplay
    global userGame, startTime, endTime, seconds, sounds
    newGame = True
    if sounds:
        winsound.PlaySound("Sound/init.wav", winsound.SND_ASYNC)

    if loadGameplay is False:
        score1 = 0  # Set scores to 0 if we did not load game scores
        score2 = 0

    if newGame:
        loop = True
        score1 = 0
        score2 = 0

    if loadGameplay:
        userSaveFile = open("Game-files/"+userGame)
        dataList = userSaveFile.read().split("\n")
        score1 = int(dataList[5])
        score2 = int(dataList[6])

    startTime = 0
    endTime = 0
    while loop:

        finalTime = endTime - startTime
        # Round final time to 10 decimal places and get seconds
        seconds = round(float(finalTime % 60), 10)
        # Do not bother adding slower than 1.5 second to the list
        if seconds < 1.999 and seconds != 0.000000:
            addLeaderboard()

        if score1 >= 3:  # Game lasts until 3 points
            loop = False
            game = False
            newGame = True
            winner = player1
            if sounds:
                winsound.PlaySound("Sound/you-won.wav", winsound.SND_ASYNC)
        elif score2 >= 3:
            loop = False
            game = False

            winner = player2
        else:
            gameArena()

    # End game menu
    congrats = Label(window, text=winner + " Won!", bg="black",
                     font=("Helvetica 35"),
                     width=20, height=2, fg="white")
    congrats.place(x=700, y=300)
    btn = Button(window, text="R e s t a r t", command=gameLoop,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=806, y=450)
    btn = Button(window, text="Main menu", command=startScreen,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=806, y=550)


def playerName():
    # Input player names menu
    global canvas, player1Box, player2Box, multi, file
    canvas = Canvas(window, width=w, height=h)
    bg_label = Label(window, image=file)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.pack()

    player1Input = Label(window, text="P l a y e r 1   n a m e :",
                         bg="black", font=("Helvetica 15"),
                         width=28, height=2, fg="white")
    player1Input.place(x=806, y=410)

    player1Box = Entry(window, width=16, font=("Helvetica 25"))
    player1Box.place(x=806, y=450)

    if multi:  # We only ask for the second player name if it's multiplayer
        player2Input = Label(window, text="P l a y e r 2   n a m e :",
                             bg="black", font=("Helvetica 15"),
                             width=28, height=2, fg="white")
        player2Input.place(x=806, y=510)

        player2Box = Entry(window, width=16, font=("Helvetica 25"))
        player2Box.place(x=806, y=550)

    btn = Button(window, text="Continue", command=getNames,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=806, y=800)

    btnBack = Button(window, text="Back", command=startScreen,
                     width=10, height=2,
                     bg="#2794a1", font=("Helvetica 15"),
                     pady="5", bd=5, relief="flat")
    btnBack.place(x=400, y=900)
    window.update()


def getNames():
    global player1, player2, player1Box, player2Box, multi
    player1 = str(player1Box.get())
    regex = "[ ,]"
    check1 = re_search(regex, player1)
    check2 = False

    if multi:
        player2 = str(player2Box.get())
        check2 = re_search(regex, player2)

    # Checking inputs

    if len(player1) > 10 or len(player2) > 10:
        wrong = Label(window, text="Too long name", bg="black",
                      font=("Helvetica 15"), width=28,
                      height=2, fg="red")
        wrong.place(x=806, y=300)
        window.update()
        sleep(1.5)
        playerName()

    elif len(player1) == 0 or len(player2) == 0:
        wrong = Label(window, text="Empty name", bg="black",
                      font=("Helvetica 15"), width=28,
                      height=2, fg="red")
        wrong.place(x=806, y=300)
        window.update()
        sleep(1.5)
        playerName()

    elif player1 == player2:
        wrong = Label(window, text="Same names", bg="black",
                      font=("Helvetica 15"), width=28,
                      height=2, fg="red")
        wrong.place(x=806, y=300)
        window.update()
        sleep(1.5)
        playerName()

    elif check1 or check2:
        wrong = Label(window, text="Cannot include space or coma!",
                      bg="black", font=("Helvetica 15"), width=28,
                      height=2, fg="red")
        wrong.place(x=806, y=300)
        window.update()
        sleep(1.5)
        playerName()
    elif "," in player1 or "," in player2:
        wrong = Label(window, text="Cannot include coma!",
                      bg="black", font=("Helvetica 15"), width=28,
                      height=2, fg="red")
        wrong.place(x=806, y=300)
        window.update()
        sleep(1.5)
        playerName()

    else:
        difficulty()  # Go to next menu if everything is okay


def singlePlayer():
    global multi, loadGameplay
    multi = False
    loadGameplay = False
    playerName()


def multiPlayer():
    global multi, loadGameplay
    multi = True
    loadGameplay = False
    playerName()


def difficulty():
    global file
    canvas = Canvas(window, width=w, height=h)
    bg_label = Label(window, image=file)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.file = file
    canvas.pack()

    # Choose difficulty buttons and label
    choose = Label(window, text="Choose difficulty", bg="black",
                   font=("Helvetica 15"), width=28,
                   height=2, fg="white")
    choose.place(x=806, y=310)
    btn = Button(window, text="Easy", command=easy,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=400)
    btn = Button(window, text="Medium", command=medium,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=500)
    btn = Button(window, text="Hard", command=hard,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=600)

    btnBack = Button(window, text="Back", command=playerName,
                     width=10, height=2,
                     bg="#2794a1", font=("Helvetica 15"),
                     pady="5", bd=5, relief="flat")
    btnBack.place(x=400, y=900)


def easy():
    global speed
    speed = 3  # Game difficulty depends on speed
    gameLoop()


def medium():
    global speed
    speed = 5
    gameLoop()


def hard():
    global speed
    speed = 7
    gameLoop()


def pause(event):
    global paused, multi, exitLoop, exitLoop2, loop, game
    paused = True
    exitLoop2 = False  # need this to continue
    pausedTxt = Label(window, text="Paused", bg="black",
                      font=("Helvetica 15"), width=28,
                      height=2, fg="white")
    pausedTxt.place(x=806, y=310)

    if multi is False:  # Cannot save multiplayer game
        btn1 = Button(window, text="Save game", command=saveGame,
                      width=25, height=2,
                      bg="#2794a1", font=("Helvetica 15"),
                      pady="5", bd=5, relief="flat")
        btn1.place(x=816, y=400)

    btn2 = Button(window, text="Main Menu", command=startScreen,
                  width=25, height=2,
                  bg="#2794a1", font=("Helvetica 15"),
                  pady="5", bd=5, relief="flat")
    btn2.place(x=816, y=500)
    btn3 = Button(window, text="Continue", command=continueGame,
                  width=25, height=2,
                  bg="#2794a1", font=("Helvetica 15"),
                  pady="5", bd=5, relief="flat")
    btn3.place(x=816, y=600)

    # Stick in pause loop until it's exited
    while paused:

        if multi is False:
            btn1 = Button(window, text="Save game", command=saveGame,
                          width=25, height=2, bg="#2794a1",
                          font=("Helvetica 15"), pady="5", bd=5,
                          relief="flat")
        btn2 = Button(window, text="Main Menu", command=startMenu,
                      width=25, height=2, bg="#2794a1", font=("Helvetica 15"),
                      pady="5", bd=5, relief="flat")
        btn3 = Button(window, text="Continue", command=continueGame,
                      width=25, height=2, bg="#2794a1", font=("Helvetica 15"),
                      pady="5", bd=5, relief="flat")
        if exitLoop:  # Clicking Main Menu
            paused = False
        elif exitLoop2:  # Clicking Continue
            paused = False
        window.update()

    loop = True
    pausedTxt.destroy()
    window.update()
    if exitLoop:  # needs to be True to get to the start screen
        startScreen()


def continueGame():
    global paused, exitLoop2
    exitLoop2 = True


def saveGame():
    global player1, direction1, direction2, blocksCoordsX
    global blocksCoordsY, posBike1, posBike2
    global score1, score2, gameFiles, blocks2CoordsX, blocks2CoordsY, speed

    # Append to Saved_games file
    gameFiles = open("Saved_games", "a")
    gameFiles.write(player1+",")
    gameFiles.close()

    # Create/overwrite player saved game, 1 saved game per user
    saveFile = open("Game-files/"+player1, "w")
    saveFile.write(direction1 + "\n" + direction2 + "\n" + str(player1) +
                   "\n" + str(posBike1) + "\n" + str(posBike2) + "\n" +
                   str(score1) + "\n" + str(score2) + "\n" + str(speed))
    saveFile.close()

    # Showing to the user that game has been saved
    savedTxt = Label(window, text="Saved", bg="black",
                     font=("Helvetica 15"), width=28,
                     height=2, fg="white")
    savedTxt.place(x=806, y=310)
    window.update()
    sleep(1)
    savedTxt.destroy()

    pause("<Escape>")  # Giving basic event to get back


def startMenu():
    global exitLoop, game, loop, canvas2
    game = False
    loop = False
    exitLoop = True
    canvas2.delete(all)  # We do not need game arena (canvas2) anymore
    canvas2.destroy()


def closeGame():
    global game, loop, exitLoop, sounds
    game = False
    loop = False
    exitLoop = True
    if sounds:
        winsound.PlaySound(None, winsound.SND_NODEFAULT)
    wait = Label(window, text="Please wait! Closing...",
                 bg="black", font=("Helvetica 15"),
                 width=28, height=2, fg="white")
    wait.place(x=806, y=270)
    window.update()
    window.destroy()  # Destroy main window with everything else


def loadGame():
    global canvas, multi, loadGameplay, file
    multi = False
    loadGameplay = True
    canvas = Canvas(window, width=w, height=h)
    bg_label = Label(window, image=file)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.file = file  # Need to assign to object bc of garbage collector
    canvas.pack()

    chooseFile = Label(window, text="Choose file",
                       bg="black", font=("Helvetica 15"),
                       width=28, height=2, fg="white")
    chooseFile.place(x=806, y=310)

    # Open saved games and make button for last 5 of them
    gameFiles = open("Saved_games", "r")

    yAxis = 400
    gameFiles = gameFiles.read().split(",")
    gameFiles.reverse()  # Get the newest, which were appended to the end
    gameFiles = gameFiles[1:6]  # Only 5 saved games to not overfill the screen
    for gameName in gameFiles:
        # lambda i=i: means that only care when button clicked
        btn = Button(window, text=gameName,
                     command=lambda gameName=gameName: openFile(gameName),
                     width=25, height=2,
                     bg="#2794a1", font=("Helvetica 15"),
                     pady="5", bd=5, relief="flat")
        btn.place(x=818, y=yAxis)
        yAxis += 80

    btnBack = Button(window, text="Back", command=startScreen,
                     width=10, height=2,
                     bg="#2794a1", font=("Helvetica 15"),
                     pady="5", bd=5, relief="flat")
    btnBack.place(x=400, y=900)
    window.update()


def openFile(gameName):
    global loadSaved, userGame
    loadSaved = True
    userGame = gameName  # Whose game was loaded
    gameLoop()


def settingsScreen():
    global file
    canvas = Canvas(window, width=w, height=h)
    bg_label = Label(window, image=file)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.pack()

    # Setting buttons
    btn = Button(window, text="Sound", command=soundOn,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=400)

    btn = Button(window, text="Controls", command=controls,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=480)

    btn = Button(window, text="Full Screen Mode", command=fullScreen,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=816, y=560)

    btnBack = Button(window, text="Back", command=startScreen,
                     width=10, height=2,
                     bg="#2794a1", font=("Helvetica 15"),
                     pady="5", bd=5, relief="flat")
    btnBack.place(x=400, y=900)
    window.update()


def controls():
    global file
    canvas = Canvas(window, width=w, height=h)
    bg_label = Label(window, image=file)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.pack()

    global userInputUp, userInputDown, userInputRight, userInputLeft

    infoLabel = Label(window, text="Change controls:",
                      bg="black", font=("Helvetica 14 bold"),
                      width=40, height=3, fg="white")
    infoLabel.place(x=726, y=130)
    infoLabel = Label(window, text="Default buttons are Up, Down, Left, Right",
                      bg="black", font=("Helvetica 14"), width=40,
                      height=3, fg="white")
    infoLabel.place(x=746, y=190)

    # Get user inputs for each turn ( up, down, right, left)
    userInputUpLabel = Label(window, text="Turn up:", bg="black",
                             font=("Helvetica 15"), width=28,
                             height=2, fg="white")
    userInputUpLabel.place(x=806, y=310)
    userInputUp = Entry(window, width=16, font=("Helvetica 25"))
    userInputUp.place(x=816, y=350)

    userInputDownLabel = Label(window, text="Turn down:", bg="black",
                               font=("Helvetica 15"), width=28,
                               height=2, fg="white")
    userInputDownLabel.place(x=806, y=400)
    userInputDown = Entry(window, width=16, font=("Helvetica 25"))
    userInputDown.place(x=816, y=440)

    userInputRightLabel = Label(window, text="Turn right:", bg="black",
                                font=("Helvetica 15"), width=28,
                                height=2, fg="white")
    userInputRightLabel.place(x=806, y=490)
    userInputRight = Entry(window, width=16, font=("Helvetica 25"))
    userInputRight.place(x=816, y=530)

    userInputLeftLabel = Label(window, text="Turn left:", bg="black",
                               font=("Helvetica 15"), width=28,
                               height=2, fg="white")
    userInputLeftLabel.place(x=806, y=580)
    userInputLeft = Entry(window, width=16, font=("Helvetica 25"))
    userInputLeft.place(x=816, y=620)

    # Button to apply changes
    btn = Button(window, text="Apply", command=userInputApply,
                 width=25, height=2,
                 bg="#2794a1", font=("Helvetica 15"),
                 pady="5", bd=5, relief="flat")
    btn.place(x=817, y=730)

    btnBack = Button(window, text="Back", command=settingsScreen,
                     width=10, height=2,
                     bg="#2794a1", font=("Helvetica 15"),
                     pady="5", bd=5, relief="flat")
    btnBack.place(x=420, y=900)
    window.update()


def userInputApply():
    global keyUp, keyDown, keyRight, keyLeft, userInputUp
    global userInputDown, userInputRight, userInputLeft
    # Assign user inputs to variables
    keyUp = str(userInputUp.get())
    keyDown = str(userInputDown.get())
    keyRight = str(userInputRight.get())
    keyLeft = str(userInputLeft.get())

    # Check if inputs allowed
    regex = "^[a-z]$"
    check1 = re_search(regex, keyUp)
    check2 = re_search(regex, keyDown)
    check3 = re_search(regex, keyRight)
    check4 = re_search(regex, keyLeft)

    if (len(keyUp) > 1 or len(keyDown) > 1 or
            len(keyRight) > 1 or len(keyLeft) > 1):
        errorLabel = Label(window, text="Only one key allowed for each!",
                           bg="black", font=("Helvetica 14"), width=40,
                           height=2, fg="red")
        errorLabel.place(x=746, y=100)
        window.update()
        sleep(2)
        errorLabel.destroy()
        controls()

    elif (keyUp == keyDown or keyUp == keyRight or keyUp == keyLeft or
          keyDown == keyRight or keyUp == keyLeft or keyLeft == keyRight):
        errorLabel = Label(window, text="Cannot use the same keys!",
                           bg="black", font=("Helvetica 14"),
                           width=40, height=2, fg="red")
        errorLabel.place(x=746, y=100)
        window.update()
        sleep(2)
        errorLabel.destroy()
        controls()

    elif check1 is None or check2 is None or check3 is None or check4 is None:
        errorLabel = Label(window, text="Capital letters/symbols not allowed!",
                           bg="black", font=("Helvetica 14"),
                           width=40, height=2, fg="red")
        errorLabel.place(x=746, y=100)
        window.update()
        sleep(2)
        errorLabel.destroy()
        controls()

    else:
        # < and > for tkinter to understand these are keys
        keyUp = "<" + keyUp + ">"
        keyDown = "<" + keyDown + ">"
        keyRight = "<" + keyRight + ">"
        keyLeft = "<" + keyLeft + ">"

        successLabel = Label(window, text="Success",
                             bg="black", font=("Helvetica 14"),
                             width=40, height=2, fg="green")
        successLabel.place(x=746, y=100)
        window.update()
        sleep(2)
        successLabel.destroy()
        controls()


def leaderboard():
    global file
    canvas = Canvas(window, width=w, height=h)
    bg_label = Label(window, image=file)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Not assign it to object we will lose all bc of garbage collector
    canvas.file = file
    canvas.pack()

    scoresLabel = Label(window, text="Top 5", bg="black",
                        font=("Helvetica 15 bold"), width=28,
                        height=2, fg="white")
    scoresLabel.place(x=788, y=310)

    leaderboardFile = open("Leaderboard", "r")

    # Get fastest top 5 times with users after sorting the list
    yAxis = 400
    scores = leaderboardFile.read().split(",")
    del scores[-1]  # Last score is empty in file
    # Sort on the basis of the second element which are times
    scores.sort(key=lambda i: i.split()[1])

    for score in scores[0:5]:
        scoreLabel = Label(window, text=score, bg="black",
                           font=("Helvetica 15"), width=28, height=3,
                           fg="white")
        scoreLabel.place(x=806, y=yAxis)
        yAxis += 80

    btnBack = Button(window, text="Back", command=startScreen, width=10,
                     height=2, bg="#2794a1", font=("Helvetica 15"),
                     pady="5", bd=5, relief="flat")
    btnBack.place(x=400, y=900)
    window.update()


def addLeaderboard():
    global seconds, player1
    leaderboardFile = open("Leaderboard", "a")
    leaderboardFile.write(player1 + ": " + str(seconds) + " s,")


def soundOn():
    # This is for windows or for future, modules not allowd rn
    global sounds
    if sounds:
        sounds = False
        enabledTxt = "Disabled"
    else:
        sounds = True
        enabledTxt = "Enabled"
    winsound.PlaySound("Sound/none.wav", winsound.SND_ASYNC)
    enabled = Label(window, text=enabledTxt, bg="black", font=("Helvetica 35"),
                    width=20, height=2, fg="white")
    enabled.place(x=688, y=280)
    window.update()
    sleep(1)
    enabled.destroy()
    window.update()


def endCredits():
    canvas = Canvas(window, bg="black", width=w, height=h)
    canvas.pack()
    blackScreen = Label(window, text="", bg="black", width=1000, height=100)
    blackScreen.place(x=0, y=0)

    window.update()

    # Load Credits from file
    text = open("Credits", "r")
    text = text.read()
    text = Label(window, text=text, bg="black", width=50, height=55,
                 fg="white", font=("Helvetica 15"))
    text.place(x=673, y=800)
    x = 0
    ch = 1000
    # Scrolling credits
    while x < 2100:
        text.place(y=ch)
        x += 1
        ch -= 1
        window.update()
        sleep(0.01)
    startScreen()


def bossKey(event):
    # If b is clicked then Numbers spreadsheet is displayed
    canvas = Canvas(window, bg="black", width=w, height=h)
    file = PhotoImage(file="Images/screenshot.png")
    bg_label = Label(window, image=file)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.pack()
    window.update()
    sleep(5)
    window.destroy()  # After 5 s program crashes, your boss wont see exactly


def fullScreen():
    global fullScreenOn
    if fullScreenOn:
        if platform.system() == "Windows":
            window.attributes('-fullscreen', False)
        elif platform.system() == "Linux":
            window.attributes('-zoomed', True)
        else:
            fullScreenOn = False
    else:
        if platform.system() == "Windows":
            window.attributes('-fullscreen', True)
        elif platform.system() == "Linux":
            window.attributes('-zoomed', True)
        else:
            fullScreenOn = False


hack = False

loadingScreen()

winsound.PlaySound("Sound/Welcome.wav", winsound.SND_ASYNC)
sleep(3)
startScreen()  # Start Main Menu after 1 second
window.mainloop()
winsound.PlaySound("Sound/bg2.wav", winsound.SND_ALIAS)
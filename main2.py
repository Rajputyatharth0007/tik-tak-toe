from tkinter import *
from PIL import Image, ImageTk

def reset():
    start_tic_tac_toe(parent, p1, p2)


def button1():
    
    global b1,choice
    if choice.get()%2 !=0:
        bt1.config(image=circleimgtk)
        bt1.config(state=DISABLED)
        choice.set(choice.get()+1)
        print(choice.get())
        b1 = 0
        

    else:
        bt1.config(image=crossimgtk)
        bt1.config(state=DISABLED)
        choice.set(choice.get()+1)
        print(choice.get())
        b1 = 1
    check_winner()
    return choice

def button2():
    global b2,choice
    if choice.get()%2 !=0:
        bt2.config(image=circleimgtk)
        bt2.config(state=DISABLED)
        choice.set(choice.get()+1)
        b2 = 0

    else:
        bt2.config(image=crossimgtk)
        bt2.config(state=DISABLED)
        choice.set(choice.get()+1)
        b2 = 1
    check_winner()
    return choice

def button3():
    global b3,choice
    if choice.get()%2 !=0:
        bt3.config(image=circleimgtk)
        bt3.config(state=DISABLED)
        choice.set(choice.get()+1)
        b3 = 0

    else:
        bt3.config(image=crossimgtk)
        bt3.config(state=DISABLED)
        choice.set(choice.get()+1)
        b3 = 1
    check_winner()
    return choice

def button4():
    global b4,choice
    if choice.get()%2 !=0:
        bt4.config(image=circleimgtk)
        bt4.config(state=DISABLED)
        choice.set(choice.get()+1)
        b4 = 0

    else:
        bt4.config(image=crossimgtk)
        bt4.config(state=DISABLED)
        choice.set(choice.get()+1)
        b4 = 1
    check_winner()
    return choice

def button5(): 
    global b5,choice
    if choice.get()%2 !=0:
        bt5.config(image=circleimgtk)
        bt5.config(state=DISABLED)
        choice.set(choice.get()+1)
        b5 = 0

    else:
        bt5.config(image=crossimgtk)
        bt5.config(state=DISABLED)
        choice.set(choice.get()+1)
        b5 = 1
    check_winner()
    return choice   

def button6():
    global b6,choice
    if choice.get()%2 !=0:
        bt6.config(image=circleimgtk)
        bt6.config(state=DISABLED)
        choice.set(choice.get()+1)
        b6 = 0 

    else:
        bt6.config(image=crossimgtk)
        bt6.config(state=DISABLED)
        choice.set(choice.get()+1)
        b6 = 1
    check_winner()
    return choice

def button7(): 
    global b7,choice
    if choice.get()%2 !=0:
        bt7.config(image=circleimgtk)
        bt7.config(state=DISABLED)
        choice.set(choice.get()+1)
        b7 = 0

    else:
        bt7.config(image=crossimgtk)
        bt7.config(state=DISABLED)
        choice.set(choice.get()+1)
        b7 = 1
    check_winner()
    return choice

def button8():
    global b8,choice
    if choice.get()%2 !=0:
        bt8.config(image=circleimgtk)
        bt8.config(state=DISABLED)
        choice.set(choice.get()+1)
        b8 = 0

    else:
        bt8.config(image=crossimgtk)
        bt8.config(state=DISABLED)
        choice.set(choice.get()+1)
        b8 = 1
    check_winner()
    return choice

def button9():
    global b9,choice
    if choice.get()%2 !=0:
        bt9.config(image=circleimgtk)
        bt9.config(state=DISABLED)
        choice.set(choice.get()+1)
        b9 = 0


    else:
        bt9.config(image=crossimgtk)
        bt9.config(state=DISABLED)
        choice.set(choice.get()+1)
        b9 = 1

    check_winner()
    return choice

def check_winner():
    if (b1 == b2 == b3 == 0) or (b4 == b5 == b6 == 0) or (b7 == b8 == b9 == 0) or (b1 == b4 == b7 == 0) or (b2 == b5 == b8 == 0) or (b3 == b6 == b9 == 0) or (b1 == b5 == b9 == 0) or (b3 == b5 == b7 == 0):
        lb5.config(text=f"{p1_name} Wins!",fg = "Red")
        lb5.config(bg="lightGreen")
        print("Player1 wins")
        #disable_all()

    elif (b1 == b2 == b3 == 1) or (b4 == b5 == b6 == 1) or (b7 == b8 == b9 == 1) or (b1 == b4 == b7 == 1) or (b2 == b5 == b8 == 1) or (b3 == b6 == b9 == 1) or (b1 == b5 == b9 == 1) or (b3 == b5 == b7 == 1):
        lb5.config(text=f"{p2_name} Wins!")
        lb5.config(bg="lightGreen",fg = "Red")
        print("Player 2 wins")
        #disable_all()

    elif all(bt["state"] == DISABLED for bt in [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]):
        print("It's a tie!")
        lb5.config(text="Game a tie!",bg= "Cyan",fg="Red")
       # disable_all()

#this for main window

def start_tic_tac_toe(parent, p1, p2):
    global choice, b1, b2, b3, b4, b5, b6, b7, b8, b9
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    global circleimgtk, crossimgtk, lb5
    global p1_name, p2_name
    p1_name = p1
    p2_name = p2

    game = Toplevel(parent)
    game.title("Tic Tac Toe Game")
    game.config(bg="light blue")

    Label(
        game,
        text=f"Player 1: {p1} (O)  vs  Player 2: {p2} (X)",
        font=("Arial",14),
        bg="cornsilk",
        fg="grey"
    ).place(x=540,y=120,width=500,height=50)

    
    choice=IntVar()
    choice.set(1)
    b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = -1


    #this is for images
    circleimg = Image.open("circle.png")

    crossimg = Image.open("cross.png")

    circleimgtk = ImageTk.PhotoImage(circleimg)

    crossimgtk = ImageTk.PhotoImage(crossimg)



    #buttons for tic tak tok
    bt1=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button1)
    bt1.place(x=590,y=200,width=130,height=110)

    bt2=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button2)
    bt2.place(x=720,y=200,width=130,height=110)

    bt3=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button3)
    bt3.place(x=855,y=200,width=130,height=110)

    bt4=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button4)
    bt4.place(x=590,y=320,width=130,height=110)   

    bt5=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button5)
    bt5.place(x=720,y=320,width=130,height=110)

    bt6=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",  command=button6)
    bt6.place(x=855,y=320,width=130,height=110)

    bt7=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey", command=button7)
    bt7.place(x=590,y=440,width=130,height=110)

    bt8=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey", command=button8)
    bt8.place(x=720,y=440,width=130,height=110)

    bt9=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey", command=button9)
    bt9.place(x=855,y=440,width=130,height=110)

    #labels for tic tak tok

    lb1=Label(game,text="Tic Tac Tok Game",font=("Bernard MT Condensed",30),bg="Cyan",fg="Red")
    lb1.place(x=580,y=50,width=400,height=50)

    lb2= Label(game,font=("Arial",12),bg="black")
    lb2.place(x=590,y=310,width=395,height=10)

    lb3 = Label(game,font=("Arial",12),bg="black")
    lb3.place(x=590,y=430,width=395,height=10)

    lb4 = Label(game,font=("Arial",12),bg="black")
    lb4.place(x=710,y=200,width=10,height=350)

    lb6 = Label(game,font=("Arial",12),bg="black")
    lb6.place(x=850,y=200,width=10,height=350)

    lb5 = Label(game,font=("Arial",12),bg="light blue")
    lb5.place(x=615,y=650,width=350,height=50)

    rb = Button(game,text="retry",font=("Arial",12),bg="light blue",command=reset)
    rb.place(x=815,y=650,width=80,height=50)


    game.mainloop()

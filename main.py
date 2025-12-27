from tkinter import *
from PIL import Image, ImageTk
import random

def retry():
    global b1, b2, b3, b4, b5, b6, b7, b8, b9
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    global lb5

    b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = -1
    for bt in [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]:
        bt.config(image='', state=NORMAL)
    lb5.config(text="", bg="light blue")


def disable_all():
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    for bt in [bt1,bt2,bt3,bt4,bt5,bt6,bt7,bt8,bt9]:
        bt.config(state=DISABLED)


def player_move(index):
    global b1, b2, b3, b4, b5, b6, b7, b8, b9
    global list_buttons
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9

    if index == 1:
        bt1.config(image=circleimgtk)
        bt1.config(state=DISABLED)
        b1 = 0
        list_buttons.append(1)

    elif index == 2:
        bt2.config(image=circleimgtk)
        bt2.config(state=DISABLED)
        b2 = 0
        list_buttons.append(2)

    elif index == 3:
        bt3.config(image=circleimgtk)
        bt3.config(state=DISABLED)
        b3 = 0
        list_buttons.append(3)

    elif index == 4:
        bt4.config(image=circleimgtk)
        bt4.config(state=DISABLED)
        b4 = 0
        list_buttons.append(4)

    elif index == 5:
        bt5.config(image=circleimgtk)
        bt5.config(state=DISABLED)
        b5 = 0
        list_buttons.append(5)

    elif index == 6:
        bt6.config(image=circleimgtk)
        bt6.config(state=DISABLED)
        b6 = 0
        list_buttons.append(6)

    elif index == 7:
        bt7.config(image=circleimgtk)
        bt7.config(state=DISABLED)
        b7 = 0
        list_buttons.append(7)

    elif index == 8:
        bt8.config(image=circleimgtk)
        bt8.config(state=DISABLED)
        b8 = 0
        list_buttons.append(8)

    elif index == 9:
        bt9.config(image=circleimgtk)
        bt9.config(state=DISABLED)
        b9 = 0
        list_buttons.append(9)

    check_winner()
    random_choice(list_buttons)
    check_winner()
    

def check_winner():
    global b1, b2, b3, b4, b5, b6, b7, b8, b9
    global lb5
    if (b1 == b2 == b3 == 0) or (b4 == b5 == b6 == 0) or (b7 == b8 == b9 == 0) or (b1 == b4 == b7 == 0) or (b2 == b5 == b8 == 0) or (b3 == b6 == b9 == 0) or (b1 == b5 == b9 == 0) or (b3 == b5 == b7 == 0):
        lb5.config(text="Circle Wins!",fg = "Red")
        lb5.config(bg="lightGreen")
        print("Player1 wins")
        disable_all()

    elif (b1 == b2 == b3 == 1) or (b4 == b5 == b6 == 1) or (b7 == b8 == b9 == 1) or (b1 == b4 == b7 == 1) or (b2 == b5 == b8 == 1) or (b3 == b6 == b9 == 1) or (b1 == b5 == b9 == 1) or (b3 == b5 == b7 == 1):
        lb5.config(text="Cross Wins!")
        lb5.config(bg="lightGreen",fg = "Red")
        print("Player2 wins")
        disable_all()

    elif all(bt["state"] == DISABLED for bt in [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]):
        print("It's a tie!")
        lb5.config(text="It's a tie!",bg= "Cyan",fg="Red")
       



def random_choice(list_buttons):
    global b1, b2, b3, b4, b5, b6, b7, b8, b9  
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9
    if len(list_buttons) == 9:
        return  # board is full

    comp_choice = random.randint(1, 9)

    while comp_choice in list_buttons:
        comp_choice = random.randint(1, 9)


    if comp_choice == 1:
        bt1.config(image=crossimgtk)
        bt1.config(state=DISABLED)
        b1 = 1
        list_buttons.append(1)
        
    elif comp_choice == 2:
        bt2.config(image=crossimgtk)
        bt2.config(state=DISABLED)
        b2 = 1
        list_buttons.append(2)
        
    elif comp_choice == 3:
        bt3.config(image=crossimgtk)
        bt3.config(state=DISABLED)
        b3 = 1
        list_buttons.append(3)
        
    elif comp_choice == 4:
        bt4.config(image=crossimgtk)
        bt4.config(state=DISABLED)
        b4 = 1
        list_buttons.append(4)
        
    elif comp_choice == 5:
        bt5.config(image=crossimgtk)
        bt5.config(state=DISABLED)
        b5 = 1
        list_buttons.append(5)
        
    elif comp_choice == 6:
        bt6.config(image=crossimgtk)
        bt6.config(state=DISABLED)
        b6 = 1
        list_buttons.append(6)
        
    elif comp_choice == 7:
        bt7.config(image=crossimgtk)
        bt7.config(state=DISABLED)
        b7 = 1
        list_buttons.append(7)
        
    elif comp_choice == 8:
        bt8.config(image=crossimgtk)
        bt8.config(state=DISABLED)
        b8 = 1
        list_buttons.append(8)
        

    elif comp_choice == 9:
        bt9.config(image=crossimgtk)
        bt9.config(state=DISABLED)
        b9 = 1
        list_buttons.append(9)
        

def start_tic_tac_toe(parent, p1, p2):
    global choice, b1, b2, b3, b4, b5, b6, b7, b8, b9
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9,list_buttons
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

    game.geometry("1400x800")
    b1 = b2 = b3 = b4 = b5 = b6 = b7 = b8 = b9 = -1
    list_buttons = []
    
    #this is for images
    circleimg = Image.open("circle.png")
    crossimg = Image.open("cross.png")

    circleimgtk = ImageTk.PhotoImage(circleimg)
    crossimgtk = ImageTk.PhotoImage(crossimg)


    #buttons for tic tak tok
    bt1=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=lambda:player_move(1))
    bt1.place(x=590,y=200,width=130,height=110)

    bt2=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=lambda:player_move(2))
    bt2.place(x=720,y=200,width=130,height=110)

    bt3=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=lambda:player_move(3))
    bt3.place(x=855,y=200,width=130,height=110)

    bt4=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=lambda:player_move(4))
    bt4.place(x=590,y=320,width=130,height=110)   

    bt5=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=lambda:player_move(5))
    bt5.place(x=720,y=320,width=130,height=110)

    bt6=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=lambda:player_move(6))
    bt6.place(x=855,y=320,width=130,height=110)

    bt7=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey", command=lambda:player_move(7))
    bt7.place(x=590,y=440,width=130,height=110)

    bt8=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey", command=lambda:player_move(8))
    bt8.place(x=720,y=440,width=130,height=110)

    bt9=Button(game,text="",font=("Arial",30),width=6,height=3,bg="Grey", command=lambda:player_move(9))
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

    rb = Button(game, text="Exit Game", font=("Arial", 14), command=game.destroy)
    rb.place(x=1300,y=20,width=80,height=30)

    ng = Button(game, text="New Game", font=("Arial", 14), command=retry)
    ng.place(x=1150,y=20,width=100,height=30)
    
    game.mainloop()
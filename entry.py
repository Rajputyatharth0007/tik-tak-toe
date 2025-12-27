from tkinter import *
import main2,main


def start_game():
    p1 = entry1.get()
    p2 = entry2.get()

    if p1 == "" or p2 == "":
        error_label.config(text="Please enter both names!")
        return

    root.withdraw()   # hide entry window
    main2.start_tic_tac_toe(root, p1, p2)

def start_game2():
    p1 = entry1.get()
    p2 = "Computer"

    if p1 == "":
        error_label.config(text="Please enter your name!")
        return

    root.withdraw()   # hide entry window
    main.start_tic_tac_toe(root, p1, p2)

def singleplayer():
    global entry1
    lb1=Label(root, text="Player 1 name:", font=("Arial", 20),bg="lightgreen",fg="red")
    lb1.place(x=130,y=220,width=250,height=40)

    entry1 = Entry(root, font=("Arial", 20))
    entry1.place(x=130,y=270,width=250,height=30) 

    
    start_button = Button(root, text="Start Game", font=("Arial", 14), command=start_game2)
    start_button.place(x=150,y=410,width=200,height=40)


def two_player():
    global entry1, entry2
    lb1=Label(root, text="Player 1 name:", font=("Arial", 20),bg="lightgreen",fg="red")
    lb1.place(x=130,y=220,width=250,height=40)

    entry1 = Entry(root, font=("Arial", 20))
    entry1.place(x=130,y=270,width=250,height=30)
    

    lb2=Label(root, text="Player 2 name:", font=("Arial", 20),bg="lightgreen",fg="red")
    lb2.place(x=130,y=310,width=250,height=40)

    entry2 = Entry(root, font=("Arial", 20 ))
    entry2.place(x=130,y=370,width=250,height=30)

    
    start_button = Button(root, text="Start Game", font=("Arial", 14), command=start_game)
    start_button.place(x=150,y=410,width=200,height=40)


root = Tk()
root.title("Tic Tac Toe - Entry")
root.geometry("500x500")
root.config(bg="lightblue")
label = Label(root, text="Welcome to Tic Tac Toe Game!", font=("Arial", 20),bg="cyan",fg="red")
label.place(x=50,y=40,width=430,height=40)


lb3 = Label(root, text="Choose game mode", font=("Arial", 20),bg="Green",fg="red")
lb3.place(x=90,y=100,width=350,height=40)

bt1 = Button(root, text="Single Player", font=("Arial", 18),command=singleplayer)
bt1.place(x=100,y=160,width=150,height=40)

bt2 = Button(root, text="Two Player", font=("Arial", 18),command=two_player)
bt2.place(x=270,y=160,width=150,height=40)



root.mainloop()
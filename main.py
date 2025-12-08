from tkinter import *
from PIL import Image, ImageTk
import random


def button1():
    
    if choice.get()%2 ==0:
        bt1.config(image=circleimgtk)
        bt1.config(state=DISABLED)
        choice.set(choice.get()+1)
        print(choice.get())
        

    else:
        bt1.config(image=crossimgtk)
        bt1.config(state=DISABLED)
        choice.set(choice.get()+1)
        print(choice.get())
    check_winner()
    return choice

def button2():
    
    if choice.get()%2 ==0:
        bt2.config(image=circleimgtk)
        bt2.config(state=DISABLED)
        choice.set(choice.get()+1)

    else:
        bt2.config(image=crossimgtk)
        bt2.config(state=DISABLED)
        choice.set(choice.get()+1)
    check_winner()
    return choice

def button3():
    
    if choice.get()%2 ==0:
        bt3.config(image=circleimgtk)
        bt3.config(state=DISABLED)
        choice.set(choice.get()+1)

    else:
        bt3.config(image=crossimgtk)
        bt3.config(state=DISABLED)
        choice.set(choice.get()+1)
    check_winner()
    return choice

def button4():
    if choice.get()%2 ==0:
        bt4.config(image=circleimgtk)
        bt4.config(state=DISABLED)
        choice.set(choice.get()+1)

    else:
        bt4.config(image=crossimgtk)
        bt4.config(state=DISABLED)
        choice.set(choice.get()+1)
    check_winner()
    return choice

def button5(): 
    if choice.get()%2 ==0:
        bt5.config(image=circleimgtk)
        bt5.config(state=DISABLED)
        choice.set(choice.get()+1)

    else:
        bt5.config(image=crossimgtk)
        bt5.config(state=DISABLED)
        choice.set(choice.get()+1)
    check_winner()
    return choice   

def button6():
    if choice.get()%2 ==0:
        bt6.config(image=circleimgtk)
        bt6.config(state=DISABLED)
        choice.set(choice.get()+1)

    else:
        bt6.config(image=crossimgtk)
        bt6.config(state=DISABLED)
        choice.set(choice.get()+1)
    check_winner()
    return choice

def button7(): 
    if choice.get()%2 ==0:
        bt7.config(image=circleimgtk)
        bt7.config(state=DISABLED)
        choice.set(choice.get()+1)

    else:
        bt7.config(image=crossimgtk)
        bt7.config(state=DISABLED)
        choice.set(choice.get()+1)
    check_winner()
    return choice

def button8():
    if choice.get()%2 ==0:
        bt8.config(image=circleimgtk)
        bt8.config(state=DISABLED)
        choice.set(choice.get()+1)

    else:
        bt8.config(image=crossimgtk)
        bt8.config(state=DISABLED)
        choice.set(choice.get()+1)
    check_winner()
    return choice

def button9():
    if choice.get()%2 ==0:
        bt9.config(image=circleimgtk)
        bt9.config(state=DISABLED)
        choice.set(choice.get()+1)

    else:
        bt9.config(image=crossimgtk)
        bt9.config(state=DISABLED)
        choice.set(choice.get()+1)
    check_winner()
    return choice

def check_winner():

    if (bt1["image"] == bt2["image"] == bt3["image"] != "") or \
    (bt4["image"] == bt5["image"] == bt6["image"] != "") or \
    (bt7["image"] == bt8["image"] == bt9["image"] != "") or \
    (bt1["image"] == bt4["image"] == bt7["image"] != "") or \
    (bt2["image"] == bt5["image"] == bt8["image"] != "") or \
    (bt3["image"] == bt6["image"] == bt9["image"] != "") or \
    (bt1["image"] == bt5["image"] == bt9["image"] != "") or \
    (bt3["image"] == bt5["image"] == bt7["image"] != ""):
        print("We have a winner!")
        lb6.config(text="We have a winner!")

    elif all(bt["state"] == DISABLED for bt in [bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9]):
        print("It's a tie!")
        lb6.config(text="It's a tie!")


'''
def random_choice(x):
    comp_choice = random.randint(1, 9)

    if comp_choice == x:
        bt2.config(image=crossimgtk)
    else:
        bt3.config(image=crossimgtk)'''

#this for main window
root = Tk()
root.geometry("400x400")
root.title("Tic Tac Tok Game")
root.minsize(400,400)
root.config(bg="lightblue")

choice=IntVar()
choice.set(1)
#this is for images
circleimg = Image.open("circle.png")
crossimg = Image.open("cross.png")

circleimgtk = ImageTk.PhotoImage(circleimg)
crossimgtk = ImageTk.PhotoImage(crossimg)


#buttons for tic tak tok
bt1=Button(root,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button1)
bt1.place(x=650,y=150,width=85,height=85)

bt2=Button(root,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button2)
bt2.place(x=745,y=150,width=90,height=85)

bt3=Button(root,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button3)
bt3.place(x=845,y=150,width=85,height=85)

bt4=Button(root,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button4)
bt4.place(x=650,y=245,width=90,height=90)   

bt5=Button(root,text="",font=("Arial",30),width=6,height=3,bg="Grey",command=button5)
bt5.place(x=745,y=245,width=90,height=90)

bt6=Button(root,text="",font=("Arial",30),width=6,height=3,bg="Grey",  command=button6)
bt6.place(x=845,y=245,width=85,height=90)

bt7=Button(root,text="",font=("Arial",30),width=6,height=3,bg="Grey", command=button7)
bt7.place(x=650,y=345,width=85,height=85)

bt8=Button(root,text="",font=("Arial",30),width=6,height=3,bg="Grey", command=button8)
bt8.place(x=745,y=345,width=90,height=85)

bt9=Button(root,text="",font=("Arial",30),width=6,height=3,bg="Grey", command=button9)
bt9.place(x=845,y=345,width=85,height=85)

#labels for tic tak tok

lb1=Label(root,text="Tic Tac Tok Game",font=("Bernard MT Condensed",30),bg="Cyan",fg="Red")
lb1.place(x=650,y=50,width=300,height=50)

lb2= Label(root,font=("Arial",12),bg="black")
lb2.place(x=650,y=235,width=280,height=10)

lb3 = Label(root,font=("Arial",12),bg="black")
lb3.place(x=650,y=335,width=280,height=10)

lb4 = Label(root,font=("Arial",12),bg="black")
lb4.place(x=735,y=150,width=10,height=280)

lb5 = Label(root,font=("Arial",12),bg="black")
lb5.place(x=835,y=150,width=10,height=280)

lb6 = Label(root,font=("Arial",12),bg="lightblue")
lb6.place(x=650,y=450,width=150,height=40)

root.mainloop()
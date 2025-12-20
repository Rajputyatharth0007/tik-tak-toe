from tkinter import *
import main2

root = Tk()
root.title("Tic Tac Toe - Entry")
root.config(bg="lightblue")
label = Label(root, text="Welcome to Tic Tac Toe Game!", font=("Arial", 16),bg="cyan",fg="red")
label.pack(pady=20)
def start_game():
    p1 = entry1.get()
    p2 = entry2.get()

    if p1 == "" or p2 == "":
        error_label.config(text="Please enter both names!")
        return

    root.withdraw()   # hide entry window
    main2.start_tic_tac_toe(root, p1, p2)


lb1=Label(root, text="Player 1 name:", font=("Arial", 12),bg="lightgreen",fg="pink")
lb1.pack(pady=5)

entry1 = Entry(root, font=("Arial", 12))
entry1.pack(pady=5)
print(entry1.get())

lb2=Label(root, text="Player 2 name:", font=("Arial", 12),bg="lightgreen",fg="pink" )
lb2.pack(pady=5)

entry2 = Entry(root, font=("Arial", 12))
entry2.pack(pady=5)

start_button = Button(root, text="Start Game", font=("Arial", 14), command=start_game)
start_button.pack(pady=10)



root.mainloop()
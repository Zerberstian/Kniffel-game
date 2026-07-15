import tkinter 

root = tkinter.Tk()

root.title("Kniffel Game")

root.geometry("1000x600")  # Set the window size 
placeholder_Zettel = tkinter.Frame(root, width=400, height=600)
placeholder_Zettel.configure(bg="lightgray")  # Set the background color of the frame
placeholder_Zettel.place(x=600, y=0)  # Position the frame at the top-left corner

placeholder_regeln = tkinter.Frame(root, width=600, height=300)
placeholder_regeln.configure(bg="lightblue")  # Set the background color of the frame
placeholder_regeln.place(x=0, y=300)  # Position the frame at the top-left corner

placeholder_spielbereich = tkinter.Frame(root, width=600, height=300)
placeholder_spielbereich.configure(bg="lightyellow")  # Set the background color of the frame
placeholder_spielbereich.place(x=0, y=0)  # Position the frame at the top-left corner

placeholder_reroll_btw = tkinter.Frame(root, width=80, height=40)
placeholder_reroll_btw.configure(bg="lightgreen")  # Set the background color of the frame
placeholder_reroll_btw.place(x=520, y=260)  # Position the frame at the top-left corner

with open("Kniffel-game/src/kniffel/gui/regeln.txt", "r") as file:
    rules_text = file.read()

text_widget = tkinter.Text(placeholder_regeln, width=70, height=15)
text_widget.pack()
text_widget.insert(tkinter.END, rules_text)

root.mainloop()
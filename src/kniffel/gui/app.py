import tkinter as tk

root = tk.Tk()

root.title("Kniffel Game")

root.geometry("1000x600")  # Set the window size 
placeholder_Zettel = tk.Frame(root)
placeholder_Zettel.configure(bg="lightgray")  # Set the background color of the frame
placeholder_Zettel.grid(sticky="nsew")  # Position the frame at the top-left corner

"""
placeholder_regeln = tk.Frame(root, width=600, height=300)
placeholder_regeln.configure(bg="lightblue")  # Set the background color of the frame
placeholder_regeln.place(x=0, y=300)  # Position the frame at the top-left corner
"""

placeholder_spielbereich = tk.Frame(root)
placeholder_spielbereich.configure(bg="lightyellow")  # Set the background color of the frame
placeholder_spielbereich.grid(column=0, row=0, rowspan=5, sticky="nsew") # Position the frame at the top-left corner

"""
placeholder_reroll_btw = tk.Frame(root, width=80, height=40)
placeholder_reroll_btw.configure(bg="lightgreen")  # Set the background color of the frame
placeholder_reroll_btw.place(x=520, y=260)  # Position the frame at the top-left corner
"""

with open("Kniffel-game/src/kniffel/gui/regeln.txt", "r", encoding="utf-8") as file:
    rules_text = file.read()

text_widget = tk.Text(root)
text_widget.grid(column=0, row=5, sticky="nsew")
text_widget.insert(tk.END, rules_text)



root.mainloop()
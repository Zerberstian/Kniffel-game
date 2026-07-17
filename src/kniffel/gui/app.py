import tkinter as tk
    
with open("Kniffel-game/src/kniffel/gui/regeln.txt", "r", encoding="utf-8") as file:
    rules_text = file.read()

root = tk.Tk()
root.title("Kniffel Game")
root.maxsize(width=1920, height=1080)       # 1920x1080
root.minsize(width=900, height=600)         # 900x600
root.geometry("1600x900")                   # Set the window size 

# Weight of the Root-grid
root.grid_columnconfigure(0, weight=1)      
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=4)

placeholder_Zettel = tk.Frame(root)
placeholder_Zettel.configure(bg="lightgray")  # Set the background color of the frame
placeholder_Zettel.grid(row=0 ,column=1, rowspan=2, sticky="nsew")  # Position the frame at the top-left corner

placeholder_Zettel.grid_columnconfigure(0, weight=1)
placeholder_Zettel.grid_columnconfigure(1, weight=1)

Einer_Label = tk.Label(placeholder_Zettel, text="Einer").grid(row=0, column=0, sticky="nsew")
Einer_Button = tk.Button(placeholder_Zettel, text=" ", command=lambda:print("einer")).grid(row=0, column=1, sticky="nsew")

Zweier_Label = tk.Label(placeholder_Zettel, text="zweier").grid(row=1, column=0, sticky="nsew")
Zweier_Button = tk.Button(placeholder_Zettel, text=" ", command=lambda:print("zweier")).grid(row=1, column=1, sticky="nsew")

Dreier_Label = tk.Label(placeholder_Zettel, text="dreier").grid(row=2, column=0, sticky="nsew")
Dreier_Button = tk.Button(placeholder_Zettel, text=" ", command=lambda:print("dreier")).grid(row=2, column=1, sticky="nsew")

Vierer_Label= tk.Label(placeholder_Zettel, text="vierer").grid(row=3, column=0, sticky="nsew")
Vierer_Button = tk.Button(placeholder_Zettel, text=" ", command=lambda:print("vierer")).grid(row=3, column=1, sticky="nsew")

Fünfer_Label= tk.Label(placeholder_Zettel, text="fünfer").grid(row=4, column=0, sticky="nsew")
Fünfer_Button = tk.Button(placeholder_Zettel, text=" ", command=lambda:print("Fünfer")).grid(row=4, column=1, sticky="nsew")


Sechser_Label= tk.Label(placeholder_Zettel, text="sechser").grid(row=5, column=0, sticky="nsew")
Sechser_Button = tk.Button(placeholder_Zettel, text=" ", command=lambda:print("sechser")).grid(row=5, column=1, sticky="nsew")

Bonus_Oben_Label= tk.Label(placeholder_Zettel, text="Bonus Oben").grid(row=6, column=0, sticky="nsew")
Bonus_Oben_Anzeige_Label = tk.Label(placeholder_Zettel, text=" ").grid(row=6, column=1, sticky="nsew")



placeholder_spielbereich = tk.Frame(root)
placeholder_spielbereich.configure(bg="lightyellow")  # Set the background color of the frame
placeholder_spielbereich.grid(column=0, row=0, sticky="nsew") # Position the frame at the top-left corner

btn1 = tk.Button(placeholder_spielbereich, text=f"")
btn1.grid(column=0, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn1.configure(bg= "#f34b4b")

btn2 = tk.Button(placeholder_spielbereich, text=f"")
btn2.grid(column=1, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn2.configure(bg= "#f34b4b")

btn3 = tk.Button(placeholder_spielbereich, text=f"")
btn3.grid(column=2, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn3.configure(bg= "#f34b4b")

btn4 = tk.Button(placeholder_spielbereich, text=f"")
btn4.grid(column=3, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn4.configure(bg="#f34b4b")

btn5 = tk.Button(placeholder_spielbereich, text=f"")
btn5.grid(column=4, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn5.configure(bg= "#f34b4b")

placeholder_spielbereich.grid_columnconfigure(0, weight=1)
placeholder_spielbereich.grid_columnconfigure(1, weight=1)
placeholder_spielbereich.grid_columnconfigure(2, weight=1)
placeholder_spielbereich.grid_columnconfigure(3, weight=1)
placeholder_spielbereich.grid_columnconfigure(4, weight=1)
placeholder_spielbereich.grid_rowconfigure(0, weight=1)

"""
placeholder_reroll_btw = tk.Frame(root, width=80, height=40)
placeholder_reroll_btw.configure(bg="lightgreen")  # Set the background color of the frame
placeholder_reroll_btw.place(x=520, y=260)  # Position the frame at the top-left corner
"""

text_widget = tk.Text(root)
text_widget.grid(column=0, row=1, sticky="nsew")
text_widget.insert(tk.END, rules_text)

root.mainloop()
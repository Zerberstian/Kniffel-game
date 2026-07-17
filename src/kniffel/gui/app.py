import tkinter as tk
from Scorecard_view import ScoreFrame
from typing import List

Label_Names  =  ["Einer:", 
                "Zweier:",
                "Dreier:", 
                "Vierer:", 
                "Fünfer:", 
                "Sechser:", 
                "Bonus Oben:",
                "Dreierpasch:",
                "Viererpasch:",
                "Full House:",
                "Kleine Straße:",
                "Große Straße:",
                "Kniffel:",
                "Chance:",
                "Bonus Unten:",
                "Ergebnis:"]

NUMBER_OF_CATEGORIES = 16
FONTSTYLE = "Times New Roman"
FONTSIZE = 20

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

placeholder_spielbereich = tk.Frame(root)
placeholder_spielbereich.configure(bg="lightyellow")  # Set the background color of the frame
placeholder_spielbereich.grid(column=0, row=0, sticky="nsew") # Position the frame at the top-left corner

btnList = []

btn1 = tk.Button(placeholder_spielbereich)
btn1.grid(column=0, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn1.configure(bg= "#f34b4b", text=f"")
btnList.append(btn1)

btn2 = tk.Button(placeholder_spielbereich)
btn2.grid(column=1, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn2.configure(bg= "#f34b4b", text=f"")
btnList.append(btn2)

btn3 = tk.Button(placeholder_spielbereich)
btn3.grid(column=2, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn3.configure(bg= "#f34b4b", text=f"")
btnList.append(btn3)

btn4 = tk.Button(placeholder_spielbereich)
btn4.grid(column=3, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn4.configure(bg="#f34b4b", text=f"")
btnList.append(btn4)

btn5 = tk.Button(placeholder_spielbereich)
btn5.grid(column=4, row=0, ipadx=20, ipady=10)#, sticky="nsew")
btn5.configure(bg= "#f34b4b", text=f"")
btnList.append(btn5)

btn6 = tk.Button(placeholder_spielbereich)
btn6.grid(column=5, row=1, ipadx=10, ipady=10)#, sticky="nsew")
btn6.configure(bg= "#5cee74", fg="#e92e2e", text=f"roll", font=(FONTSTYLE, FONTSIZE))

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


CreatedFrames: List[tk.Frame] = [] 

for i in range(NUMBER_OF_CATEGORIES):
    frame = ScoreFrame(placeholder_Zettel, i)
    frame.pack(side="top", fill="both")#, expand=True)
    CreatedFrames.append(frame)
        

root.mainloop()
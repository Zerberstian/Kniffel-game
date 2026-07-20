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
FONTSIZESMOL = 16
DICE_IPADX = 30
DICE_IPADY = 20
DICE_BG = "#ffffff"

with open("Kniffel-game/src/kniffel/gui/regeln.txt", "r", encoding="utf-8") as file:
    rules_text = file.read()

root = tk.Tk()
root.title("Kniffel Game")
root.maxsize(width=1920, height=1080)       # 1920x1080
root.minsize(width=900, height=600)         # 900x600
root.geometry("1600x900")                   # Set the window size 
root.configure(bg="green")

# Weight of the Root-grid
root.grid_columnconfigure(0, weight=1)      
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=2)
root.grid_rowconfigure(1, weight=2)

Scorecard_Area = tk.Frame(root)
Scorecard_Area.configure(bg="lightgray")  # Set the background color of the frame
Scorecard_Area.grid(row=0 ,column=1, rowspan=2, sticky="nsew")  # Position the frame at the top-left corner

Scorecard_Area.grid_columnconfigure(0, weight=1)
Scorecard_Area.grid_columnconfigure(1, weight=1)

Dice_Playarea = tk.Frame(root)
Dice_Playarea.configure(bg="#499240")  # Set the background color of the frame
Dice_Playarea.grid(column=0, row=0, sticky="nsew") # Position the frame at the top-left corner

Dice_Playarea.grid_rowconfigure(0, minsize=200)

Dice_Button_List = []



GUI_Dice_1 = tk.Button(Dice_Playarea)
GUI_Dice_1.grid(column=0, row=0, ipadx=DICE_IPADX, ipady=DICE_IPADY)#, sticky="nsew")
GUI_Dice_1.configure(bg= DICE_BG, text=f"")
Dice_Button_List.append(GUI_Dice_1)

GUI_Dice_2 = tk.Button(Dice_Playarea)
GUI_Dice_2.grid(column=1, row=0, ipadx=DICE_IPADX, ipady=DICE_IPADY)#, sticky="nsew")
GUI_Dice_2.configure(bg= DICE_BG, text=f"")
Dice_Button_List.append(GUI_Dice_2)

GUI_Dice_3 = tk.Button(Dice_Playarea)
GUI_Dice_3.grid(column=2, row=0, ipadx=DICE_IPADX, ipady=DICE_IPADY)#, sticky="nsew")
GUI_Dice_3.configure(bg= DICE_BG, text=f"")
Dice_Button_List.append(GUI_Dice_3)

GUI_Dice_4 = tk.Button(Dice_Playarea)
GUI_Dice_4.grid(column=3, row=0, ipadx=DICE_IPADX, ipady=DICE_IPADY)#, sticky="nsew")
GUI_Dice_4.configure(bg=DICE_BG, text=f"")
Dice_Button_List.append(GUI_Dice_4)

GUI_Dice_5 = tk.Button(Dice_Playarea)
GUI_Dice_5.grid(column=4, row=0, ipadx=DICE_IPADX, ipady=DICE_IPADY)#, sticky="nsew")
GUI_Dice_5.configure(bg= DICE_BG, text=f"")
Dice_Button_List.append(GUI_Dice_5)

Reroll_Button = tk.Button(Dice_Playarea)
Reroll_Button.grid(column=5, row=1, ipadx=10, ipady=10)#, sticky="nsew")
Reroll_Button.configure(bg= DICE_BG, text=f"roll", font=(FONTSTYLE, FONTSIZE))

Dice_Playarea.grid_columnconfigure(0, weight=1)
Dice_Playarea.grid_columnconfigure(1, weight=1)
Dice_Playarea.grid_columnconfigure(2, weight=1)
Dice_Playarea.grid_columnconfigure(3, weight=1)
Dice_Playarea.grid_columnconfigure(4, weight=1)
Dice_Playarea.grid_rowconfigure(0, weight=2)


Rule_Widget = tk.Text(root)
Rule_Widget.grid(column=0, row=1, sticky="nsew")
Rule_Widget.configure(font=(FONTSTYLE, FONTSIZESMOL))
Rule_Widget.insert(tk.END, rules_text)


CreatedFrames: List[tk.Frame] = [] 

for i in range(NUMBER_OF_CATEGORIES):
    score_Sub_Frames = ScoreFrame(Scorecard_Area, i)
    score_Sub_Frames.pack(side="top", fill="both", expand=True)
    score_Sub_Frames.configure(bg="#c46464")
    CreatedFrames.append(score_Sub_Frames)
        

root.mainloop()
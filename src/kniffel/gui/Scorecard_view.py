import tkinter as tk
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

class ScoreFrame(tk.Frame): 
    def __init__(self, master: tk.Frame, i):
        super().__init__(master)

        self.master = master

        self.CategoryLabel = None
        self.CategoryButton = None
        self.index = i

        self.createLabel()
        self.createButton()


    def createLabel(self):
        self.CategoryLabel = tk.Label(self)
        self.CategoryLabel.configure(text = Label_Names[self.index], font=(FONTSTYLE, FONTSIZE))
        self.CategoryLabel.grid(row=0, column=0)
        

#  Placeholder aktuell für Buttons
    def createButton(self):
        self.CategoryButton = tk.Button(self)
        self.CategoryButton.configure(text = "")
        self.CategoryButton.grid(row=0, column=1)
        
    

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")

    frame1 = tk.Frame(root)
    frame1.configure(bg="#e62929")
    frame1.pack(fill="both", expand=True)

    CreatedFrames: List[tk.Frame] = [] 

    for i in range(NUMBER_OF_CATEGORIES):
        frame = ScoreFrame(frame1, i)
        frame.pack(side="top")#, fill="both")#, expand=True)
        CreatedFrames.append(frame)
        


    print(CreatedFrames)

    root.mainloop()
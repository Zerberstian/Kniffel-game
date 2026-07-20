import tkinter as tk
from typing import List

Score_Lable_name_List  =  ["Einer:", 
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

'''Constants for the File'''
NUMBER_OF_CATEGORIES = 16
FONTSTYLE = "Times New Roman"
FONTSIZE = 20
FONTSIZESMOL = 16
DICE_IPADX = 30
DICE_IPADY = 20
DICE_BG = "#ffffff"

'''Class with function call in init to use function on object creation'''
class ScoreFrame(tk.Frame): 
    def __init__(self, master: tk.Frame, i):
        super().__init__(master)

        self.master = master

        self.CategoryLabel = None
        self.CategoryButton = None
        self.index = i

        self.createLabel()
        self.createButton()

    '''creates Label for each Category in Score_Lable_name_List'''
    def createLabel(self):
        self.CategoryLabel = tk.Label(self)
        self.CategoryLabel.configure(text = Score_Lable_name_List[self.index], font=(FONTSTYLE, FONTSIZE), bg=DICE_BG)    # The Label has the same bg color as the Bottons
        self.CategoryLabel.grid(row=0, column=0, sticky="nsew")
        

    '''creates a empty Button for each Category'''
    def createButton(self):
        self.CategoryButton = tk.Button(self)
        self.CategoryButton.configure(text = "", font=(FONTSTYLE, FONTSIZE), bg=DICE_BG)
        self.CategoryButton.grid(row=0, column=1, sticky="nsew")
        
    

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")

    Master_Frame_Scorecard = tk.Frame(root)
    Master_Frame_Scorecard.configure(bg="#e62929")
    Master_Frame_Scorecard.pack(fill="both", expand=True)

    CreatedFrames: List[tk.Frame] = [] 

    for i in range(NUMBER_OF_CATEGORIES):
        score_Sub_Frames = ScoreFrame(Master_Frame_Scorecard, i)
        score_Sub_Frames.pack(side="top")#, fill="both")#, expand=True)
        CreatedFrames.append(score_Sub_Frames)
        


    print(CreatedFrames)

    root.mainloop()
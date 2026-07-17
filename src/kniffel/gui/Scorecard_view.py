import tkinter as tk
from typing import List

NUMBER_OF_CATEGORIES = 16


class ScoreFame(tk.Frame): 
    def __init__(self, master: tk.Frame):

        self.master = master
        #self.CreatedFrames: List[tk.Frame] = [] 
        super().__init__(master)


    def createLabel():
        pass

    def createButton():
        pass
    

if __name__ == "__main__":
    root = tk.Tk()

    frame1 = tk.Frame(root)
    frame1.configure(bg="#e62929")
    frame1.pack(fill="both", expand=True)

    CreatedFrames: List[tk.Frame] = [] 

    for i in range(NUMBER_OF_CATEGORIES):
        frame = ScoreFame(frame1)
        frame.pack(side="top")
        CreatedFrames.append(frame)
        print(i)


    #scoreframe = ScoreFame(frame1).pack()

    print(CreatedFrames)

    root.mainloop()
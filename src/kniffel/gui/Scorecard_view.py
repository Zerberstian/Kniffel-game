import tkinter as tk
from typing import Callable, List

from ..game.category import ScoreCategory
from ..game.score_card import ScoreCard

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


NUMBER_OF_CATEGORIES = 16
FONTSTYLE = "Times New Roman"
FONTSIZE = 20
FONTSIZESMOL = 16
DICE_IPADX = 30
DICE_IPADY = 20
DICE_BG = "#ffffff"
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
        self.CategoryLabel.configure(text = Score_Lable_name_List[self.index], font=(FONTSTYLE, FONTSIZE), bg=DICE_BG)
        self.CategoryLabel.grid(row=0, column=0, sticky="nsew")
        

    def createButton(self):
        self.CategoryButton = tk.Button(self)
        self.CategoryButton.configure(text = "", font=(FONTSTYLE, FONTSIZE), bg=DICE_BG)
        self.CategoryButton.grid(row=0, column=1, sticky="nsew")
        
    

'''Index der ScoreFrames, die keiner Kategorie entsprechen (Bonus/Ergebnis-Zeilen)'''
UPPER_BONUS_INDEX = 6
LOWER_BONUS_INDEX = 14
'''Kniffel-Bonus (mehrfacher Kniffel) noch nicht in ScoreCard implementiert, Zeile bleibt leer - und muss noch im Backend hinzugefügt werden '''
TOTAL_INDEX = 15
_VIRTUAL_INDICES = (UPPER_BONUS_INDEX, LOWER_BONUS_INDEX, TOTAL_INDEX)


class ScorecardView:
    """Verbindet die ScoreFrame-Widgets mit der ScoreCard; Kategorie-Buttons lösen die Auswahl aus."""

    def __init__(
        self,
        frames: List[ScoreFrame],
        categories: List[ScoreCategory],
        on_category_chosen: Callable[[ScoreCategory], None],
    ) -> None:
        self._frames = frames
        self._categories = categories
        self._category_frames = [frame for i, frame in enumerate(frames) if i not in _VIRTUAL_INDICES]

        for frame, category in zip(self._category_frames, categories):
            frame.CategoryButton.configure(command=lambda c=category: on_category_chosen(c))

    def set_enabled(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        for frame in self._category_frames:
            frame.CategoryButton.configure(state=state)

    def render(self, score_card: ScoreCard) -> None:
        for frame, category in zip(self._category_frames, self._categories):
            value = score_card.score(category)
            frame.CategoryButton.configure(text="" if value is None else str(value))

        self._frames[UPPER_BONUS_INDEX].CategoryButton.configure(text=str(score_card.upper_section_bonus()))
        self._frames[TOTAL_INDEX].CategoryButton.configure(text=str(score_card.total_score()))


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
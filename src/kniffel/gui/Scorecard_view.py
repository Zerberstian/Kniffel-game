import tkinter as tk
from typing import Callable, List, Optional

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
PREVIEW_FG = "#9aa0a6"
class ScoreFrame(tk.Frame):
    def __init__(self, master: tk.Frame, i, bg: str = DICE_BG):
        super().__init__(master, bg=bg)

        self.master = master
        self._bg = bg

        self.CategoryLabel = None
        self.CategoryButton = None
        self.index = i

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=90)
        self.grid_rowconfigure(0, weight=1)

        self.createLabel()
        self.createButton()

    def createLabel(self):
        self.CategoryLabel = tk.Label(self)
        self.CategoryLabel.configure(
            text=Score_Lable_name_List[self.index], font=(FONTSTYLE, FONTSIZE), bg=self._bg, anchor="w"
        )
        self.CategoryLabel.grid(row=0, column=0, sticky="nsew", padx=(10, 0))

    def createButton(self):
        self.CategoryButton = tk.Button(self)
        self.CategoryButton.configure(
            text="", font=(FONTSTYLE, FONTSIZE), bg=DICE_BG, fg="black", disabledforeground="black"
        )
        self.CategoryButton.grid(row=0, column=1, sticky="nsew", padx=6, pady=4)
        
    

'''Index der ScoreFrames, die keiner Kategorie entsprechen (Bonus/Ergebnis-Zeilen)'''
UPPER_BONUS_INDEX = 6
LOWER_BONUS_INDEX = 14
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

        '''Bonus-/Ergebnis-Zeilen haben keine Kategorie und keinen Command - sollen nicht klickbar aussehen'''
        for i in _VIRTUAL_INDICES:
            frames[i].CategoryButton.configure(state=tk.DISABLED, relief=tk.FLAT)

    def set_enabled(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        for frame in self._category_frames:
            frame.CategoryButton.configure(state=state)

    def render(self, score_card: ScoreCard, dice_values: Optional[List[int]] = None) -> None:
        for frame, category in zip(self._category_frames, self._categories):
            value = score_card.score(category)
            if value is not None:
                frame.CategoryButton.configure(text=str(value), state=tk.DISABLED, fg="black")
            elif dice_values is not None:
                preview = category.calculate_score(dice_values)
                frame.CategoryButton.configure(text=str(preview), state=tk.NORMAL, fg=PREVIEW_FG)
            else:
                frame.CategoryButton.configure(text="", state=tk.NORMAL, fg="black")

        self._frames[UPPER_BONUS_INDEX].CategoryButton.configure(text=str(score_card.upper_section_bonus()))
        self._frames[LOWER_BONUS_INDEX].CategoryButton.configure(text=str(score_card.lower_section_bonus()))
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
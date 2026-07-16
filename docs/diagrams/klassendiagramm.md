# Klassendiagramm

```mermaid
classDiagram
    class Dice {
        -value : int
        -held : bool
        +roll() void
        +hold() void
        +release() void
    }

    class DiceCup {
        -dice : List~Dice~
        -rolls_left : int
        +roll_all() void
        +roll_unheld() void
        +reset() void
        +values() List~int~
    }

    class ScoreCategory {
        +name : str
        +calculate_score(dice: List~int~) int*
    }

    class NumberCategory {
        -target : int
        +calculate_score(dice: List~int~) int
    }
    class ThreeOfAKind {
        +calculate_score(dice: List~int~) int
    }
    class FourOfAKind {
        +calculate_score(dice: List~int~) int
    }
    class FullHouse {
        +calculate_score(dice: List~int~) int
    }
    class SmallStraight {
        +calculate_score(dice: List~int~) int
    }
    class LargeStraight {
        +calculate_score(dice: List~int~) int
    }
    class Kniffel {
        +calculate_score(dice: List~int~) int
    }
    class Chance {
        +calculate_score(dice: List~int~) int
    }

    class ScoreCard {
        -entries : dict
        +set_score(category: ScoreCategory, value: int) void
        +is_filled(category: ScoreCategory) bool
        +upper_section_bonus() int
        +total_score() int
    }

    class Player {
        -name : str
        -score_card : ScoreCard
    }

    class Game {
        -players : List~Player~
        -current_player_index : int
        -dice_cup : DiceCup
        -categories : List~ScoreCategory~
        +current_player() Player
        +roll_dice() void
        +choose_category(category: ScoreCategory) void
        +next_turn() void
        +is_over() bool
        +winner() Player
    }

    class GameConnector {
        -game : Game
        -view : App
        +on_roll() void
        +on_hold_toggle(dice_id: int) void
        +on_category_chosen(category: ScoreCategory) void
        +refresh_view() void
    }

    class App {
        -connector : GameConnector
        -dice_view : DiceView
        -scorecard_view : ScorecardView
        +build() void
    }

    class DiceView {
        +render(dice: List~Dice~) void
    }

    class ScorecardView {
        +render(score_card: ScoreCard) void
    }

    ScoreCategory <|-- NumberCategory
    ScoreCategory <|-- ThreeOfAKind
    ScoreCategory <|-- FourOfAKind
    ScoreCategory <|-- FullHouse
    ScoreCategory <|-- SmallStraight
    ScoreCategory <|-- LargeStraight
    ScoreCategory <|-- Kniffel
    ScoreCategory <|-- Chance

    DiceCup "1" *-- "5" Dice : dice
    Game "1" *-- "1" DiceCup : dice_cup
    Game "1" *-- "2..6" Player : players
    Game "1" o-- "13" ScoreCategory : categories
    Player "1" *-- "1" ScoreCard : score_card
    ScoreCard "1" o-- "13" ScoreCategory : entries

    GameConnector --> Game : steuert
    GameConnector --> App : aktualisiert
    App --> GameConnector : Benutzeraktionen
    App "1" *-- "1" DiceView : dice_view
    App "1" *-- "1" ScorecardView : scorecard_view
```

---

Das Diagramm zeigt die drei Schichten
`game/`, `connector/`, `gui/` und insbesondere die Vererbungshierarchie der
Bewertungskategorien

**Erklärung:**

- **Vererbung/Polymorphie:** Alle 13 Kniffel-Kategorien sind Unterklassen von
  `ScoreCategory` und überschreiben `calculate_score()`. Die sechs
  Zahlenkategorien (Einer…Sechser) werden dabei nicht als sechs Klassen
  dupliziert, sondern durch eine einzige `NumberCategory` mit Parameter
  `target` abgedeckt.
- **Zusammensetzung:** `Game` besteht aus `Player`n und einem `DiceCup`,
  `DiceCup` besteht aus 5 `Dice`. Diese Objekte existieren nicht unabhängig
  vom übergeordneten Objekt.
- **Schichtentrennung:** `game/`-Klassen haben keine Kenntnis von `App`,
  `DiceView` oder `ScorecardView`. Nur `GameConnector` kennt beide Seiten und
  vermittelt zwischen Spiellogik und Tkinter-Oberfläche.

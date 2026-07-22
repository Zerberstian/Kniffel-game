# Arbeitsdokumentation HP

## Übersicht (chronologisch)

| Datum          | Aufgabenpaket                                           | Bereich                              |
| -------------- | ------------------------------------------------------- | ------------------------------------ |
| 09.07.2026     | Projektstruktur / Dateistruktur und Klassendiagramm     | Dokumentation und Planung            |
| 10./13.07.2026 | `dice.py` (Dice, DiceCup) + test                        | Programmlogik Backend                |
| 13.07.2026     | `category.py` (ScoreCategory-Hierarchie) + test         | Programmlogik Backend                |
| 14.07.2026     | Dokumentation der Softwareentwicklung (dieses Dokument) | Dokumentation                        |
| 15.07.2026     | `score_card.py` (ScoreCard) + test                      | Programmlogik Backend                |
| 16.07.2026     | `player.py` (Player) + test                             | Programmlogik Backend                |
| 16.07.2026     | `game.py` (Game) + test                                 | Programmlogik Backend                |
| 16.07.2026     | `game_connector.py` (GameConnector) + test              | Programmlogik Connect                |
| 16.07.2026     | Einführung`dice_id` + Sortierung in `DiceView`          | Programmlogik und GUI-Funktionalität |

---

## README & Klassendiagramm

> 09.07.2026

siehe `~/docs/diagramms` und `README.md`

## dice.py

> 10.-13.07.2026

**Bereich:** Programmlogik Backend

**Aufgaben:**

- `Dice`: Wert + `held`-Flag, `roll()`, `hold()`, `release()`
- `DiceCup`: hält 5 `Dice`, `roll_all()`, `roll_unheld()`, `reset()`, `rolls_left`
- Tests: `test_dice.py`

**Umsetzung:**

- Konstanten statt Magic Numbers:

  ```python
  MIN_VALUE = 1
  MAX_VALUE = 6
  DICE_PER_CUP = 5
  ROLLS_PER_TURN = 3
  ```

- `held` liegt im `Dice`-Objekt selbst, kein Index-Tracking im `DiceCup`
- Wurf-Limit zentral in einer privaten Hilfsmethode statt Prüfung in jeder Wurf-Methode:

  ```python
  def _consume_roll(self) -> None:
      if self._rolls_left <= 0:
          raise RuntimeError("Keine Würfe mehr in diesem Zug übrig.")
      self._rolls_left -= 1
  ```

- `roll_all()` und `roll_unheld()` rufen beide nur `_consume_roll()` auf

- `reset()` setzt Held-Flags **und** `rolls_left` zurück → ein `DiceCup` ist rundenübergreifend wiederverwendbar, keine neue Instanz nötig

## category.py

> 13.07.2026

**Bereich:** Programmlogik Backend

**Aufgaben:**

- `ScoreCategory` als abstrakte Basisklasse
- Unterklassen: `NumberCategory`, `ThreeOfAKind`, `FourOfAKind`, `FullHouse`, `SmallStraight`, `LargeStraight`, `Kniffel`, `Chance`
- gemeinsames Logging-Setup aus `test_dice.py` nach `tests/_support.py` ausgelagert um Duplikate zu vermeiden
- Tests: `test_category.py`

**Umsetzung:**

- `ABC` + `@abstractmethod` erzwingt Implementierung in jeder Unterklasse:

  ```python
  class ScoreCategory(ABC):
      @abstractmethod
      def calculate_score(self, dice: List[int]) -> int:
          ...
  ```

- eine `NumberCategory`-Klasse mit `target`-Parameter statt 6 Einzelklassen (Einer…Sechser):

  ```python
  class NumberCategory(ScoreCategory):
      def __init__(self, name: str, target: int) -> None:
          super().__init__(name)
          self._target = target

      def calculate_score(self, dice: List[int]) -> int:
          return dice.count(self._target) * self._target
  ```

- feste Punktwerte als Modulkonstanten statt hartkodiert in den Klassen:

  ```python
  FULL_HOUSE_SCORE = 25
  SMALL_STRAIGHT_SCORE = 30
  LARGE_STRAIGHT_SCORE = 40
  KNIFFEL_SCORE = 50
  ```

- Festgesetzte Komibinationen für kleine und große Straße:

  ```python
  _SMALL_STRAIGHT_SEQUENCES = ({1,2,3,4}, {2,3,4,5}, {3,4,5,6})
  _LARGE_STRAIGHT_SEQUENCES = ({1,2,3,4,5}, {2,3,4,5,6})
  ```

- Polymorphie ist der hierbei Kernpunkt der Hierarchie: jede Kategorie wird identisch über `calculate_score(dice)` aufgerufen - `Counter` für x-of-a-kind/FullHouse, `set` für Straights/Kniffel, `count()` für NumberCategory

## score_card.py

> 15.07.2026

**Bereich:** Programmlogik Backend

**Aufgaben:**

- `ScoreCard`: pro Kategorie höchstens ein Eintrag (`None` = offen), `set_score()`, `is_filled()`
- Bonusregel obere Sektion: `upper_section_bonus()`, `total_score()`
- Tests: `test_score_card.py`

**Umsetzung:**

- Einträge als `Dict[ScoreCategory, Optional[int]]` statt Liste
- die Prüfung läuft direkt über die Kategorie, kein zusätzliches Index-Mapping nötig:

  ```python
  def __init__(self, categories: List[ScoreCategory]) -> None:
      self._entries: Dict[ScoreCategory, Optional[int]] = {category: None for category in categories}
  ```

- doppeltes Eintragen wird verhindert statt stillschweigend überschrieben:

  ```python
  def set_score(self, category: ScoreCategory, value: int) -> None:
      if category not in self._entries:
          raise KeyError(f"Unbekannte Kategorie: {category.name}")
      if self.is_filled(category):
          raise ValueError(f"{category.name} ist bereits eingetragen")
      self._entries[category] = value
  ```

- Bonusgrenze als Konstatnen statt hardgecoded:

  ```python
  UPPER_SECTION_BONUS_THRESHOLD = 63
  UPPER_SECTION_BONUS = 35
  ```

- Bonus zählt nur `NumberCategory`-Einträge (obere Sektion) über einen `isinstance`-Check statt fixer Namensliste - und greift somit automatisch für jede `NumberCategory`-Instanz:

  ```python
  upper_sum = sum(
      value
      for category, value in self._entries.items()
      if value is not None and isinstance(category, NumberCategory)
  )
  return UPPER_SECTION_BONUS if upper_sum >= UPPER_SECTION_BONUS_THRESHOLD else 0
  ```

- `total_score()` summiert alle anschließend die eingetragenen Werte plus Bonus, offene (`None`) Einträge werden übersprungen

## player.py

> 16.07.2026

**Bereich:** Programmlogik Backend

**Aufgaben:**

- `Player`: Name + eigene `ScoreCard`
- Tests: `test_player.py`

**Umsetzung:**

- Kategorien werden dem Konstruktor übergeben statt in `Player` selbst erzeugt - laut Klassendiagramm sind Kategorien geteilte Objekte, keine Player-eigenen:

  ```python
  def __init__(self, name: str, categories: List[ScoreCategory]) -> None:
      self._name = name
      self._score_card = ScoreCard(categories)
  ```

- jeder Spieler bekommt dabei trotzdem seine eigene `ScoreCard`-Instanz, obwohl die Kategorien-Liste geteilt ist - Eintragungen eines Spielers wirken sich nicht auf andere aus

## game.py

> 16.07.2026

**Bereich:** Programmlogik Backend

**Aufgaben:**

- `Game`: Spielerliste, aktueller Spieler, gemeinsamer `DiceCup`, Kategorien
- `current_player()`, `roll_dice()`, `choose_category()`, `next_turn()`, `is_over()`, `winner()`
- Tests: `test_game.py`

**Umsetzung:**

- `Game` erzeugt seine `Player` und den `DiceCup` selbst, bekommt die Kategorien aber übergeben (Aggregation, geteilt mit allen `ScoreCard`s):

  ```python
  def __init__(self, player_names: List[str], categories: List[ScoreCategory]) -> None:
      self._categories = categories
      self._players: List[Player] = [Player(name, categories) for name in player_names]
      self._current_player_index = 0
      self._dice_cup = DiceCup()
  ```

- `roll_dice()` unterscheidet ersten Wurf vom zweiten/dritten über `rolls_left` statt über einen extra Zustand - ist `rolls_left` noch auf dem Startwert, wurde in diesem Zug noch nicht gewürfelt:

  ```python
  def roll_dice(self) -> None:
      if self._dice_cup.rolls_left == ROLLS_PER_TURN:
          self._dice_cup.roll_all()
      else:
          self._dice_cup.roll_unheld()
  ```

- `choose_category()` bündelt Punkten + Zugwechsel, damit das nicht bei jedem Aufruf (später `GameConnector`) wiederholt werden muss:

  ```python
  def choose_category(self, category: ScoreCategory) -> None:
      score = category.calculate_score(self._dice_cup.values())
      self.current_player().score_card.set_score(category, score)
      self.next_turn()
  ```

- `next_turn()` setzt den `DiceCup` zurück und rechnet den Spielerindex mit Modulo weiter - kein Sonderfall für "letzter Spieler wieder von vorne":

  ```python
  def next_turn(self) -> None:
      self._dice_cup.reset()
      self._current_player_index = (self._current_player_index + 1) % len(self._players)
  ```

- `is_over()` prüft direkt über `ScoreCard.is_filled()` je Spieler und Kategorie statt eigenen Zähler mitzuführen
- `winner()` per `max(..., key=...)` über `total_score()` statt manueller Vergleichsschleife

## game_connector.py

> 16.07.2026

**Bereich:** Programmlogik Backend

**Aufgaben:**

- `GameConnector`: einzige Klasse, die sowohl `Game` als auch die GUI (`App`) kennt
- `on_roll()`, `on_hold_toggle()`, `on_category_chosen()`, `refresh_view()`
- Tests: `test_game_connector.py` (mit einer Fake-View statt echter GUI)

**Umsetzung:**

- `Dice`-Zugriff war bisher nirgends öffentlich (`DiceCup` hatte nur `values() -> List[int]`), `DiceView.render()` braucht laut Diagramm aber die `Dice`-Objekte selbst (wegen `held`). Deshalb kleine Ergänzung in `dice.py`/`game.py` um eine `dice`-Zugriffskette analog zu `rolls_left`:

  ```python
  # DiceCup
  @property
  def dice(self) -> List[Dice]:
      return list(self._dice)

  # Game
  def dice(self) -> List[Dice]:
      return self._dice_cup.dice
  ```

- `view` bewusst als `Any` typisiert statt `App` zu importieren: `gui/app.py` ist noch keine `App`, sondern nur ein Skript, das beim Import direkt `tk.Tk()` und `root.mainloop()` ausführt - ein wirklicher Import hätte ein Fenster geöffnet und somit die Tests blockiert:

  ```python
  def __init__(self, game: Game, view: Any) -> None:
      self._game = game
      self._view = view
  ```

- jede Aktion delegiert an `Game` und ruft danach `refresh_view()` auf, damit die View nie manuell geupdated werden muss:

  ```python
  def on_category_chosen(self, category: ScoreCategory) -> None:
      self._game.choose_category(category)
      self.refresh_view()
  ```

- `refresh_view()` ruft `dice_view.render()` und `scorecard_view.render()` auf - `GameConnector` ist die einzige Klasse, die beide Seiten (Spiellogik und GUI) kennen darf, deshalb hier bewusst der direkte Zugriff auf die Teil-Views von `App`
- Getestet wird also mit einer einfachen Fake-View (zwei Attribute mit `render()`) statt der echten, noch nicht fertigen GUI-Klasse

## dice_id & Sortierung in DiceView

> 16.07.2026

**Bereich:** Programmlogik GUI / Merge

**Aufgaben:**

- `DiceView.render()`: Würfel sortiert nach Wert anzeigen statt in Wurf-Reihenfolge
- Merge-Konflikt mit `origin/main`: dort gab es bereits `dice_id` in `DiceCup`, aber auch ein `sort_dice()` direkt im Model - Sortierung ist Anzeigesache, nicht Spiellogik, deshalb verworfen (siehe Merge-Commit)

**Umsetzung (logische Kette):**

1. Anzeige soll sortiert sein (z.B. alle Fünfer nebeneinander), das Model braucht das nicht - `values()`/`calculate_score()` ist die Reihenfolge egal
2. Sortieren im `DiceCup` (origin's `sort_dice()`) vermischt Spiellogik mit reinem Anzeige-Bedürfnis → stattdessen sortiert `DiceView.render()` selbst:

   ```python
   for die in sorted(dice, key=lambda d: d.value):
       ...
   ```

3. Dadurch stimmt die Listenposition nach dem Sortieren nicht mehr mit der Position in `DiceCup._dice` überein - "Klick auf Index 2" träfe nach dem Sortieren den falschen Würfel
4. Lösung: jeder `Dice` bekommt eine stabile `dice_id` (Vergabe bei Erzeugung, unabhängig von späterer Sortierung in der Ansicht):

   ```python
   def __init__(self, dice_id: int) -> None:
       ...
       self.dice_id = dice_id
   ```

5. `DiceView` hängt die `dice_id` als Attribut ans jeweilige Label, unabhängig von dessen Anzeigeposition:

   ```python
   label.dice_id = die.dice_id
   ```

6. `GameConnector.on_hold_toggle(dice_id)` sucht den Würfel darüber statt über einen Index - Es funktioniert also unabhängig von der Sortierung:

   ```python
   def on_hold_toggle(self, dice_id: int) -> None:
       die = next(d for d in self._game.dice() if d.dice_id == dice_id)
       die.release() if die.held else die.hold()
   ```

---

## to-dos

> 22.07.2026

**Bereich:** Planung & Projektfinalisierung

##### 1. `ScorecardView`-Klasse

- verwaltet die `ScoreFrame`
  -Liste aus Scorecard_view.py
- implementiert render(score_card) (Werte in Labels/Buttons eintragen) und verbindet
- jeden CategoryButton mit `on_category_chosen(category)`

##### 2. App-Klasse in app.py

- Game, GameConnector, DiceView, ScorecardView instanziieren
- Würfel-Buttons → `on_hold_toggle(dice_id)`
- Reroll-Button → `on_roll()`

##### 3. Import in app.py fixen

- `from Scorecard_view import ScoreFrame` unresolved bei Ausführung als Package (-m)
  → relativer Import nötig

##### 4. sort_GUI_Dice.py löschen

- Duplikat (self außerhalb einer Klasse
- range(Dice_Button_List) statt Länge)
- Sortierung läuft bereits korrekt in `DiceView.render()`

##### 5. Funktionierender Entrypoint

- Spieler-Namen/Kategorien festlegen
- Game erzeugen
- alles verbinden, dann erst `mainloop()`

##### 6. Spielende

- `Game.is_over()`
- und `winner()` irgendwo in der GUI abfangen und anzeigen.

# Arbeitsdokumentation HP

## Übersicht (chronologisch)

| Datum            | Aufgabenpaket                                           | Bereich                   |
| ---------------- | ------------------------------------------------------- | ------------------------- |
| 09.07.2026       | Projektstruktur / Dateistruktur und Klassendiagramm     | Dokumentation und Planung |
| 10. & 13.07.2026 | `dice.py` (Dice, DiceCup) + test                        | Programmlogik Backend     |
| 13.07.2026       | `category.py` (ScoreCategory-Hierarchie) + test         | Programmlogik Backend     |
| 14.07.2026       | Dokumentation der Softwareentwicklung (dieses Dokument) | Dokumentation             |
| 15.07.2026       | `score_card.py` (ScoreCard) + test                      | Programmlogik Backend     |

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

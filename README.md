# Kniffel-Game

Digitale Umsetzung des Würfelspiels **Kniffel** (Yahtzee) im Rahmen des Moduls
Projektmanagement / Vertiefung Objektorientierte Programmierung.

- **Programmiersprache:** Python 3.11+
- **GUI:** Tkinter (Python-Standardbibliothek, keine externe Abhängigkeit nötig)
- **Architektur:** Logik - Konnektor und GUI, strikt getrennt

## Ordnerstruktur

```text
Kniffel-game/
├── README.md
├── docs/                           Projektmanagement- & Prüfungs-Dokumentation
│   ├── management/                 Projektdefinition, Machbarkeits- und Risikoanalyse, Terminplan (GANTT)
│   └── diagrams/                   Klassendiagramm
├── src/
│   └── kniffel/
│       ├── __init__.py
│       ├── __main__.py             Entrypoint: python -m kniffel Ausführung
│       ├── game/                   Spiellogik – keine GUI, rein objektorientiert
│       │   ├── dice.py             Dice, DiceCup
│       │   ├── category.py         ScoreCategory-Hierarchie (eine Klasse je Kniffel-Kategorie)
│       │   ├── scorecard.py        Punktetabelle eines Spielers
│       │   ├── player.py           Spielersteuerung
│       │   └── game.py             Rundensteuerung, Spielerwechsel, Spielende
│       ├── connector/              Verbindung zwischen Game und GUI
│       │   └── game_connector.py
│       └── gui/                    Reine Tkinteransicht, enthält keine Spiellogik
│           ├── app.py              Hauptfenster
│           ├── dice_view.py        Würfelfeld
│           └── scorecard_view.py   Score-Karte
└── tests/                          Einzelne Unit-Tests für game/ (laufen ohne GUI)
    ├── test_dice.py
    ├── test_category.py
    ├── test_diceview.py
    └── test_game.py
```

## Dokumentation

Die Projektmanagement-Artefakte (Projektdefinition, Machbarkeitsanalyse,
Projektstrukturplan, GANTT, Risikoanalyse, Klassendiagramm) liegen in
`docs/`.

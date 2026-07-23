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
├── pyproject.toml                  Package-Metadaten, editable install (src-Layout)
├── requirements.txt                Abhängigkeiten die installiert werden müssen
├── docs/                           Projektmanagement- & Prüfungs-Dokumentation
│   ├── management/                 Projektdefinition, Machbarkeits- und Risikoanalyse, Terminplan (GANTT)
│   └── diagrams/                   Klassendiagramm
├── src/
│   └── kniffel/
│       ├── __init__.py
│       ├── __main__.py             
│       ├── game/                   Spiellogik – keine GUI, rein objektorientiert
│       │   ├── dice.py             Dice, DiceCup
│       │   ├── category.py         ScoreCategory-Hierarchie (eine Klasse je Kniffel-Kategorie)
│       │   ├── score_card.py       Punktetabelle eines Spielers
│       │   ├── player.py           Spielersteuerung
│       │   └── game.py             Rundensteuerung, Spielerwechsel, Spielende
│       ├── connector/              Verbindung zwischen Game und GUI
│       │   └── game_connector.py
│       └── gui/                    Reine Tkinteransicht, enthält keine Spiellogik
│           ├── app.py              Hauptfenster
│           ├── dice_view.py        Würfelfeld
│           └── scorecard_view.py   Score-Karte
└── tests/                          Einzelne Unit-Tests für game/ (laufen ohne GUI)
    ├── _support.py                 Gemeinsames Logging-Setup für Tests
    ├── test_dice.py
    ...
    └── test_game.py
```

## Setup

```bash
git clone https://github.com/Zerberstian/Kniffel-game.git
cd Kniffel-game
python -m venv .venv
.venv\Scripts\activate        # Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Das Package wird per `pip install -e .` (editable install, siehe
`pyproject.toml`) installiert. Dadurch ist `kniffel` überall importierbar.

## Tests

laufen mit:

```bash
pytest tests
```
## App-Start
die App kann in `~\Kniffel-game` mittels folgendem Command ausgeführt werden:

```bash
.venv\Scripts\python.exe -m kniffel.gui.app
```

## Dokumentation

Die Projektmanagement-Artefakte (Projektdefinition, Machbarkeitsanalyse,
Projektstrukturplan, GANTT, Risikoanalyse, Klassendiagramm) liegen in
`docs/`.

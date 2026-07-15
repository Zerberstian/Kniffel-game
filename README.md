# Kniffel-Game

Digitale Umsetzung des Würfelspiels **Kniffel** (Yahtzee) im Rahmen des Moduls
Projektmanagement / Vertiefung Objektorientierte Programmierung.

- **Programmiersprache:** Python 3.11+
- **GUI:** Tkinter (Python-Standardbibliothek, keine externe Abhängigkeit nötig)
- **Architektur:** Logik - Konnektor und GUI, strikt getrennt

## Ordnerstruktur

<pre>
Kniffel-game/
├── README.md
├── pyproject.toml                  Package-Metadaten, editable install (src-Layout)
├── requirements.txt                Abhängigkeiten die installiert werden müssen
├── <span style="color:#CB65F0">docs/</span>                           <span style="color:#CB65F0">Projektmanagement- &amp; Prüfungs-Dokumentation</span>
│   ├── <span style="color:#CB65F0">management/</span>                 <span style="color:#CB65F0">Projektdefinition, Machbarkeits- und Risikoanalyse, Terminplan (GANTT)</span>
│   └── <span style="color:#CB65F0">diagrams/</span>                   <span style="color:#CB65F0">Klassendiagramm</span>
├── src/
│   └── kniffel/
│       ├── __init__.py
│       ├── __main__.py             Entrypoint: python -m kniffel Ausführung
│       ├── <span style="color:#30E864">game/</span>                   <span style="color:#30E864">Spiellogik – keine GUI, rein objektorientiert</span>
│       │   ├── <span style="color:#30E864">dice.py</span>             <span style="color:#30E864">Dice, DiceCup</span>
│       │   ├── <span style="color:#30E864">category.py</span>         <span style="color:#30E864">ScoreCategory-Hierarchie (eine Klasse je Kniffel-Kategorie)</span>
│       │   ├── <span style="color:#30E864">score_card.py</span>       <span style="color:#30E864">Punktetabelle eines Spielers</span>
│       │   ├── <span style="color:#30E864">player.py</span>           <span style="color:#30E864">Spielersteuerung</span>
│       │   └── <span style="color:#30E864">game.py</span>             <span style="color:#30E864">Rundensteuerung, Spielerwechsel, Spielende</span>
│       ├── <span style="color:#E09F00">connector/</span>              <span style="color:#E09F00">Verbindung zwischen Game und GUI</span>
│       │   └── <span style="color:#E09F00">game_connector.py</span>
│       └── <span style="color:#ED47AA">gui/</span>                    <span style="color:#ED47AA">Reine Tkinteransicht, enthält keine Spiellogik</span>
│           ├── <span style="color:#ED47AA">app.py</span>              <span style="color:#ED47AA">Hauptfenster</span>
│           ├── <span style="color:#ED47AA">dice_view.py</span>        <span style="color:#ED47AA">Würfelfeld</span>
│           └── <span style="color:#ED47AA">scorecard_view.py</span>   <span style="color:#ED47AA">Score-Karte</span>
└── <span style="color:#42B8FA">tests/</span>                          <span style="color:#42B8FA">Einzelne Unit-Tests für game/ (laufen ohne GUI)</span>
    ├── <span style="color:#42B8FA">_support.py</span>                 <span style="color:#42B8FA">Gemeinsames Logging-Setup für Tests</span>
    ├── <span style="color:#42B8FA">test_dice.py</span>
    ├── <span style="color:#42B8FA">test_category.py</span>
    ├── <span style="color:#42B8FA">test_score_card.py</span>
    ├── <span style="color:#42B8FA">test_diceview.py</span>
    └── <span style="color:#42B8FA">test_game.py</span>
</pre>

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

## Dokumentation

Die Projektmanagement-Artefakte (Projektdefinition, Machbarkeitsanalyse,
Projektstrukturplan, GANTT, Risikoanalyse, Klassendiagramm) liegen in
`docs/`.

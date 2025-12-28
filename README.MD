
# Apple Health Data Analyser

A Python application for analyzing and visualizing health data exported from Apple Health.

## Overview

This project processes health metrics from Apple Health exports and provides insights through data analysis.

## Project Structure

### `/YazioFoods`
Scripts that export nutrition entries from Apple Health data filled by the Yazio app and recreate complete daily menus.

### `/FddbAndYazioFoods`
Scripts for processing and combining nutrition data from both Fddb and Yazio sources into unified daily menu reconstructions.

## Features

- Import Apple Health XML exports
- Parse and clean health metrics, for now only nutrition from Yazio and Fddb

## Requirements

- Python 3.8+

## Getting Started

1. Clone this repository
3. Export your health data from Apple Health
4. Run the analysis script with your exported file

### Typical output:
❯ python extract_meals.py Export.xml 2025-11-01 2025-12-25
```
2025-11-01 — Meal 1 (17:05)
  • Pesto Rosso
  Calories: 158 kcal | Protein: 2.4 g | Carbs: 3.7 g | Fat: 14.4 g

2025-11-01 — Meal 2 (18:12)
  • Frische Pasta mit Tomatensauce und geriebenem Käse
  • Menemen mit Ei
  • Vollkornbrötchen
  Calories: 1770 kcal | Protein: 66.5 g | Carbs: 200.3 g | Fat: 68.5 g

2025-11-02 — Meal 3 (16:31)
  • Vollkornbrot mit Münchner Leberkäse
  • Hühnerei, Eier, gekocht
  • Leibniz, Butterkeks
  Calories: 1039 kcal | Protein: 64.1 g | Carbs: 112.2 g | Fat: 47.6 g
```

python weeky_food_summary.py Export.xml > weekly.csv
```
2025,35,Raspberry Açai Brekky Smoothie Bowl,6,602
2025,35,Rotini Nudeln mit Tomatensauce und Basilikum,2,840
2025,35,Rührei mit Tomaten und Olivenöl,2,560
2025,35,Salami Aldi ,2,159
2025,35,Salatgurke (ohne Schale). frisch,2,12
2025,35,Schlemmerfilet Bordelaise Knusper,2,886
2025,35,Schokopudding,2,228
2025,35,Sesam Bagel mit Käse. Tomate und Gurke,2,886
2025,35,Sesam Bagel mit Oliven. Käse. Honig. frischem Gemüse und Pfirsich,2,1442
2025,35,Suclac (rice pudding) mit schwarzem Tee,2,548
2025,35,Süßkartoffeln. gekocht,2,904
2025,35,Vollkornbrot mit Leberkäse. Käse und Gurkenscheiben. schwarzer Tee,2,842
2025,35,Wassermelone. frisch,2,462
2025,35,Weintrauben . grün kernlos,2,174
```

python weekly_foods_by_meal.py_yazio_fddb.py Export.xml > weekly.csv
```
Week 2025-52
  Frühstück:
    • Chiasamen. getrocknet (2×)
    • Mandarine. frisch (2×)
    • Griechischer Joghurt. natur (2×)
    • Raspberry Açai Brekky Smoothie Bowl (2×)
    • Knusper Müsli Dinkel (2×)
    • Hühnerei. Eier. gekocht (1×)
    • Honig (1×)
    • Edamer Käse 30% Fett i.Tr. (1×)
    • Orange (Apfelsine). frisch (1×)
    • Vollkornbrot  (1×)
    • Geflügel Salami () (1×)
    • Kürbiskernbrötchen () (1×)
  Snack 1:
    • Ei (gekocht) (1×)
    • Apfel (Pink Lady) (1×)
    • Kiwi (frisch) (1×)
  Abendessen:
    • Pizza Salami (Durchschnitt) (1×)
  Mittagessen:
    • Rotkohl () (1×)
    • Kartoffeln () (1×)
    • Braune Soße () (1×)
    • Ente mit Haut () (1×)
  Snack 2:
    • Pflaumen-Streusel-Kuchen (Pflaume) (1×)
```


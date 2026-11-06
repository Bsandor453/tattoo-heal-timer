# Tetoválás gyógyulási időzítő

Grafikus Python-alkalmazás friss tetoválások napi ápolásának és gyógyulási fázisainak követésére.

Add meg, hány nap telt el a tetoválás óta, és a program azonnal megmutatja az adott naphoz tartozó gyógyulási szakaszt, valamint a higiéniai és ápolási teendőket.

## Funkciók

- **Napválasztás gombokkal:** a `−` és `+` gomb egy napot léptet, a szakaszgombok pedig az adott szakasz első napjára ugranak.
- **Valós idejű frissítés:** a beviteli mezőbe írt szám már gépelés közben frissíti a tartalmat. Érvénytelen bevitelnél hibaüzenet jelenik meg. A mezőben a fel és le nyíl is léptet.
- **Saját osztály:** a `HealingGuide` osztály szűri ki a gyógyulási adatokból az adott naphoz tartozó szakaszt és tanácsokat.
- **Külön modulok:** a felület és az eseménykezelő logika külön fájlban van.
- **Fertőzésmegelőzés:** a program napra szabott higiéniai tanácsokat ad, és mindig látszanak azok a tünetek is, amelyeknél orvoshoz kell fordulni.

## Futtatás

Python 3.10 vagy újabb kell hozzá, más csomagot nem kell telepíteni. A Tkinter a Windowsos Python része, Linuxon külön kell telepíteni (például `sudo apt install python3-tk`).

A projekt mappájában:

```
python -m tattoo_heal_timer
```

## Tesztek

```
python -m unittest
```

## Felépítés

| Fájl | Feladata |
| --- | --- |
| `tattoo_heal_timer/healing.py` | Adatok és szűrés: szakaszok, tanácsok, `HealingGuide` osztály |
| `tattoo_heal_timer/controller.py` | Eseménykezelő logika: mi történik gombnyomásra és gépelésre |
| `tattoo_heal_timer/ui.py` | Grafikus felület (Tkinter) |
| `tattoo_heal_timer/__main__.py` | Összekapcsolja a részeket és elindítja a programot |
| `tests/` | Automatikus tesztek |

## Fontos

A tanácsok általános, tájékoztató jellegűek, és nem helyettesítik a tetováló utasításait vagy az orvosi véleményt.

#!/usr/bin/env python3
"""Fill empty msgstr entries in translations/ui/de.po (Argos EN→DE + BIM glossary)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import argostranslate.translate

ROOT = Path(__file__).resolve().parents[1]
PO = ROOT / "translations" / "ui" / "de.po"

# Preferred BIM / Revit / 3DCADius wording over raw machine output.
GLOSSARY: dict[str, str] = {
    "Align": "Ausrichten",
    "Align (AL): pick a reference line, then what to line up with it": "Ausrichten (AL): Bezugslinie wählen, dann was daran ausgerichtet wird",
    "Architecture": "Architektur",
    "Associated Level": "Zugeordnete Ebene",
    "Attach Top/Base": "Oben/Unten anbinden",
    "Beam": "Träger",
    "Bottom": "Unten",
    "Cancel": "Abbrechen",
    "Ceiling": "Decke",
    "Ceiling Plan": "Deckenplan",
    "Ceiling Plans": "Deckenpläne",
    "Centimetres": "Zentimeter",
    "Close": "Schließen",
    "Close Inactive": "Inaktive schließen",
    "Column": "Stütze",
    "Constraints": "Zwangsbedingungen",
    "Copy": "Kopieren",
    "Crop View": "Ansicht beschneiden",
    "Cut Plane": "Schnittebene",
    "Dark Mode": "Dunkelmodus",
    "Data": "Daten",
    "Data Outlet": "Datensteckdose",
    "Delete": "Löschen",
    "Demolish": "Abbruch",
    "Detach Top/Base": "Oben/Unten lösen",
    "Detail Level": "Detaillierungsgrad",
    "Dimension": "Bemaßung",
    "Dimensions": "Bemaßungen",
    "Door": "Tür",
    "Down Conductor": "Ableitung",
    "Duplicate View": "Ansicht duplizieren",
    "Earthing": "Erdung",
    "Earthing Conductor": "Erdungsleiter",
    "Earthing Electrode": "Erder",
    "Edit": "Bearbeiten",
    "Edit Family": "Familie bearbeiten",
    "Edit Type": "Typ bearbeiten",
    "Electrical": "Elektro",
    "Elevation": "Ansicht",
    "Elevations (Building Elevation)": "Ansichten (Gebäudeansicht)",
    "Equality Display": "Gleichheitsanzeige",
    "Extents": "Ausdehnung",
    "Families": "Familien",
    "Favorites": "Favoriten",
    "Filters": "Filter",
    "Finish": "Fertigstellen",
    "Flip": "Umdrehen",
    "Floor": "Geschossdecke",
    "Floor Plan": "Grundriss",
    "Floor Plans": "Grundrisse",
    "Floor by Face": "Decke nach Fläche",
    "Geometry": "Geometrie",
    "Graphics": "Grafik",
    "Grid": "Achse",
    "Hide Category": "Kategorie ausblenden",
    "Hide Element": "Element ausblenden",
    "IDs of Selection": "IDs der Auswahl",
    "Identity Data": "Identitätsdaten",
    "Inspection Box": "Prüfschacht",
    "Kind": "Art",
    "Language": "Sprache",
    "Level": "Ebene",
    "Lightning Protection": "Blitzschutz",
    "Line Through": "Linie durch",
    "Linked Models": "Verknüpfte Modelle",
    "Manage": "Verwalten",
    "Mass Floors": "Massengeschosse",
    "Massing": "Massenmodell",
    "Materials": "Materialien",
    "Metres": "Meter",
    "Millimetres": "Millimeter",
    "Mirror": "Spiegeln",
    "Model by Face": "Modell nach Fläche",
    "Modify": "Ändern",
    "Move": "Verschieben",
    "New Family": "Neue Familie",
    "New Project": "Neues Projekt",
    "Offset": "Versatz",
    "Orientation": "Ausrichtung",
    "Other": "Sonstiges",
    "Override Graphics": "Grafik überschreiben",
    "Paint": "Farbe auftragen",
    "Patch Panel": "Patchfeld",
    "Phasing": "Phasen",
    "Place View": "Ansicht platzieren",
    "Plumbing": "Sanitär",
    "Prefix": "Präfix",
    "Project Browser": "Projektbrowser",
    "Project Language": "Projektsprache",
    "Project Parameters": "Projektparameter",
    "Project Units": "Projekteinheiten",
    "Properties": "Eigenschaften",
    "Purge Unused": "Nicht verwendetes bereinigen",
    "Rack": "Gestell",
    "Railing": "Geländer",
    "Ramp": "Rampe",
    "Redo": "Wiederherstellen",
    "Remove Paint": "Farbe entfernen",
    "Replace With Text": "Durch Text ersetzen",
    "Roof": "Dach",
    "Roof by Face": "Dach nach Fläche",
    "Room": "Raum",
    "Room Area Computation": "Raumberechnung",
    "Rotate": "Drehen",
    "Save": "Speichern",
    "Save As…": "Speichern unter…",
    "Schedules/Quantities (all)": "Listen/Mengen (alle)",
    "Section": "Schnitt",
    "Section Box": "Schnittbox",
    "Sections (Building Section)": "Schnitte (Gebäudeschnitt)",
    "Select by ID": "Nach ID auswählen",
    "Settings": "Einstellungen",
    "Sheet": "Plan",
    "Sheets (all)": "Pläne (alle)",
    "Shortcuts": "Tastenkürzel",
    "Show Mass": "Masse anzeigen",
    "Snaps": "Fangpunkte",
    "Stair": "Treppe",
    "Structure": "Tragwerk",
    "Suffix": "Suffix",
    "Tag": "Beschriftung",
    "Technical Standards": "Technische Normen",
    "Text": "Text",
    "Thin Lines": "Dünne Linien",
    "Top": "Oben",
    "Type Properties": "Typeigenschaften",
    "Undo": "Rückgängig",
    "Update to Face": "An Fläche anpassen",
    "User Interface": "Benutzeroberfläche",
    "Value": "Wert",
    "View": "Ansicht",
    "View Depth": "Ansichtstiefe",
    "View Range": "Ansichtsbereich",
    "View Templates": "Ansichtsvorlagen",
    "Views (all)": "Ansichten (alle)",
    "Visibility/Graphics": "Sichtbarkeit/Grafik",
    "Voice Outlet": "Telefonsteckdose",
    "Wall": "Wand",
    "Wall by Face": "Wand nach Fläche",
    "Walls": "Wände",
    "Window": "Fenster",
    "Above": "Darüber",
    "Below": "Darunter",
    "Capture & Descent": "Auffang & Ableitung",
    "Cabling": "Verkabelung",
    "Conceptual Mass": "Konzeptmasse",
    "Outlets & Equipment": "Dosen & Geräte",
    "Apply": "Übernehmen",
    "OK": "OK",
    "Yes": "Ja",
    "No": "Nein",
    "Open…": "Öffnen…",
    "Feet and inches": "Fuß und Zoll",
    "Feet": "Fuß",
    "Inches": "Zoll",
    "File": "Datei",
    "Help": "Hilfe",
    "Insert": "Einfügen",
    "Annotate": "Beschriften",
    "Search": "Suchen",
    "Search the Project Browser": "Projektbrowser durchsuchen",
    "3D View": "3D-Ansicht",
    "3D Views": "3D-Ansichten",
    "Building information modelling, open and free.": "Bauwerksdatenmodellierung, offen und kostenlos.",
}


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")


def unesc(s: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            n = s[i + 1]
            out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(n, n))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def protect_placeholders(text: str) -> tuple[str, list[str]]:
    held: list[str] = []

    def keep(m: re.Match[str]) -> str:
        held.append(m.group(0))
        return f"⟦{len(held) - 1}⟧"

    return re.sub(r"\{\}|\{[^{}]+\}|`[^`]+`|\b[A-Z]{1,3}\b(?=:)", keep, text), held


def restore_placeholders(text: str, held: list[str]) -> str:
    def put(m: re.Match[str]) -> str:
        i = int(m.group(1))
        return held[i] if 0 <= i < len(held) else m.group(0)

    return re.sub(r"⟦(\d+)⟧", put, text)


def translate(english: str) -> str:
    if english in GLOSSARY:
        return GLOSSARY[english]
    if not english.strip():
        return english
    # Keep pure symbols / numbers / shortcuts unchanged.
    if re.fullmatch(r"[\d\s./:+\-–—%°'\"{}()\[\]]+", english):
        return english
    protected, held = protect_placeholders(english)
    try:
        de = argostranslate.translate.translate(protected, "en", "de")
    except Exception as e:  # noqa: BLE001
        print(f"fail: {english!r}: {e}", file=sys.stderr)
        return ""
    de = restore_placeholders(de, held)
    if english.count("{}") != de.count("{}"):
        return english
    # Light cleanup of common machine artifacts
    de = de.replace("..", ".").strip()
    return de


def main() -> None:
    text = PO.read_text(encoding="utf-8")
    pair_re = re.compile(r'^msgid "(.*)"\nmsgstr "(.*)"$', re.M)
    filled = 0
    kept = 0
    skipped = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal filled, kept, skipped
        msgid_esc, msgstr_esc = m.group(1), m.group(2)
        msgid = unesc(msgid_esc)
        if msgid == "":
            return m.group(0)
        if msgstr_esc.strip():
            # Refresh glossary hits even if already filled.
            if msgid in GLOSSARY and unesc(msgstr_esc) != GLOSSARY[msgid]:
                filled += 1
                return f'msgid "{msgid_esc}"\nmsgstr "{esc(GLOSSARY[msgid])}"'
            kept += 1
            return m.group(0)
        de = translate(msgid)
        if not de.strip():
            skipped += 1
            return m.group(0)
        filled += 1
        if filled % 100 == 0:
            print(f"… {filled}", flush=True)
        return f'msgid "{msgid_esc}"\nmsgstr "{esc(de)}"'

    new = pair_re.sub(repl, text)
    PO.write_text(new, encoding="utf-8")
    empty = len(re.findall(r'^msgstr ""$', new, re.M))
    print(f"done filled_or_updated={filled} kept={kept} skipped={skipped} empty_left={empty}")


if __name__ == "__main__":
    main()

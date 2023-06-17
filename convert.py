import json
import re

def convert_txt_to_json(txt_path):
    with open(txt_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split de tekst in liederen op basis van de "LIED" headers
    songs = content.split("LIED")

    # Verwijder lege elementen en trim witruimte van elk lied
    songs = [song.strip() for song in songs if song.strip()]

    hymns = []
    for song in songs:
        lines = song.splitlines()

        # Zoek het liednummer en de titel op basis van de eerste regel
        num_match = re.search(r"\bLIED\s+(\d+)", lines[0], re.IGNORECASE)
        num = num_match.group(1) if num_match else ""
        num = re.sub(r"\bLIED\s+\d+", "", lines[0], flags=re.IGNORECASE).strip()
        title = ""
        # Verwijder het nummer uit de lijnen
        lines = lines[1:]

        # Splits de versen op basis van dubbele linebreaks
        verse_lines = []
        current_verse = []
        for line in lines:
            if line.strip() == "":
                # Dubbele linebreak gevonden, voeg het huidige vers toe aan de lijst
                if current_verse:
                    verse_lines.append(current_verse)
                    current_verse = []
            else:
                # Voeg de regel toe aan het huidige vers, tenzij deze een genummerde string bevat
                if not re.match(r"\d+\.", line):
                    current_verse.append(line)

        # Voeg het laatste vers toe aan de lijst
        if current_verse:
            verse_lines.append(current_verse)

        # Bouw het lied op
        hymn = {
            "num": num,
            "title": title,
            "stanzas": {
                "verses": verse_lines,
                "refrain": []
            }
        }

        hymns.append(hymn)

    # Bouw het JSON-object op
    data = {
        "lang": "nl",
        "header": {
            "title": "Gezangen Zions Nederlands",
            "shortTitle": "Gezangen Zions NL",
            "fullPdfUrl": "https://sdarm.org/files/publications/books/pdf/trm.pdf"
        },
        "hymns": hymns,
        "topics": [
            {
                "name": "Ere- en Lofzangen",
                "start": hymns[0]["num"],
                "end": hymns[-1]["num"]
            }
        ]
    }

    return data

def export_json_to_file(json_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)

# Geef het pad naar het tekstbestand op
txt_path = "hymnal.txt"

# Converteer het tekstbestand naar JSON
json_output = convert_txt_to_json(txt_path)

# Geef het pad naar het uitvoerbestand op
output_file = "hymnal.json"

# Exporteer de JSON-gegevens naar een bestand

export_json_to_file(json_output, output_file)

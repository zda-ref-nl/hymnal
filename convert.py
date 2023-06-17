import json

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
        header = lines[0].strip().split(maxsplit=1)
        if len(header) >= 2:
            num = header[0]
            title = header[1]
        else:
            num = ""
            title = ""

        # Verwijder het nummer en de titel uit de lijnen
        lines = lines[1:]

        # Voeg het lied toe aan de lijst van liederen
        hymns.append({
            "num": num,
            "title": title,
            "stanzas": {
                "verses": [stanza.splitlines() for stanza in lines],
                "refrain": []
            }
        })

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
                "start": "1",
                "end": str(len(hymns))
            }
        ]
    }

    # Converteer het data-object naar JSON
    json_output = json.dumps(data, indent=4, ensure_ascii=False)

    return json_output

# Geef het pad naar het tekstbestand op
txt_path = "hymnal.txt"

# Converteer het tekstbestand naar JSON
json_output = convert_txt_to_json(txt_path)

def export_json_to_file(json_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(json_data)
# Converteer het tekstbestand naar JSON
json_output = convert_txt_to_json(txt_path)

# Geef het pad naar het uitvoerbestand op
output_file = "hymnal.json"

# Exporteer de JSON-gegevens naar een bestand
export_json_to_file(json_output, output_file)

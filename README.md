# Meme Hitster

Hitster, maar met virale Nederlandse filmpjes. Scan een kaart (of tik het nummer in),
kijk het filmpje, raad het jaar en leg de kaart op je tijdlijn.

## Bestanden

| Bestand | Wat |
|---|---|
| `videos.md` | Verzamellijst: link, fragment en notities per video |
| `titels.txt` | **Jaartal + titel per kaart** – dit pas je aan |
| `cards.json` | Wordt gemaakt uit de twee bestanden hierboven – niet met de hand aanpassen |
| `index.html` | De speler (telefoon én laptop) |
| `print.html` | Printbare kaarten |
| `tools/bouw_kaarten.py` | Maakt `cards.json` |

## Kaart toevoegen of titel aanpassen

1. Nieuwe video: regel toevoegen in `videos.md` (en in `titels.txt` met hetzelfde nummer).
2. Titel of jaartal wijzigen: alleen `titels.txt` aanpassen.
3. Daarna: `python3 tools/bouw_kaarten.py`

## Lokaal testen

```
python3 -m http.server 8765 --bind 0.0.0.0
```
Laptop: <http://localhost:8765> · iPhone (zelfde wifi): `http://<ip-van-de-mac>:8765`

## Spelen

- **Telefoon:** scan de QR-code. Telefoon dwars = beeldvullend (handig voor AirPlay).
- **Laptop:** tik het kaartnummer in. Toetsen: `spatie` speel/pauze · `R` opnieuw · `O` onthul · cijfers + `Enter` nieuwe kaart.

## Printen

Open `print.html` **op de online site** (de QR-codes wijzen naar het adres waar de pagina staat).
A4, 100%, dubbelzijdig, omslaan via de lange zijde, achtergrondafbeeldingen aan.

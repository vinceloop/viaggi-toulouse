"""Genera le 13 tracce MP3 in assets/audio/ a partire dagli script in assets/scripts/,
usando le voci neurali gratuite di Microsoft Edge TTS (nessuna API key richiesta).

Uso:
    py -3 -m pip install --user edge-tts
    py -3 tools/generate_audio.py

Dopo aver modificato un testo in assets/scripts/NN_slug.txt, rilancia lo script:
sovrascrive solo assets/audio/NN_slug.mp3.

Voci italiane disponibili (elenco aggiornato con `py -3 -m edge_tts --list-voices | findstr it-IT`):
    it-IT-DiegoNeural, it-IT-ElsaNeural, it-IT-IsabellaNeural, it-IT-GiuseppeMultilingualNeural

PRONUNCIA DEI NOMI FRANCESI
edge-tts non supporta SSML (nessun tag <lang> per cambiare lingua a metà frase), quindi
la voce italiana leggerebbe i toponimi francesi con fonetica italiana, in modo sbagliato.
FRENCH_RESPELLING sotto riscrive foneticamente (solo per l'audio, mai per i testi visibili
in assets/scripts/ o in index.html) i nomi francesi ricorrenti, cosicché l'ortografia letta
dal motore italiano suoni più vicina all'originale francese. È un'approssimazione empirica,
non una trascrizione IPA precisa: se dopo l'ascolto un termine suona ancora male, aggiungi o
correggi una voce nella lista (le sostituzioni sono applicate nell'ordine dato, quindi le
frasi più lunghe/specifiche vanno PRIMA delle loro sotto-parti, altrimenti verrebbero
consumate parzialmente dalla regola più generica).
"""
import asyncio
import os

import edge_tts

VOICE = "it-IT-GiuseppeMultilingualNeural"
RATE = "-4%"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT, "assets", "scripts")
AUDIO_DIR = os.path.join(ROOT, "assets", "audio")

STOPS = [
    "01_place_saint_pierre",
    "02_jacobins",
    "03_daurade",
    "04_pont_neuf",
    "05_hotel_assezat",
    "06_place_saintes_scarbes",
    "07_cathedrale_saint_etienne",
    "08_rue_saint_rome",
    "09_place_du_capitole",
    "10_rue_du_taur",
    "11_saint_sernin",
    "12_marche_victor_hugo",
    "13_gare_matabiau",
]

FRENCH_RESPELLING = [
    # frasi composte (più specifiche) prima delle loro sotto-parti
    ("Cathédrale Saint-Étienne", "Cattedrale Sant-Etièn"),
    ("Basilique Notre-Dame de la Daurade", "Basilica Notre-Dam de la Dorad"),
    ("Basilique Saint-Sernin", "Basilica Sen-Sernèn"),
    ("Notre-Dame de la Daurade", "Notre-Dam de la Dorad"),
    ("Notre-Dame du Taur", "Notre-Dam du Tor"),
    ("Place Saint-Pierre", "Plas Sen-Pierre"),
    ("Place Saint-Sernin", "Plas Sen-Sernèn"),
    ("Place des Jacobins", "Plas de Giacobèn"),
    ("Couvent des Jacobins", "Cuvàn de Giacobèn"),
    ("Place de la Daurade", "Plas de la Dorad"),
    ("Quai de la Daurade", "Ké de la Dorad"),
    ("Place d'Assézat", "Plas d'Assézà"),
    ("Hôtel d'Assézat", "Otèl d'Assézà"),
    ("Pierre d'Assézat", "Pierre d'Assézà"),
    ("Fondation Bemberg", "Fondasiòn Bemberg"),
    ("Place Saintes-Scarbes", "Plas Sent-Scarb"),
    ("Saintes-Scarbes", "Sent-Scarb"),
    ("hôtels particuliers", "otèl particulié"),
    ("Rue Pargaminières", "Ru Pargaminièr"),
    ("Rue Saint-Rome", "Ru Sen-Rom"),
    ("Place du Capitole", "Plas du Capitòl"),
    ("Rue du Taur", "Ru du Tor"),
    ("Marché Victor Hugo", "Marscé Victor Hugo"),
    ("Place Victor Hugo", "Plas Victor Hugo"),
    ("Gare Matabiau", "Gar Matabiò"),
    ("Vierge Noire", "Vièrj Noàr"),
    ("Pont Neuf", "Pon Neuf"),
    # sotto-parti / occorrenze isolate rimaste
    ("Saint-Étienne", "Sant-Etièn"),
    ("Saint-Sernin", "Sen-Sernèn"),
    ("Jacobins", "Giacobèn"),
    ("Daurade", "Dorad"),
    ("Assézat", "Assézà"),
    ("Capitole", "Capitòl"),
    ("Capitouls", "Capitùl"),
    ("Marché", "Marscé"),
    ("il quai", "il ké"),
]


def respell_for_audio(text):
    for french, phonetic in FRENCH_RESPELLING:
        text = text.replace(french, phonetic)
    return text


async def generate(name):
    src = os.path.join(SCRIPTS_DIR, name + ".txt")
    dst = os.path.join(AUDIO_DIR, name + ".mp3")
    with open(src, "r", encoding="utf-8") as f:
        text = respell_for_audio(f.read().strip())
    await edge_tts.Communicate(text, VOICE, rate=RATE).save(dst)
    print(f"OK {name}.mp3 ({os.path.getsize(dst)} bytes)")


async def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    for name in STOPS:
        await generate(name)


if __name__ == "__main__":
    asyncio.run(main())

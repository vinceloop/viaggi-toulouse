TOULOUSE — AUDIOGUIDA WEB

La cartella contiene una pagina web responsive pensata per essere usata da telefono mentre si cammina.

CONTENUTO
- index.html              pagina principale
- manifest.webmanifest    supporto installazione come web app
- sw.js                   cache offline dopo il primo caricamento
- assets/scripts/         testo delle 13 tappe (sorgente della narrazione)
- assets/audio/           13 tracce MP3 con voce neurale italiana (generate, vedi sotto)
- tools/generate_audio.py script per (ri)generare le tracce MP3 dai testi

NARRAZIONE AUDIO
Ogni tappa ha una traccia MP3 con voce italiana naturale (Microsoft Edge Neural
TTS, voce "it-IT-GiuseppeMultilingualNeural", generata gratuitamente offline —
vedi tools/generate_audio.py). I nomi propri francesi (Jacobins, Daurade,
Capitole, Saint-Étienne, ecc.) sono riscritti foneticamente solo per l'audio
(mai nei testi visibili) così che la voce italiana li pronunci in modo più
vicino al francese — vedi FRENCH_RESPELLING in tools/generate_audio.py. Se
modifichi un testo in assets/scripts/, rilancia lo script per rigenerare il
relativo MP3. Se per qualsiasi motivo un file audio non fosse disponibile (rete,
hosting), la pagina passa automaticamente alla sintesi vocale del browser (Web
Speech API) come riserva, con un selettore di voce e velocità che compare solo
in quel caso.

COME USARLA
1. Carica l'intera cartella su un hosting statico (GitHub Pages, Netlify, Cloudflare Pages, ecc.).
2. Apri l'URL dal telefono.
3. Se vuoi, aggiungila alla schermata Home del telefono.
4. Dopo il primo caricamento la pagina può mantenere in cache i contenuti per l'uso offline, quando il sito è servito in HTTPS.

IN ALTERNATIVA
Puoi anche aprire index.html localmente, ma le funzioni offline/installazione del service worker richiedono HTTPS o localhost.

# EV Tracker
Quota di mercato delle auto elettriche (BEV) per paese, aggiornata automaticamente ogni giorno.

## Messa online (una volta sola)
1. Crea un repository su GitHub e carica tutti i file di questa cartella (incluso `.github`).
2. Settings > Pages > Source: "Deploy from a branch", branch `main`, cartella `/docs`.
3. Actions > "Aggiorna dati e sito" > Run workflow. Al termine il sito è su `https://TUO-UTENTE.github.io/NOME-REPO/`.

## Aggiungere un paese
- Aggiungi una riga in `registry.py`.
- Crea `collectors/<codice>.py` (es. `se.py`) con `collect()` che restituisce `{"2026-09": {"total": 123, "bev": 45}}`.

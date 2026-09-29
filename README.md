# 🚚 bot-trafficoets2

> Sistema Logistico H24 per il traffico dei camionisti di Euro Truck Simulator 2 su Discord.

Questo bot permette di gestire in modo automatico i viaggi, le consegne e i convogli di una Virtual Trucking Company (VTC) direttamente all'interno di un server Discord, fornendo al contempo informazioni in tempo reale sul traffico delle tratte principali di ETS2.

## 🚀 Funzionalità principali
- **Logistica Autonoma H24:** Registrazione di partenza e arrivo dei carichi tramite semplici comandi.
- **Visualizzazione Info Traffico:** Aggiornamenti sulle zone calde del gioco (es. Calais - Duisburg).
- **Statistiche di Consegna:** Monitoraggio del tonnellaggio trasportato dai singoli utenti.

## 🛠️ Comandi Disponibili

| Comando | Descrizione | Sintassi |
| :--- | :--- | :--- |
| `!parti` | Avvia una nuova sessione di viaggio logistico | `!parti [Origine] [Destinazione] [Carico]` |
| `!arrivato` | Conclude il viaggio registrando il peso | `!arrivato [Tonnellate]` |
| `!traffico` | Mostra la situazione attuale del traffico stradale | `!traffico` |

## ⚙️ Installazione e Requisiti

Per avviare il bot in locale o sul tuo server di hosting, assicurati di aver installato Python 3.8+ e le dipendenze richieste:

```bash
pip install discord.py
```

1. Clona questa repository.
2. Inserisci il token del tuo bot all'interno del file principale `bot_ets2_autonomo.py`.
3. Avvia lo script:
```bash
python bot_ets2_autonomo.py
```

## 📝 Licenza
Questo progetto è distribuito sotto licenza Open Source. Sentiti libero di contribuire con Pull Request o segnalando bug nella sezione Issues!

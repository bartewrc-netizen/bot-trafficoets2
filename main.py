import discord
from discord.ext import commands
import datetime
import sqlite3

# Impostazione dei permessi (Intents)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- CONFIGURAZIONE DATABASE ---
def inizializza_db():
    # Connette al database (crea il file azienda_trasporti.db se non esiste)
    conn = sqlite3.connect('azienda_trasporti.db')
    cursor = conn.cursor()
    # Crea la tabella per memorizzare i dati dei camionisti
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utenti (
            discord_id TEXT PRIMARY KEY,
            nome_utente TEXT,
            viaggi_completati INTEGER DEFAULT 0,
            tonnellate_totali INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Inizializza il database all'avvio dello script
inizializza_db()

@bot.event
async def on_ready():
    print(f'Loggato come {bot.user.name} | Database Pronto!')
    await bot.change_presence(activity=discord.Game(name="Euro Truck Simulator 2"))

# --- COMANDI LOGISTICA ---

@bot.command()
async def parti(ctx, partenza: str, arrivo: str, carico: str):
    """Registra la partenza di un viaggio."""
    ora_partenza = datetime.datetime.now().strftime("%H:%M")
    embed = discord.Embed(title="🚚 Nuova Consegna Avviata!", color=discord.Color.blue())
    embed.add_field(name="Camionista", value=ctx.author.display_name, inline=False)
    embed.add_field(name="Tratta", value=f"Da **{partenza}** a **{arrivo}**", inline=True)
    embed.add_field(name="Merce", value=carico, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def arrivato(ctx, tonnellate: int):
    """Registra l'arrivo e salva i dati nel Database."""
    user_id = str(ctx.author.id)
    username = ctx.author.display_name

    # Salvataggio o aggiornamento dati nel database SQLite
    conn = sqlite3.connect('azienda_trasporti.db')
    cursor = conn.cursor()
    
    # Inserisce l'utente se nuovo, altrimenti aggiorna i suoi dati sommandoli
    cursor.execute('''
        INSERT INTO utenti (discord_id, nome_utente, viaggi_completati, tonnellate_totali)
        VALUES (?, ?, 1, ?)
        ON CONFLICT(discord_id) DO UPDATE SET
            viaggi_completati = viaggi_completati + 1,
            tonnellate_totali = tonnellate_totali + ?
    ''', (user_id, username, tonnellate, tonnellate))
    
    conn.commit()
    conn.close()

    embed = discord.Embed(title="✅ Consegna Completata e Registrata!", color=discord.Color.green())
    embed.add_field(name="Camionista", value=username, inline=False)
    embed.add_field(name="Carico Accreditato", value=f"+ {tonnellate} Tonnellate", inline=True)
    await ctx.send(embed=embed)

# --- NUOVO COMANDO: CLASSIFICA ---

@bot.command()
async def classifica(ctx):
    """Mostra i migliori camionisti dell'azienda in base alle tonnellate."""
    conn = sqlite3.connect('azienda_trasporti.db')
    cursor = conn.cursor()
    
    # Prende i primi 5 utenti con più tonnellate trasportate
    cursor.execute('SELECT nome_utente, viaggi_completati, tonnellate_totali FROM utenti ORDER BY tonnellate_totali DESC LIMIT 5')
    righe = cursor.fetchall()
    conn.close()

    embed = discord.Embed(title="🏆 Classifica Aziendale Camionisti", color=discord.Color.gold())
    
    if not righe:
        embed.description = "Nessun viaggio registrato al momento. Usa `!arrivato` per iniziare!"
    else:
        testo_classifica = ""
        percorso_icone = ["🥇", "🥈", "🥉", "🚛", "🚛"]
        
        for i, riga in enumerate(righe):
            icona = percorso_icone[i] if i < len(percorso_icone) else "🚛"
            testo_classifica += f"{icona} **{riga[0]}** - {riga[2]} Tonnellate ({riga[1]} viaggi)\n"
        
        embed.description = testo_classifica

    await ctx.send(embed=embed)

@bot.command()
async def traffico(ctx):
    """Mostra un report rapido sul traffico."""
    embed = discord.Embed(title="🚦 Bollettino Traffico ETS2", color=discord.Color.orange())
    embed.add_field(name="📍 Calais - Duisburg", value="🔴 Traffico intenso segnalato.", inline=False)
    await ctx.send(embed=embed)

bot.run('IL_TUO_TOKEN_QUI')

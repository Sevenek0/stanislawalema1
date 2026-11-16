# Bot Discord – zdjęcia na GIF-y

## Komendy (prefix `!`)
| Komenda | Co robi |
|---|---|
| `!gif [ms]` + zdjęcia | 1 zdjęcie → pulsujący GIF, kilka zdjęć → pokaz slajdów (ms = czas klatki, domyślnie 500) |
| `!efekt <nazwa>` + zdjęcie | Efekty: `obrot`, `puls`, `trzes`, `tecza`, `odbicie`, `zoom` |
| `!avatargif <efekt> [@ktoś]` | GIF z avatara |
| `!avatar [@ktoś]` | Pokazuje avatar |
| `!ping`, `!info` | Ping / info o bocie |
| `!moneta`, `!kostka [ścian]`, `!wybierz a \| b \| c` | Losowanie |
| `!pomoc` | Lista komend |

Możesz też odpowiedzieć (reply) na cudzą wiadomość ze zdjęciem i wpisać `!gif` / `!efekt ...`.

Napisz `67` → bot odpisze `wypierdalaj`.

## Uruchomienie
1. https://discord.com/developers/applications → **New Application** → **Bot** → **Reset Token** (skopiuj token).
2. W zakładce **Bot** włącz **MESSAGE CONTENT INTENT**.
3. **OAuth2 → URL Generator**: zaznacz `bot`, uprawnienia: Send Messages, Attach Files, Embed Links, Read Message History → otwórz link i dodaj bota na serwer.
4. Na komputerze (Python 3.10+):
   ```bash
   pip install -r requirements.txt
   cp .env.example .env   # wklej token do .env
   python bot.py
   ```

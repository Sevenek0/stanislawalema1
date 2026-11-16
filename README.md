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

## 🍎 Odpalanie na Macu (dla zjebanego systemu)

Kroki 1–3 z góry (token, MESSAGE CONTENT INTENT, dodanie bota na serwer) robisz tak samo. Potem:

### 1. Zainstaluj Pythona
Otwórz **Terminal** (Cmd + Spacja → wpisz `Terminal` → Enter) i sprawdź:
```bash
python3 --version
```
- Jeśli pokaże `Python 3.10` albo nowszy, to masz go i przechodzisz dalej.
- Jeśli wyskoczy okienko z prośbą o instalację „narzędzi wiersza poleceń” albo wersja jest stara, pobierz Pythona z https://www.python.org/downloads/macos/ i zainstaluj jak zwykły program.
  - **WAŻNE:** po instalacji wejdź w Finder → Programy → folder `Python 3.x` i kliknij dwa razy **`Install Certificates.command`**. Bez tego bot wywali błąd `SSL: CERTIFICATE_VERIFY_FAILED`.

> Na Macu piszesz **`python3`** i **`pip3`**, a nie `python` i `pip`. Samo `python` nie działa.

### 2. Pobierz bota
Na GitHubie zielony przycisk **Code** → **Download ZIP** → rozpakuj (np. na Pulpit). W Terminalu przejdź do folderu, wpisz `cd ` (ze spacją), przeciągnij folder z Findera do okna Terminala i wciśnij Enter:
```bash
cd /Users/TWOJA_NAZWA/Desktop/stanislawalema1
```

### 3. Zrób wirtualne środowisko i zainstaluj biblioteki
(Bez tego macOS lubi wywalać `externally-managed-environment`.)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Jeśli zadziałało, na początku linijki w Terminalu masz `(.venv)`.

### 4. Wklej token
```bash
cp .env.example .env
open -e .env
```
Otworzy się TextEdit. Zamień `tu_wklej_token_bota` na swój token, zapisz (Cmd + S) i zamknij.

> Plik `.env` zaczyna się od kropki, więc Finder go **nie pokazuje**. Żeby go zobaczyć, wciśnij **Cmd + Shift + .** w Finderze.

### 5. Odpal
```bash
python3 bot.py
```
Jak zobaczysz `Zalogowano jako ...`, bot działa. **Nie zamykaj okna Terminala**, bo bot się wtedy wyłączy. Zatrzymujesz go przez **Ctrl + C**.

### Następnym razem
```bash
cd /ścieżka/do/stanislawalema1
source .venv/bin/activate
python3 bot.py
```

### Typowe błędy na Macu
| Błąd | Co zrobić |
|---|---|
| `command not found: python` | Pisz `python3` |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Odpal `Install Certificates.command` (krok 1) |
| `externally-managed-environment` | Zrób venv (krok 3) |
| `ModuleNotFoundError: discord` | Zapomniałeś `source .venv/bin/activate` |
| `PrivilegedIntentsRequired` | Włącz MESSAGE CONTENT INTENT w Developer Portal |
| `Brak DISCORD_TOKEN` | Plik `.env` jest pusty, źle nazwany (np. `.env.txt`) albo nie ma go w folderze bota |
| Bot zasypia, kiedy zamkniesz klapę MacBooka | Bo Mac idzie spać. Odpal `caffeinate -i python3 bot.py` i nie zamykaj klapy |

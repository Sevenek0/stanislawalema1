"""Bot Discord: zdjęcia -> GIF-y + podstawowe komendy."""
import os
import random
import re
import time

import discord
from discord.ext import commands

import gif_tools

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PREFIX = os.getenv("PREFIX", "!")
OBRAZKI = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif")

intents = discord.Intents.default()
intents.message_content = True  # trzeba też włączyć w Developer Portal!

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
START = time.time()


def _zalaczniki(ctx: commands.Context):
    return [
        a for a in ctx.message.attachments
        if (a.content_type or "").startswith("image/") or a.filename.lower().endswith(OBRAZKI)
    ]


async def _obrazki_z_wiadomosci(ctx: commands.Context):
    """Zdjęcia z wiadomości albo z wiadomości, na którą ktoś odpowiada."""
    zal = _zalaczniki(ctx)
    if not zal and ctx.message.reference:
        ref = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        zal = [a for a in ref.attachments if (a.content_type or "").startswith("image/")]
    return zal


@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user} (id: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name=f"{PREFIX}pomoc"))


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # 67 -> wypierdalaj
    if re.search(r"(?<!\d)6\s*7(?!\d)", message.content):
        await message.reply("wypierdalaj")
        return

    await bot.process_commands(message)


@bot.command(name="pomoc", aliases=["help"])
async def pomoc(ctx):
    e = discord.Embed(title="📖 Komendy", color=discord.Color.blurple())
    e.add_field(name=f"{PREFIX}gif [ms]", value="Wyślij 1+ zdjęć → GIF (kilka zdjęć = pokaz slajdów, ms = czas klatki)", inline=False)
    e.add_field(name=f"{PREFIX}efekt <nazwa>", value="1 zdjęcie → animowany GIF. Efekty: " + ", ".join(gif_tools.EFEKTY), inline=False)
    e.add_field(name=f"{PREFIX}avatargif <efekt> [@ktoś]", value="Robi GIF z avatara", inline=False)
    e.add_field(name=f"{PREFIX}ping", value="Ping bota", inline=True)
    e.add_field(name=f"{PREFIX}avatar [@ktoś]", value="Pokazuje avatar", inline=True)
    e.add_field(name=f"{PREFIX}moneta", value="Orzeł czy reszka", inline=True)
    e.add_field(name=f"{PREFIX}kostka [ścian]", value="Rzut kostką", inline=True)
    e.add_field(name=f"{PREFIX}wybierz a | b | c", value="Losuje jedną opcję", inline=True)
    e.add_field(name=f"{PREFIX}info", value="Info o bocie", inline=True)
    e.set_footer(text="Tip: możesz też odpowiedzieć (reply) na wiadomość ze zdjęciem.")
    await ctx.send(embed=e)


@bot.command()
async def gif(ctx, czas_ms: int = 500):
    zal = await _obrazki_z_wiadomosci(ctx)
    if not zal:
        return await ctx.reply(f"Wyślij zdjęcie(a) razem z `{PREFIX}gif` albo odpowiedz na wiadomość ze zdjęciem.")
    czas_ms = max(20, min(czas_ms, 5000))
    async with ctx.typing():
        try:
            dane = [await a.read() for a in zal[:10]]
            if len(dane) == 1:
                plik = gif_tools.efekt(dane[0], "puls")
            else:
                plik = gif_tools.pokaz_slajdow(dane, czas_ms)
        except Exception as ex:
            return await ctx.reply(f"Nie udało się zrobić GIF-a: {ex}")
    await ctx.reply(file=discord.File(plik, "gif.gif"))


@bot.command()
async def efekt(ctx, nazwa: str = None):
    if nazwa not in gif_tools.EFEKTY:
        return await ctx.reply("Dostępne efekty: " + ", ".join(f"`{e}`" for e in gif_tools.EFEKTY))
    zal = await _obrazki_z_wiadomosci(ctx)
    if not zal:
        return await ctx.reply(f"Wyślij zdjęcie razem z `{PREFIX}efekt {nazwa}`.")
    async with ctx.typing():
        try:
            plik = gif_tools.efekt(await zal[0].read(), nazwa)
        except Exception as ex:
            return await ctx.reply(f"Nie udało się zrobić GIF-a: {ex}")
    await ctx.reply(file=discord.File(plik, f"{nazwa}.gif"))


@bot.command()
async def avatargif(ctx, nazwa: str = "obrot", kto: discord.User = None):
    if nazwa not in gif_tools.EFEKTY:
        return await ctx.reply("Dostępne efekty: " + ", ".join(f"`{e}`" for e in gif_tools.EFEKTY))
    kto = kto or ctx.author
    async with ctx.typing():
        dane = await kto.display_avatar.replace(format="png", size=256).read()
        plik = gif_tools.efekt(dane, nazwa)
    await ctx.reply(file=discord.File(plik, f"avatar_{nazwa}.gif"))


@bot.command()
async def ping(ctx):
    await ctx.reply(f"🏓 Pong! {round(bot.latency * 1000)} ms")


@bot.command()
async def avatar(ctx, kto: discord.User = None):
    kto = kto or ctx.author
    e = discord.Embed(title=f"Avatar {kto.display_name}")
    e.set_image(url=kto.display_avatar.url)
    await ctx.send(embed=e)


@bot.command()
async def moneta(ctx):
    await ctx.reply(random.choice(["🦅 Orzeł", "🪙 Reszka"]))


@bot.command()
async def kostka(ctx, scian: int = 6):
    scian = max(2, min(scian, 1000))
    await ctx.reply(f"🎲 Wypadło: **{random.randint(1, scian)}** (k{scian})")


@bot.command()
async def wybierz(ctx, *, opcje: str = ""):
    lista = [o.strip() for o in opcje.split("|") if o.strip()]
    if len(lista) < 2:
        return await ctx.reply(f"Użycie: `{PREFIX}wybierz pizza | kebab | sushi`")
    await ctx.reply(f"🤔 Wybieram: **{random.choice(lista)}**")


@bot.command()
async def info(ctx):
    up = int(time.time() - START)
    h, r = divmod(up, 3600)
    m, s = divmod(r, 60)
    e = discord.Embed(title="🤖 Info", color=discord.Color.green())
    e.add_field(name="Serwery", value=str(len(bot.guilds)))
    e.add_field(name="Uptime", value=f"{h}h {m}m {s}s")
    e.add_field(name="Ping", value=f"{round(bot.latency * 1000)} ms")
    await ctx.send(embed=e)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, (commands.BadArgument, commands.UserNotFound)):
        return await ctx.reply(f"Złe argumenty. Wpisz `{PREFIX}pomoc`.")
    raise error


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("Brak DISCORD_TOKEN! Ustaw zmienną środowiskową albo plik .env")
    bot.run(token)

"""Funkcje do przerabiania zdjęć na GIF-y (Pillow)."""
import io
import math
import random

from PIL import Image, ImageOps

MAX_SIZE = 480  # maks. bok GIF-a w px, żeby plik nie był za duży dla Discorda
EFEKTY = ["obrot", "puls", "trzes", "tecza", "odbicie", "zoom"]


def _wczytaj(dane: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(dane))
    img = ImageOps.exif_transpose(img).convert("RGBA")
    img.thumbnail((MAX_SIZE, MAX_SIZE))
    return img


def _na_tle(img: Image.Image, rozmiar, tlo=(0, 0, 0, 0)) -> Image.Image:
    plotno = Image.new("RGBA", rozmiar, tlo)
    x = (rozmiar[0] - img.width) // 2
    y = (rozmiar[1] - img.height) // 2
    plotno.paste(img, (x, y), img)
    return plotno


def _zapisz(klatki, czas_ms: int) -> io.BytesIO:
    out = io.BytesIO()
    klatki = [k.convert("RGB").convert("P", palette=Image.ADAPTIVE) for k in klatki]
    klatki[0].save(
        out,
        format="GIF",
        save_all=True,
        append_images=klatki[1:],
        duration=czas_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )
    out.seek(0)
    return out


def pokaz_slajdow(lista_danych, czas_ms: int = 500) -> io.BytesIO:
    """Kilka zdjęć -> animowany GIF (każde zdjęcie to jedna klatka)."""
    obrazy = [_wczytaj(d) for d in lista_danych]
    szer = max(o.width for o in obrazy)
    wys = max(o.height for o in obrazy)
    klatki = [_na_tle(o, (szer, wys), (0, 0, 0, 255)) for o in obrazy]
    return _zapisz(klatki, czas_ms)


def efekt(dane: bytes, nazwa: str, n: int = 20) -> io.BytesIO:
    """Jedno zdjęcie -> animowany GIF z wybranym efektem."""
    img = _wczytaj(dane)
    w, h = img.size
    klatki = []

    if nazwa == "obrot":
        bok = int(math.hypot(w, h))
        for i in range(n):
            r = img.rotate(-360 * i / n, resample=Image.BICUBIC, expand=True)
            klatki.append(_na_tle(r, (bok, bok), (0, 0, 0, 255)))

    elif nazwa == "puls":
        for i in range(n):
            s = 0.85 + 0.15 * math.sin(2 * math.pi * i / n)
            r = img.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
            klatki.append(_na_tle(r, (w, h), (0, 0, 0, 255)))

    elif nazwa == "trzes":
        moc = max(4, min(w, h) // 25)
        for _ in range(n):
            dx, dy = random.randint(-moc, moc), random.randint(-moc, moc)
            plotno = Image.new("RGBA", (w, h), (0, 0, 0, 255))
            plotno.paste(img, (dx, dy), img)
            klatki.append(plotno)

    elif nazwa == "tecza":
        hsv = img.convert("RGB").convert("HSV")
        hch, sch, vch = hsv.split()
        for i in range(n):
            przes = int(256 * i / n)
            nowa_h = hch.point(lambda p, d=przes: (p + d) % 256)
            klatka = Image.merge("HSV", (nowa_h, sch, vch)).convert("RGBA")
            klatki.append(klatka)

    elif nazwa == "odbicie":
        lustro = ImageOps.mirror(img)
        klatki = [_na_tle(img, (w, h), (0, 0, 0, 255)), _na_tle(lustro, (w, h), (0, 0, 0, 255))]
        return _zapisz(klatki, 300)

    elif nazwa == "zoom":
        for i in range(n):
            s = 1 + 0.6 * i / (n - 1)
            cw, ch = int(w / s), int(h / s)
            x, y = (w - cw) // 2, (h - ch) // 2
            klatki.append(img.crop((x, y, x + cw, y + ch)).resize((w, h), Image.LANCZOS))
        klatki += klatki[-2:0:-1]  # w tę i z powrotem

    else:
        raise ValueError(f"Nieznany efekt: {nazwa}")

    return _zapisz(klatki, 60)

"""Prepara as imagens de exemplo do lab de visao.

- samples/bus.jpg: foto de exemplo oficial do Ultralytics (contem pessoas).
- samples/formas.png: imagem sintetica gerada localmente (NAO contem pessoa).

Uso: python samples.py
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
SAMPLES = BASE / "samples"
BUS_URL = "https://ultralytics.com/images/bus.jpg"


def main() -> None:
    SAMPLES.mkdir(exist_ok=True)

    bus = SAMPLES / "bus.jpg"
    if not bus.exists():
        print(f"baixando {BUS_URL} ...")
        urllib.request.urlretrieve(BUS_URL, bus)  # noqa: S310 - URL fixa de amostra
    print(f"ok: {bus}")

    formas = SAMPLES / "formas.png"
    if not formas.exists():
        from PIL import Image, ImageDraw  # pillow ja vem com o ultralytics

        img = Image.new("RGB", (640, 640), "#1b2130")
        d = ImageDraw.Draw(img)
        d.rectangle([60, 80, 260, 280], fill="#5b9dff")
        d.ellipse([320, 120, 560, 360], fill="#3ecf8e")
        d.polygon([(120, 560), (320, 380), (520, 560)], fill="#ffc247")
        d.rectangle([400, 420, 600, 600], outline="#ff6b6b", width=8)
        img.save(formas)
    print(f"ok: {formas}")


if __name__ == "__main__":
    main()

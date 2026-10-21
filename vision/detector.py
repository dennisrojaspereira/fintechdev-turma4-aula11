"""Classificador "tem pessoa ou nao?" com YOLOv8 (analise PREDITIVA, discriminativa).

Caso de uso fintech (ficticio): onboarding/KYC da TechPix — a selfie enviada
contem uma pessoa? Nao e geracao de texto: e um modelo treinado que PREVE
classes e caixas a partir de pixels, com confianca mensuravel.

Uso:
    python detector.py samples/bus.jpg
    python detector.py minha-foto.png --conf 0.5

Na primeira execucao o modelo yolov8n.pt (~6 MB) e baixado automaticamente.
A imagem anotada (caixas + classes) e salva em out/.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def detectar(caminho: Path, conf: float = 0.5) -> int:
    from ultralytics import YOLO  # import tardio: primeiro uso baixa o modelo

    model = YOLO(str(BASE / "yolov8n.pt"))
    resultado = model.predict(str(caminho), conf=conf, verbose=False)[0]

    deteccoes: list[tuple[str, float]] = []
    for box in resultado.boxes:
        nome = model.names[int(box.cls)]
        deteccoes.append((nome, float(box.conf)))

    print(f"Imagem: {caminho.name}  |  limiar de confianca: {conf}")
    print(f"Objetos detectados: {len(deteccoes)}")
    for nome, c in sorted(deteccoes, key=lambda d: -d[1]):
        marcador = ">>" if nome == "person" else "  "
        print(f"  {marcador} {nome:<14} confianca={c:.2f}")

    pessoas = [c for nome, c in deteccoes if nome == "person"]
    print()
    if pessoas:
        print(f"VEREDITO: PESSOA DETECTADA ({len(pessoas)}x, maior confianca {max(pessoas):.2f})")
    else:
        print("VEREDITO: NENHUMA PESSOA na imagem")

    out_dir = BASE / "out"
    out_dir.mkdir(exist_ok=True)
    anotada = out_dir / f"anotada-{caminho.stem}.jpg"
    resultado.save(str(anotada))
    print(f"Imagem anotada: {anotada.relative_to(BASE)}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("imagem", type=Path)
    p.add_argument("--conf", type=float, default=0.5)
    args = p.parse_args()
    if not args.imagem.exists():
        print(f"imagem nao encontrada: {args.imagem}")
        sys.exit(2)
    sys.exit(detectar(args.imagem, args.conf))

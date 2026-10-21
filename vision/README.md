# Lab de visão — "tem pessoa ou não?" com YOLOv8

Demo de **análise preditiva** (ML discriminativo) para contrastar com o chatbot
generativo do Lab 2. Caso fictício: KYC da TechPix — a selfie contém uma pessoa?
Conceitos em [docs/analise-preditiva.md](../docs/analise-preditiva.md).

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt   # ultralytics + torch (CPU ok)
.\.venv\Scripts\python.exe samples.py                            # baixa bus.jpg e gera formas.png
```

## Usar

```powershell
.\.venv\Scripts\python.exe detector.py samples\bus.jpg      # => PESSOA DETECTADA
.\.venv\Scripts\python.exe detector.py samples\formas.png   # => NENHUMA PESSOA
.\.venv\Scripts\python.exe detector.py qualquer-foto.jpg --conf 0.5
```

O modelo `yolov8n.pt` (~6 MB) baixa sozinho na primeira execução. A imagem
anotada (caixas + classes + confiança) sai em `out/`.

No tour (http://localhost:9000), o passo **Preditiva × Generativa** roda as duas
detecções ao vivo e exibe a imagem anotada na tela.

## O que discutir

- Limiar de confiança = decisão de negócio (recall × falso positivo).
- Golden dataset de imagens rotuladas = o "Gherkin" do modelo preditivo.
- Preditivo não alucina nem sofre injection — sofre **drift** e adversarial.

# Análise não preditiva × preditiva × generativa

Três famílias de "IA/analytics" que resolvem problemas diferentes, com formas de
validação diferentes. Misturá-las é a receita para usar a ferramenta errada.

## As três famílias

| | **Não preditiva** (descritiva/diagnóstica) | **Preditiva** (ML discriminativo) | **Generativa** (LLMs) |
|---|---|---|---|
| **Pergunta** | O que aconteceu? Por quê? | O que vai acontecer / o que é isto? | Produza algo novo (texto, código…) |
| **Saída** | Agregações, métricas, fatos | Classe/score/número + **confiança** | Conteúdo aberto, não determinístico |
| **Exemplo TechPix** | Extrato, trilha de auditoria, dashboard de UNKNOWN por hora | Score de fraude; **"a selfie do KYC contém uma pessoa?" (YOLO)** | Chatbot de FAQ (Lab 2) |
| **Verdade** | O dado em si (exato) | Rótulos de treino + distribuição real | Base de conhecimento + julgamento |
| **Como valida** | Reconciliação, testes de pipeline de dados | **Precision/recall, matriz de confusão, limiar, drift** | Evals, groundedness, guardrails, juiz |
| **Erro típico** | Número errado (bug de query) | Falso positivo / falso negativo | Alucinação, injection |

## Onde o YOLO entra

YOLO ("You Only Look Once") é um modelo **preditivo discriminativo** de visão
computacional: uma única passada da rede prevê, para cada objeto, **classe**
(ex.: `person`) + **caixa** (regressão de coordenadas) + **confiança**. Ele não
"escreve" nada — ele **classifica**. Treinado no dataset COCO (80 classes).

No lab usamos o **YOLOv8n** (nano, ~6 MB): caso fintech fictício de
onboarding/KYC — *a imagem enviada contém uma pessoa?*

```text
foto → YOLOv8n → [("person", 0.87), ("bus", 0.92), ...] → tem "person" ≥ limiar? → SIM/NÃO
```

## Pontos de engenharia (mesma disciplina da aula)

1. **O limiar de confiança é uma decisão de negócio**, não um detalhe técnico:
   baixá-lo aumenta recall (menos fraude passa sem pessoa) e aumenta falso
   positivo (manequim/foto de foto aprovada). Quem escolhe é produto + risco,
   com matriz de confusão na mesa — igual ao limite de R$ 5.000 do PRD.
2. **Oráculo independente de novo:** o teste do modelo é um conjunto rotulado
   que ele nunca viu (golden dataset de imagens) — o paralelo exato do
   `evals/dataset.json` do chatbot e do Gherkin da API.
3. **Determinismo relativo:** mesma imagem + mesmo modelo + mesmo limiar ⇒ mesma
   resposta. Diferente do LLM, dá para fazer teste de regressão clássico.
4. **Preditivo ≠ generativo nos controles:** YOLO não sofre prompt injection,
   mas sofre **drift** (câmeras novas, iluminação) e **ataques adversariais**
   — cada família tem sua superfície de risco.

## Demo do lab ([vision/](../vision/README.md))

- `samples/bus.jpg` (foto oficial de exemplo do Ultralytics) ⇒ **pessoas detectadas**.
- `samples/formas.png` (imagem sintética com formas geométricas) ⇒ **nenhuma pessoa**.
- Saída: veredito + confiança por objeto + imagem anotada com as caixas.

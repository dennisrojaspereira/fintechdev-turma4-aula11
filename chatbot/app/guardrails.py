"""Guardrails deterministicos de entrada e saida.

Regras financeiras criticas NAO dependem do LLM: sao validadas aqui, antes
(entrada) e depois (saida) da geracao. O bot e informativo — nunca executa
transferencias nem revela dados sensiveis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

MSG_INJECAO = (
    "Não posso atender a esse pedido. Sou o assistente informativo da TechPix e "
    "sigo apenas as instruções originais do serviço."
)
MSG_TRANSFERENCIA = (
    "Eu não executo transferências, pagamentos ou qualquer operação financeira. "
    "Para transferir, use o app TechPix autenticado. Posso explicar como o Pix "
    "funciona, limites, prazos e estados de uma transferência."
)
MSG_CODIGO = (
    "Não escrevo nem forneço código, scripts ou comandos por este canal. Sou o "
    "assistente informativo da TechPix: posso explicar como o Pix funciona, limites, "
    "prazos, estados de uma transferência e devoluções."
)
MSG_DADOS_PESSOAIS = (
    "Por segurança, não trato dados pessoais como CPF, senhas ou números de conta "
    "neste canal, e não tenho acesso a dados de contas. Consulte o app TechPix "
    "autenticado."
)
MSG_SAIDA_BLOQUEADA = (
    "A resposta gerada foi bloqueada pelos controles de segurança da TechPix. "
    "Reformule a pergunta de forma informativa."
)

_INJECAO = [
    r"ignore\s+(as|suas|todas|essas|minhas)?\s*(instru|regras|diretrizes)",
    r"desconsidere\s+(as|suas|todas)?\s*(instru|regras|diretrizes)",
    r"system\s*prompt",
    r"prompt\s+d[oe]\s+sistema",
    r"revele?\s+(seu|o|suas)\s+(prompt|instru|configura)",
    r"voc[eê]\s+agora\s+[eé]",
    r"finja\s+que\s+(voc[eê]|n[aã]o)",
    r"modo\s+(desenvolvedor|dan|sem\s+restri)",
    r"ignore\s+previous\s+instructions",
]

_TRANSFERENCIA = [
    r"\btransfira\b",
    r"\btransferir\s+(r\$|\d)",
    r"\b(fa[cç]a|execute|realize|envie|mande)\b.{0,40}\b(pix|transfer[eê]ncia|pagamento)\b",
    r"\bpague?\b.{0,30}\b(boleto|conta|r\$)",
    r"\bagende?\b.{0,30}\b(pix|transfer[eê]ncia)\b",
]

_PEDIDO_CODIGO = [
    r"\b(escreva|gere|fa[çc]a|crie|monte|mostre|me\s+d[eê])\b.{0,50}\b(c[oó]digo|script|fun[çc][aã]o|programa|classe|snippet|query|sql)\b",
    r"\bc[oó]digo\s+(em|no|de|para)\b",
    r"\b(python|javascript|typescript|java|c#|golang|rust|sql)\b.{0,30}\b(c[oó]digo|script|fun[çc][aã]o|exemplo de implementa)",
    r"\bem\s+(python|javascript|typescript|java|golang|rust)\b",
    r"\bimplemente\b",
]

_DADOS_PESSOAIS = [
    r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",  # CPF
    r"\bmeu\s+(saldo|extrato|cpf|cart[aã]o)\b",
    r"\bsenha\b",
    r"\bn[uú]mero\s+d[ae]\s+(conta|cart[aã]o)\b",
]

_SAIDA_PROIBIDA = [
    r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",                 # CPF
    r"(?i)(api[_-]?key|secret[_-]?key|senha)\s*[:=]\s*\S+",  # segredos
    r"(?i)transfer[eê]ncia\s+(realizada|efetuada|conclu[ií]da)",  # bot "executou" algo
    r"```",                                               # bloco de codigo gerado
    r"(?m)^\s*(def |class \w+[:(]|import \w+|from \w+ import )",  # codigo python solto
]


@dataclass
class Decisao:
    permitido: bool
    motivo: str | None = None
    resposta: str | None = None


def _match(padroes: list[str], texto: str) -> bool:
    return any(re.search(p, texto, flags=re.IGNORECASE) for p in padroes)


def avaliar_entrada(pergunta: str) -> Decisao:
    if _match(_INJECAO, pergunta):
        return Decisao(False, "prompt_injection", MSG_INJECAO)
    if _match(_TRANSFERENCIA, pergunta):
        return Decisao(False, "operacao_financeira", MSG_TRANSFERENCIA)
    if _match(_PEDIDO_CODIGO, pergunta):
        return Decisao(False, "pedido_de_codigo", MSG_CODIGO)
    if _match(_DADOS_PESSOAIS, pergunta):
        return Decisao(False, "dados_pessoais", MSG_DADOS_PESSOAIS)
    return Decisao(True)


def avaliar_saida(resposta: str) -> Decisao:
    if _match(_SAIDA_PROIBIDA, resposta):
        return Decisao(False, "saida_proibida", MSG_SAIDA_BLOQUEADA)
    return Decisao(True)

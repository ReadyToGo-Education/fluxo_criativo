"""Persona Sofia — Analista de Performance RTG.

Tom: direto, pedagógico, acionável. Linguagem: VTSD sempre presente. Foco:
decisão > descrição.

Este módulo centraliza o "jeito de falar" da skill — frases de abertura, de
fechamento, formato de CTAs. Todos os templates e mensagens da CLI devem
consumir daqui quando precisarem de uma voz consistente.

A persona é independente e autossuficiente.
"""

from __future__ import annotations

import random

# --- Identidade ------------------------------------------------------------

NOME = "Sofia"
PAPEL = "Analista de Performance RTG"
TAGLINE = "Análise de Tráfego · Método VTSD"


# --- Aberturas (usar aleatório pra não soar robótico) --------------------

ABERTURAS: list[str] = [
    "Vamos analisar. Olhando esses números pela lente VTSD:",
    "Puxei os dados. Aqui está o que eu vejo:",
    "Analisando os números:",
    "Bora ler isso pelo método:",
]


FECHAMENTOS: list[str] = [
    "É isso. O dado mostra. A ação está clara.",
    "Decisão > descrição. Execute isso e me chame quando os números movimentarem.",
    "Análise feita. Agora é ação.",
    "Saiu. Qualquer dúvida sobre a interpretação, estou aqui.",
]


def abertura(seed: int | None = None) -> str:
    """Frase aleatória de abertura. Pass seed pra reprodutibilidade em testes."""
    rnd = random.Random(seed) if seed is not None else random
    return rnd.choice(ABERTURAS)


def fechamento(seed: int | None = None) -> str:
    rnd = random.Random(seed) if seed is not None else random
    return rnd.choice(FECHAMENTOS)


# --- Template de cabeçalho padrão -----------------------------------------

HEADER_TEMPLATE = """\
╔══════════════════════════════════════════╗
║  SOFIA — Analista de Performance RTG     ║
║  Análise de Tráfego · Método VTSD        ║
╚══════════════════════════════════════════╝
"""


# --- CTAs acionáveis (formato padrão) -------------------------------------

def cta_pausar(recurso: str, motivo: str) -> str:
    return f"🛑 **Pausar agora:** {recurso} — {motivo}"


def cta_escalar(recurso: str, incremento_pct: float) -> str:
    return f"🚀 **Escalar:** {recurso} — subir budget em +{incremento_pct:.0f}%"


def cta_testar(recurso: str, hipotese: str) -> str:
    return f"🧪 **Testar:** {recurso} — {hipotese}"


def cta_revisar(recurso: str, elemento_vtsd: str) -> str:
    return f"🔍 **Revisar:** {recurso} — {elemento_vtsd} aparentemente falhando"


# --- Diagnóstico estruturado ----------------------------------------------

def diagnostico(texto: str) -> str:
    return f"📊 **Diagnóstico:** {texto}"


def no_vtsd(texto: str) -> str:
    return f"🎯 **No VTSD, isso significa:** {texto}"


def acao(texto: str) -> str:
    return f"✅ **Ação:** {texto}"

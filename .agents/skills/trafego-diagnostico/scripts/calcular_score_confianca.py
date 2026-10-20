#!/usr/bin/env python3
"""
Score de confiança por decisão para /trafego-diagnostico.

Recebe um JSON com as 10 variáveis e devolve o score (0 a 100), a faixa,
a pontuação de cada variável e sugestões para aumentar a confiança.

Só faz conta: não chama a Graph API, não lê o .env, não usa token.

Uso (rodar da raiz do projeto, com o interpretador detectado na sessão,
python3 ou py -3, conforme o CLAUDE.md):

    echo '{"gasto": 350, "conversoes": 8, "dias": 7}' | python3 .claude/skills/trafego-diagnostico/scripts/calcular_score_confianca.py
    python3 .claude/skills/trafego-diagnostico/scripts/calcular_score_confianca.py entrada.json

Percentuais entram como fração: 0.18 significa 18%.
Variável ausente (ou null) vale 0 ponto e aparece em "variaveis_indisponiveis".
Com menos de 7 dias de dado, a faixa é dados_insuficientes, qualquer que seja
o score (o número fica e o campo "aviso" explica a trava).

Só biblioteca padrão. Sem dependência externa.
"""

import json
import math
import re
import sys


def _numero(valor):
    """Converte o valor para float. Devolve None se não for número válido."""
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        monetario = "R$" in valor
        texto = valor.strip().replace("R$", "").replace(" ", "")
        percentual = texto.endswith("%")
        texto = texto.rstrip("%")
        if "," in texto:
            # Formato brasileiro: 1.234,56
            texto = texto.replace(".", "").replace(",", ".")
        elif monetario and re.fullmatch(r"\d{1,3}(\.\d{3})+", texto):
            # Valor em reais sem centavos: "R$ 1.000" é mil, não 1,0.
            # Só para texto com "R$": em fração ("0.300") o ponto é decimal.
            texto = texto.replace(".", "")
        try:
            numero = float(texto)
        except ValueError:
            return None
        return numero / 100 if percentual else numero
    return None


def pontuar_gasto(valor):
    """0 pts: <50 | 5 pts: 50 a 500 | 10 pts: >500"""
    valor = _numero(valor)
    if valor is None or valor < 0:
        return 0
    if valor > 500:
        return 10
    if valor >= 50:
        return 5
    return 0


def pontuar_conversoes(valor):
    """0 pts: 0 a 2 | 5 pts: 3 a 15 | 10 pts: >15"""
    valor = _numero(valor)
    if valor is None or valor < 0:
        return 0
    if valor > 15:
        return 10
    if valor >= 3:
        return 5
    return 0


def pontuar_dias(valor):
    """0 pts: <3 | 5 pts: 3 a 6 | 10 pts: 7 ou mais"""
    valor = _numero(valor)
    if valor is None or valor < 0:
        return 0
    if valor >= 7:
        return 10
    if valor >= 3:
        return 5
    return 0


def pontuar_consistencia_cv(valor):
    """0 pts: CV>0.60 | 5 pts: 0.30 a 0.60 | 10 pts: <0.30"""
    valor = _numero(valor)
    if valor is None or valor < 0:
        return 0
    if valor < 0.30:
        return 10
    if valor <= 0.60:
        return 5
    return 0


def pontuar_variacao_periodo(valor):
    """Variação vs período anterior, em fração (sinal ignorado).
    0 pts: >40% | 5 pts: 20% a 40% | 10 pts: <20%"""
    valor = _numero(valor)
    if valor is None:
        return 0
    valor = abs(valor)
    if valor < 0.20:
        return 10
    if valor <= 0.40:
        return 5
    return 0


def pontuar_frequencia(valor):
    """0 pts: >4.0 | 5 pts: 2.0 a 4.0 | 10 pts: <2.0"""
    valor = _numero(valor)
    if valor is None or valor < 0:
        return 0
    if valor < 2.0:
        return 10
    if valor <= 4.0:
        return 5
    return 0


def pontuar_concentracao(valor):
    """Fração do gasto concentrada no anúncio que mais gasta.
    0 pts: >80% | 5 pts: 40% a 80% | 10 pts: <40%"""
    valor = _numero(valor)
    if valor is None or valor < 0:
        return 0
    if valor < 0.40:
        return 10
    if valor <= 0.80:
        return 5
    return 0


def pontuar_remarketing(valor):
    """Fração do resultado que vem de remarketing.
    0 pts: >70% | 5 pts: 40% a 70% | 10 pts: <40%"""
    valor = _numero(valor)
    if valor is None or valor < 0:
        return 0
    if valor < 0.40:
        return 10
    if valor <= 0.70:
        return 5
    return 0


PONTOS_ATRIBUICAO = {
    "pixel_capi": 10,
    "pixel_ativo": 5,
    "pixel_sem_capi": 3,
    "janela_desconhecida": 2,
    "sem_pixel": 0,
}


def pontuar_atribuicao(valor):
    """pixel_capi 10 | pixel_ativo 5 | pixel_sem_capi 3 | janela_desconhecida 2 | sem_pixel 0"""
    if not isinstance(valor, str):
        return 0
    return PONTOS_ATRIBUICAO.get(valor.strip().lower(), 0)


def pontuar_distancia_meta(valor):
    """Razão CPA atual / CPA meta (ou CPL atual / CPL meta).
    0 pts: >2x | 5 pts: 1.3x a 2x | 10 pts: até 1.3x"""
    valor = _numero(valor)
    if valor is None or valor < 0:
        return 0
    if valor <= 1.3:
        return 10
    if valor <= 2.0:
        return 5
    return 0


def classificar_faixa(score):
    if score >= 75:
        return "alta_confianca"
    if score >= 50:
        return "media_confianca"
    if score >= 25:
        return "baixa_confianca"
    return "dados_insuficientes"


def sugestoes(dados, variaveis_pontuadas):
    sug = []
    if variaveis_pontuadas["conversoes"]["pontos"] < 10:
        atual = _numero(dados.get("conversoes")) or 0
        faltam = int(16 - atual)
        if faltam > 0:
            sug.append(f"+{faltam} conversões (para amostra mais confiável)")
    if variaveis_pontuadas["dias_analisados"]["pontos"] < 10:
        atual = _numero(dados.get("dias")) or 0
        faltam = math.ceil(7 - atual)
        if faltam > 0:
            sug.append(f"+{faltam} {'dia' if faltam == 1 else 'dias'} de dados")
    if variaveis_pontuadas["consistencia_cv"]["pontos"] < 5:
        sug.append("Reduzir a variação diária (estabilizar criativos e orçamento)")
    # Sem valor (ex.: entidade de nível anúncio, em que a variável não se aplica),
    # não sugerir diversificar: a variável só aparece em variaveis_indisponiveis.
    if (
        dados.get("pct_gasto_top1_anuncio") is not None
        and variaveis_pontuadas["concentracao_top1"]["pontos"] < 5
    ):
        sug.append("Diversificar criativos para reduzir a concentração de gasto")
    if variaveis_pontuadas["dependencia_remarketing"]["pontos"] < 5:
        sug.append("Aumentar a proporção de prospecção em relação ao remarketing")
    if variaveis_pontuadas["qualidade_atribuicao"]["pontos"] < 5:
        sug.append("Ativar a API de Conversões (CAPI) para melhorar a qualidade de atribuição")
    return sug


def calcular(dados):
    funcoes = {
        "volume_gasto": ("gasto", pontuar_gasto),
        "conversoes": ("conversoes", pontuar_conversoes),
        "dias_analisados": ("dias", pontuar_dias),
        "consistencia_cv": ("cv_metrica_norte", pontuar_consistencia_cv),
        "variacao_periodo": ("variacao_periodo_pct", pontuar_variacao_periodo),
        "frequencia": ("frequencia", pontuar_frequencia),
        "concentracao_top1": ("pct_gasto_top1_anuncio", pontuar_concentracao),
        "dependencia_remarketing": ("pct_remarketing", pontuar_remarketing),
        "qualidade_atribuicao": ("qualidade_atribuicao", pontuar_atribuicao),
        "distancia_meta": ("cpa_sobre_target", pontuar_distancia_meta),
    }

    variaveis_pontuadas = {}
    indisponiveis = []

    for nome_var, (chave_json, func) in funcoes.items():
        valor = dados.get(chave_json)
        pontos = func(valor)
        variaveis_pontuadas[nome_var] = {"valor": valor, "pontos": pontos}
        if valor is None:
            indisponiveis.append(nome_var)

    score = sum(v["pontos"] for v in variaveis_pontuadas.values())
    faixa = classificar_faixa(score)

    # Trava pelos dias (princípio 12 do SKILL.md): com menos de 7 dias de dado,
    # a faixa é dados_insuficientes, qualquer que seja o score. O número fica.
    aviso = None
    dias = _numero(dados.get("dias"))
    if dias is not None and dias < 7 and faixa != "dados_insuficientes":
        aviso = (
            f"Menos de 7 dias de dado ({dias:g}): faixa travada em dados_insuficientes. "
            f"Sem a trava, o score {score} daria {faixa}."
        )
        faixa = "dados_insuficientes"

    risco = "baixo"
    if faixa == "dados_insuficientes":
        risco = "critico"
    elif faixa == "baixa_confianca":
        risco = "alto"
    elif faixa == "media_confianca":
        risco = "medio"

    resultado = {
        "score": score,
        "faixa": faixa,
        "risco_da_decisao": risco,
        "variaveis": variaveis_pontuadas,
        "variaveis_indisponiveis": indisponiveis,
        "o_que_aumentaria_confianca": sugestoes(dados, variaveis_pontuadas),
    }
    if aviso:
        resultado["aviso"] = aviso
    return resultado


def _ler_entrada():
    """Lê o JSON do arquivo passado como argumento ou, sem argumento, do stdin (UTF-8)."""
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8-sig") as arquivo:
            return arquivo.read()
    return sys.stdin.buffer.read().decode("utf-8-sig")


def _sair_com_erro(mensagem):
    print(json.dumps({"erro": mensagem}, ensure_ascii=False))
    sys.exit(1)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    try:
        bruto = _ler_entrada()
    except OSError as e:
        _sair_com_erro(f"Não consegui ler o arquivo de entrada: {e}")
    try:
        dados = json.loads(bruto)
    except json.JSONDecodeError as e:
        _sair_com_erro(f"JSON inválido: {e}")
    if not isinstance(dados, dict):
        _sair_com_erro("A entrada precisa ser um objeto JSON com as 10 variáveis.")
    resultado = calcular(dados)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

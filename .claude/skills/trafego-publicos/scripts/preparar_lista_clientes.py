#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepara uma lista de clientes (CSV) para o público de lista de clientes da Meta.

Tudo acontece no computador do aluno, sem internet e sem token:

1. Lê o CSV e detecta as colunas de e-mail, telefone, nome, sobrenome,
   cidade, estado, CEP e país (só as que existirem).
2. Normaliza cada valor pelas regras da Meta:
   - e-mail: minúsculo, sem espaços;
   - telefone: só dígitos, com código do país (55 quando faltar);
   - nome e sobrenome: minúsculos, sem acento, sem pontuação
     (nome = primeira palavra, sobrenome = última palavra);
   - cidade e estado: minúsculos, sem acento, sem espaço e sem pontuação;
   - CEP: só letras minúsculas e dígitos, sem espaço e sem traço;
   - país: código de 2 letras em minúsculo (ex: br).
3. Transforma cada valor num código SHA-256 (hash). O valor original nunca
   é gravado em arquivo.
4. Grava lotes de no máximo 10.000 linhas no formato "payload" da Meta
   (schema + data), um arquivo JSON por lote.
5. Mostra na tela só contagens. Nenhum dado pessoal é exibido.

Uso (a partir da raiz do projeto, com o Python detectado na sessão):

    python3 .claude/skills/trafego-publicos/scripts/preparar_lista_clientes.py \
        <caminho_do_csv> <pasta_de_saida> [--ddi 55] [--tamanho-lote 10000] \
        [--campos email,telefone] [--coluna email="Nome da coluna"]

Só usa a biblioteca padrão do Python. Não abre conexão com a internet e não
lê o .env.
"""

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

LIMITE_META_POR_LOTE = 10000
MINIMO_META = 100

# Ordem dos campos no schema da Meta (formato de várias chaves).
ORDEM_CAMPOS = ["EMAIL", "PHONE", "FN", "LN", "CT", "ST", "ZIP", "COUNTRY"]

ROTULOS = {
    "EMAIL": "e-mail",
    "PHONE": "telefone",
    "FN": "nome",
    "LN": "sobrenome",
    "CT": "cidade",
    "ST": "estado",
    "ZIP": "CEP",
    "COUNTRY": "país",
}

# Nomes aceitos no --coluna (sem acento, minúsculos).
APELIDOS_COLUNA = {
    "email": "EMAIL",
    "telefone": "PHONE",
    "phone": "PHONE",
    "nome": "FN",
    "nome_completo": "NOME_COMPLETO",
    "sobrenome": "LN",
    "cidade": "CT",
    "estado": "ST",
    "cep": "ZIP",
    "pais": "COUNTRY",
    "ddd": "DDD",
}

# Palavras que indicam coluna de outra pessoa ou de outra coisa (não do cliente).
PALAVRAS_EXCLUIDAS = {
    "produto", "product", "oferta", "offer", "plano", "afiliado", "affiliate",
    "afiliacao", "empresa", "company", "loja", "campanha", "curso", "pagina",
    "page", "arquivo", "cupom", "vendedor", "produtor", "coprodutor", "recebedor",
}

# Palavras que indicam outro significado para "estado" (situação, não UF).
PALAVRAS_EXCLUIDAS_ESTADO = {"compra", "pagamento", "transacao", "pedido", "civil", "status", "assinatura"}

# Palavras que deixam a coluna preferida quando há mais de uma candidata.
PALAVRAS_PREFERIDAS = {"comprador", "cliente", "buyer", "customer", "aluno", "lead", "contato"}

PAISES = {
    "br": "br", "bra": "br", "brasil": "br", "brazil": "br",
    "pt": "pt", "prt": "pt", "portugal": "pt",
    "us": "us", "usa": "us", "eua": "us", "estados unidos": "us", "united states": "us",
    "ar": "ar", "argentina": "ar",
    "mx": "mx", "mexico": "mx",
    "es": "es", "espanha": "es", "espana": "es", "spain": "es",
    "cl": "cl", "chile": "cl",
    "co": "co", "colombia": "co",
    "uy": "uy", "uruguai": "uy", "uruguay": "uy",
    "py": "py", "paraguai": "py", "paraguay": "py",
    "pe": "pe", "peru": "pe",
    "ca": "ca", "canada": "ca",
    "gb": "gb", "uk": "gb", "reino unido": "gb", "united kingdom": "gb",
    "fr": "fr", "franca": "fr", "france": "fr",
    "de": "de", "alemanha": "de", "germany": "de",
    "it": "it", "italia": "it", "italy": "it",
    "jp": "jp", "japao": "jp", "japan": "jp",
    "ao": "ao", "angola": "ao",
    "mz": "mz", "mocambique": "mz", "mozambique": "mz",
}

RE_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[a-z]{2,}")


def sem_acento(texto):
    """Remove acentos e cedilha mantendo as letras."""
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def normalizar_cabecalho(texto):
    """Cabeçalho em minúsculo, sem acento e com palavras separadas por espaço."""
    texto = sem_acento(texto or "").lower()
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return texto.strip()


def classificar_cabecalho(cabecalho):
    """Devolve o campo que o cabeçalho representa, ou None."""
    texto = normalizar_cabecalho(cabecalho)
    palavras = set(texto.split())
    if not palavras or palavras & PALAVRAS_EXCLUIDAS:
        return None

    if "email" in palavras or "e mail" in texto or texto == "mail":
        return "EMAIL"
    if texto == "ddd" or texto.startswith("ddd "):
        return "DDD"
    if palavras & {"telefone", "celular", "phone", "whatsapp", "fone", "tel", "mobile", "zap"}:
        return "PHONE"
    if palavras & {"sobrenome", "surname"} or "last name" in texto or "ultimo nome" in texto:
        return "LN"
    if "primeiro nome" in texto or "first name" in texto or texto == "fn":
        return "FN"
    if "nome" in palavras or "name" in palavras:
        return "NOME_COMPLETO"
    if palavras & {"cidade", "city", "municipio"}:
        return "CT"
    if (palavras & {"estado", "uf", "state", "provincia"}) and not (palavras & PALAVRAS_EXCLUIDAS_ESTADO):
        return "ST"
    if palavras & {"cep", "zip", "postal"} or "codigo postal" in texto:
        return "ZIP"
    if palavras & {"pais", "country"}:
        return "COUNTRY"
    return None


def parece_dado(celula):
    """Indica se uma célula do cabeçalho parece ser um dado (arquivo sem cabeçalho)."""
    if "@" in celula:
        return True
    return len(re.sub(r"\D", "", celula)) >= 8


def escolher_colunas(cabecalhos, forcadas):
    """Mapeia cada campo para o índice de uma coluna do CSV."""
    candidatas = {}
    for indice, cabecalho in enumerate(cabecalhos):
        campo = classificar_cabecalho(cabecalho)
        if campo:
            candidatas.setdefault(campo, []).append(indice)

    escolhidas = {}
    for campo, indices in candidatas.items():
        preferidas = [
            i for i in indices
            if set(normalizar_cabecalho(cabecalhos[i]).split()) & PALAVRAS_PREFERIDAS
        ]
        escolhidas[campo] = (preferidas or indices)[0]

    for campo, nome_coluna in forcadas.items():
        alvo = normalizar_cabecalho(nome_coluna)
        achou = [i for i, c in enumerate(cabecalhos) if normalizar_cabecalho(c) == alvo]
        if not achou:
            raise SystemExit(
                f"Erro: a coluna indicada para {ROTULOS.get(campo, campo.lower())} "
                "não foi encontrada no CSV. Confira o nome exato do cabeçalho."
            )
        escolhidas[campo] = achou[0]

    # Nome completo só vira nome/sobrenome quando não há coluna própria.
    if "NOME_COMPLETO" in escolhidas:
        indice = escolhidas.pop("NOME_COMPLETO")
        escolhidas.setdefault("FN_COMPLETO", indice)
    return escolhidas


def normalizar_email(valor):
    valor = re.sub(r"\s+", "", valor).lower()
    return valor if RE_EMAIL.fullmatch(valor) else None


def normalizar_telefone(valor, ddd, ddi):
    bruto = valor.strip()
    ja_tem_ddi = bruto.startswith("+") or bruto.startswith("00")
    digitos = re.sub(r"\D", "", bruto)
    if ddd:
        digitos_ddd = re.sub(r"\D", "", ddd)
        if digitos_ddd and len(digitos) in (8, 9):
            digitos = digitos_ddd + digitos
    digitos = digitos.lstrip("0")
    if not ja_tem_ddi and len(digitos) in (10, 11):
        digitos = ddi + digitos
    if not 10 <= len(digitos) <= 15:
        return None
    return digitos


def palavras_de_nome(valor):
    texto = sem_acento(valor).lower()
    texto = re.sub(r"[^a-z]+", " ", texto)
    return texto.split()


def normalizar_compacto(valor):
    """Cidade e estado: minúsculo, sem acento, sem espaço e sem pontuação."""
    texto = sem_acento(valor).lower()
    texto = re.sub(r"[^a-z]+", "", texto)
    return texto or None


def normalizar_cep(valor):
    texto = re.sub(r"[^0-9a-z]+", "", sem_acento(valor).lower())
    return texto if len(texto) >= 3 else None


def normalizar_pais(valor):
    texto = re.sub(r"[^a-z ]+", " ", sem_acento(valor).lower())
    texto = re.sub(r"\s+", " ", texto).strip()
    if texto in PAISES:
        return PAISES[texto]
    return None


def gerar_hash(valor):
    return hashlib.sha256(valor.encode("utf-8")).hexdigest()


def formatar_numero(numero):
    """Número com ponto de milhar (ex: 10.000)."""
    return f"{numero:,}".replace(",", ".")


def ler_texto(caminho):
    dados = caminho.read_bytes()
    for codificacao in ("utf-8-sig", "cp1252"):
        try:
            return dados.decode(codificacao)
        except UnicodeDecodeError:
            continue
    raise SystemExit("Erro: não consegui ler o arquivo. Salve o CSV em UTF-8 e tente de novo.")


def detectar_separador(texto):
    amostra = texto[:20000]
    try:
        return csv.Sniffer().sniff(amostra, delimiters=",;\t|").delimiter
    except csv.Error:
        primeira = amostra.splitlines()[0] if amostra else ""
        return ";" if primeira.count(";") > primeira.count(",") else ","


def interpretar_colunas_forcadas(lista):
    forcadas = {}
    for item in lista or []:
        if "=" not in item:
            raise SystemExit('Erro: use --coluna no formato campo="Nome da coluna" (ex: email="E-mail").')
        chave, nome = item.split("=", 1)
        campo = APELIDOS_COLUNA.get(normalizar_cabecalho(chave).replace(" ", "_"))
        if not campo:
            raise SystemExit(
                "Erro: campo desconhecido em --coluna. Use email, telefone, nome, "
                "nome_completo, sobrenome, cidade, estado, cep, pais ou ddd."
            )
        forcadas[campo] = nome.strip().strip('"').strip("'")
    return forcadas


def ajustar_saida_utf8():
    """Garante acentuação correta nas mensagens, inclusive no terminal do Windows."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main():
    ajustar_saida_utf8()
    parser = argparse.ArgumentParser(
        description="Normaliza e aplica hash SHA-256 numa lista de clientes (CSV), gerando lotes no formato da Meta."
    )
    parser.add_argument("csv", help="caminho do arquivo CSV")
    parser.add_argument("saida", help="pasta onde os lotes JSON serão gravados")
    parser.add_argument("--ddi", default="55", help="código do país usado quando o telefone não tem (padrão: 55)")
    parser.add_argument(
        "--tamanho-lote", type=int, default=LIMITE_META_POR_LOTE,
        help="linhas por lote (máximo 10.000, limite da Meta)",
    )
    parser.add_argument(
        "--coluna", action="append",
        help='indica a coluna manualmente, ex: --coluna email="E-mail do comprador"',
    )
    parser.add_argument(
        "--campos",
        help="limita os campos enviados, ex: --campos email,telefone (padrão: todos os detectados)",
    )
    args = parser.parse_args()

    caminho_csv = Path(args.csv).expanduser()
    pasta_saida = Path(args.saida).expanduser()
    ddi = re.sub(r"\D", "", args.ddi) or "55"
    tamanho_lote = args.tamanho_lote
    if tamanho_lote < 1 or tamanho_lote > LIMITE_META_POR_LOTE:
        raise SystemExit("Erro: --tamanho-lote precisa ficar entre 1 e 10.000.")

    if not caminho_csv.is_file():
        raise SystemExit("Erro: o arquivo CSV não foi encontrado nesse caminho.")

    if pasta_saida.is_dir() and any(pasta_saida.glob("lote-*.json")):
        raise SystemExit(
            "Erro: a pasta de saída já tem lotes de uma preparação anterior. "
            "Apague esses lotes ou escolha uma pasta vazia."
        )

    forcadas = interpretar_colunas_forcadas(args.coluna)
    texto = ler_texto(caminho_csv)
    leitor = csv.reader(texto.splitlines(), delimiter=detectar_separador(texto))

    try:
        cabecalhos = next(leitor)
    except StopIteration:
        raise SystemExit("Erro: o CSV está vazio.")
    except csv.Error:
        raise SystemExit("Erro: não consegui interpretar a primeira linha do CSV.")

    if any(parece_dado(c) for c in cabecalhos):
        raise SystemExit(
            "Erro: a primeira linha parece ter dados de clientes, não nomes de colunas. "
            "Coloque uma linha de cabeçalho (ex: Email;Telefone;Nome) e rode de novo."
        )

    colunas = escolher_colunas(cabecalhos, forcadas)
    if "EMAIL" not in colunas and "PHONE" not in colunas:
        raise SystemExit(
            "Erro: não encontrei coluna de e-mail nem de telefone. Indique com "
            '--coluna email="Nome da coluna" ou --coluna telefone="Nome da coluna".'
        )

    campos_no_schema = [c for c in ORDEM_CAMPOS if c in colunas]
    if "FN_COMPLETO" in colunas:
        for campo in ("FN", "LN"):
            if campo not in campos_no_schema:
                campos_no_schema.append(campo)
        campos_no_schema = [c for c in ORDEM_CAMPOS if c in campos_no_schema]

    if args.campos:
        pedidos = set()
        for item in args.campos.split(","):
            campo = APELIDOS_COLUNA.get(normalizar_cabecalho(item).replace(" ", "_"))
            if campo == "NOME_COMPLETO":
                pedidos.update({"FN", "LN"})
            elif campo in ORDEM_CAMPOS:
                pedidos.add(campo)
            else:
                raise SystemExit(
                    "Erro: campo desconhecido em --campos. Use email, telefone, nome, "
                    "sobrenome, cidade, estado, cep ou pais."
                )
        campos_no_schema = [c for c in campos_no_schema if c in pedidos]
        if "EMAIL" not in campos_no_schema and "PHONE" not in campos_no_schema:
            raise SystemExit("Erro: --campos precisa incluir email ou telefone.")

    contagem = {
        "linhas_lidas": 0,
        "linhas_vazias": 0,
        "sem_identificador": 0,
        "duplicadas": 0,
    }
    em_branco = {c: 0 for c in campos_no_schema}
    invalidos = {c: 0 for c in campos_no_schema}

    vistos = set()
    linhas_hash = []

    def valor_da(linha, campo):
        indice = colunas.get(campo)
        if indice is None or indice >= len(linha):
            return ""
        return (linha[indice] or "").strip()

    numero_linha = 1
    try:
        for linha in leitor:
            numero_linha += 1
            if not any((c or "").strip() for c in linha):
                contagem["linhas_vazias"] += 1
                continue
            contagem["linhas_lidas"] += 1

            normalizados = {}

            if "EMAIL" in campos_no_schema:
                bruto = valor_da(linha, "EMAIL")
                if not bruto:
                    em_branco["EMAIL"] += 1
                else:
                    valor = normalizar_email(bruto)
                    if valor:
                        normalizados["EMAIL"] = valor
                    else:
                        invalidos["EMAIL"] += 1

            if "PHONE" in campos_no_schema:
                bruto = valor_da(linha, "PHONE")
                if not bruto:
                    em_branco["PHONE"] += 1
                else:
                    valor = normalizar_telefone(bruto, valor_da(linha, "DDD"), ddi)
                    if valor:
                        normalizados["PHONE"] = valor
                    else:
                        invalidos["PHONE"] += 1

            # Nome e sobrenome (coluna própria ou nome completo dividido).
            nome_bruto = valor_da(linha, "FN") if "FN" in colunas else ""
            sobrenome_bruto = valor_da(linha, "LN") if "LN" in colunas else ""
            completo_bruto = valor_da(linha, "FN_COMPLETO") if "FN_COMPLETO" in colunas else ""

            if "FN" in campos_no_schema:
                palavras = palavras_de_nome(nome_bruto or completo_bruto)
                if not (nome_bruto or completo_bruto):
                    em_branco["FN"] += 1
                elif palavras:
                    normalizados["FN"] = palavras[0]
                else:
                    invalidos["FN"] += 1

            if "LN" in campos_no_schema:
                if sobrenome_bruto:
                    palavras = palavras_de_nome(sobrenome_bruto)
                else:
                    palavras = palavras_de_nome(completo_bruto)
                    palavras = palavras[1:] if len(palavras) > 1 else []
                if not (sobrenome_bruto or completo_bruto):
                    em_branco["LN"] += 1
                elif palavras:
                    normalizados["LN"] = palavras[-1]
                else:
                    invalidos["LN"] += 1

            for campo, funcao in (
                ("CT", normalizar_compacto),
                ("ST", normalizar_compacto),
                ("ZIP", normalizar_cep),
                ("COUNTRY", normalizar_pais),
            ):
                if campo not in campos_no_schema:
                    continue
                bruto = valor_da(linha, campo)
                if not bruto:
                    em_branco[campo] += 1
                    continue
                valor = funcao(bruto)
                if valor:
                    normalizados[campo] = valor
                else:
                    invalidos[campo] += 1

            if "EMAIL" not in normalizados and "PHONE" not in normalizados:
                contagem["sem_identificador"] += 1
                continue

            registro = tuple(
                gerar_hash(normalizados[c]) if c in normalizados else ""
                for c in campos_no_schema
            )
            if registro in vistos:
                contagem["duplicadas"] += 1
                continue
            vistos.add(registro)
            linhas_hash.append(list(registro))
    except csv.Error:
        raise SystemExit(f"Erro: o CSV tem um problema de formato perto da linha {numero_linha}.")

    pasta_saida.mkdir(parents=True, exist_ok=True)
    lotes = []
    for inicio in range(0, len(linhas_hash), tamanho_lote):
        numero = len(lotes) + 1
        destino = pasta_saida / f"lote-{numero:03d}.json"
        payload = {"schema": campos_no_schema, "data": linhas_hash[inicio:inicio + tamanho_lote]}
        destino.write_text(json.dumps(payload, ensure_ascii=True), encoding="utf-8")
        lotes.append((destino.name, len(payload["data"])))

    validas = len(linhas_hash)
    print("Preparação da lista de clientes concluída (nenhum dado pessoal exibido).")
    print("")
    print("Colunas usadas:")
    for campo in ORDEM_CAMPOS:
        if campo in colunas and campo in campos_no_schema:
            print(f"  - {ROTULOS[campo]}: coluna \"{cabecalhos[colunas[campo]]}\"")
    if "FN_COMPLETO" in colunas and ("FN" in campos_no_schema or "LN" in campos_no_schema):
        print(f"  - nome e sobrenome: divididos da coluna \"{cabecalhos[colunas['FN_COMPLETO']]}\"")
    if "DDD" in colunas and "PHONE" in campos_no_schema:
        print(f"  - DDD: coluna \"{cabecalhos[colunas['DDD']]}\" (juntado ao telefone)")
    print("")
    print("Contagens:")
    print(f"  - linhas lidas: {contagem['linhas_lidas']}")
    print(f"  - linhas válidas (enviáveis): {validas}")
    print(f"  - descartadas sem e-mail nem telefone válidos: {contagem['sem_identificador']}")
    print(f"  - duplicadas removidas: {contagem['duplicadas']}")
    if contagem["linhas_vazias"]:
        print(f"  - linhas em branco ignoradas: {contagem['linhas_vazias']}")
    print("")
    print("Por campo (inválidos / em branco):")
    lidas = contagem["linhas_lidas"] or 1
    for campo in campos_no_schema:
        percentual = round(100 * invalidos[campo] / lidas)
        print(f"  - {ROTULOS[campo]}: {invalidos[campo]} inválidos ({percentual}%) / {em_branco[campo]} em branco")
    print("")
    print(f"Schema dos lotes: {', '.join(campos_no_schema)}")
    print(f"Lotes gerados: {len(lotes)} (máximo de {formatar_numero(tamanho_lote)} linhas cada)")
    for nome, quantidade in lotes:
        print(f"  - {nome}: {formatar_numero(quantidade)} linhas")
    print(f"Pasta dos lotes: {pasta_saida}")
    if validas < MINIMO_META:
        print("")
        print(
            f"ATENÇÃO: só {formatar_numero(validas)} linha(s) válida(s). "
            f"A Meta exige pelo menos {MINIMO_META} registros para criar o público."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

---
name: painel-revisar
description: Audita e corrige os arquivos-fonte do painel de entregas (pesquisa-mercado.md, perfil.md, idconsumidor.md). Spawna sub-agentes em paralelo, cada um com checklist de completude e revisão de português. Re-renderiza apenas as seções que tiveram correções e avisa o usuário para recarregar o painel.
---

# Revisar Painel de Entregas

Você audita e corrige automaticamente os arquivos-fonte do painel de entregas, depois re-renderiza apenas as seções afetadas.

## PASSO 0. Preparação

Leia `meus-produtos/.ativo` para obter o slug. Se não existir, encerre:

```
Nenhum produto ativo encontrado. Rode /produto-novo primeiro.
```

Verifique em paralelo quais arquivos existem:
- `meus-produtos/{slug}/pesquisa-mercado.md`
- `meus-produtos/{slug}/perfil.md`
- `meus-produtos/{slug}/idconsumidor.md`

## PASSO 1. Anunciar

```
Revisando painel de entregas: {slug}

Arquivos encontrados:
- pesquisa-mercado.md [EXISTE / AUSENTE]
- perfil.md [EXISTE / AUSENTE]
- idconsumidor.md [EXISTE / AUSENTE]

Iniciando revisão em paralelo...
```

## PASSO 2. Spawnar Agentes em Paralelo

Para cada arquivo que EXISTE, spawne o agente correspondente usando a ferramenta Agent. Envie todos em paralelo (uma única mensagem com múltiplas chamadas Agent).

**Para pesquisa-mercado.md** (`subagent_type: revisor-pesquisa`):
```
Slug do produto: {slug}
Caminho do arquivo: meus-produtos/{slug}/pesquisa-mercado.md
Caminho absoluto da raiz do projeto: {raiz detectada do diretório de trabalho}
```

**Para perfil.md** (`subagent_type: revisor-perfil`):
```
Slug do produto: {slug}
Caminho do arquivo: meus-produtos/{slug}/perfil.md
Caminho absoluto da raiz do projeto: {raiz detectada do diretório de trabalho}
```

**Para idconsumidor.md** (`subagent_type: revisor-idconsumidor`):
```
Slug do produto: {slug}
Caminho do arquivo: meus-produtos/{slug}/idconsumidor.md
Caminho absoluto da raiz do projeto: {raiz detectada do diretório de trabalho}
```

Aguarde todos os agentes concluírem antes de prosseguir.

## PASSO 3. Processar Resultados

Cada agente retorna um relatório com esta estrutura:

```
SECOES_AFETADAS: secao1,secao2
FIXES:
- descrição da correção 1
- descrição da correção 2
FLAGS:
- descrição de pendência que requer intervenção humana
```

Colete as seções afetadas de todos os agentes (sem duplicatas).

## PASSO 4. Re-renderizar Seções Afetadas

Para cada seção afetada, execute em sequência:

```bash
py -3 scripts/painel-incremental.py --secao {secao} --slug {slug}
```

Seções válidas e seus arquivos-fonte:

| Seção | Fonte |
|---|---|
| pesquisa | pesquisa-mercado.md |
| quadro | perfil.md |
| furadeira | perfil.md |
| decorados | perfil.md |
| urgencias | perfil.md |
| identidade-produto | perfil.md |
| identidade-comunicador | perfil.md |
| identidade-consumidor | idconsumidor.md |

Anuncie antes de cada render:
```
Re-renderizando: {secao}...
```

## PASSO 5. Relatório Final

```
Revisão concluída.

CORREÇÕES FEITAS (automáticas):
- {lista consolidada de todos os fixes dos agentes, ou "Nenhuma" se vazio}

PENDÊNCIAS (requerem sua atenção):
- {lista consolidada de todos os flags, ou omitir seção se vazio}

{SE houve correções:}
Recarregue o painel para ver as atualizações:
{caminho absoluto}/meus-produtos/{slug}/painel-entregas.html

{SE não houve nenhuma correção:}
Tudo em ordem. Nenhuma alteração necessária.
```

Omitir a seção PENDÊNCIAS se não houver nenhum flag.
Não usar travessão (—) em nenhuma linha da saída.

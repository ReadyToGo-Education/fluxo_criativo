---
name: workshop-marketing:dashboard-concorrente-remover
description: Remover um concorrente analisado anteriormente em /dashboard-social. Apaga a pasta `entregas/concorrentes/{slug}/` e regenera o painel para refletir a remocao.
---

# Remover Concorrente. Apagar Pasta e Atualizar Painel

Remove permanentemente um concorrente analisado pelo `/dashboard-social` (modo concorrente). Apaga a pasta inteira e regenera a secao "Redes Sociais" do painel.

## Usage

```
/dashboard-concorrente-remover
```

## O Que Fazer

### 1. Detectar produto ativo

Leia `meus-produtos/.ativo` para saber o slug do produto. Se nao existir ou estiver vazio, avise:

```
ERRO: nenhum produto ativo. Use /produto-novo primeiro.
```

### 2. Listar concorrentes existentes

Liste as subpastas de `meus-produtos/{ativo}/entregas/concorrentes/` (se a pasta existir). Para cada subpasta, leia `meta.json` para extrair o nome bonito e a data de atualizacao.

Se nao existir nenhum concorrente analisado, avise:

```
Voce ainda nao analisou nenhum concorrente.
Use /dashboard-social e escolha "Concorrente" para comecar.
```

### 3. Mostrar lista e perguntar qual remover

```
Concorrentes analisados:

1. Erico Rocha (analisado em 11/05/2026 14:30) — Instagram, YouTube
2. Camila Farani (analisado em 09/05/2026 09:15) — TikTok, LinkedIn
3. Joao da Silva (analisado em 03/05/2026 17:42) — Instagram

Digite o numero do concorrente para remover (ou "cancelar"):
```

### 4. Confirmar antes de apagar

Apos receber o numero, leia o `meta.json` do escolhido e exiba a confirmacao:

```
Voce vai remover permanentemente:

Nome:        Erico Rocha
Plataformas: Instagram (@ericosanrocha), YouTube (@ericorochaoficial)
Pasta:       meus-produtos/{ativo}/entregas/concorrentes/erico-rocha/

Isso vai apagar todos os arquivos (dashboards, imagens, insights, log).

Confirma? Digite "sim" para apagar.
```

So prossiga se a resposta for "sim" (ou variantes claras como "pode", "manda", "aprovo"). Qualquer outra resposta, cancele.

### 5. Apagar a pasta

Use `shutil.rmtree` via Python (ou comando equivalente):

```bash
{python} -c "import shutil; shutil.rmtree('meus-produtos/{ativo}/entregas/concorrentes/{slug}')"
```

### 6. Regerar a secao do painel

```bash
{python} scripts/painel-incremental.py --secao dashboards --slug {ativo}
```

### 7. Entrega final

```
Concorrente "Erico Rocha" removido.

A aba "Concorrentes" do painel foi atualizada. Abra o painel para conferir.
```

## Regras

- **Sempre pedir confirmacao explicita "sim"** antes de apagar. Operacao destrutiva e irreversivel.
- **Nunca apagar a pasta `concorrentes/` inteira** mesmo que so reste um item. Sempre apague apenas a subpasta `{slug}`.
- **Se a pasta `concorrentes/` ficar vazia apos a remocao**, deixa ela vazia (nao apaga). O parser detecta sozinho que nao ha concorrentes e mostra o placeholder.
- **Nao usar travessao** em nenhum texto exibido ao usuario.
- **Se o aluno passar o slug direto na linha de comando** (ex: `/dashboard-concorrente-remover erico-rocha`), pule a etapa 3 e va direto para a confirmacao.

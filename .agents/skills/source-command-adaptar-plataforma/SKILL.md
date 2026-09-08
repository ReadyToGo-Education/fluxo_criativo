---
name: "source-command-adaptar-plataforma"
description: "Converte scripts e instrucoes Windows/PowerShell para Mac ou Linux. Adapta agendamento (Task Scheduler → cron/launchd), comandos de instalacao e execucao para o sistema operacional do aluno."
---

# source-command-adaptar-plataforma

Use this skill when the user asks to run the migrated source command `adaptar-plataforma`.

## Command Template

# Adaptar Plataforma. Mac e Linux

Adapta qualquer script ou instrucao do workshop para o sistema operacional correto do aluno.

Consulte a skill `adaptar-plataforma` para todas as tabelas de conversao e equivalencias tecnicas.

---

## PASSO 0. Detectar SO

Execute antes de qualquer pergunta:

```bash
uname -s 2>/dev/null || echo "Windows"
```

Salve o resultado. Use em todas as instrucoes que seguem.

---

## PASSO 1. Identificar o Que Adaptar

Pergunte (se o usuario nao tiver especificado):

```
Qual script ou instrucao quer adaptar para o seu sistema?

1. instagram-dashboard (script de atualizacao + agendamento diario)
2. ads-relatorio (agendamento do relatorio de Ads)
3. Outro script .ps1 que recebi
4. Instrucoes de instalacao com comandos Windows

Digite o numero:
```

---

## PASSO 2. Executar Adaptacao

### Opcao 1. instagram-dashboard

Verifique se `entregas/instagram-dashboard/atualizar.py` existe.

**Se existir:**

Mostre as instrucoes corretas para o SO detectado:

**macOS:**
```
O script atualizar.py ja funciona no macOS.

Para rodar manualmente:
python3 entregas/instagram-dashboard/atualizar.py --abrir

Para instalar a dependencia (se ainda nao instalou):
pip3 install requests

Para agendar todo dia as 08:00 (opcional):
```
Execute a configuracao do cron/launchd conforme a skill `adaptar-plataforma` (secao launchd para Mac).

**Linux:**
```
O script atualizar.py ja funciona no Linux.

Para rodar manualmente:
python3 entregas/instagram-dashboard/atualizar.py --abrir

Para instalar a dependencia:
pip3 install requests

Para agendar todo dia as 08:00 (opcional):
crontab -e
# Adicione a linha:
0 8 * * * cd /caminho/do/projeto && python3 entregas/instagram-dashboard/atualizar.py >> entregas/instagram-dashboard/log.txt 2>&1
```

**Se nao existir:** oriente a rodar `/instagram-dashboard` para criar o script primeiro.

---

### Opcao 2. ads-relatorio

O `ads-relatorio` usa agendamento na nuvem do Codex (CronCreate), que e independente de SO. Nao precisa de adaptacao de agendamento.

Se o aluno estiver com duvida sobre credenciais ou configuracao, redirecione para `/ads-relatorio`.

---

### Opcao 3. Script .ps1 personalizado

Peca o conteudo do script:

```
Cole o conteudo do script .ps1 aqui para eu converter.
```

Apos receber, converta usando as tabelas da skill `adaptar-plataforma`:
- Caminhos: barras invertidas → barras normais
- `Invoke-RestMethod` → `requests` (Python) ou `curl` (bash)
- `Test-Path` → `Path(...).exists()` (Python)
- `Get-Content` / `Add-Content` → `open()` Python
- `$env:VAR` → `os.environ.get('VAR')` (Python) ou `$VAR` (bash)
- Formatacao de data → `datetime.strftime()`
- Leitura do `.env` → parse manual Python (ver skill `adaptar-plataforma`)

Entregue o script convertido em Python (preferencial por ser cross-platform) ou bash (se for simples).

Apresente o script convertido e pergunte:

```
1. Aprovar e salvar
2. Quero ajustar algo
```

---

### Opcao 4. Instrucoes de instalacao Windows

Pergunte o que o aluno precisa instalar ou configurar, depois converta as instrucoes usando a skill `adaptar-plataforma`.

---

## PASSO 3. Agendamento (quando solicitado)

Se o aluno quiser agendar a execucao automatica:

**macOS — launchd (recomendado):**

1. Pergunte o caminho completo do projeto (ex: `/Users/nome/Documents/workshop`)
2. Pergunte o horario desejado (padrao: 08:00)
3. Gere o arquivo `.plist` conforme a skill `adaptar-plataforma` (secao launchd)
4. Salve em `~/Library/LaunchAgents/br.workshop.{nome-script}.plist`
5. Execute:
```bash
launchctl load ~/Library/LaunchAgents/br.workshop.{nome-script}.plist
```
6. Confirme com `launchctl list | grep br.workshop`

**Linux — crontab:**

1. Pergunte o caminho completo do projeto
2. Pergunte o horario desejado (padrao: 08:00)
3. Mostre a linha exata para adicionar com `crontab -e`
4. Instrua a verificar com `crontab -l`

---

## PASSO 4. Entrega

```
Adaptacao concluida para {SO detectado}.

{lista do que foi adaptado}

Para rodar agora:
{comando correto para o SO}

{se agendou: "Agendado para rodar todo dia as {horario}."}
```

---

## REGRAS

- Sempre detectar o SO com `uname` antes de dar qualquer instrucao.
- Nunca dar instrucoes de `schtasks` para usuarios de Mac ou Linux.
- Nunca usar `python` (sem numero) em instrucoes para Mac — sempre `python3`.
- Preferir Python como lingua de conversao (funciona nos tres SOs).
- Usar launchd no Mac como primeira opcao de agendamento (mais robusto que cron).
- Nao mostrar codigo do script convertido inline. Salvar e informar o caminho.

---
name: adaptar-plataforma
description: >
  Converte scripts e comandos Windows/PowerShell para Mac ou Linux.
  Adapta agendamentos (Task Scheduler → cron/launchd), comandos de
  instalacao, execucao e instrucoes de uso para o SO do aluno.
  Referencia tecnica usada pelo command adaptar-plataforma.
---

# Adaptar Plataforma. Conversao Windows → Mac/Linux

Referencia tecnica de conversao para quando o aluno nao usa Windows.
Toda skill do workshop que gerar scripts de automacao DEVE consultar
esta referencia antes de gerar instrucoes de instalacao ou agendamento.

---

## Deteccao de SO

Detectar automaticamente com Bash antes de qualquer instrucao:

```bash
uname -s 2>/dev/null || echo "Windows"
```

| Retorno | SO |
|---|---|
| `Darwin` | macOS |
| `Linux` | Linux |
| `Windows` ou erro | Windows (shell nao tem `uname`) |

No Claude Code no Windows, `uname` pode falhar ou nao existir. Nesse
caso, assuma Windows e oferta PowerShell como padrao.

---

## Python. Instalacao por SO

| SO | Python disponivel? | Comando |
|---|---|---|
| Windows | Nao necessariamente | `python --version` ou `py -3 --version` |
| macOS | Sim (Homebrew ou sistema) | `python3 --version` |
| Linux | Sim (sistema) | `python3 --version` |

**Se Python nao estiver disponivel no Windows:**
1. Abra o Microsoft Store e instale "Python 3.12"
2. Ou baixe em python.org/downloads
3. Marque "Add Python to PATH" na instalacao

**Dependencia unica do workshop (para scripts de automacao):**
```bash
# Mac/Linux
pip3 install requests

# Windows
pip install requests
```

---

## Execucao de Scripts Python

| SO | Comando |
|---|---|
| Windows (Python no PATH) | `python atualizar.py --abrir` |
| Windows (py launcher) | `py -3 atualizar.py --abrir` |
| macOS | `python3 atualizar.py --abrir` |
| Linux | `python3 atualizar.py --abrir` |

**Abrir arquivo HTML no navegador via terminal:**

| SO | Comando |
|---|---|
| Windows | `start arquivo.html` |
| macOS | `open arquivo.html` |
| Linux | `xdg-open arquivo.html` |

---

## Agendamento. Task Scheduler → cron

O Task Scheduler e exclusivo do Windows. Em Mac e Linux, use cron.

### Windows (Task Scheduler via schtasks)

```powershell
schtasks /create /tn "NomeTarefa" /tr "python C:\caminho\script.py" /sc DAILY /st 08:00 /f
```

### macOS e Linux (crontab)

```bash
# Abrir editor do crontab
crontab -e

# Linha para rodar todo dia as 08:00
0 8 * * * cd /caminho/do/projeto && python3 entregas/instagram-dashboard/atualizar.py >> entregas/instagram-dashboard/log.txt 2>&1
```

**Sintaxe do cron:** `minuto hora * * * comando`
- `0 8 * * *` = todos os dias as 08:00
- `0 7 * * 1` = toda segunda-feira as 07:00

**Editor no crontab -e:**
- Se abrir o vim: pressione `i` para editar, `Esc` depois `:wq` para salvar
- Se preferir nano: `EDITOR=nano crontab -e`

**Verificar se foi salvo:**
```bash
crontab -l
```

### macOS alternativo. launchd (recomendado para Mac)

O launchd e mais robusto que cron no macOS porque inicia junto com o sistema.

Crie o arquivo `~/Library/LaunchAgents/br.workshop.{nome-script}.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>br.workshop.{nome-script}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/caminho/completo/ao/projeto/entregas/{pasta}/{script}.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/caminho/completo/ao/projeto/entregas/{pasta}/log.txt</string>
    <key>StandardErrorPath</key>
    <string>/caminho/completo/ao/projeto/entregas/{pasta}/log.txt</string>
</dict>
</plist>
```

Ativar:
```bash
launchctl load ~/Library/LaunchAgents/br.workshop.{nome-script}.plist
```

Desativar:
```bash
launchctl unload ~/Library/LaunchAgents/br.workshop.{nome-script}.plist
```

---

## Conversao de Comandos PowerShell → bash/Python

### Caminhos de Arquivo

| PowerShell | bash (Mac/Linux) |
|---|---|
| `C:\Users\nome\projeto` | `/Users/nome/projeto` (Mac) ou `/home/nome/projeto` (Linux) |
| `Join-Path $dir "arquivo.txt"` | `"$dir/arquivo.txt"` |
| `Split-Path $path -Parent` | `dirname "$path"` |
| `Split-Path $path -Leaf` | `basename "$path"` |

### Operacoes com Arquivos

| PowerShell | bash | Python |
|---|---|---|
| `Test-Path $arquivo` | `test -f "$arquivo"` | `Path(arquivo).exists()` |
| `New-Item -ItemType Directory -Path $dir` | `mkdir -p "$dir"` | `Path(dir).mkdir(parents=True)` |
| `Get-Content $arquivo` | `cat "$arquivo"` | `Path(arquivo).read_text()` |
| `Add-Content $arquivo $texto` | `echo "$texto" >> "$arquivo"` | `open(arquivo,'a').write(texto)` |
| `Remove-Item $arquivo` | `rm "$arquivo"` | `Path(arquivo).unlink()` |

### Variaveis de Ambiente

| PowerShell | bash | Python |
|---|---|---|
| `$env:VARIAVEL` | `$VARIAVEL` | `os.environ.get('VARIAVEL')` |
| `[System.Environment]::SetEnvironmentVariable(...)` | `export VARIAVEL=valor` | nao aplicavel em runtime |

### Requisicoes HTTP

| PowerShell | Python (requests) | bash (curl) |
|---|---|---|
| `Invoke-RestMethod -Uri $url -Method POST -Body $json` | `requests.post(url, json=data)` | `curl -X POST -H "Content-Type: application/json" -d "$json" "$url"` |
| `Invoke-WebRequest -Uri $url -OutFile $arquivo` | `requests.get(url); open(arquivo,'wb').write(r.content)` | `curl -o "$arquivo" "$url"` |
| `-Headers @{"Authorization"="Bearer $token"}` | `headers={"Authorization": f"Bearer {token}"}` | `-H "Authorization: Bearer $token"` |

### Formatacao de Data

| PowerShell | Python |
|---|---|
| `Get-Date -Format "yyyy-MM-dd HH:mm:ss"` | `datetime.now().strftime("%Y-%m-%d %H:%M:%S")` |
| `Get-Date -Format "yyyy-MM-dd"` | `datetime.now().strftime("%Y-%m-%d")` |

### Leitura de Arquivo .env

| PowerShell | Python |
|---|---|
| `Get-Content .env \| ForEach-Object { if ($_ -match '...') {...} }` | `python-dotenv` ou parse manual com `open('.env').readlines()` |

Parse manual em Python (sem dependencia extra):
```python
env = {}
try:
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
except FileNotFoundError:
    pass
```

---

## Scripts do Workshop. Equivalencias por OS

### instagram-dashboard

| SO | Script principal | Como rodar |
|---|---|---|
| Windows | `atualizar.py` | `python entregas/instagram-dashboard/atualizar.py --abrir` |
| macOS | `atualizar.py` | `python3 entregas/instagram-dashboard/atualizar.py --abrir` |
| Linux | `atualizar.py` | `python3 entregas/instagram-dashboard/atualizar.py --abrir` |

O `.py` e o script principal e funciona nos tres sistemas. O `.ps1` e backup apenas para Windows.

**Agendamento diario:**
- Windows: Task Scheduler (via `schtasks` ou Interface Grafica)
- Mac: crontab ou launchd (preferir launchd)
- Linux: crontab

---

## Regras para Skills que Geram Automacoes

Toda skill que gerar scripts de automacao (instagram-dashboard, ads-relatorio etc.) deve:

1. **Detectar o SO no inicio** com `uname -s` antes de dar instrucoes de instalacao.
2. **Gerar Python como script principal** quando possivel (funciona nos tres sistemas).
3. **Dar instrucoes de agendamento corretas para o SO detectado:**
   - Windows: Task Scheduler (schtasks ou interface grafica)
   - Mac: launchd ou crontab (mostrar launchd primeiro como recomendado)
   - Linux: crontab
4. **Nunca dar instrucoes de schtasks para usuarios de Mac ou Linux.**
5. **Nunca assumir que `python` (sem numero) existe no Mac** — usar sempre `python3`.

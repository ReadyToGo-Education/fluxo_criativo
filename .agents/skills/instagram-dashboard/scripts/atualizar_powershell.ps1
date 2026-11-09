# Workshop Inteligente - Instagram Dashboard (Backup PowerShell)
# Use quando o Python nao estiver disponivel no PATH
param([switch]$Abrir)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Localizar Python
$py = @('python', 'python3', 'py') | Where-Object { Get-Command $_ -ErrorAction SilentlyContinue } | Select-Object -First 1

if (-not $py) {
    Write-Error "Python nao encontrado. Instale em python.org e tente novamente."
    exit 1
}

$script = Join-Path $ScriptDir "atualizar.py"
$args_list = @($script)
if ($Abrir) { $args_list += '--abrir' }

& $py @args_list

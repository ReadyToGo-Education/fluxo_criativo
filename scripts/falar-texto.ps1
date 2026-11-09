# Fala o conteúdo de um arquivo de texto usando a voz Microsoft Daniel (pt-BR).
# Uso: powershell -NoProfile -ExecutionPolicy Bypass -File falar-texto.ps1 <caminho-do-txt>
param([Parameter(Mandatory = $true)][string]$ArquivoTexto)

$texto = Get-Content -Raw -Encoding UTF8 $ArquivoTexto
if ([string]::IsNullOrWhiteSpace($texto)) { exit 0 }

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime]

$synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
$daniel = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices |
    Where-Object { $_.DisplayName -like '*Daniel*' } | Select-Object -First 1
if ($daniel) { $synth.Voice = $daniel }

$op = $synth.SynthesizeTextToStreamAsync($texto)

# Converter IAsyncOperation em Task para aguardar (padrão WinRT no PowerShell 5.1)
$asTask = [System.WindowsRuntimeSystemExtensions].GetMethods() |
    Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } |
    Select-Object -First 1
$task = $asTask.MakeGenericMethod([Windows.Media.SpeechSynthesis.SpeechSynthesisStream]).Invoke($null, @($op))
$task.Wait()
$streamWinRT = $task.Result

# Salvar o áudio em WAV temporário e tocar
$wav = [System.IO.Path]::GetTempFileName() + '.wav'
$streamNet = [System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($streamWinRT)
$fs = [System.IO.File]::Create($wav)
$streamNet.CopyTo($fs)
$fs.Close()

$player = New-Object System.Media.SoundPlayer $wav
$player.PlaySync()

Remove-Item $wav -Force -ErrorAction SilentlyContinue
exit 0

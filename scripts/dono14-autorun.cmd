@echo off
rem Rotina agendada 02h: leitura diaria do funil Dono 14% (headless).
rem Registrada no Agendador de Tarefas do Windows. Log em scripts\autorun.log
rem
rem A MARCA .autorun-em-curso (criada aqui, apagada no fim) existe para o hook de
rem SessionStart saber que a sessao que esta abrindo E o proprio autorun. Sem ela,
rem o hook injetava "a rotina das 02h nao rodou, verifique o autorun.log para o
rem motivo" na propria sessao do autorun, que ia ao log, nao achava a marca de
rem "fim" (escrita so depois que ela termina) e concluia que tinha travado. Isso
rem gerou aviso falso em 06, 08, 09, 12, 15 e 16/08.
rem
rem 11/10/2026: o prompt passou de 32 mil caracteres e o Windows recusou a linha de
rem comando ('o nome do arquivo ou a extensao e muito grande', codigo 1, a rotina nao
rem rodou). O prompt agora entra pelo stdin (pipe), que nao tem esse limite.
cd /d "C:\Users\rodri\OneDrive\Documentos\Claude\Projects\fluxo-criativo"
echo autorun em curso desde %date% %time% > scripts\.autorun-em-curso
echo ===== %date% %time% inicio ===== >> scripts\autorun.log
powershell -NoProfile -Command "$tok = (Get-Content .env | Where-Object { $_ -match '^CLAUDE_CODE_OAUTH_TOKEN=' }) -replace '^CLAUDE_CODE_OAUTH_TOKEN=',''; if ($tok) { $env:CLAUDE_CODE_OAUTH_TOKEN = $tok.Trim() } else { $api = (Get-Content .env | Where-Object { $_ -match '^ANTHROPIC_API_KEY=' }) -replace '^ANTHROPIC_API_KEY=',''; if ($api) { $env:ANTHROPIC_API_KEY = $api.Trim() } }; Get-Content -Raw 'scripts/dono14-autorun-prompt.md' | claude -p --permission-mode acceptEdits --max-turns 160" >> scripts\autorun.log 2>&1
echo ===== %date% %time% fim (codigo %errorlevel%) ===== >> scripts\autorun.log
del /q scripts\.autorun-em-curso 2>nul

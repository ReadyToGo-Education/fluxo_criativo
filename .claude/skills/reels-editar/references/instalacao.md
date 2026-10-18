# Instalação de primeira vez do /reels-editar

O editor roda 100% no computador, sem API paga. Precisa de placa de vídeo NVIDIA para a transcrição e para o aprimorar voz ficarem rápidos (sem placa, a transcrição cai para o processador e o aprimorar voz fica lento).

Nada desta lista vai para o git. As ferramentas pesadas ficam em `%LOCALAPPDATA%\reels-editar\` (fora do OneDrive, para não sincronizar centenas de MB):

| Pasta | O que guarda |
|---|---|
| `bin\deep-filter.exe` | reduzir ruído (DeepFilterNet v0.5.6) |
| `clearvoice\checkpoints\` | modelo do aprimorar voz (MossFormer2_SE_48K, 212 MB) |
| `trabalho\R0XX\` | arquivos intermediários de cada Reel |
| `ambiente.json` | quais Pythons o editor usa |

## Passo único

```bash
py -3 .claude/skills/reels-editar/scripts/instalar.py
```

O script confere tudo e instala o que faltar:

1. **FFmpeg** no PATH. Se faltar, ele só avisa: instalar com `winget install ffmpeg` e abrir um terminal novo.
2. **deep-filter v0.5.6**, baixado do GitHub oficial (`github.com/Rikorose/DeepFilterNet/releases/tag/v0.5.6`, arquivo `deep-filter-0.5.6-x86_64-pc-windows-msvc.exe`). O script confere o SHA-256 antes de aceitar o arquivo.
3. **faster-whisper** e as bibliotecas CUDA (`nvidia-cublas-cu12`, `nvidia-cudnn-cu12`), mais Pillow e NumPy, no Python que rodou o instalador (no computador do Rodrigo, o `py -3`, Python 3.14).
4. **ClearerVoice** (`pip install clearvoice soundfile`) no primeiro Python que tiver PyTorch com CUDA (no computador do Rodrigo, o `py -3.12`). Se nenhum tiver, o script avisa o comando:

   ```bash
   py -3.12 -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
   ```

   Depois, rodar o instalador de novo.

No fim ele grava `ambiente.json` com os dois Pythons.

Os modelos de IA não são baixados pelo instalador: o do Whisper (`large-v3-turbo`, 1,6 GB, no cache do Hugging Face) e o do aprimorar voz (212 MB) descem sozinhos no primeiro Reel. A primeira edição demora uns minutos a mais por isso.

## Só conferir

```bash
py -3 .claude/skills/reels-editar/scripts/instalar.py --verificar
```

Sai com código 1 e lista o que falta. A skill roda essa conferência no Passo 0 de toda edição.

## Mac ou Linux

O fluxo é o mesmo, mas o instalador não baixa o deep-filter automaticamente: baixar o binário do sistema na mesma página de releases, salvar como `~/.cache/reels-editar/bin/deep-filter` e dar permissão de execução. A transcrição sem NVIDIA roda no processador (cerca de 4 vezes mais lenta).

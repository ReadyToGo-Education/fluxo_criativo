# Prompt Claude in Chrome v1. Só Imagens

> Versão para alunos que querem usar o Claude in Chrome **apenas para gerar as 6 imagens**.
> A legenda já está pronta localmente (gerada pelo Passo 4 desta skill, revisada pelo Manual da Copy).

---

## Quando usar

Quando o aluno escolheu **opção 2a** no Passo 3.3 da skill `/carrossel`. Significa: ele confia na legenda revisada que o projeto gerou, e só precisa do Claude in Chrome para automatizar a geração das 6 imagens no ChatGPT.

---

## Placeholders

| Placeholder | Origem | Exemplo |
|---|---|---|
| `{CAMINHO_COMPLETO_DO_TXT}` | Passo 3.2 do output triplo | `<raiz-do-projeto>\meus-produtos\<seu-produto>\entregas\conteudo-social\carrossel-nunca\prompts.txt` |

---

## Prompt pronto para o aluno colar no Claude in Chrome

```
No meu computador existe um arquivo de prompts em {CAMINHO_COMPLETO_DO_TXT}. Ele contem 6 prompts de geracao de imagem, separados por linha em branco.

PARTE 1. LER O ARQUIVO
Abra o arquivo e leia os 6 prompts. Guarde cada um separadamente, na ordem em que aparecem.

PARTE 2. GERAR AS 6 IMAGENS NO CHATGPT
Abra o navegador e va para chatgpt.com. Inicie uma conversa nova.

Para cada um dos 6 prompts, em ordem, faca:
1. Cole o prompt no campo de mensagem do ChatGPT e envie.
2. Aguarde ate a imagem ser gerada por completo. A imagem aparece na conversa e o campo de digitacao volta a ficar disponivel.
3. Espere mais 5 segundos depois que a imagem aparecer.
4. So entao envie o proximo prompt.

Repita ate as 6 imagens estarem geradas, todas na mesma conversa. Nao baixe as imagens.

REGRAS DE EXECUCAO:
- Trabalhe sem me pedir confirmacao a cada etapa. Execute do inicio ao fim.
- Se o ChatGPT pedir login, parar de gerar, ou der erro em alguma imagem, me avise nesse momento e pause.
- Se o arquivo nao existir ou estiver vazio, me avise e pare antes de abrir o navegador.

Quando terminar, me avise que as 6 imagens estao prontas e quantas geraram com sucesso.
```

---

## Como a skill apresenta este prompt ao aluno

A skill `/carrossel` (no Passo 3.4) substitui `{CAMINHO_COMPLETO_DO_TXT}` pelo caminho absoluto real do `prompts.txt` que acabou de salvar, e exibe o prompt acima em bloco de código no chat. O aluno copia, abre o Claude in Chrome e cola.

A skill também salva o prompt montado em:
```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/prompt-claude-in-chrome.txt
```

Para o aluno poder reutilizar mais tarde sem ter que repetir o fluxo.

---

## Observação sobre acentos no prompt

Note que o prompt acima usa texto sem acentos no corpo (ex: "geracao", "automacao"). Isso é proposital: alguns ambientes do Claude in Chrome ainda têm comportamentos inconsistentes com caracteres acentuados em prompts longos. As strings que precisam de acento (título dos slides, subtítulo, legenda) já estão DENTRO do `prompts.txt`, não no corpo deste prompt orquestrador.

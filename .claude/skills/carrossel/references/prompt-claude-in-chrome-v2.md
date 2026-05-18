# Prompt Claude in Chrome v2. Imagens + Legenda no Mesmo Chat

> Versão para alunos que querem que o Claude in Chrome **gere as 6 imagens E a legenda** dentro da mesma conversa do ChatGPT.
> A legenda local revisada (gerada pelo Passo 4 da skill) continua existindo como fallback.

---

## Quando usar

Quando o aluno escolheu **opção 2b** no Passo 3.3 da skill `/carrossel`. Significa: ele prefere que o ChatGPT crie a legenda em cima das imagens que acabou de gerar (a legenda pode "respirar" o visual). O projeto continua gerando a legenda local também, e o aluno escolhe qual usar.

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

PARTE 3. GERAR A LEGENDA NO MESMO CHAT
Quando as 6 imagens estiverem prontas, envie a mensagem abaixo no mesmo chat do ChatGPT. Cole exatamente o texto entre as marcas <<< e >>>, sem as marcas.

<<<
Agora, com base nas 6 imagens que voce acabou de gerar (que formam um carrossel de Instagram em ordem), escreva a legenda do post seguindo as regras abaixo. Devolva apenas a legenda final pronta para colar no Instagram, sem introducao, sem explicacao, sem comentario sobre o que voce fez.

REGRAS DE ESCRITA (obrigatorias, todas):
- Nao use travessao em nenhum momento. Use virgula, ponto, dois pontos ou parenteses.
- Nao use ponto de exclamacao.
- Nao comece com pergunta. Comece com afirmacao direta.
- Nao use a estrutura "Nao e X. E Y.".
- Nao use "mesmo que" nem "sem precisar".
- Nao cite produto, curso, treinamento, metodo ou marca no primeiro paragrafo. O lead fala da dor, do desejo ou da transformacao do leitor, nunca do produto.
- Nada de palavras genericas que soam bem e nao dizem nada (jornada, transformacao interna, reconectar, padrao interno, caminho terapeutico, processo de autoconhecimento). Toda frase precisa de cena concreta, numero, prazo ou argumento especifico.
- Toda afirmacao precisa de tese. Explique a causa, nao so o sintoma. Exemplo: "Voce procrastina porque seu cerebro foi programado para acao imediata, nao para acumular reservas".
- Sigla ou nome tecnico so com explicacao no mesmo paragrafo.
- Portugues brasileiro com acentuacao correta segundo o Acordo Ortografico de 1990.

ESTRUTURA OBRIGATORIA:
1. Primeira linha: gancho de scroll, afirmacao concreta e especifica, sem mencionar produto.
2. Corpo: 3 a 5 paragrafos curtos (1 a 3 linhas cada) desenvolvendo a tese do carrossel. Conecte os argumentos com logica.
3. Pico de tensao: nomeie o problema real e a causa que ninguem mais esta dizendo.
4. Virada: apresente o caminho de saida de forma direta, sem rodeio.
5. CTA unico, claro, sem ponto de exclamacao. Escolha o mais alinhado ao tema do carrossel: "Comenta CARROSSEL que te mando o link", "Salva esse post para reler depois", "Me segue para receber a parte 2", ou equivalente.
6. Hashtags: 5 a 8 hashtags relevantes ao tema, em uma linha unica no final, separadas por espaco.

TAMANHO: entre 600 e 1.200 caracteres no corpo (sem contar hashtags).
>>>

PARTE 4. ENTREGAR PARA MIM
Depois que o ChatGPT devolver a legenda, copie o texto completo da legenda e cole aqui no nosso chat. Me mostre a legenda na integra para eu revisar antes de salvar.

REGRAS DE EXECUCAO:
- Trabalhe sem me pedir confirmacao a cada etapa. Execute do inicio ao fim.
- Se o ChatGPT pedir login, parar de gerar, ou der erro em alguma imagem, me avise nesse momento e pause.
- Se o arquivo nao existir ou estiver vazio, me avise e pare antes de abrir o navegador.

Quando terminar, me avise que as 6 imagens estao prontas e cole a legenda aqui.
```

---

## Como a skill apresenta este prompt ao aluno

A skill `/carrossel` (no Passo 3.4) substitui `{CAMINHO_COMPLETO_DO_TXT}` pelo caminho absoluto real do `prompts.txt`, e exibe o prompt em bloco de código no chat. O aluno copia, abre o Claude in Chrome e cola.

A skill também salva o prompt montado em:
```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/prompt-claude-in-chrome.txt
```

---

## Importante. Legenda local continua sendo gerada

Mesmo quando o aluno escolhe 2b, o Passo 4 da skill **continua gerando a legenda local revisada**. A skill avisa:

```
Vou gerar duas legendas:

1. A legenda local (revisada pelo Manual da Copy, salva em legenda.txt)
2. A legenda que o ChatGPT vai gerar em cima das 6 imagens (quando o Claude in Chrome terminar a Parte 3 do prompt)

Voce escolhe qual usar no Instagram. Recomendacao: comparar as duas e usar a que ficar melhor.
```

---

## Observação sobre acentos

Mesmo motivo do v1: o corpo do prompt usa texto sem acento (compatibilidade com Claude in Chrome). As regras dentro do bloco `<<<...>>>` que o ChatGPT vai receber também estão sem acento, mas pedem explicitamente que a legenda final seja gerada **com acentuação correta segundo o Acordo Ortográfico de 1990**.

---
name: "imagem-no-codex"
description: "Gera as imagens dos fluxos do workshop aqui mesmo no Codex, com a ferramenta de imagem do próprio Codex, no lugar do prompt para colar no ChatGPT ou do script pago do OpenRouter. Use sempre que um fluxo do workshop for gerar imagem. Criativo estático (29 formatos), furadeira visual (também dentro do produto-concepcao), carrossel, banner, imagem de anúncio. Só existe no Codex."
---

# Imagem no Codex

<!-- Origem: codex-extras/skills/imagem-no-codex/. Esta skill só existe no Codex. Edite lá e rode scripts/exportar-para-codex.py. -->

O Claude Code não gera imagem. Por isso os fluxos do workshop em `.claude/` terminam num prompt para o aluno colar no ChatGPT ou no Gemini, ou num script que paga o OpenRouter. No Codex, a ferramenta de imagem do próprio Codex (`image_gen`, a mesma da skill de sistema `imagegen`) gera a arte aqui mesmo, pelo plano do ChatGPT do aluno, sem chave de API.

Esta skill diz como trocar o passo de imagem de cada fluxo. O resto do fluxo (entrevista, copy, aprovação, nomes de arquivo, menus finais) continua exatamente como está no arquivo original.

## Regras gerais

0. **Sem perguntar.** No Codex, não pergunte como gerar a imagem e não mostre menu de caminhos (ChatGPT, Chrome, OpenRouter). Depois da aprovação do texto, gere direto. Os prompts continuam salvos no arquivo do fluxo. Se o aluno pedir por conta própria o prompt para colar no ChatGPT, ou pedir o OpenRouter, siga o caminho original do fluxo.

1. **Ferramenta.** Gere com `image_gen` e siga as regras da skill de sistema `imagegen` do Codex para fundo transparente, edição e várias imagens (uma chamada por imagem). Não use o modo de linha de comando dela (`scripts/image_gen.py`, que pede `OPENAI_API_KEY`), a não ser que o aluno peça.

2. **Prompt.** Use o prompt que o fluxo do workshop já monta, sem reescrever o conteúdo. Quando o fluxo pede uma proporção, garanta que ela esteja escrita logo no começo do prompt (ex.: `Vertical 4:5 image, 1080x1350.`).

3. **Salvar na pasta do aluno.** A ferramenta salva a imagem em `generated_images`, dentro da pasta do Codex. O fluxo precisa dela na pasta do produto, com o nome certo. Logo depois de cada imagem gerada, copie com o script desta skill:

   ```bash
   python3 .agents/skills/imagem-no-codex/scripts/copiar-imagem-gerada.py --destino "{caminho de saída do fluxo}"
   ```

   - No Windows, use `py -3` quando `python3` não existir (seção "Scripts e Compatibilidade" do `AGENTS.md`).
   - Se a ferramenta informou o caminho do arquivo gerado, passe também `--origem "{caminho}"`. Sem `--origem`, o script pega a imagem mais recente de `generated_images`.
   - O script cria as pastas, copia a imagem e mostra largura, altura e proporção.
   - Nunca deixe uma entrega só em `generated_images`.

4. **Conferir antes de mostrar.** Olhe a imagem e compare com o que foi pedido: proporção (o script mostra), textos da arte contra o texto aprovado (acentos e palavras em português) e elementos da cena. Se algo saiu errado, peça uma edição pontual só daquilo e salve de novo no mesmo caminho. No máximo 2 tentativas. Depois disso, mostre a imagem e diga o que ficou diferente.

5. **Anúncio de próximo passo.** Antes de gerar, anuncie usando o tempo de "Gerar a imagem do criativo via API" em `.claude/rules/tempo-estimado.md` (é o mesmo modelo de imagem). Quando forem várias imagens em sequência, sem tempo calibrado no arquivo, não invente número: diga quantas imagens são e mostre o progresso com `⏳ Passo {n}/{total}`.

6. **Quando não der.** Se a ferramenta não estiver disponível (o plano gratuito do ChatGPT não gera imagem no Codex) ou o limite do plano acabar, avise em uma linha, em linguagem simples, e volte ao caminho original do fluxo: prompt para colar no ChatGPT ou OpenRouter. Nunca troque de caminho sem avisar.

7. **Linguagem com o aluno.** Fale em "gerar a imagem aqui" e, quando fizer sentido, que ela "usa o limite do seu plano do ChatGPT, sem custo extra". Não fale em `image_gen`, ferramenta, skill, script nem `generated_images`.

## /criativo-estatico (29 formatos)

O orquestrador lê cada formato em `.claude/commands/criativo-estatico/{formato}.md`. Esses arquivos continuam com o fluxo do Claude Code. No Codex, mude três pontos.

**1. Menu de formatos do orquestrador.** Troque a frase final da lista ("Em qualquer formato, no fim você escolhe gerar a imagem colando o prompt no ChatGPT (grátis) ou direto pela API...") por:

```
Em qualquer formato, no fim eu gero a imagem aqui mesmo e já salvo na sua
pasta (usa o limite do seu plano do ChatGPT, sem custo extra).
```

**2. Sem a pergunta "Como você quer gerar a imagem?".** Todo formato faz essa pergunta no passo de gerar e salvar. No Codex, não pergunte (regra geral 0). Depois da aprovação, siga direto o modo API do formato do começo ao fim (salvar o `.md`, gravar o prompt em `.txt`, nomes de arquivo, mensagens, menu final e o sub-fluxo de Stories), com estas diferenças:

  - não leia a `OPENROUTER_API_KEY` e não pergunte o modelo;
  - cada vez que o formato mandar rodar `scripts/gerar-criativo-estatico.py`, gere a imagem com `image_gen` usando os mesmos dados do comando: o texto do arquivo em `--prompt-file`, a proporção de `--aspect`, a imagem de `--reference-image` (quando houver) e salve no caminho de `--out` (regra geral 3);
  - nas mensagens ao aluno, troque "via API" por "aqui mesmo" e não fale em custo;
  - se não der para gerar (regra geral 6), mostre os prompts como no modo ChatGPT do formato.

**3. Stories a partir do Feed.** O sub-fluxo de Stories é uma edição: a imagem do Feed entra como referência, com o prompt curto de recomposição que o formato já traz. A imagem do Feed precisa estar visível na conversa. Se ela foi gerada nesta conversa, já está. Se não (outra sessão, ou o aluno pediu Stories depois), abra o arquivo `-feed.png` com `view_image` antes de editar.

Nos rótulos que o formato mostra ao aluno antes da aprovação, troque "PROMPT PRO CHATGPT" por "PROMPT DA IMAGEM". A animação em loop (Replicate) continua igual.

## /furadeira-visual

Os passos 1 a 7 do command (contexto, layout, paleta, prompt em inglês e `prompt-furadeira.md`) continuam iguais. Os passos 8 e 9 mudam:

- **Passo 8.** Não peça para o aluno colar o prompt no ChatGPT. Anuncie `🔍 Próximo passo: gerar a imagem da Furadeira. Tempo estimado: 2 a 3 minutos.` e gere com `image_gen` usando o prompt em inglês do passo 6, com fundo transparente. Salve em `meus-produtos/{ativo}/entregas/furadeira/furadeira.png` (caminho fixo, sobrescreve).
- **Passo 9.** Antes de mostrar, confira você mesmo os textos da imagem contra a Furadeira do `perfil.md` (nome do método, nomes das fases e acentos). Se houver palavra errada, peça até 2 edições pontuais corrigindo só aquela palavra. Depois mostre a imagem e pergunte:

  ```
  Conferi a imagem. {o que está certo, o que corrigi, o que ainda ficou errado}

  1. Ficou boa, pode usar
  2. Tem erros aceitáveis (uso como rascunho, e você refaz no Canva para a página de vendas)
  3. Gerar de novo com outro layout ou paleta

  Digite o número:
  ```

  - **1** ou **2**: siga para o passo 10.
  - **3**: use o cenário C do passo 9 (segundo layout da preferência ou próxima paleta), monte o prompt de novo e gere outra vez.
- Os passos 10 e 11 continuam iguais.
- A regra "Não chamar API de imagem" do command vale para APIs pagas (Gemini, OpenRouter). A geração aqui no Codex roda pelo plano do aluno e está liberada.

## /produto-concepcao (imagem da Furadeira)

O bloco "Gerar Representação Visual" manda executar o `/furadeira-visual`. No Codex, execute-o com a seção "/furadeira-visual" desta skill, e não com o passo de colar no ChatGPT. Por isso:

- Não mostre o bloco "Aguardar imagem ou opção de pular" ("Cole o prompt no ChatGPT..."). Quando o aluno escolher 1 ou 2 na conferência da imagem, siga direto para o Bloco 2B/6.
- No `perfil.md`, registre `_formato: PNG`, `_png: meus-produtos/{ativo}/entregas/furadeira/furadeira.png` e `_prompt: meus-produtos/{ativo}/entregas/furadeira/prompt-furadeira.md`.
- Se não der para gerar (regra geral 6), use o bloco original: colar no ChatGPT ou pular por enquanto.

## /carrossel

No passo de gerar as imagens (`references/passo-output-triplo.md` da skill `carrossel`), pule as seções 3.3 a 3.5: não detecte capacidades e não mostre o menu de caminhos. A "regra dura" de sempre exibir o menu não vale no Codex (regra geral 0). Gere as imagens direto, assim:

1. Anuncie `🔍 Próximo passo: gerar as 6 imagens do carrossel, uma por vez.`
2. Gere um slide por vez, do 1 ao 6, com o prompt de cada slide: o `prompts.txt` da pasta do carrossel (6 prompts separados por linha em branco), quando existir, ou os prompts mostrados no chat. Do slide 2 em diante, use o slide 1 como referência de estilo (paleta, tipografia, luz e tratamento de cor), sem copiar o conteúdo dele.
3. Salve cada um em `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/imagens/slide-{n}.png` (regra geral 3) e mostre `⏳ Passo {n}/6: slide {n} pronto.`
4. No fim, liste a pasta e os 6 arquivos, como no caminho da API, sem falar em custo. Siga para o Passo 5 (legenda).
5. Se um slide falhar, ofereça tentar de novo só aquele slide ou seguir pelo Manual (os prompts já estão no chat).

No modo "Gerar todos" (9 carrosséis, 54 imagens), avise numa linha, antes de começar, que as imagens usam o limite do plano do ChatGPT. Se o limite acabar no meio, pare e deixe os prompts dos slides que faltam para o aluno colar no ChatGPT.

## Outros fluxos de imagem

Vale para qualquer outro passo que mande o aluno colar um prompt de imagem no ChatGPT ou no Gemini, ou que rode um script de imagem pelo OpenRouter (por exemplo `scripts/gerar-banner-estatico.py`, `scripts/gerar-carrossel-foto.py`, `scripts/recriar-imagem-estilo.py`, o `/img-anuncio` e a skill `usar-referencia-visual`):

- Gere a imagem aqui mesmo, sem perguntar, no lugar do passo de colar ou do script (regra geral 0).
- Use os mesmos dados que o script receberia: o texto do prompt, a proporção, a imagem de referência e o caminho de saída. Imagem de referência entra como edição ou referência visual, aberta antes com `view_image` quando ainda não estiver na conversa.
- Salve no mesmo caminho e com o mesmo nome que o script usaria, para o resto do fluxo encontrar o arquivo.

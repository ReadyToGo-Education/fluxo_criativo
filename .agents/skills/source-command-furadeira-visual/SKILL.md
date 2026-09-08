---
name: "source-command-furadeira-visual"
description: "Gerar a imagem PNG da Furadeira do produto ativo. Le a Furadeira ja escrita no perfil.md (gerada por /gerar-furadeira), decide o layout visual conforme mecanica + nicho, monta um prompt em ingles para o aluno colar no ChatGPT, recebe a imagem de volta e salva no projeto + painel de entregas."
---

# source-command-furadeira-visual

Use this skill when the user asks to run the migrated source command `furadeira-visual`.

## Command Template

# Furadeira Visual (Imagem PNG via ChatGPT)

Gera a imagem PNG da Furadeira a partir da Furadeira já escrita no `perfil.md`. A skill decide o layout sozinha (com base na mecânica registrada e no nicho), monta o prompt em inglês, exibe pra colar no ChatGPT, recebe a imagem de volta e salva.

Pré-requisito: a Furadeira precisa estar gerada no `perfil.md`. Se não estiver, redireciona para `/gerar-furadeira`.

## Usage

```
/furadeira-visual
```

## O Que Fazer

### 1. Carregar contexto

Leia `meus-produtos/.ativo`. Se vazio, pare e informe:

```
Nenhum produto ativo. Use /produto-novo ou /produto-trocar primeiro.
```

Leia `meus-produtos/{ativo}/perfil.md`. Procure pela seção "## Furadeira (Método)".

**Se a seção não existir ou não tiver o campo `**Mecânica(s):**`** definido, pare e informe:

```
A Furadeira ainda não foi gerada no perfil.md. Use /gerar-furadeira primeiro para criar o método estruturado. Depois rode /furadeira-visual para gerar a imagem.
```

Extraia da seção Furadeira:
- **Nome do método**
- **Mecânica(s)** declarada(s)
- **Estrutura específica** (fases, ramificações, categorias, pilares, ritual, etc., conforme a mecânica)
- **Eficiência principal**

Extraia também do perfil.md:
- **Nicho** (extrair também de idconsumidor.md se existir, para refinar o tom)

### 2. Carregar bases de conhecimento

Leia:
- `.Codex/skills/furadeira-visual/SKILL.md` (regras de mapeamento mecânica → layout, paleta por nicho, estrutura do prompt)
- `.Codex/skills/furadeira-visual/references/6-mecanicas.md` (definição das 6 mecânicas)
- `.Codex/skills/furadeira-visual/references/metodo-visual.md` (descrição estrutural de cada layout)

### 3. Decidir o layout automaticamente

Aplique a tabela mecânica → layout da skill `furadeira-visual`:

| Mecânica registrada | Layouts compatíveis (preferência decrescente) |
|---|---|
| Fases e Sequências | Roadmap Vertical, Linear Horizontal, Hexágonos em Cadeia, Trilha Ondulada, Pirâmide Invertida |
| Lógica Condicional | Fluxograma Condicional, Régua de Comportamento |
| Enquadramento | Grid de Categorias, Quadrantes 2x2, Hub Numerado com Quadrantes |
| Listas | Hub Central / Diamante, Roda Eneagrama, Roda Octogonal, Mandala Concêntrica |
| Empecilhos (com Fases) | Roadmap Vertical com caixas de obstáculo lateral, Linear Horizontal com bloqueios |
| Dinâmica de Entrega | Curva Exponencial, Régua de Comportamento, Trilha Ondulada com frequência |

Desempate por nicho (consulte tabela completa na skill):
- Espiritual → preferir Mandala, Roda, Hub
- Corporativo → preferir Linear, Hub Numerado
- Feminino → preferir Trilha Ondulada, Grid Categorias
- Esportivo / Saúde → preferir Roadmap, Curva Exponencial
- Educação / Idiomas → preferir Hexágonos, Pirâmide
- Criativo → preferir Mandala, Hub Central

### 4. Inferir paleta pelo nicho

Aplique a tabela de paleta por nicho da skill `furadeira-visual` (cada nicho tem cor dominante + acento + texto em HEX). Não perguntar ao aluno. Se o nicho não encaixar em nenhuma categoria, usar a paleta genérica (Azul royal `#2563EB` + Dourado `#E8A200` + Branco).

### 5. Anunciar a decisão

```
🔍 Próximo passo: montar o prompt para um {nome do layout escolhido} com paleta {nome da paleta}, baseado na mecânica {mecânica registrada}. Tempo estimado: cerca de 30 segundos.
```

### 6. Montar o prompt em inglês

Estrutura obrigatória do prompt (preencher os placeholders):

```
Professional flat design infographic for a method called "{nome do método}".
Transparent background, PNG with alpha channel. No background color, no background fill.

VISUAL STYLE:
{descrição textual rica do layout escolhido em 4 a 6 frases — estrutura, conexões,
hierarquia, espaçamento, ícones, decoração}

METHOD CONTENT (keep all text exactly in Brazilian Portuguese, do not translate):

{conteúdo específico da mecânica:
 - Fases: cada fase numerada com nome + 1 frase
 - Condicional: a decisão crítica + as ramificações com seus protocolos
 - Enquadramento: as categorias com nomes próprios e características
 - Listas: os pilares com seus nomes e 1 frase de explicação
 - Empecilhos: os 3 a 5 obstáculos com nomes
 - Dinâmica: o ritual com frequência e duração}

LAYOUT: {nome do layout + posicionamento dos elementos no canvas}
ICON STYLE: {outline thin / filled solid / illustrative — escolher conforme nicho}
COLOR PALETTE: dominant {HEX e nome}, accent {HEX e nome}, text {HEX e nome}
TYPOGRAPHY: {sans-serif moderna / serif clássica / display bold}
TONE: {corporate sober / spiritual ethereal / vibrant modern / clean academic / minimalist premium}

HARD CONSTRAINTS:
- Transparent background (PNG with alpha channel). No white fill, no colored fill, no gradient wash behind the full canvas.
- All visible text must be in Brazilian Portuguese (pt-BR). Never translate names, phases, categories or labels.
- Render all accented characters correctly: ã, á, â, à, é, ê, í, ó, ô, õ, ú, ç. "Ação" not "Acao".
- No people, no faces, no photographs, no realistic scenes, no handwriting.
- No logos, no watermarks, no decorative frames around the full canvas.
- Aspect ratio 4:3, minimum width 1200px.
- Output: clean professional infographic ready for presentation slide or sales page.
```

Use a estrutura completa do prompt detalhada em `.Codex/skills/furadeira-visual/SKILL.md`.

### 7. Salvar prompt em arquivo

Anuncie:

```
🔍 Próximo passo: salvar prompt em arquivo Markdown. Tempo estimado: cerca de 5 segundos.
```

Salve em `meus-produtos/{ativo}/entregas/furadeira/prompt-furadeira.md` com este conteúdo:

> **ATENÇÃO:** salvar o arquivo NÃO é o fim do passo. Após salvar, execute o Passo 8 imediatamente — exibir o prompt completo no chat. Não encerre, não mostre apenas o caminho do arquivo, não escreva "Abra o arquivo acima".

~~~markdown
# Prompt para gerar a imagem da Furadeira no ChatGPT

## Como usar

1. Acesse https://chatgpt.com/ e abra um chat novo.
2. Cole o prompt abaixo no campo de mensagem.
3. Envie e aguarde o ChatGPT gerar a imagem.
4. Quando a imagem aparecer, clique com o botão direito > Salvar imagem como > escolha PNG.
5. Volte aqui no chat do Workshop e cole a imagem (ou salve em `meus-produtos/{ativo}/entregas/furadeira/furadeira.png` e diga "imagem salva").

**Importante:** verifique se o fundo da imagem está transparente (xadrez cinza/branco no editor). Se vier com fundo branco sólido, peça pro ChatGPT regenerar com a instrução "transparent background, PNG with alpha channel".

## Prompt

```
{prompt em inglês completo, montado no passo 6}
```

## Detalhes da decisão

- **Mecânica do método:** {mecânica registrada}
- **Layout escolhido:** {nome do layout + por que combina com a mecânica}
- **Paleta:** {nome da paleta + cores HEX, justificativa pelo nicho}
- **Tom visual:** {tom escolhido pelo nicho}
~~~

### 8. Exibir o prompt no chat

> **OBRIGATÓRIO.** Exibir o prompt completo no chat imediatamente após salvar o arquivo. Não pule este passo. Não substitua o conteúdo por um link para o arquivo. O aluno precisa ver o texto aqui para copiar sem abrir nada.

Mostre o prompt em inglês completo no chat (sem o bloco de código markdown — direto, pronto pra copiar):

```
✅ Prompt gerado. Caminho: meus-produtos/{ativo}/entregas/furadeira/prompt-furadeira.md

Copie o bloco abaixo e cole no ChatGPT (https://chatgpt.com/):

---

{prompt em inglês completo}

---

**⚠ Aviso importante.** O ChatGPT costuma errar texto em português brasileiro (acentos, palavras técnicas). A imagem geralmente sai com layout e paleta corretos, mas com palavras tipo "Metodo" no lugar de "Método" ou "Coracao" no lugar de "Coração". Isso é limitação do modelo de imagem, não do prompt. Use a imagem como referência de layout. Para produção (página de vendas, anúncios), reproduza no Canva ou Figma com o texto correto (gasta uns 15 minutos).

Quando o ChatGPT gerar a imagem:

1. Clique com o botão direito > Salvar imagem como > escolha PNG
2. Volte aqui e cole a imagem no chat (arrastar ou Ctrl+V)
   OU salve manualmente em:
   meus-produtos/{ativo}/entregas/furadeira/furadeira.png
   e me avise "imagem salva"

Estou esperando a imagem.
```

### 9. Receber a imagem

Aguarde o aluno responder. Há 3 cenários possíveis:

**A. Aluno cola a imagem no chat.**

> **OBRIGATÓRIO.** Mover o arquivo imediatamente, sem perguntar nada antes. Não apresente opções de qualidade, não peça confirmação, não comente os erros antes de mover. Primeiro move, depois (se quiser) comenta.

1. Identifique o caminho temporário da imagem.
2. Crie a pasta `meus-produtos/{ativo}/entregas/furadeira/` se não existir:
   ```
   bash -c "mkdir -p 'meus-produtos/{ativo}/entregas/furadeira'"
   ```
3. Copie a imagem para `meus-produtos/{ativo}/entregas/furadeira/furadeira.png` (sobrescreve se já existir), independente do nome original do arquivo.
4. Confirme: `✅ Imagem salva em meus-produtos/{ativo}/entregas/furadeira/furadeira.png`

Só após mover: se houver erros visíveis de texto (problema comum do ChatGPT com português), mencione brevemente como observação e siga para o passo 10.

**B. Aluno diz "imagem salva" ou variações ("ta na mao", "salvei", "pronto").**
1. Verifique se `meus-produtos/{ativo}/entregas/furadeira/furadeira.png` existe.
2. Se não existir, peça pro aluno conferir o caminho.

**C. Aluno desiste / quer regenerar prompt.**
- Se ele pedir outra opção de layout, sugira o segundo layout da preferência (passo 3) e reconstrua o prompt.
- Se ele pedir outra paleta, refaça com a próxima da tabela.

### 10. Atualizar o painel de entregas

Anuncie:

```
🔍 Próximo passo: atualizar o painel de entregas com a nova furadeira. Tempo estimado: cerca de 10 segundos.
```

Rode:

```
py -3 scripts/painel-incremental.py --slug {ativo}
```

Se o script falhar, avise:
```
Não foi possível atualizar o painel automaticamente. Rode manualmente quando puder:
py -3 scripts/painel-incremental.py --slug {ativo}
```

### 11. Mensagem final

```
✅ Concluído: imagem da Furadeira salva.

Caminho: {raiz-do-projeto}/meus-produtos/{ativo}/entregas/furadeira/furadeira.png

Próximo:
- /copy-pagina para usar a Furadeira na seção Método da página de vendas (a imagem é embutida automaticamente)
- /furadeira-visual de novo se quiser regenerar com outro layout ou paleta
```

## Tratamento de erros

| Cenário | Mensagem ao aluno |
|---|---|
| Sem produto ativo | "Nenhum produto ativo. Use /produto-novo ou /produto-trocar primeiro." |
| Furadeira não gerada no perfil | "A Furadeira ainda não foi gerada no perfil.md. Use /gerar-furadeira primeiro." |
| Falha ao salvar PNG | "Não consegui salvar a imagem. Confira se a pasta meus-produtos/{ativo}/entregas/furadeira/ existe e tem permissão de escrita." |
| Aluno cola arquivo que não é PNG/JPG | "O arquivo enviado não é uma imagem. Aceito apenas PNG, JPG ou WEBP. Tente de novo." |
| painel-incremental.py falhou | Avisar caminho do PNG e instruir o aluno a rodar manualmente. |

## Regras

- Sem entrevista. Decidir layout e paleta sozinha com base em mecânica + nicho.
- Não chamar a skill `revisora` (prompt técnico em inglês não é copy de venda).
- Prompts sempre em inglês para o ChatGPT, mas conteúdo do método (nomes de fases, categorias, etc.) sempre em português brasileiro.
- Caminho fixo do PNG: `meus-produtos/{ativo}/entregas/furadeira/furadeira.png`. Sobrescrever se já existir.
- Anunciar "próximo passo" antes de operações longas (regra global do AGENTS.md).
- Não gerar HTML. Não usar templates HTML antigos. Não chamar API de imagem (Gemini, OpenRouter etc.). A imagem é gerada pelo ChatGPT do aluno e devolvida pra cá.
- Se o aluno regenerar a Furadeira via `/gerar-furadeira` depois, ele precisa rodar `/furadeira-visual` de novo. A imagem antiga continua válida até ser sobrescrita.

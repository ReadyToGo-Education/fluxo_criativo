# Estilo. Carrossel "Ninguém Conta"

> Carrossel viral de 6 slides que revela verdades ocultas, mecânicas escondidas e detalhes que praticantes do nicho NÃO falam em público sobre como atingir um objetivo específico. Oposto do marketing motivacional, é a real, sem filtro.
> Este estilo **delega o prompt-base** para `references/prompt-ninguem-conta.md`. O prompt é executado EXATAMENTE como está, sem reescrita. A única adaptação permitida é pré-preencher o Passo 1 (Coleta) com dados do produto ativo quando existirem.

---

## Coleta do Passo 1

O fluxo de coleta do Ninguém Conta **ignora** o `passo-coleta-base.md` padrão. A coleta é a do `prompt-ninguem-conta.md` (6 perguntas, uma a mais que os outros clássicos):

### 1.1. Nicho e produto em UMA frase
Se `perfil.md` tiver Quadro/categoria do produto, pré-preencha como sugestão.

### 1.2. @ do Instagram
Se `.env` tiver `IG_USER` ou `perfil.md` tiver handle, pré-preencha como sugestão.

### 1.3. Cores padrão da marca
Default sem paleta: creme bege `#F2EAD9` (slides 1-5) + verde-sálvia escuro `#3D4A3F` (slide 6). Se o aluno quiser a atmosfera bastidor sugerida pelo prompt, oferecer alternativa: bege escuro `#D9CFB8` (slides 1-5) + verde-musgo `#2E3B2C` (slide 6).

### 1.4. Tipo de comunicação (texto)
5 opções do prompt: clássica/sóbria, bem-humorada, técnica, inspiracional, crua/real. Default: "crua e direta".

### 1.5. Objetivo principal do público (PERGUNTA EXTRA deste estilo)
Pergunta exclusiva do Ninguém Conta. Pergunte: "Qual o objetivo concreto que seu público quer atingir? Quanto mais específico, melhor."

Regra de exemplo personalizado: antes de exibir, leia `perfil.md` (Quadro, Decorados, nicho) e `idconsumidor.md` (dores, desejos, paliativos) do produto ativo, e ofereça 2 a 3 exemplos de objetivo coerentes com o nicho. Se o perfil/idconsumidor não der pistas suficientes, use 2 exemplos neutros relacionados ao nicho.

Esse objetivo vira a variável `[OBJETIVO]` referenciada em todo o prompt (slides 1-5, CTA do slide 6, regras de geração de ideias).

### 1.6. Estilo de design visual
7 opções (Sofisticado e elegante, Editorial e cinematográfico, Despojado e bem-humorado, Energético e vibrante, Sério e técnico, Aconchegante e humano, Provocativo e ousado) ou descrição livre.

---

## Passo 2. Execução

A skill `/carrossel` no estilo Ninguém Conta faz o seguinte:

1. **Carrega** `references/prompt-ninguem-conta.md` inteiro.
2. **Executa o Passo 1 do prompt** (coleta de 6 dados, incluindo o Objetivo do público), uma pergunta por turno, com pré-preenchimento de sugestão a partir do `perfil.md`/`idconsumidor.md`/`.env`.
3. Passa pela **confirmação consolidada** (Passo 2.5 da SKILL.md). O resumo deve mostrar o Objetivo coletado, pois é a âncora do carrossel inteiro.
4. **Executa o prompt do Passo 2 ao Passo 4 exatamente como está**, na sessão atual:
   - Passo 2: gera os 6 slides com aprovação interna, aplicando o critério REVELADOR + DEFENDIDO + ÚTIL PRO OBJETIVO.
   - Passo 3: 3 outputs (chat slide por slide, arquivo `prompts.txt`, comando Cowork).
   - Passo 4: gera a legenda do Instagram com Manual da Copy e salva `legenda.txt`.
5. O texto dos 6 slides passa pelo **Manual da Copy + revisora** silenciosamente antes do gate de aprovação do Passo 2 do prompt.

---

## Diferenças importantes em relação aos outros estilos clássicos ainda não migrados

| Aspecto | Ninguém Conta (verbatim) | Estilos clássicos no modelo leve (Sempre, Odeio, Erros, Amo) |
|---|---|---|
| Fonte de regras | `references/prompt-ninguem-conta.md` (prompt completo, verbatim) | `references/estilos/{estilo}.md` (rules leves) + `passo-coleta-base.md` |
| Coleta | 6 perguntas, com Objetivo do público como pergunta exclusiva | 5 perguntas (handle, nicho, cores, tom, design) |
| Execução | A skill executa o prompt do estilo do início ao fim | A skill conduz Passo 3 padrão usando guidance leve |
| Output de prompts visuais | Output Triplo do próprio prompt (chat + `prompts.txt` + comando Cowork) | `passo-output-triplo.md` compartilhado |
| Output de legenda | Passo 4 do próprio prompt (com Manual da Copy citado explicitamente) | `passo-legenda.md` compartilhado |

---

## Modo "Gerar todos"

No fluxo "Gerar todos" (Passo 2 da SKILL.md, ramo `todos`), Ninguém Conta roda com **valores pré-coletados** no Passo 2.B da SKILL.md (handle, nicho_produto, cores_marca, tom_texto, **objetivo_publico**, estilo_design):

- A skill pula o Passo 1 do `prompt-ninguem-conta.md` (Coleta interativa) e injeta os valores diretamente. O Objetivo do público é tratado como mais um dado coletado em lote.
- Em seguida executa o Passo 2 do prompt sem o gate de aprovação interativa (aprovação acontece depois, em lote, no Passo 2.D da SKILL.md).
- Passo 3 e Passo 4 do prompt rodam normalmente (visuais e legenda).

---

## Saída no projeto

Pasta de saída:

```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-ninguem-conta/
```

Arquivos gerados (definidos pelo próprio `prompt-ninguem-conta.md`):
- `texto.md` (6 slides aprovados, convenção da skill, ver Passo 3 da SKILL.md)
- `prompts.txt` (6 prompts visuais em inglês, separados por linha em branco, Passo 3.2 do prompt)
- `legenda.txt` (legenda do Instagram, revisada pelo Manual da Copy, Passo 4.5 do prompt)

Adicionalmente, durante a execução o prompt entrega no chat o **comando Cowork** pronto para automatizar a geração das imagens no ChatGPT via Claude in Chrome.

---

## Paleta default

- **Slides 1-5.** Fundo creme bege `#F2EAD9` + texto verde-sálvia escuro `#3D4A3F`.
- **Slide 6 (CTA).** Fundo verde-sálvia escuro `#3D4A3F` + texto creme bege `#F2EAD9`.

Alternativa "atmosfera bastidor" sugerida pelo prompt: bege escuro `#D9CFB8` (slides 1-5) + verde-musgo `#2E3B2C` (slide 6). Se o aluno responder com outra paleta no Passo 1.3, use a dele.

---

## Atmosfera fotográfica (definida no prompt)

Cenas que sugerem o lado escondido do objetivo: bastidores, close-ups de objetos que carregam a história não contada, momentos de vulnerabilidade. Realismo documental, sem polimento publicitário, sem rosto humano nítido. Mood cru, íntimo, sem retoque. O template de prompt de imagem do `prompt-ninguem-conta.md` já traz essa direção em inglês (`Cinematic intimate lighting, documentary realism, raw mood without advertising polish`).

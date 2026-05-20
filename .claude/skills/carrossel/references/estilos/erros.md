# Estilo. Carrossel "Erros"

> Carrossel viral de 6 slides que entrega 5 erros contraintuitivos, práticos e sabotadores do desejo declarado pelo público (coisas que a pessoa faz achando que está certa, mas que atrasam o desejo) + CTA criativa.
> Este estilo **delega o prompt-base** para `references/prompt-erros.md`. O prompt é executado EXATAMENTE como está, sem reescrita. A única adaptação permitida é pré-preencher o Passo 1 (Coleta) com dados do produto ativo quando existirem.

---

## Coleta do Passo 1

O fluxo de coleta do Erros **ignora** o `passo-coleta-base.md` padrão. A coleta é a do `prompt-erros.md` (6 perguntas, uma a mais que os outros estilos por causa do Desejo do público):

### 1.1. Nicho e produto em UMA frase
Se `perfil.md` tiver Quadro/categoria do produto, pré-preencha como sugestão.

### 1.2. @ do Instagram
Se `.env` tiver `IG_USER` ou `perfil.md` tiver handle, pré-preencha como sugestão.

### 1.3. Cores padrão da marca
Default sem paleta: creme bege `#F2EAD9` (slides 1-5) + verde-sálvia escuro `#3D4A3F` (slide 6).

### 1.4. Tipo de comunicação (texto)
6 opções: clássica/profissional, bem-humorada, técnica, inspiracional, descontraída/casual, polêmica/provocativa. Default: "clássica direta".

### 1.5. Desejo principal do público (pergunta EXTRA do estilo Erros)
Pergunte: "Qual o desejo concreto do seu público?"

**Regra de exemplo personalizado.** Antes de exibir, leia `perfil.md` (Quadro, Decorados, nicho) e `idconsumidor.md` (dores, desejos, paliativos) do produto ativo. Gere 2 a 3 exemplos de desejo COERENTES com o nicho do produto e o público-alvo, em vez de exemplos genéricos.

Exemplos por nicho:
- Produto de tarô → "tirar a primeira leitura sem trava, virar leitora consultora, deixar de depender de outros pra interpretar cartas"
- Produto de finanças → "sair do vermelho em 6 meses, montar a primeira reserva de emergência, parar de gastar tudo no dia 10"
- Produto fitness pós-parto → "voltar a calçar a calça pré-gravidez, tirar foto de praia sem culpa, ter energia pra brincar com filho sem cansar"

Se o perfil/idconsumidor não der pistas suficientes, use 2 exemplos neutros relacionados ao nicho. Aguarde a resposta e salve como `desejo_publico`.

### 1.6. Estilo de design visual
7 opções (Sofisticado e elegante, Editorial e cinematográfico, Despojado e bem-humorado, Energético e vibrante, Sério e técnico, Aconchegante e humano, Provocativo e ousado) ou descrição livre.

---

## Passo 2. Execução

A skill `/carrossel` no estilo Erros faz o seguinte:

1. **Carrega** `references/prompt-erros.md` inteiro.
2. **Executa o Passo 1 do prompt** (coleta de 6 dados, com o Desejo do público como pergunta extra), uma pergunta por turno, com pré-preenchimento de sugestão a partir do `perfil.md`/`idconsumidor.md`/`.env`.
3. Passa pela **confirmação consolidada** (Passo 2.5 da SKILL.md), incluindo o desejo declarado no resumo.
4. **Executa o prompt do Passo 2 ao Passo 4 exatamente como está**, na sessão atual:
   - Passo 2: gera os 6 slides (Slides 1-5 começam com `Erro #N:` e cada erro sabota o desejo declarado; Slide 6 é CTA criativa) com aprovação interna.
   - Passo 3: 3 outputs (chat slide por slide, arquivo `prompts.txt`, comando Cowork).
   - Passo 4: gera a legenda do Instagram com Manual da Copy e salva `legenda.txt`.
5. O texto dos 6 slides passa pelo **Manual da Copy + revisora** silenciosamente antes do gate de aprovação do Passo 2 do prompt.

---

## Diferenças importantes em relação aos outros estilos clássicos

| Aspecto | Erros (verbatim) | Estilos clássicos no modelo leve (Sempre, Odeio, Amo, Ninguém Conta) |
|---|---|---|
| Fonte de regras | `references/prompt-erros.md` (prompt completo, verbatim) | `references/estilos/{estilo}.md` (rules leves) + `passo-coleta-base.md` |
| Execução | A skill executa o prompt do estilo do início ao fim | A skill conduz Passo 3 padrão usando guidance leve |
| Coleta | 6 perguntas (inclui Desejo do público) | 5 perguntas (sem Desejo) |
| Output de prompts visuais | Output Triplo do próprio prompt (chat + `prompts.txt` + comando Cowork) | `passo-output-triplo.md` compartilhado |
| Output de legenda | Passo 4 do próprio prompt (com Manual da Copy citado explicitamente) | `passo-legenda.md` compartilhado |

---

## Modo "Gerar todos"

No fluxo "Gerar todos" (Passo 2 da SKILL.md, ramo `todos`), Erros roda com **valores pré-coletados** no Passo 2.B da SKILL.md (handle, nicho_produto, cores_marca, tom_texto, desejo_publico, estilo_design):

- A skill pula o Passo 1 do `prompt-erros.md` (Coleta interativa) e injeta os valores diretamente, inclusive o `desejo_publico` coletado uma única vez no Passo 2.B.
- Em seguida executa o Passo 2 do prompt sem o gate de aprovação interativa (aprovação acontece depois, em lote, no Passo 2.D da SKILL.md).
- Passo 3 e Passo 4 do prompt rodam normalmente (visuais e legenda).

---

## Saída no projeto

Pasta de saída:

```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-erros/
```

Arquivos gerados (definidos pelo próprio `prompt-erros.md`):
- `texto.md` (6 slides aprovados — convenção da skill, ver Passo 3 da SKILL.md)
- `prompts.txt` (6 prompts visuais em inglês, separados por linha em branco — Passo 3.2 do prompt)
- `legenda.txt` (legenda do Instagram, revisada pelo Manual da Copy — Passo 4.5 do prompt)

Adicionalmente, durante a execução o prompt entrega no chat o **comando Cowork** pronto para automatizar a geração das imagens no ChatGPT via Claude in Chrome.

---

## Paleta default

- **Slides 1-5.** Fundo creme bege `#F2EAD9` + texto verde-sálvia escuro `#3D4A3F`.
- **Slide 6 (CTA).** Fundo verde-sálvia escuro `#3D4A3F` + texto creme bege `#F2EAD9`.

Inverte o jogo de contraste no slide 6 para fechar com peso. Se o aluno responder com outra paleta no Passo 1.3, use a dele.

---

## Atmosfera fotográfica

Cenas que **sugerem sutilmente o erro/comportamento sabotador** descrito em cada slide. Luz naturalista cinematográfica, sem rosto humano nítido (apenas de costas/perfil quando houver figura humana). O prefixo `Erro #N:` no título pode ter destaque visual diferente (cor ou peso) se servir ao design, e o caractere `#` precisa ser renderizado corretamente, sem ser removido ou substituído.

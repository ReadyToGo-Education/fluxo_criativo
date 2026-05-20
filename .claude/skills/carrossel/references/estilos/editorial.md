# Estilo. Carrossel "Editorial"

> Carrossel de 6 slides com narrativa aprofundada de especialista, baseada em notícias reais, pesquisas científicas, dados concretos, polêmicas e contas malucas do nicho. O slide 1 abre com uma notícia/dado impactante; a venda só aparece no slide 6.
> Este estilo **delega o prompt-base** para `references/prompt-editorial.md`. O prompt é executado EXATAMENTE como está, sem reescrita. A única adaptação permitida é pré-preencher o Passo 1 (Briefing) com produto e público do produto ativo.
> O entregável final é UM PROMPT ÚNICO pra colar no ChatGPT que contém as instruções de todos os 6 slides; o aluno pede "cria o 1", "cria o 2"... até o 6.

---

## Coleta do Passo 1 da skill

O fluxo de coleta do Editorial **ignora** o `passo-coleta-base.md` padrão. A coleta é a do `prompt-editorial.md`:

### 1.1. Produto/serviço
"Qual o produto/serviço?"

Se `perfil.md` tiver Quadro/produto, pré-preencha como sugestão: "Sugestão a partir do seu produto: {valor}. Confirme ou corrija."

### 1.2. Público
"Qual o público?"

Se `idconsumidor.md` ou `perfil.md` tiver descrição clara do público, pré-preencha como sugestão.

### 1.3. Tipo de CTA do slide 6
"Qual CTA você quer no slide 6?"

1. ManyChat (comente X e receba isca no direct)
2. Seguir o perfil
3. Engajar (pedir opinião nos comentários)
4. Salvar o post

> O tema é escolhido depois, entre 10 ideias que a skill levanta no Passo 3 do prompt. Não pergunte na coleta.

---

## Passo 2. Execução

A skill `/carrossel` no estilo Editorial faz o seguinte:

1. **Carrega** `references/prompt-editorial.md` inteiro.
2. **Executa o Passo 1 do prompt** (Briefing), uma pergunta por turno, com pré-preenchimento de sugestão a partir do `perfil.md`.
3. **Executa o Passo 2 do prompt** (Tipo de CTA), exibe as 4 opções e aguarda escolha.
4. Passa pela **confirmação consolidada** (Passo 2.5 da SKILL.md).
5. **Executa o prompt da etapa Passo 3 à Passo 5 exatamente como está**, na sessão atual:
   - Passo 3: gera 10 ideias com ângulos variados (notícia real, polêmica, conta maluca, pesquisa científica, comparação) e pede pra escolher 1.
   - Passo 4: escreve o texto completo dos 6 slides + legenda do Instagram e pede aprovação.
   - Passo 5: entrega UM prompt único pra colar no ChatGPT (não 6 prompts separados).
6. O texto dos slides passa pelo **Manual da Copy + revisora** de forma silenciosa antes de ser exibido no Passo 4. As regras de copy do prompt (sem travessão, dados específicos em negrito, corpo em fonte regular, compliance sem doença/remédio) já estão alinhadas com o Manual.

---

## Diferenças importantes em relação aos 6 estilos clássicos

| Aspecto | 6 estilos clássicos | Editorial |
|---|---|---|
| Número de slides | 6 fixos | 6 fixos |
| Estrutura do slide 1 | Frase começando com "Nunca/Sempre/..." | Notícia/dado impactante com título grande + subtítulo menor + foto jornalística |
| Estrutura dos slides 2-5 | Continuação do padrão do estilo | Narrativa editorial. Slide 2 contexto/outro lado, slide 3 dado científico, slide 4 a virada, slide 5 reflexão |
| Slide 6 (último) | CTA criativa baseada nos 5 anteriores | CTA com fundo escuro e palavra-gatilho em amarelo dourado |
| Coleta extra | 5 dados base (@, nicho, paleta, tom, estilo de design) | 2 dados base (produto/serviço, público) + tipo de CTA |
| Geração de tema | Gerado dentro do estilo a partir do nicho | 10 ideias com ângulos variados, aluno escolhe 1 |
| Prompts visuais | 6 prompts em inglês template 4:5 | UM prompt único em português pra colar no ChatGPT |
| Legenda | Gerada à parte | Gerada junto com os 6 slides no Passo 4 |
| Saída no projeto | `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/` + texto + prompts + legenda | Mesma pasta, formato `carrossel-editorial/` com texto + legenda + prompt único do ChatGPT |

---

## Modo "Gerar todos"

No fluxo "Gerar todos" (Passo 2 da SKILL.md, ramo `todos`), Editorial roda com **escolha automática de tema**, igual ao modo aleatório da Notícia e da Curiosidade:

- A skill executa o Passo 3 do prompt (gera as 10 ideias) e, em vez de perguntar, **seleciona automaticamente a ideia mais forte** das 10 (maior potencial de gancho + dado mais sólido).
- O tipo de CTA usado é o coletado no Passo 2.B da SKILL.md (pergunta "Editorial: tipo de CTA").
- O restante do prompt (Passos 4 e 5) roda normalmente.

---

## Saída no projeto

Pasta de saída:

```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-editorial/
```

Arquivos gerados:
- `texto.md` (6 slides + legenda do Instagram, já aprovados no Passo 4 do prompt)
- `prompt-chatgpt.txt` (o prompt único pra colar no ChatGPT, gerado no Passo 5)

> A legenda do Instagram é entregue junto com os 6 slides no Passo 4 do prompt. Não há `legenda.txt` separado; a legenda fica dentro de `texto.md`.

---

## Paleta

Sem paleta default. A paleta vem das regras do prompt:
- Slides 1 a 5: fundo 100% branco
- Slide 6: fundo escuro com texto branco + palavra-gatilho em amarelo dourado (#FFD700)
- Tipografia sans-serif editorial
- Sem ícones, sem molduras, sem emoji decorativo

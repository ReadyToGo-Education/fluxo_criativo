# Estilo. Carrossel "Curiosidade"

> Carrossel que pega uma CURIOSIDADE ATEMPORAL do nicho (fato chocante, dado contraintuitivo, descoberta, recorde, estatística inusitada, bastidor conhecido) e transforma em narrativa de revista de 7 a 9 slides.
> Este estilo **delega o prompt-base** para `references/prompt-curiosidade.md`. O prompt é executado EXATAMENTE como está, sem reescrita. A única adaptação permitida é pré-preencher a Etapa 1 com dados do produto ativo.
> A âncora é o tema, não a data. Para notícia recente dos últimos 7 dias, o estilo certo é "Notícia" (opção 7 do menu).

---

## Coleta do Passo 1

O fluxo de coleta da Curiosidade **ignora** o `passo-coleta-base.md` padrão. A coleta é a Etapa 1 do `prompt-curiosidade.md`:

### 1.1. @ do Instagram
"Qual o @ do seu Instagram?"

Se `perfil.md` (ou `idconsumidor.md`) tiver um handle, pré-preencha como sugestão: "Sugestão a partir do seu produto: {handle}. Confirme ou corrija."

### 1.2. Nicho
"Qual o seu nicho? (ex: música, finanças, maternidade, surf)"

Se `perfil.md` tiver nicho, pré-preencha como sugestão.

### 1.3. Produto
"Qual o produto que você vende? (nome, formato e para quem é)"

Se `perfil.md` tiver Quadro, formato e público, pré-preencha como sugestão.

> O tema e o tom NÃO são coletados aqui. O tema é escolhido na Etapa 3 do prompt (depois da busca na web) e o tom na Etapa 4. No modo individual, são interativos. No modo "Gerar todos", veja a regra abaixo.

---

## Passo 2. Execução

A skill `/carrossel` no estilo Curiosidade faz o seguinte:

1. **Carrega** `references/prompt-curiosidade.md` inteiro.
2. **Executa a Etapa 1** (coleta de @, nicho, produto), uma pergunta por turno, com pré-preenchimento de sugestão a partir do `perfil.md`.
3. Passa pela **confirmação consolidada** (Passo 2.5 da SKILL.md).
4. **Executa o prompt da Etapa 2 à Etapa 7 exatamente como está**, na sessão atual:
   - Etapa 2: busca de 5 curiosidades atemporais via `WebSearch`.
   - Etapa 3: aluno escolhe 1 das 5.
   - Etapa 4: aluno escolhe o tom (7 opções).
   - Etapa 5: escreve os 7 a 9 slides.
   - Etapa 6: gate de aprovação do texto.
   - Etapa 7: prompts visuais nos 3 modos + arquivo consolidado.
5. A data para o nome do arquivo consolidado é calculada via `Bash` com `Get-Date -Format "yyyy-MM-dd"` (PowerShell).
6. O texto dos slides passa pelo **Manual da Copy + revisora** de forma silenciosa antes de ser exibido na Etapa 6. As regras de copy do prompt (sem travessão, sem exclamação, sem pergunta na capa, sem "não é X, é Y", toda afirmação com dado) já estão alinhadas com o Manual, então a revisão não altera o prompt, só garante o padrão.

---

## Diferenças importantes em relação aos 6 estilos atemporais

| Aspecto | 6 estilos atemporais | Curiosidade |
|---|---|---|
| Número de slides | 6 fixos | 7 a 9 (variável) |
| Estrutura do slide 1 | Frase começando com "Nunca/Sempre/..." | Capa com o FATO em até 8 palavras + subtítulo curto opcional |
| Slide N (último) | CTA criativa | CTA fixo: "Todos os dias, conteúdo sobre [nicho] aqui no @[handle]. Me segue para receber a próxima." |
| Prompts visuais | Template único 4:5 dois blocos | 3 modos (foto real composta, DALL-E ilustrativo, composição limpa) |
| Coleta extra | Sem Desejo, sem Objetivo | @, nicho, produto (Etapa 1) + tema (Etapa 3) + tom (Etapa 4) |
| Dependência externa | Não | `WebSearch` (busca real de curiosidades atemporais) |
| Arquivo consolidado | Não | `carrossel-curiosidade-[slug]-[data].txt` com delimitadores `=== SLIDE N ===` para automações |

---

## Modo "Gerar todos"

No fluxo "Gerar todos" (Passo 2 da SKILL.md, ramo `todos`), Curiosidade roda com **escolha automática de tema**, igual ao modo aleatório da Notícia:

- A skill executa a Etapa 2 (busca das 5 curiosidades) e, em vez de perguntar, **seleciona automaticamente a curiosidade mais forte** das 5 (maior potencial de gancho com o nicho + fonte mais sólida).
- O tom usado é o coletado no Passo 2.B da SKILL.md (pergunta "Curiosidade: tom").
- O restante do prompt (Etapas 5 a 7) roda normalmente.

---

## Saída no projeto

Pasta de saída:

```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-curiosidade/
```

Arquivos gerados:
- `texto.md` (slides 1 a N, já aprovados)
- `carrossel-curiosidade-[slug]-[data].txt` (arquivo consolidado da Etapa 7, Parte B, com os prompts visuais delimitados)

> A legenda do Instagram para a Curiosidade já vem embutida no slide N (CTA fixo). Se o aluno quiser uma legenda separada e mais elaborada, pode rodar a skill `revisora` em cima do texto.

---

## Paleta

Sem paleta default rígida. A paleta é determinada pelo prompt-base (Etapa 7) conforme o tema escolhido. Use:
- 3 cores em hex consistentes entre todos os slides (a mesma `PALETA` repetida em cada prompt visual)
- Tipografia serif editorial
- Sem ícones, formas geométricas decorativas ou emoji na arte

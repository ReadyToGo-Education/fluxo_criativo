---
name: workshop-marketing:copy-pagina
description: Criar copy completa e/ou página HTML de vendas, captura ou obrigado. Para vendas 8D, preenche blocos atômicos do repositório com a copy aprovada (preserva layout do tema; não redesenha o template). Light Copy e metodologia VTSD.
---

# Página de Vendas. Copy e HTML

Cria a copy completa da página de vendas e/ou a página HTML profissional com estrutura de conversão baseada na metodologia VTSD.

## Usage

```
/copy-pagina
```

---

## O Que Fazer

### 1. Contexto

Leia `meus-produtos/.ativo` para obter o slug do produto ativo. Depois leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md).

Para os bullets e os blocos de benefícios, leia também só a seção `## Decorados (Benefícios)` de `meus-produtos/{ativo}/perfil.md`. Se existir `meus-produtos/{ativo}/entregas/copy-pagina/bullets-{produto}.md` (gerado pelo `/copy-bullets`), use os bullets salvos como matéria-prima dos bullets das etapas do método (Bloco 06) e das descrições dos entregáveis (Bloco 08). Os 3 bullets do hero continuam no padrão Urgência Oculta + Decorado. Para o Bloco 07 (Para quem é / não é), leia também só a seção `## Baldes de Para Quem É` de `meus-produtos/{ativo}/idconsumidor.md` (se existir). Para o FAQ e a quebra de objeções, leia também só a seção `## Objeções de Compra` de `meus-produtos/{ativo}/idconsumidor.md` (se existir).

**Verificação de copy existente (obrigatória antes da Pergunta):**

Cheque se existe `meus-produtos/{ativo}/entregas/copy-pagina/copy-{ativo}.md` **E** se esse arquivo tem os 16 títulos `## Bloco 01` até `## Bloco 16` (numeração com dois dígitos, conforme `.claude/skills/paginas/references/template-copy-pagina-vendas.md`).

- **Copy existe e tem os 16 blocos** → estado **COM_COPY**. Pegue o tamanho do arquivo em KB e a data da última modificação (`stat` ou equivalente) para exibir no aviso.
- **Copy não existe OU está incompleta (faltando blocos)** → estado **SEM_COPY**.

### 2. Aviso de copy existente (OBRIGATÓRIO antes de qualquer pergunta)

**Se estado = COM_COPY**, mostre ANTES de qualquer outra coisa o bloco abaixo, em destaque, e espere o usuário confirmar:

```
✓ Copy aprovada encontrada

Arquivo: meus-produtos/{ativo}/entregas/copy-pagina/copy-{ativo}.md
Tamanho: {X} KB, {N} linhas, 16 blocos completos
Última modificação: {DD/MM/YYYY HH:MM}

Se regenerar, essa copy será sobrescrita. Como prosseguir?

1. Usar essa copy e gerar só a página HTML (recomendado, sem refazer texto)
2. Regenerar copy do zero (sobrescreve o arquivo atual)
3. Editar trechos da copy atual sem regenerar tudo (ajuste cirúrgico)

Digite o número:
```

Se o usuário escolher:

- **1** → informe que a copy está pronta e que o próximo passo é acionar `/pagina-visual` para gerar a página HTML seção por seção com prints de referência.
- **2** → siga para o Fluxo A (Só a copy), com aviso de que o arquivo anterior será substituído.
- **3** → pergunte quais blocos ele quer editar (ex: "Bloco 02, 09 e 15"), faça apenas esses ajustes na copy existente e depois pergunte se quer gerar a página HTML em seguida (via `/pagina-visual`).

**Se estado = SEM_COPY**, não mostre o aviso acima. Siga direto para a Pergunta 2.

### 3. Primeira Pergunta (apenas se estado = SEM_COPY)

```
O que você quer criar?

1. Só a copy (texto completo nos 16 blocos, pronta para qualquer template)
2. Só a página HTML (bloqueada sem copy aprovada)
3. Copy + página HTML (recomendado: copy nos 16 blocos primeiro, depois /pagina-visual)

Este produto ainda não tem copy aprovada. Recomendo a opção 3: a copy vai nos 16 blocos padrão, você aprova, e depois acionamos o /pagina-visual para montar a página HTML seção por seção. Assim você sai com copy + página finalizada em uma sessão.

Digite o número:
```

---

## FLUXO A. Só a Copy

> Ativar quando o usuário escolher a opção 1.

### A1. Entrevista rápida (máximo 2-3 perguntas)

Você já tem o `resumo-produto.md` e as seções lidas no passo 1 com Quadro, Furadeira, Decorados, Urgências Ocultas, Identidades, objeções e pesquisa de mercado. Use TUDO isso para gerar a copy. Pergunte apenas o que NÃO está no perfil:

```
Tem promoção, desconto ou condição especial ativa?
(ex: "Lançamento com 40% de desconto até sexta". ou "não")
```

```
Tem bônus específicos que quer incluir?
(ex: "Planilha de precificação + script de objeções". ou "não, pode criar")
```

```
Tem depoimentos reais? Se sim, passe nome e resultado de cada um.
(ex: "Ana, estava cobrando R$30, agora cobra R$120 por leitura". ou "não tenho")
```

```
Qual o ângulo de entrada da copy?

1. Inadequação. a pessoa está desatualizada ou fazendo errado
2. Identificação. a pessoa se reconhece na dor descrita
3. Plug & Play. a pessoa quer algo pronto para usar
4. Promessa Boa Demais. existe história real com números verificáveis

Digite o número:
```

**Pergunta de modo de geração (obrigatória antes do resumo):**

```
Como você quer que eu gere a copy?

1. Bloco a bloco (recomendado). eu gero um bloco, salvo no arquivo, você valida e só então passo para o próximo. Mais lento, qualidade maior, você corrige o rumo antes de acumular erros.
2. Em 2 partes. eu gero Blocos 01 a 09 de uma vez, depois 10 a 16, e só então você revisa tudo. Mais rápido, exige revisão maior no fim.

Digite o número:
```

Guarde a escolha como **MODO_GERACAO = bloco_a_bloco** ou **MODO_GERACAO = duas_partes** para usar em A3.

Confirme antes de gerar:

```
Resumo do que vou criar:
- Produto: [nome do produto]
- Preço: [preço do perfil]
- Ângulo: [ângulo escolhido]
- Bônus: [bônus informados ou "vou criar 3 coerentes"]
- Depoimentos: [reais ou "vou criar modelos para substituir"]
- Modo de geração: [Bloco a bloco com validação / Em 2 partes]

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### A2. Princípios de Copy (Light Copy. SEMPRE)

**Fonte única e obrigatória:** antes de gerar uma linha de copy, leia `.claude/skills/revisora/references/manual-copy.md`. É ali que vivem:

- O **princípio central** ("a melhor copy não parece copy").
- Os **15 princípios fundamentais** (ensinar em vez de prometer; nomear cria realidade; produto não aparece no lead; tom de escritor; especificidade mata generalização; informar, não vender; crie um inimigo; argumente sempre; razão + emoção; Quadro + Decorado; dor real; ancoragem em bônus; headline em toda seção; depoimento com resultado; autoridade com conquista concreta).
- Os **20 vícios proibidos** (travessão, "não é X, é Y", perguntas no gancho, promessa vaga, "mesmo que/sem precisar", produto no lead, emojis, imperativo, lero-lero, cópia sem tese, sigla sem explicação, depoimento genérico, autoridade sem prova, copy só de promessa, bônus sem valor, seção sem headline, Quadro sem Decorado, dor só sintoma, emoção sem razão, AI slop).
- O **checklist final** (Blocos A/B/C/D) que a `revisora` aplica antes da entrega.

A aprovação do usuário só acontece depois que esse checklist passar.

**Princípios específicos de página de vendas (reforço do Manual):**
1. **Headline em TODA seção:** nenhuma seção começa sem um título curto e curioso. Seção sem headline é seção invisível.
2. **Facilitação visual do método:** a Furadeira precisa virar diagrama, esquema ou comparativo no HTML, não só parágrafo.
3. **Depoimento com resultado concreto:** cada depoimento tem antes + depois + número ou prazo. Elogio genérico é marcado para substituição.
4. **Autoridade com conquista concreta:** o bloco de autoridade precisa da jornada de origem com fragilidade + virada + número ou situação verificável. Para low ticket sem autoridade pessoal, usar "método testado com X pessoas".
5. **Bônus ancorados em valor:** cada bônus tem nome, descrição e R$ individual. Stack de valor com total maior que o preço.
6. **Vender Quadro + Decorado, não só Quadro:** a cada bloco de benefício, um Decorado tangível aparece (não só a transformação ampla).
7. **Parágrafo técnico em itálico:** ao menos um parágrafo ancora a emoção com razão (explica por que aquilo funciona logicamente ou biologicamente).
8. **Nomear cria realidade:** criar nome próprio para o problema, a causa ou o método ("Programação Emocional Repetitiva", "Negociação Terapêutica"). "Método Exclusivo" não vale.

Use os 26 elementos literários quando apropriado (consulte skill `vtsd-completo` para lista completa).

### A2.5 Estrutura do arquivo de copy (obrigatória para vendas 8D)

A copy da página de vendas **deve** ser salva com **títulos fixos** alinhados aos blocos HTML (16 blocos). Consulte o modelo:

- `.claude/skills/paginas/references/template-copy-pagina-vendas.md`

**Regras:**

- Cada bloco = um título `## Bloco NN — Nome` **exatamente** como no template (numeração com dois dígitos: 01, 02, … 16).
- Não renomeie, não una dois blocos num só, não pule número. Isso garante que a página HTML use **a mesma copy** bloco a bloco.
- O conteúdo persuasivo segue as regras das seções abaixo, mas **sempre** sob esses títulos.

### A3. Geração da copy (16 blocos)

Use o **MODO_GERACAO** escolhido na confirmação. O arquivo é sempre o mesmo: `meus-produtos/{ativo}/entregas/copy-pagina/copy-[produto].md`.

**Lista de referência dos 16 blocos (usada pelos dois modos):**

- **Bloco 01 — Hero:** headline, subheadline, PROIBIDO nome do produto/método/curso/sigla no hero; 3 bullets (UO + decorado); indicação de vídeo; texto do botão.
- **Bloco 02 — Dor:** dor amplificada, cotidiano.
- **Bloco 03 — Paliativo:** ferramentas, produtos e soluções concorrentes do mercado que resolvem parcialmente o problema, e por que cada uma não entrega o resultado completo.
- **Bloco 04 — Prova social (primeiro bloco):** 2 a 3 depoimentos curtos; modelos marcados se não houver reais.
- **Bloco 05 — CTA intermediário:** frase + botão.
- **Bloco 06 — Método (Furadeira):** primeira vez com nome do método em destaque; macroetapas; mínimo 3 parágrafos de argumentação.
- **Bloco 07 — Para quem é / não é:** baldes da identidade do consumidor.
- **Bloco 08 — Entregáveis:** lista com nome + valor de cada item.
- **Bloco 09 — Bônus:** 3 bônus com nome, descrição e R$ cada.
- **Bloco 10 — Stack de valor:** itens, valores, total, preço real, parcelamento.
- **Bloco 11 — Prova social (segundo bloco) ou Depoimentos:** 3 a 5 depoimentos completos (antes/depois); modelos se necessário.
- **Bloco 12 — Suporte**
- **Bloco 13 — Garantia:** prazo (7/15/30), texto de risco zero.
- **Bloco 14 — Autoridade do criador**
- **Bloco 15 — FAQ:** 5 a 8 Q&A com objeções da persona.
- **Bloco 16 — Oferta final:** reprise de valor, preço, último CTA, urgência se houver; linha sobre termos/privacidade se aplicável.

---

#### MODO A3.1. Bloco a bloco (MODO_GERACAO = bloco_a_bloco)

Gere, salve e valide **um bloco por vez**. Loop para NN de 01 a 16:

1. **Anuncie antes:** `🔍 Próximo passo: gerar Bloco NN — {nome do bloco}. Tempo estimado: cerca de 20 segundos.`
2. Gere o texto do bloco com parágrafos desenvolvidos (persona, cenas, elementos literários onde couber), sob o título exato `## Bloco NN — {Nome}`.
3. Aplique a revisão A4 só neste bloco (travessão, vícios, nome do produto no hero, emojis, etc.) **antes** de mostrar.
4. **Salve imediatamente:** se o arquivo `copy-[produto].md` ainda não existir, crie-o com esse bloco. Se já existir, **acrescente** o novo bloco no final preservando os blocos anteriores. Nunca apague blocos aprovados.
5. **Atualize o painel de entregas** rodando no terminal: `py -3 scripts/painel-incremental.py --secao copy-pagina` (no Mac/Linux use `python3`). Esse script atualiza apenas a aba **Copy da Página** do `meus-produtos/{ativo}/painel-entregas.html`, preservando todas as outras seções já preenchidas (Quadro, Furadeira, Decorados, Urgências, Identidades, Pesquisa). O design escuro Fluxo Criativo é mantido. Em caso de erro, não pare o fluxo, apenas avise que o painel pode ser atualizado depois.
6. Confirme: `✅ Concluído: Bloco NN salvo e painel atualizado. Caminho: meus-produtos/{ativo}/entregas/copy-pagina/copy-[produto].md.`
7. Mostre o conteúdo do bloco no chat e pergunte:

```
Bloco NN/16 pronto e salvo no arquivo.

1. Aprovar e ir para o próximo bloco
2. Ajustar este bloco (diga o que mudar)
3. Pausar aqui (posso retomar depois com /copy-pagina)

Digite o número:
```

- Se **1:** avance para o próximo bloco.
- Se **2:** peça o ajuste, regenere **apenas este bloco**, sobrescreva a seção `## Bloco NN — …` no arquivo (mantendo os demais blocos intactos), rode de novo `py -3 scripts/painel-incremental.py --secao copy-pagina` para atualizar o painel, e volte ao passo 7.
- Se **3:** pare o loop, informe em que bloco parou e encerre. A próxima execução do command vê o arquivo com os blocos até NN-1 e pode continuar de NN. O painel de entregas já reflete o progresso parcial.

Exceção: se o usuário pediu explicitamente "ir direto à versão final" nesta sessão, pule a pergunta em cada bloco, gere os 16 em sequência salvando um a um, e só apresente no fim.

Ao concluir o Bloco 16, siga para A4 (revisão global) e A5 (confirmação final).

---

#### MODO A3.2. Em 2 partes (MODO_GERACAO = duas_partes)

Gere em **duas partes** no mesmo arquivo.

**PARTE 1. Blocos 01 a 09**

Anuncie: `🔍 Próximo passo: gerar Parte 1 (Blocos 01 a 09). Tempo estimado: cerca de 90 segundos.`

Gere e salve no arquivo. **Atualize o painel** rodando `py -3 scripts/painel-incremental.py --secao copy-pagina` (Mac/Linux: `python3`). Ao terminar, informe: `Parte 1 pronta (Blocos 01 a 09) e painel atualizado. Gerando a Parte 2 agora...`

**PARTE 2. Blocos 10 a 16**

Continue no **mesmo arquivo**, mesmo nível de detalhe. **Atualize o painel novamente** com `py -3 scripts/painel-incremental.py --secao copy-pagina` após salvar. Ao terminar, siga para A4.

### A4. Revisão e Correção Automática (OBRIGATÓRIO antes de entregar)

Antes de mostrar a copy ao usuário, acione a skill `revisora` passando o texto completo (todos os 16 blocos juntos). A `revisora` aplica o checklist do `.claude/skills/revisora/references/manual-copy.md` (Blocos A/B/C/D) e devolve o texto limpo com os ajustes feitos.

Aplique os ajustes propostos antes de mostrar a copy. Se a `revisora` devolver a copy sem ajustes, prossiga direto.

Após a revisão, informe ao usuário:
```
Revisão interna concluída. [X] ajuste(s) aplicado(s) na copy.
```

Só então apresente a copy corrigida e pergunte:
```
1. Aprovar e salvar
2. Quero ajustar algo
```

### A5. Salvar

`meus-produtos/{ativo}/entregas/copy-pagina/copy-[produto].md`

**Obrigatório:** o arquivo deve conter os **16** títulos `## Bloco NN — …` (dois dígitos), na ordem do `template-copy-pagina-vendas.md`. Sem isso, a página HTML não pode ser preenchida de forma fiel à copy.

### A6. Próximo Passo

```
Copy completa salva em meus-produtos/{ativo}/entregas/copy-pagina/copy-[produto].md

Quer montar a página HTML agora?

1. Sim, ir para /pagina-visual
2. Não agora

Digite o número:
```

Se escolher 1, acione a skill `pagina-visual`. A copy aprovada nos 16 blocos já está salva e será usada como fonte de texto pelo fluxo visual.

---

## FLUXO B. Página HTML

> A geração de HTML é feita exclusivamente pela skill `/pagina-visual`. Este fluxo apenas redireciona para ela com o contexto correto.

A copy aprovada nos 16 blocos já está salva em `meus-produtos/{ativo}/entregas/copy-pagina/copy-{ativo}.md`. O `/pagina-visual` usa esse arquivo como fonte de texto para cada seção da página.

Informe ao usuário:

```
Copy aprovada salva. O próximo passo é gerar a página HTML.

Use /pagina-visual para montar a página seção por seção com prints de referência.
A copy dos 16 blocos já está salva e será usada automaticamente como fonte de texto.

Próximos passos opcionais após a página pronta: /pagina-ajuste, /pagina-performance, /pagina-pixel, /pagina-checkout, /copy-anuncio.
```

Em seguida, acione a skill `pagina-visual`.

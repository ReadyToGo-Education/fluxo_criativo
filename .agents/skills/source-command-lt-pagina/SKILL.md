---
name: "source-command-lt-pagina"
description: "Criar a página de vendas low ticket pela régua v16 do time de criativos. Promessa central, 7 aberturas (Demonstração, Comparação, Plug & Play, Imaginação do Resultado, Defesa de Tese, Dor Espelhada, Resultado Direto) com tabela de prioridade de testes, copy completa (depoimentos na segunda seção, ancoragem de preço e seção de quem criou o produto) e um prompt único para o Lovable montar a página."
---

# source-command-lt-pagina

Use esta skill quando o usuário pedir o comando `/lt-pagina` do workshop (ou `lt-pagina`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/lt-pagina.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Página Low Ticket. Régua v16

Cria a página de vendas do produto low ticket em 3 etapas, com aprovação entre elas: promessa e 7 aberturas, copy completa e o prompt que o Lovable usa para montar a página.

**A régua completa está em `.claude/skills/pagina-low-ticket/SKILL.md`.** Leia o arquivo inteiro antes do Passo 2 e siga cada seção dele à risca. Este command é o roteiro com o aluno: diz a ordem, as perguntas, onde salvar e o que mostrar.

## Usage

```
/lt-pagina
```

---

## Passo 0. Contexto

1. Leia `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme "Contexto Persistente do Negócio" no CLAUDE.md).
2. Do resumo, tire as 3 informações que a régua pede:
   - **Produto:** seção `## Produto` (nome e formato).
   - **Preço:** seção `## Produto`.
   - **Como funciona** (o que a pessoa compra, recebe e faz com ele): seções `## Furadeira` e `## Produto`.
3. Se alguma das três faltar, pergunte só ela, uma pergunta por vez:

```
Como o seu produto funciona? O que a pessoa compra, recebe e faz com ele?
(ex: "um guia em PDF com 40 produtos coreanos separados por tipo de cabelo, com preço médio de cada um")
```

4. **Confira se o produto é low ticket.** Veja o `Tipo` e o `Preço` em `## Produto`. Siga direto quando o tipo for Low Ticket. Quando o tipo for Middle Ticket ou High Ticket, ou quando o preço passar de R$ 197 (o teto da régua), pare e pergunte:

```
Seu produto ativo, {nome}, está cadastrado como {tipo}, por {preço}.
Esta régua foi feita para produto de entrada, de resultado imediato
e decisão rápida. Para {tipo}, a página certa é a de vendas 8D.

1. Criar a página de vendas 8D com /copy-pagina (recomendado)
2. Seguir com a régua low ticket mesmo assim
3. Trocar de produto com /produto-trocar

Digite o número:
```

   - **1:** encaminhe para `/copy-pagina` e encerre este command.
   - **2:** siga para o Passo 1.
   - **3:** encaminhe para `/produto-trocar` e encerre.

   Com tipo "a definir" ou sem tipo e preço no resumo, siga e trate o produto como low ticket.

5. **O resto da régua também sai do produto.** Dor verdadeira, promessa, objeções, bullets, prova, tom e cores vêm do resumo, pela tabela do item 1 da seção "Como esta régua funciona no projeto", na skill. Não pergunte ao aluno o que o produto já tem.

---

## Passo 1. Página ou Quiz

Antes de criar a página, aplique o framework de decisão. **Nunca pergunte de cara qual formato o aluno quer.** Recomende com base nos critérios e explique o porquê.

| Critério | Aponta para QUIZ | Aponta para PÁGINA |
|---|---|---|
| Tipo de produto | Emocional / dor / identificação | Prático / ferramenta / direto ao ponto |
| Nível de consciência do lead | Não sabe que tem problema | Já sabe o que quer |
| Complexidade da decisão | Precisa diagnosticar / explicar | Decisão simples e direta |
| Faixa de preço | Até R$47 | Acima de R$97 |
| Tipo de público | Emocional | Analítico / pragmático |

**Regra:** 2 ou mais critérios para o mesmo lado, siga ele. **Desempate:** recomendar QUIZ (mais rápido de validar).

```
Com base no seu produto e público, minha recomendação é:

→ [QUIZ ou PÁGINA DE VENDAS]

Por quê:
• [Critério 1]: [explicação com dado real do produto]
• [Critério 2]: [explicação com dado real do produto]
• [Critério 3]: [explicação com dado real do produto]

Você pode trocar depois se quiser testar o outro formato.

1. Concordo, seguir com [recomendação]
2. Prefiro o outro formato
```

- **QUIZ:** encaminhe para `/lt-quiz` e encerre este command.
- **PÁGINA:** siga para o Passo 2.

---

## Passo 2. Etapa 1. Promessa e 7 aberturas

```
🔍 Próximo passo: criar a promessa central e as 7 aberturas da sua página, com a ordem de testes. Tempo estimado: 2 a 3 minutos.
```

Siga a régua nas seções "A DOR VERDADEIRA", "A PROMESSA CENTRAL", "REGRA DO PRAZO NO LOW-TICKET", "EMOÇÃO E TENSÃO", "ETAPA 1. AS 7 ABERTURAS", "HERO ESTENDIDO", "O PRIMEIRO VISUAL MOSTRA O MUNDO DO LEAD", "FORMATO DA ETAPA 1" e "TABELA DE PRIORIDADE DE TESTES".

Antes de mostrar, aplique a rotina de auto-revisão de copy do CLAUDE.md com a exceção da régua (pergunta na headline e "mesmo sem" liberados nas páginas low ticket).

Entregue no formato da régua: a linha `PROMESSA CENTRAL:`, as 7 opções já na ordem de prioridade, a tabela e a recomendação de teste A/B. Termine **só** com:

```
Qual dessas aberturas você quer usar? Pode responder pelo número ou pelo nome.
```

E pare.

Quando o aluno escolher, salve as 7 aberturas e a tabela em `meus-produtos/{ativo}/entregas/copy-pagina/lt-aberturas-{produto}.md` (servem para os próximos testes A/B), atualize o painel (item 9 da seção "Como esta régua funciona no projeto") e informe o caminho absoluto em uma linha.

---

## Passo 3. Etapa 2. Copy completa

Antes de escrever, até três perguntas, uma por vez (itens 2 e 3 da seção "Como esta régua funciona no projeto").

**3.1 Quem criou o produto.** O nome já está no resumo (`## Identidade do Comunicador`). Pergunte só os marcos:

```
Antes da copy, me conte quem está por trás do {nome do produto}.
Em 1 ou 2 parágrafos: os principais marcos e resultados reais da
sua história (tempo de mercado, números, formação, conquistas).
Se tiver uma foto sua, você vai anexá-la no Lovable junto com o prompt.
(ex: "Sou nutricionista há 12 anos, atendi mais de 3 mil pacientes e
criei o método no consultório")

Se preferir pular, responda "pular": a seção fica de fora da página.
```

Pule a pergunta quando os marcos reais já estiverem nos dados próprios dos `## Argumentos Incontestáveis`; nesse caso, só confirme se haverá foto.

**3.2 Depoimentos reais.**

```
Você já tem depoimentos reais de quem usou o produto?

1. Sim, vou colar aqui
2. Ainda não (a página nasce com depoimentos provisórios, que você
   troca pelos reais antes de publicar)

Digite o número:
```

- **1:** peça para colar os depoimentos e use as palavras originais.
- **2:** siga com os provisórios da régua.

**3.3 Vídeo (só na abertura Demonstração).**

```
O vídeo de demonstração já existe ou você vai gravar?

1. Já tenho o link (YouTube ou Shorts)
2. Vou gravar (te entrego o roteiro)

Digite o número:
```

Com link pronto, não entregue o roteiro "PARA VOCÊ GRAVAR" e diga qual formato a página vai usar: vertical para Shorts, horizontal para tutorial.

```
🔍 Próximo passo: escrever a copy completa da página com a abertura escolhida. Tempo estimado: 3 a 5 minutos.
```

Congele a estratégia e a perspectiva e siga a régua em "ETAPA 2. COPY COMPLETA" e nas seções seguintes até "FINAL DA ETAPA 2" (headlines de seção únicas, diálogos internos em lista, mecanismo, depoimentos na segunda seção, argumentos científicos, prova, oferta e garantia, quem criou o produto antes do FAQ, ancoragem de preço abrindo a oferta, bullets de curiosidade com a resposta no produto, quebra das 4 objeções, 3 passos na abertura Plug & Play e vídeo na abertura Demonstração).

- **Argumentos científicos:** decida pelo filtro de nicho da régua e diga em uma linha se entra ou não, e por quê. Se entrar, pesquise na web antes de escrever (`⏳ Passo: localizar e conferir os estudos.`). Sem pelo menos 2 estudos localizados e abertos, a seção não entra.
- **Nada inventado como fato:** número, garantia, prova, marco de quem criou o produto e estudo só se forem reais. Sem a informação, o elemento sai da página. A única exceção são os depoimentos provisórios da seção DEPOIMENTOS, quando o aluno ainda não tem os reais.
- **Ancoragem de preço:** o valor de cada item é uma estimativa honesta e a soma tem que bater. Parcelamento, valor à vista e "somente hoje" só entram se forem verdade.
- Aplique a rotina de auto-revisão de copy do CLAUDE.md, com a exceção da régua.

Mostre a copy seção por seção e, separadas no fim, as listas "DEPOIMENTOS PROVISÓRIOS (troque pelos reais antes de publicar)" (com o aviso em uma linha de que são fictícios), "PARA VOCÊ CONFERIR (não vai na página)" (estudos) e "PARA VOCÊ GRAVAR (não vai na página)" (roteiro do vídeo), quando existirem. Termine **só** com:

```
Aprovou a copy ou quer mudar alguma coisa antes de criarmos o design?
```

E pare. Ajuste só o que o aluno pedir e pergunte de novo.

Com a aprovação, salve em `meus-produtos/{ativo}/entregas/copy-pagina/lt-copy-{produto}-{abertura}.md` (a copy e, no fim, as listas de depoimentos provisórios, para conferir e para gravar), atualize o painel e informe o caminho absoluto.

---

## Passo 4. Etapa 3. Prompt do Lovable

```
🔍 Próximo passo: montar o prompt do Lovable com o design da sua página. Tempo estimado: 2 a 3 minutos.
```

**A copy está congelada.** Siga a régua de "ETAPA 3. DESIGN NO LOVABLE" até "TESTE FINAL DO DESIGN": paleta do nicho com HEX, imagem de cada seção fiel à copy, componentes de referência, grid, botões (nenhum na primeira dobra, flutuante no centro inferior), filtro crítico e o formato de entrega em 3 partes (instruções, mapa de seções e copy visível).

Os blocos que a régua manda incluir **inteiros, sem resumir**, entram copiados literalmente da skill: "REGRAS DE LAYOUT", "REGRA CRÍTICA DE IMPLEMENTAÇÃO", "ANTES DE FINALIZAR" e "VERIFICAÇÃO FINAL".

Mostre o prompt num único bloco, pronto para copiar, e pergunte:

```
1. Aprovar e salvar
2. Quero ajustar algo
```

Com a aprovação, salve em `meus-produtos/{ativo}/entregas/paginas/lt-prompt-lovable-{produto}-{abertura}.md`, atualize o painel, informe o caminho absoluto e explique:

```
✅ Concluído: prompt da página salvo. Caminho: {caminho absoluto}

Para montar a página:
1. Abra o Lovable (lovable.dev) e crie um projeto novo.
2. Cole o prompt inteiro e anexe a sua foto (para a seção de quem
   criou o produto) antes de enviar.
3. Quando a página ficar pronta, troque CHECKOUT_URL pelo link do seu
   checkout (e VIDEO_URL pelo vídeo ou link do YouTube, se a abertura
   for Demonstração).
4. Troque os depoimentos provisórios pelos reais. Página com
   depoimento inventado não vai ao ar.
5. Confira a página no celular antes de publicar.
```

---

## Passo 5. Próximo passo

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /criativo-estatico
Com a página no ar, crie os criativos para levar tráfego até ela.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Lembre também:
- **Teste A/B:** para testar a próxima abertura da tabela, rode `/lt-pagina` de novo e escolha outra. A copy e o prompt ganham arquivos próprios.
- **Painel de Entregas:** a aba Low Ticket mostra a promessa, a ordem de testes, as aberturas já criadas, a copy mais recente e o alerta enquanto houver depoimentos provisórios.
- **Revisão da página publicada:** `/feedback-low-ticket` audita a página pela mesma régua.

---

## Regras

1. Nunca pular uma etapa. Nunca criar o design antes da aprovação da copy.
2. Uma pergunta por vez, sempre com opções numeradas quando houver escolha.
3. Nada inventado como fato: estudo, número, garantia, resultado ou marco de quem criou o produto. Depoimento só real, com a única exceção dos provisórios da seção DEPOIMENTOS, sempre listados para troca e nunca publicados.
4. Nas páginas low ticket vale a exceção da régua: pergunta na headline, "mesmo sem" e depoimentos provisórios liberados. O resto do checklist de Light Copy continua valendo (sem travessão, sem ponto de exclamação, produto fora do lead, sem promessa vaga).
5. O projeto não gera o HTML da página low ticket: a entrega é o prompt do Lovable.

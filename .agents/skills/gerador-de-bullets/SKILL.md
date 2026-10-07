---
name: gerador-de-bullets
description: >
  Gera 110 bullets de copy (frases curtas de uma ou duas linhas que provocam curiosidade sobre uma
  entrega concreta do produto) a partir de duas informações: o nicho e o que a pessoa ensina ou entrega.
  Monta o inventário de entregas do produto, cruza com as 11 técnicas de bullet (benefício com obstáculo,
  erro e consequência, contradição aparente, detalhe específico, lista delimitada, substituição, diagnóstico,
  mecanismo com nome próprio, verdadeira razão e inimigo, condição e prova, inadequação), entrega 10 bullets por técnica
  numerados de 1 a 110 e fecha com os 10 bullets mais fortes prontos pra virar headline, assunto de e-mail
  ou abertura de anúncio.
  Use quando pedirem "gera bullets", "bullets pra minha página", "fascinations", "frases de curiosidade",
  "110 bullets do meu produto", "bullets pra VSL / e-mail / anúncio", ou quando descreverem o que ensinam
  e pedirem as frases que vendem isso.
  No projeto, roda pelo /copy-bullets: lê o resumo do produto ativo no lugar das duas perguntas e salva
  os bullets aprovados em meus-produtos/{ativo}/entregas/copy-pagina/bullets-{produto}.md, de onde
  /lt-pagina, /copy-pagina e outras skills de página os reaproveitam.
  Não escreve a página inteira (/lt-pagina, /copy-pagina), nem a VSL (/copy-roteiro), nem o anúncio
  completo, nem gera ideias de produto (/produto-novo). Os bullets são peças de copy, não a oferta.
  Base: guia "70 bullets para criação de produtos digitais" (7 técnicas), carta do Gary Halbert com a coleção
  de bullets do John Carlton, newsletter Bencivenga Bullets e o Manual da Copy, nos Apêndices A e B deste arquivo.
---

# Gerador de 110 bullets. Halbert, Carlton, Bencivenga e o guia das 7 técnicas

Skill autossuficiente. A partir do nicho e do que a pessoa ensina, monta o inventário de entregas do produto, cruza cada entrega com as 11 técnicas de bullet e devolve 110 bullets numerados, mais os 10 mais fortes separados no fim. A pessoa só informa o nicho e o conteúdo, e depois aprova ou pede ajuste.

Bullet é a frase curta que mostra uma descoberta útil e dá ao leitor um motivo concreto pra querer o resto. A curiosidade fica no caminho, a utilidade precisa estar clara. "Três perguntas para transformar um tema amplo em um problema que seu produto resolve" é bullet. "Aula sobre escolha de nicho" é descrição de sumário. O John Carlton escreve os bullets antes da headline: é neles que a oferta vira concreta.

> Idioma: responda sempre em português do Brasil, com acentuação correta.
> Travessão proibido em qualquer texto gerado. Use vírgula, ponto ou dois pontos. Ponto de exclamação proibido. Pergunta no bullet proibida: bullet é afirmação.

---

## Como esta skill funciona no projeto

O texto abaixo deste cabeçalho é o da skill original, com os ajustes listados no item 6. Esta seção diz como ela se encaixa no projeto.

1. **Entrada pelo `/copy-bullets`.** O command é o roteiro com o aluno: contexto, geração, aprovação e onde salvar.
2. **Contexto pelo resumo do produto, no lugar das duas perguntas.** Leia `meus-produtos/{ativo}/resumo-produto.md` (regra "Contexto Persistente do Negócio" do CLAUDE.md). Com produto ativo, não faça as perguntas do Passo 0: anuncie em uma linha o nicho e o que o produto entrega, como a própria skill manda quando o contexto já existe. As duas perguntas só valem sem produto ativo ou quando o aluno pedir bullets de outro produto.

   | Parte da skill | De onde vem no resumo do produto | Detalhe completo (só se precisar) |
   |---|---|---|
   | Nicho e público (pergunta 1) | `## Produto` (nicho) e `## Público (Identidade do Consumidor)` (perfil e frases que diria, para as palavras do público) | `idconsumidor.md`, `## Identidade do Consumidor` |
   | O que ensina ou entrega (pergunta 2) e o inventário do Passo 1 | `## Furadeira` (etapas do método, literais) e `Formato` em `## Produto`. Cada etapa e cada microetapa rende entrega | `perfil.md`, `## Furadeira (Método)` |
   | A dor real (Passo 1, item 3, e a cota de 10 bullets de dor real) | `## Urgências Ocultas`: Dores e Urgências Quentes | |
   | O Decorado (Passo 1, item 4, e a cota de 10 bullets de Decorado) | `## Decorados principais` | `perfil.md`, `## Decorados (Benefícios)` |
   | Crenças, contradição e diagnóstico (técnicas 3, 6 e 7) | `## Urgências Ocultas`: Dúvidas e Assuntos Relacionados; `## Objeções principais` | `idconsumidor.md`, `## Objeções de Compra (Framework dos 7 Argumentos)` |
   | O inimigo (técnica 9) e a inadequação datada (técnica 11) | `## Pesquisa de mercado (síntese)`: concorrentes, objeções reais do público e assuntos quentes | `pesquisa-mercado.md`, seções 2 (concorrentes), 5 (objeções reais) e 6 (assuntos quentes) |
   | Mecanismo com nome próprio (técnica 8) | Os nomes das etapas e dos mecanismos em `## Furadeira`. Dá para criar um nome novo para algo que o produto realmente faz (Apêndice A, técnica 8), nunca para algo que ele não entrega. O nome do método e as siglas ficam fora dos 10 quentes, que viram headline (produto fora do lead) | |
   | Condição e prova (técnica 10) | Só os dados próprios do aluno em `## Argumentos Incontestáveis` (alunos, faturamento, resultados). Dado de mercado não vira prova do produto | `perfil.md`, `## Argumentos Incontestáveis` |
   | Tom | `## Identidade do Comunicador`: tom, mantras e jargões; nada do que está em "Não gosta" (no perfil, "Evitar na comunicação") | |

3. **Aprovação e salvamento.** No Passo 5, as opções seguem o padrão do projeto ("1. Aprovar e salvar" e "2. Quero ajustar algo"). Aprovado, salve em `meus-produtos/{ativo}/entregas/copy-pagina/bullets-{produto}.md` (`{produto}` é o conteúdo de `meus-produtos/.ativo`), no formato do Passo 2 e do Passo 3, com uma linha de data no topo. Informe o caminho absoluto.
4. **Quem reaproveita os bullets salvos.** O arquivo é matéria-prima, nunca copiado sem filtro:
   - `/lt-pagina` e `/feedback-low-ticket` (régua `pagina-low-ticket`): as técnicas 1 a 7 desta skill são as 7 técnicas da seção BULLETS DE CURIOSIDADE da régua. A régua escolhe de 8 a 12, só os que têm resposta localizável numa parte do produto, e acrescenta a indicação "→ parte do produto";
   - `/copy-pagina`: bullets das etapas do método (Bloco 06) e descrições dos entregáveis (Bloco 08). Os 3 bullets do hero seguem no padrão Urgência Oculta + Decorado;
   - `/feedback-pagina` e `/pagina-ajuste`: ao reescrever bullets fracos de uma página existente;
   - `/elementos-literarios`: quando a peça escolhida for bullets;
   - `pagina-precheckout`: os 3 bullets curtos de benefício podem sair dos 10 quentes.
5. **Tempo do anúncio.** O anúncio do Passo 1 segue o formato do projeto e a faixa de `.claude/rules/tempo-estimado.md` ("Gerar 110 bullets").
6. **Ajustes feitos no texto original:** frontmatter com o nome da pasta e as skills do projeto; Passo 0 começa pelo resumo; caminho do Manual da Copy (`.claude/skills/revisora/references/manual-copy.md`); "as 11 técnicas de `tecnicas-de-bullet.md`" virou "do Apêndice A"; aprovação, encerramento e "Estrutura de pastas" passaram a salvar o arquivo do item 3; as skills irmãs viraram os commands do projeto (`pagina-low-ticket` → `/lt-pagina`; `roteiro-vsl` → `/copy-roteiro`, formato VVV; `ideias-low-ticket-urgencia` → ideias de produto do `/produto-novo`). Também foram corrigidos três deslizes do texto original: "mais 20" continua do 111, e não do 101 (sobra da versão de 100 bullets); o mapa de entrega fala em 11 técnicas, e não em 10; e a cota de pelo menos 5 bullets de inadequação datada, que só aparecia no checklist (f), entrou também nas cotas do Passo 2 e na seção 14 do Apêndice A. O anúncio do Passo 1 ganhou o número de passos e o tempo da tabela do projeto.

---

## Pré-requisitos de contexto

Antes da primeira pergunta, ler:

- o Apêndice A, no fim deste arquivo, (o que é bullet e o teste dos dois critérios, as 11 técnicas com estrutura, quando usar, exemplos certos e errados, o amplificador entre parênteses, os 5 passos do guia, a distribuição dos 110 e os antipadrões).
- o Apêndice B, no fim deste arquivo, (os bullets literais do Carlton e do guia por técnica, as lições do Halbert e do Bencivenga, o mapa de entrega para técnica e as 5 categorias de copy).
- `.claude/skills/revisora/references/manual-copy.md` (princípio central, 15 princípios, 20 vícios proibidos, checklist Blocos A a D). Todo bullet é copy e segue o Manual.

Se algum desses arquivos não estiver disponível (skill rodando sozinha no Claude chat, por exemplo), seguir com as regras resumidas nesta skill e nos apêndices da versão em arquivo único. Elas bastam.

Não perguntar o que já está no contexto. Se a pessoa já disse o nicho e o que ensina na primeira mensagem, anunciar em vez de perguntar: "Vi que você trabalha com X e ensina Y. Vou usar isso. Se quiser ajustar, me avisa." Se ela colou uma lista de aulas, módulos ou um sumário, usar como inventário de entregas e pular o Passo 1.

---

## REGRA DURA. Uma pergunta por turno

Fazer UMA pergunta, esperar a resposta, só então fazer a próxima. Nunca agrupar perguntas. Pergunta fechada sempre com opções numeradas e `Digite o número:`. Pergunta aberta sempre com exemplo entre parênteses.

---

## Passo 0. As duas perguntas de entrada

No projeto, comece pelo resumo do produto ativo (item 2 da seção "Como esta skill funciona no projeto") e pule as perguntas. Elas valem só sem produto ativo ou para bullets de outro produto: uma por turno, sem menu.

Primeira:

```
Vou gerar 110 bullets pro seu produto: frases curtas que despertam curiosidade sobre o que você entrega, prontas pra página, VSL, e-mail e anúncio.

Qual é o seu nicho? Pra quem você vende?
(ex: "Confeitaria pra quem vende bolo em casa", "Musculação pra homens acima de 40", "Arquitetura de interiores pra escritórios pequenos")
```

Aguarde a resposta. Depois, a segunda:

```
E o que você ensina ou entrega nesse produto? Pode escrever em texto corrido, ou colar o sumário, os módulos ou as aulas se já tiver.
(ex: "um curso de 6 módulos sobre precificação e captação de clientes", "um e-book com 12 receitas de bolo caseiro de alto giro", "uma planilha que monta o treino da semana")
```

Aguarde. Quanto mais concreto o que ela colar, melhores os bullets. Se vier vago ("ensino as pessoas a venderem mais"), fazer UMA pergunta de aprofundamento pedindo as entregas específicas (ex: "me dá 3 ou 4 coisas práticas que a pessoa aprende ou recebe: uma pergunta, um passo, uma ferramenta, um erro que você corrige").

## Passo 1. Inventário de entregas (uso interno)

Antes dos bullets, montar em memória uma lista de 12 a 20 entregas concretas do produto. Cada entrega é uma coisa que o produto faz a pessoa conseguir, evitar, decidir ou receber. Puxar de quatro lugares:

1. O que a pessoa colou (aulas, módulos, sumário, descrição).
2. O caminho do nicho: as etapas que a pessoa atravessa até o resultado grande (começo, erro comum, virada, resultado). Cada etapa rende entrega.
3. A dor real, não a superficial (Manual, princípio 11): o que constrange a pessoa na frente dos outros. Pelo menos 3 entregas saem daqui.
4. O Decorado, não só o Quadro (Manual, princípio 10): a consequência da técnica (dinheiro, tempo livre, reconhecimento, fila de espera, o que os outros dizem). Pelo menos 3 entregas saem daqui.

Se a pesquisa real na web ajudar a achar as palavras que o público usa e as crenças do nicho (pro inimigo e pra contradição), fazer busca curta. Não é obrigatório, não vira relatório. O inventário é insumo, não é mostrado.

Antes de gerar, anunciar em uma linha:

```
🔍 Próximo passo: montar os 110 bullets do seu produto nas 11 técnicas e separar os 10 mais fortes (4 passos). Tempo estimado: 3 a 5 minutos.
```

## Passo 2. Os 110 bullets (entrega principal)

Cruzar o inventário com as 11 técnicas do Apêndice A. Dez bullets por técnica, numerados de 1 a 110 em sequência contínua. Cada técnica vira um bloco com título e os seus 10 bullets.

As 11 técnicas, nesta ordem:

1. Benefício com obstáculo. Como [resultado] com [limitação concreta].
2. Erro e consequência. O erro em [etapa] que [consequência].
3. Contradição aparente. Por que [ação boa] pode [efeito ruim]; Como [ação inesperada] ajuda a [resultado].
4. Detalhe específico. A [pergunta, campo, ajuste] para [benefício].
5. Lista delimitada. [Número] [sinais, passos] para [resultado].
6. Substituição. Por que evitar [prática] e o que fazer no lugar.
7. Diagnóstico. Como descobrir se [problema] vem de [A] ou [B].
8. Mecanismo com nome próprio. O "[nome]" que [efeito].
9. Verdadeira razão e inimigo. A verdadeira razão por que [problema], que [inimigo] nunca contou.
10. Condição e prova. Se você [condição fácil], [resultado]; O que [autoridade] faz quando [situação].
11. Inadequação. Se você ainda [prática defasada, com ano, fonte ou ferramenta], [o que está perdendo].

Como gerar cada bloco:

1. Para a técnica, escolher 10 entregas diferentes do inventário. Nenhuma entrega se repete dentro do bloco. Entre blocos, a mesma entrega pode voltar só numa técnica bem diferente, e nunca com o mesmo benefício.
2. Escrever o bullet com a estrutura da técnica: abertura + objeto concreto + benefício ou consequência. Uma ideia por bullet.
3. Variar a abertura dentro do bloco. A estrutura é a mesma, a primeira palavra não precisa ser. Nunca dez bullets seguidos com a mesma primeira palavra.
4. Em até 28 dos 110, acrescentar o amplificador entre parênteses (prova, virada, quem mais não sabe, facilidade), com até 20 palavras, sem repetir o que o bullet já disse e sem virar segunda promessa.
5. Passar cada bullet no teste dos dois critérios: utilidade clara (dá pra apontar o que ganha ou evita) e curiosidade preservada (a resposta está dentro do produto). Falhou em um, reescreve ou troca.

Cotas que valem no conjunto dos 110:

- Pelo menos 66 com número, prazo, valor ou situação concreta.
- Pelo menos 10 falando do Decorado (a consequência), não só da técnica.
- Pelo menos 10 nascidos da dor real (o que constrange na frente dos outros).
- Pelo menos um inimigo concreto na técnica 9 (o que ensinam na faculdade, o professor do YouTube, a vendedora, o jeito antigo).
- Pelo menos 5 de inadequação datada na técnica 11 (com ano, fonte ou ferramenta).
- Nenhum bullet inventa número, passo ou prova que o produto não tem.

Formato da entrega:

```
## 110 bullets. {nicho}

### 01. Benefício com obstáculo
1. {bullet}
2. {bullet}
...
10. {bullet}

### 02. Erro e consequência
11. {bullet}
...
```

E assim até o bloco 11, bullet 110.

## Passo 3. Os 10 bullets quentes

Depois dos 110, separar os 10 mais fortes, de técnicas diferentes, com o número de origem, prontos pra virar headline, assunto de e-mail ou abertura de anúncio:

```
## 10 bullets quentes (os que eu levaria pra headline, e-mail e anúncio)

- (#) {bullet}
- (#) {bullet}
...
```

Critério de "quente": dor real ou desejo forte, número ou situação concreta, curiosidade alta, e sustenta prova. Nunca escolher dois do mesmo bloco se der pra variar.

## Passo 4. Revisão interna antes de mostrar (obrigatória, invisível)

1. Gerar os 110 e os 10 quentes internamente. Nada exibido ainda.
2. Aplicar o checklist do Manual da Copy (Parte 4, Blocos A, B, C). Bloco A é tolerância zero: zero travessão, zero exclamação, zero pergunta no bullet, zero "mesmo que / sem precisar", zero nome do produto dentro do bullet, zero "não é X, é Y".
3. Aplicar o checklist próprio desta skill (lista em Verificação, abaixo).
4. Acionar a skill `revisora` passando o texto inteiro. Aplicar as correções direto.
5. Se vier alerta `[REVISORA: ...]` que depende de dado que só a pessoa tem (número, prova, nome de técnica), reescrever o bullet pra uma versão que não depende daquele dado, ou pedir só esse dado em uma mensagem. Nunca mostrar bullet com prova inventada.
6. Só então mostrar. Nunca dizer que revisou, nunca entregar lista de problemas.

### Verificação silenciosa (checklist próprio)

- (a) Todo bullet passa nos dois critérios: utilidade clara e curiosidade preservada.
- (b) Nenhum bullet cego ("o segredo que muda tudo") e nenhum sumário disfarçado ("como escolher o nicho").
- (c) Nenhuma promessa maior que a prova; nenhum número ou passo inventado.
- (d) Cada técnica tem 10 bullets que batem com a estrutura dela; numeração 1 a 110 sem furo.
- (e) Nenhuma entrega repetida com o mesmo benefício; aberturas variadas dentro de cada bloco.
- (f) As cotas batem: 66 com concreto, 10 de Decorado, 10 de dor real, inimigo na técnica 9, pelo menos 5 de inadequação datada na técnica 11, até 28 com parêntese.
- (g) Os 10 quentes são de técnicas diferentes e trazem o número de origem.
- (h) Zero lero-lero (palavra genérica trocável por outra do mesmo campo sem mudar o sentido).
- (i) Nenhum bullet com mais de duas linhas nem com duas promessas.

## Passo 5. Aprovação e refinamento

Depois de mostrar, em uma linha:

```
Quer ajustar alguma coisa? Dá pra pedir mais de uma técnica ("mais erro e consequência"), focar numa entrega ("só sobre precificação"), deixar mais agressivo ou mais sóbrio, ou trocar os 10 quentes. Se estiver bom assim, me diz que eu fecho.

1. Aprovar e salvar
2. Quero ajustar algo
```

Com 2, perguntar o que ajustar, regerar só a parte pedida (um bloco, um recorte de entrega, os quentes) na mesma numeração, e repetir o convite. Pedido de "mais 20" gera numeração contínua (111 em diante) na técnica pedida.

## Passo 6. Encerramento

Quando a pessoa aprovar, salvar (item 3 da seção "Como esta skill funciona no projeto") e fechar conduzindo o próximo passo:

```
✅ Concluído: 110 bullets salvos. Caminho: {caminho absoluto}

Próximo passo, se precisar:
Página low ticket: /lt-pagina usa estes bullets na seção de bullets de curiosidade.
Página de vendas 8D: /copy-pagina usa estes bullets nas etapas do método e nos entregáveis.
VSL: /copy-roteiro (formato VVV) encaixa os bullets no empilhamento de valor e nas objeções.
E-mail ou anúncio: os 10 quentes viram assunto e primeira linha.
```

Esta skill entrega os bullets no chat e salva o arquivo aprovado. Não escreve a página nem a VSL, não continua pra outra skill no mesmo chat.

---

## Regras

1. Bullet tem os dois lados: utilidade clara e curiosidade preservada. Falta um, não é bullet.
2. Nenhum número, passo, prova ou nome de técnica entra no bullet sem existir (ou poder existir) no produto. Promessa nunca maior que a prova.
3. Bullet é afirmação. Nunca pergunta. Nunca nome do produto, "neste curso", "no módulo 2" dentro do bullet.
4. 110 bullets, 10 por técnica, numerados de 1 a 110, mais 10 quentes no fim.
5. Todo bullet passa pelo Manual da Copy e pela skill `revisora` antes de a pessoa ver. Sem exceção, sem avisar.
6. Português com acentuação. Sem travessão, sem ponto de exclamação, sem "mesmo que", sem "sem precisar", sem "não é X, é Y", sem lero-lero.
7. Nunca copiar literalmente bullet do Carlton ou do guia num produto que não entrega aquilo. Eles são modelo de forma, não de conteúdo.
8. Nunca expor como o sistema funciona por dentro (inventário, técnicas, cotas). Descrever o que a pessoa recebe.

## Quando NÃO usar esta skill

- Quer a página de vendas inteira do low ticket: `/lt-pagina`.
- Quer a página de vendas 8D inteira: `/copy-pagina`.
- Quer o roteiro de VSL: `/copy-roteiro` (formato VVV).
- Quer ideias de produto, não frases de copy: `/produto-novo` (opção de ideias de produto).
- Quer o anúncio completo ou o e-mail inteiro: skills de anúncio e de e-mail quando existirem. Aqui saem os bullets que alimentam essas peças.

## Estrutura de pastas criadas pela skill

Um arquivo, depois da aprovação: `meus-produtos/{ativo}/entregas/copy-pagina/bullets-{produto}.md`. A pasta `entregas/copy-pagina/` já existe em todo produto; se não existir, criar.

## Referências

- o Apêndice A, no fim deste arquivo,. As 11 técnicas com estrutura, quando usar, exemplos certos e errados, o teste dos dois critérios, o amplificador entre parênteses, os 5 passos do guia, a distribuição dos 110 e os antipadrões.
- o Apêndice B, no fim deste arquivo,. Os bullets literais do Carlton e do guia por técnica, as lições do Halbert (coleção de 500 bullets, bullet antes da headline) e do Bencivenga (prova maior que a promessa, alarme "sei, sei", Se/então, "o que estamos vendendo de verdade", SCAMPER), o mapa de entrega para técnica e as 5 categorias de copy.
- `.claude/skills/revisora/SKILL.md` e `.claude/skills/revisora/references/manual-copy.md`. Regras de linguagem de toda copy deste projeto.
- Skills irmãs no projeto: `/lt-pagina` (régua `pagina-low-ticket`), `/copy-pagina`, `/copy-roteiro` e as ideias de produto do `/produto-novo`.
- Fontes de origem: guia "70 bullets para criação de produtos digitais", "The Gary Halbert Letter" (coleção de bullets do John Carlton), "Bencivenga Bullets" (Gary Bencivenga).


---

# Apêndice A. As 11 técnicas de bullet


Base: o guia "70 bullets para vender a criação de produtos digitais" (7 técnicas com estrutura e 10 exemplos cada), a carta do Gary Halbert com a coleção de bullets do John Carlton e a newsletter Bencivenga Bullets. As 7 primeiras técnicas vêm do guia. As técnicas 8, 9 e 10 foram extraídas dos padrões do Carlton e do Bencivenga e dos princípios do Manual da Copy (nomear cria realidade, inimigo concreto, promessa do tamanho da prova).

---

## 0. O que é um bullet e qual o papel dele

Bullet é a frase curta, de uma ou duas linhas, que provoca curiosidade sobre uma coisa específica que o produto entrega. O Halbert chama de "teaser statement". O John Carlton escreve os bullets antes da headline, do subtítulo e do corpo da carta: é neles que a oferta ganha concretude.

O papel do bullet, segundo o guia: mostrar uma descoberta útil e dar ao leitor um motivo concreto para querer a explicação completa. A curiosidade fica no caminho; a utilidade precisa estar clara.

Exemplo de descrição e de bullet:

- Descrição: "Aula sobre escolha de nicho".
- Bullet: "Três perguntas para transformar um tema amplo em um problema que seu produto pode resolver".

A descrição diz o tema. O bullet diz o que a pessoa vai conseguir fazer e deixa a resposta pra dentro do produto.

### O teste de um bullet bom

Um bullet bom passa nas duas perguntas ao mesmo tempo:

1. Utilidade clara: dá pra apontar o que a pessoa ganha ou evita? (a pergunta certa, o erro que custa caro, o critério, o passo)
2. Curiosidade preservada: a resposta está dentro do produto, não no bullet?

Bullet que só tem curiosidade é bullet cego: "Um segredo que vai mudar tudo". Esconde tanto que não comunica valor. Proibido.

Bullet que só tem utilidade é descrição de sumário: "Como escolher o nicho". Diz o tema e entrega a resposta óbvia. Fraco.

### Anatomia

Abertura (Como, Por que, O erro em, A pergunta que, Os 3 sinais de, O "nome próprio" que) + objeto concreto (a etapa, a decisão, a ferramenta, a situação) + benefício ou consequência (o que ganha ou o que evita) + opcional: amplificador entre parênteses.

Tamanho: uma ou duas linhas. Até 25 palavras sem o parêntese. O parêntese, quando houver, até 20 palavras.

Uma ideia por bullet. Bullet com duas promessas vira dois bullets.

---

## Técnica 01. Benefício com obstáculo

O que faz: apresenta um resultado desejado e reconhece a dificuldade que faz o leitor pensar que aquilo não é pra ele. O caminho contorna um obstáculo específico, sem sugerir que todo esforço desaparece.

Estrutura: Como [resultado] com [limitação concreta, com número ou situação].

Quando usar: quando a pessoa se exclui da oportunidade por falta de audiência, experiência, tempo, dinheiro ou clareza.

Cuidado do Manual da Copy: "mesmo que" e "sem precisar" são vícios proibidos como muleta (vício 9). A técnica continua valendo, mas o obstáculo entra como situação concreta, não como muleta genérica. Troque "mesmo sem ter audiência" por "com 200 seguidores"; "sem precisar aparecer" por "com a câmera desligada"; "mesmo tendo pouco tempo" por "em 3 horas por semana".

Exemplos:

- "Como escolher o público do seu primeiro produto com 200 seguidores e nenhuma lista de e-mail." ✓ (obstáculo com número, resultado claro)
- "Como testar o interesse por uma ideia de curso antes de gravar a primeira aula." ✓ (obstáculo é a ausência do produto, situação concreta)
- "Como montar o cardápio de uma confeitaria caseira com um forno de 45 litros e R$ 300 de ingredientes." ✓
- "Como voltar a treinar depois dos 40 com o joelho que o ortopedista mandou poupar." ✓
- "Como ter resultados incríveis mesmo sem experiência." ❌ (muleta "mesmo sem", obstáculo vago, resultado vago)
- "Como vender todo dia sem precisar aparecer." ❌ (muleta "sem precisar", promessa maior que qualquer prova)

---

## Técnica 02. Erro e consequência

O que faz: liga uma decisão comum a um prejuízo que o leitor quer evitar. O bullet aponta a situação concreta e deixa a explicação do erro pra dentro do conteúdo.

Estrutura: O erro em [decisão ou etapa] que [consequência concreta].

Quando usar: desperdício de trabalho, ofertas confusas, decisões tomadas antes de validar, dinheiro gasto à toa, dano que a pessoa não percebe.

Exemplos:

- "O erro na escolha do tema que faz você gravar um curso inteiro antes de descobrir se alguém quer comprá-lo." ✓
- "O erro na escolha do preço que começa antes de você abrir a calculadora." ✓ (curiosidade: que erro acontece antes da calculadora?)
- "O erro na primeira semana de dieta que faz a balança subir 1 kg e a pessoa desistir no domingo." ✓
- "O erro na hora de alongar a lombar que piora a dor nos 3 dias seguintes." ✓
- "O erro que todo mundo comete e que destrói seus resultados." ❌ (sem etapa, sem consequência concreta, bullet cego)

---

## Técnica 03. Contradição aparente

O que faz: combina um benefício com uma ação que parece contrariá-lo. A explicação precisa resolver o paradoxo de forma plausível. A surpresa nasce de uma relação real, não de uma frase absurda.

Estrutura: Por que [ação aparentemente boa] pode [efeito indesejado]; ou Como [ação inesperada] ajuda a [resultado].

Quando usar: pra questionar hábitos comuns do nicho (adicionar mais, ampliar, tentar tudo, caprichar demais).

Exemplos:

- "Por que colocar mais aulas no seu produto pode deixar a transformação menos clara." ✓
- "Como uma primeira turma pequena ajuda a construir uma oferta mais precisa." ✓
- "Por que o bolo que cresce mais no forno é o que mais murcha na vitrine." ✓
- "Por que treinar abdominal todo dia atrasa a barriga que você quer." ✓
- "Por que seu peso, força e velocidade são as partes menos importantes de uma briga de rua." ✓ (Carlton; contradição com a crença do nicho)
- "Por que dormir mal faz você emagrecer." ❌ (absurdo, a explicação não sustenta; contradição precisa ser real)

---

## Técnica 04. Detalhe específico

O que faz: concentra a atenção em uma pergunta, frase, critério, campo ou ajuste concreto. Mostra o tipo de ferramenta entregue e a utilidade dela, sem revelar a ferramenta.

Estrutura: A [pergunta, frase, decisão, campo ou ajuste] para [benefício concreto].

Quando usar: quando o conteúdo entrega uma ferramenta aplicável. Evite chamar o detalhe de mágico ou garantir que ele sozinho resolve tudo.

Exemplos:

- "A pergunta para separar o que o aluno precisa aprender do que você apenas gostaria de ensinar." ✓
- "O campo no formulário de pesquisa que ajuda a colher as palavras que o cliente usa para descrever a dificuldade." ✓
- "O ajuste de 5 centímetros na posição do quadril que muda a potência da sua tacada." ✓ (Carlton, adaptado; número e objeto)
- "A frase para responder 'tá caro' sem dar desconto e sem perder o cliente." ✓
- "O detalhe que faz toda a diferença." ❌ (sem o detalhe, sem o benefício)

---

## Técnica 05. Lista delimitada

O que faz: promete um conjunto definido de critérios, perguntas, sinais ou passos. O número ajuda o leitor a visualizar o conteúdo e o esforço. Cada item precisa existir e acrescentar algo.

Estrutura: [Número] [sinais, perguntas, passos, decisões, critérios] para [resultado].

Quando usar: pra organizar decisões complexas em conjuntos fáceis de consultar. O número precisa bater com o conteúdo real.

Exemplos:

- "Três perguntas para transformar um tema amplo em um problema que seu produto pode resolver." ✓
- "Quatro sinais de que sua promessa está descrevendo conteúdo em vez de um resultado." ✓
- "Os 7 ingredientes que custam R$ 180 no carrinho e não mudam o sabor de nenhum bolo." ✓
- "As 3 primeiras coisas que você precisa fazer antes de tentar vender qualquer coisa para qualquer pessoa." ✓ (Carlton)
- "Dezenas de dicas para vender mais." ❌ (sem número, sem resultado)
- "As 58 perguntas que você precisa se fazer antes de lucrar de verdade." Só entra se as 58 existirem no produto.

---

## Técnica 06. Substituição

O que faz: mostra uma prática que merece ser revista e promete uma alternativa concreta. A força está em oferecer uma decisão melhor pra uma situação, sem transformar preferência em regra universal.

Estrutura: Por que evitar [prática em contexto] e o que fazer no lugar.

Quando usar: pra ensinar processo. O conteúdo explica em que condições a substituição faz sentido.

Exemplos:

- "Por que evitar começar pelo nome do produto e qual decisão tomar primeiro." ✓
- "Por que trocar a pergunta 'você compraria?' por uma conversa sobre o que a pessoa já tentou resolver." ✓
- "Por que trocar o alongamento antes do treino por 4 minutos de outra coisa." ✓
- "Por que evitar o desconto no primeiro 'tá caro' e o que oferecer no lugar." ✓
- "Por que você está fazendo tudo errado." ❌ (sem prática, sem alternativa)

---

## Técnica 07. Diagnóstico

O que faz: promete ajudar o leitor a distinguir problemas parecidos que exigem soluções diferentes. Torna o conteúdo valioso por evitar mudanças no lugar errado.

Estrutura: Como descobrir se [problema] vem de [causa A] ou de [causa B].

Quando usar: quando o leitor já tentou agir e não sabe o que corrigir. O conteúdo oferece critérios observáveis, não palpites.

Exemplos:

- "Como descobrir se sua ideia está sem demanda ou se você está apresentando o problema errado." ✓
- "Como distinguir falta de interesse de uma objeção que sua página ainda não respondeu." ✓
- "Como saber se o bolo solou por causa do forno ou da quantidade de fermento." ✓
- "Como descobrir se a dor no ombro vem do treino ou do jeito que você dorme." ✓
- "Como entender seus problemas de verdade." ❌ (sem as duas causas)

---

## Técnica 08. Mecanismo com nome próprio

O que faz: batiza a técnica, o fenômeno ou a ferramenta e promete o que ela faz. Nome transforma ideia em coisa que existe (Manual da Copy, princípio 2). O Carlton faz isso o tempo todo: "Stress Shock Phenomenon", "voice tool", "positioning secret", "hip-swinging secret".

Estrutura: O "[nome próprio]" que [efeito concreto]; ou Como usar a "[nome]" para [resultado].

Quando usar: quando o produto tem um método, uma técnica, um critério ou um passo que pode ganhar nome. O nome precisa existir no produto (ou ser criado e passar a existir nele). Nome entre aspas na primeira vez.

Exemplos:

- "A 'ferramenta de voz' que muda sua postura de calmo para dominante em qualquer situação surpresa." ✓ (Carlton)
- "Como evitar o 'Choque de Estresse' que derruba até faixa-preta em briga de rua e que nenhuma academia ensina." ✓ (Carlton, adaptado)
- "O 'Teste do Domingo' que mostra em 10 minutos se a sua dieta sobrevive à semana." ✓
- "A 'Pergunta do Espelho' que faz o cliente perceber sozinho que precisa do que você faz." ✓
- "O método exclusivo que vai revolucionar seus resultados." ❌ (nome genérico de vendedor; Manual, vício 4)

---

## Técnica 09. A verdadeira razão e o inimigo

O que faz: revela a causa real de um problema ou aponta quem orientou a pessoa errado (o que ensinam na faculdade, o professor do YouTube, os "especialistas", o jeito antigo). Quando a copy tem inimigo externo, a pessoa não precisa admitir que errou, só que foi mal orientada (Manual, princípio 7). O Carlton usa "The Real Reason", "the secret truth finally revealed", "experts are dead-wrong".

Estrutura: A verdadeira razão por que [problema], que [quem] nunca te contou; ou Por que [o que ensinam em X] está [custo concreto].

Quando usar: quando existe uma crença dominante no nicho que o produto contesta, ou um culpado concreto fora da pessoa. Precisa de tese: o bullet aponta a causa, o produto argumenta.

Exemplos:

- "A verdadeira razão por que as pessoas compram qualquer coisa, conhecida há décadas por vendedores, sociólogos e golpistas." ✓ (Carlton)
- "Por que os 'especialistas' das revistas de musculação estão errados em boa parte do que recomendam pra você crescer (o que funcionou pra quem treina com anabolizante não funciona pra você)." ✓ (Carlton, adaptado)
- "Por que o jeito de precificar que você aprendeu na faculdade está custando pelo menos R$ 20 mil por projeto." ✓ (Manual, princípio 13)
- "A verdadeira razão por que a vendedora da loja empurra 7 itens de enxoval que o bebê não usa." ✓ (Manual, princípio 6)
- "A verdade que ninguém te conta." ❌ (sem problema, sem razão, sem inimigo)

---

## Técnica 10. Condição e prova

O que faz: amarra a promessa a uma condição fácil de cumprir (Bencivenga: a construção "Se... então" desliga o alarme do "sei, sei") ou a uma prova (quem faz, quanto tempo levou pra descobrir, em quantas pessoas foi testado). Promessa nunca maior que a prova.

Estrutura: Se você [condição fácil e concreta], [resultado]; ou O que [grupo com autoridade] faz quando [situação]; ou Como [pessoa real] descobriu [resultado] depois de [prova].

Quando usar: quando a promessa é grande e precisa de âncora de credibilidade; quando o produto tem teste, número de alunos, tempo de pesquisa ou autoridade de terceiros. Prova inventada piora a copy (Manual, princípio 15).

Exemplos:

- "Se você tem 20 minutos por mês, dá pra organizar as finanças da casa com este método (o teste venceu a concorrente por anos)." ✓ (Bencivenga, adaptado)
- "O que os médicos fazem quando eles mesmos têm dor de cabeça." ✓ (Caples via Bencivenga; venceu por 71%)
- "O programa de aeróbico que o Leo levou 7 meses pesquisando com fisiculturistas nos EUA e na Alemanha pra descobrir." ✓ (Carlton; prova no bullet)
- "Como 3 professoras de balé de cidades com menos de 50 mil habitantes lotaram a turma da tarde em 2 meses." ✓ (prova com número; só se existir)
- "Comprovado cientificamente: funciona com qualquer pessoa." ❌ (prova vaga, promessa maior que a prova)

---

## Técnica 11. Inadequação (o atraso)

O que faz: mostra a pessoa fazendo do jeito velho, defasado, igual a todo mundo, com o recurso ultrapassado, e aponta o que ela perde por ter ficado parada. Desperta o desconforto de estar atrás sem acusar a pessoa diretamente: a culpa é da prática datada, não dela. É a forma afirmativa do clássico "Do You Make These Mistakes in English?" (Bencivenga), virado de pergunta em afirmação e ancorado numa marca concreta de tempo, de origem ou de ferramenta.

Estrutura: Se você ainda [prática defasada, com ano, fonte ou ferramenta], [o que está perdendo]; ou O que mudou em [coisa] desde [ano] e ninguém te avisou.

Quando usar: quando existe um jeito novo contra um jeito velho, uma prática datada, uma fonte que todo mundo copia, uma ferramenta ultrapassada. O atraso precisa ser concreto (um ano, um lugar, uma ferramenta), nunca "você está ultrapassada" no vazio. Aponta a prática, não a pessoa, e deixa a saída pra dentro do produto.

Cuidado: bullet é afirmação, nunca pergunta. A inadequação do Manual da Copy entra como inimigo concreto (princípio 7), não como humilhação. Se a frase ataca a pessoa em vez da prática, sai.

Exemplos:

- "Se você ainda precifica o bolo igual fazia em 2006, o aumento do ovo e da farinha está saindo do seu bolso." ✓ (marca de tempo, o que ela perde)
- "Se o seu bolo sai igual ao da receita que todo mundo copia da internet, ele compete só pelo preço." ✓ (fonte comum, consequência)
- "O que mudou no custo de um bolo desde 2020 e derruba a margem de quem não reajustou." ✓ (data, inadequação de quem ficou parado)
- "Se você ainda anota pedido e preço no caderninho, perde o reajuste toda vez que o ingrediente sobe." ✓ (ferramenta datada)
- "Se o seu cardápio é o mesmo há três anos, carrega dois ou três bolos que só ocupam o forno." ✓
- "Você ainda faz bolo do jeito errado?" ❌ (pergunta, e humilha sem nada concreto)
- "Se você é ultrapassada na confeitaria." ❌ (ataca a pessoa, sem prática concreta, sem o que ela perde)

---

## 12. O amplificador entre parênteses (Carlton)

Depois do bullet, um parêntese que adiciona uma das quatro coisas:

1. Prova: "(Leo pesquisou 7 meses com fisiculturistas profissionais pra chegar nisso.)"
2. Virada ou surpresa: "(É tão simples que parece trapaça.)"
3. Quem mais não sabe: "(Nem um profissional em mil suspeita da força desse ajuste.)"
4. Facilidade: "(Conheço avós de 80 anos com artrite que nocautearam agressores jovens com isso.)"

Regras: no máximo 20 palavras; até 28 dos 110 bullets levam parêntese; nunca repete o que o bullet já disse; nunca vira segunda promessa; sem ponto de exclamação, que o Carlton usa e o Manual proíbe.

---

## 13. Da estrutura ao bullet final (os 5 passos do guia)

1. Comece pelo conteúdo real. Anote a pergunta que a aula responde, a decisão que ajuda a tomar ou a tarefa que ensina a executar. Bullet não corrige a falta de uma entrega útil.
2. Escolha o motivo pra ler. Avançar apesar de uma dificuldade? Evitar um erro? Entender uma contradição? Ter uma ferramenta? Seguir uma lista? Trocar um hábito? Diagnosticar? Nomear? Culpar o inimigo certo? Acreditar? Esse motivo define a técnica.
3. Deixe o benefício claro. "Um segredo que vai mudar tudo" esconde tanto que não comunica valor. "A pergunta para separar o que o aluno precisa aprender do que você apenas gostaria de ensinar" mostra a utilidade e preserva a curiosidade.
4. Revise a promessa. Dá pra apontar onde está a resposta no produto? O resultado depende de condições que precisam aparecer? Tem estatística, exclusividade ou garantia sem fundamento? Remova exageros e mantenha o que pode sustentar.
5. Monte uma sequência variada. Combine técnicas pra abordar motivos diferentes de compra. Evite dez frases com a mesma abertura. Priorize os bullets mais relevantes pro público e elimine os que repetem o mesmo benefício.

---

## 14. Distribuição dos 110 e regras de variedade

- 11 técnicas, 10 bullets por técnica, numerados de 1 a 110 em sequência contínua.
- Dentro de cada técnica, as 10 frases cobrem entregas diferentes do produto. Nenhum benefício se repete dentro do bloco nem entre blocos.
- Dentro de cada técnica, variar a abertura: a estrutura é a mesma, a primeira palavra não precisa ser. "Como" pode virar "O jeito de", "O caminho para"; "Por que" pode virar "O motivo de"; "O erro" pode virar "A decisão", "O hábito", "O atalho".
- Pelo menos 66 dos 110 bullets com número, prazo, valor ou situação concreta.
- Até 28 com amplificador entre parênteses.
- Pelo menos 10 falando do Decorado (a consequência: dinheiro, reconhecimento, tempo livre, fila de espera, o que os outros dizem), não só do Quadro (a técnica).
- Pelo menos 10 nascidos da dor real (o que constrange a pessoa na frente dos outros), não da dor superficial que ela diz primeiro.
- Pelo menos 5 de inadequação datada na técnica 11 (com ano, fonte ou ferramenta).
- Ao final dos 110, os 10 bullets quentes: os mais fortes, de técnicas diferentes, com o número de origem, prontos pra virar headline, assunto de e-mail ou abertura de anúncio.

---

## 15. Antipadrões (bullet que não entra)

- Bullet cego: curiosidade sem utilidade ("o segredo que muda tudo", "a verdade que ninguém conta", "o detalhe que faz toda a diferença").
- Sumário disfarçado: utilidade sem curiosidade ("como escolher o nicho", "introdução ao tráfego pago").
- Promessa maior que a prova: "dobre o faturamento em 7 dias", "funciona com qualquer pessoa", "comprovado cientificamente" sem a prova.
- Número inventado: lista de 7 passos que o produto não tem; estatística sem fonte.
- Pergunta: bullet é afirmação. "Você sabia que...?" sai.
- Ponto de exclamação, travessão, "mesmo que", "sem precisar", "não é X, é Y".
- Nome do produto, "neste curso", "na aula 3", "no módulo 2" dentro do bullet. O bullet fala da descoberta, não do produto.
- Lero-lero: "padrão interno", "jornada de autoconhecimento", "destravar seu potencial", "elevar o nível", "de forma estratégica". Se dá pra trocar a palavra por outra do mesmo campo sem mudar o sentido, é lero-lero.
- Duas promessas no mesmo bullet.
- Bullet com mais de duas linhas.
- Dez bullets seguidos com a mesma primeira palavra.
- Cópia literal de bullet do Carlton ou do guia em produto que não entrega aquilo.


---

# Apêndice B. Exemplos literais e fontes


Material de consulta pra calibrar a forma dos bullets. São modelos de FORMA, não de conteúdo: nunca copiar um bullet destes num produto que não entrega aquilo.

---

## 1. A lição do Gary Halbert (The Gary Halbert Letter)

Halbert conta que o John Carlton, um dos melhores copywriters que ele conheceu, sempre começa escrevendo os bullets primeiro. Só depois vai pra headline, subtítulo, corpo e instruções de pedido. Bullet é a peça fundadora da carta: é onde a oferta vira concreta.

O exercício que Halbert manda fazer pra aprender a escrever bullet:

1. Pegar 500 fichas de 3x5.
2. Ir à banca (ou à biblioteca) e pegar dezenas de revistas com muita chamada na capa. A Cosmopolitan é a campeã de bullets de capa.
3. Escrever um bullet por ficha, só os quentes, até ter 500.
4. O ganho é um "imprint neurológico" de escrever bons bullets. Não tem atalho.

Regra que ele repete: só dá pra escrever assim pagando o preço (volume e obsessão). E o lembrete do próprio material: as promessas dos bullets precisam ser verdadeiras.

### Bullets do John Carlton citados por Halbert (modelos de forma)

Negócios e copy:

- "As 58 perguntas mais importantes que você precisa se fazer antes de começar a empilhar lucro no seu negócio."
- "A fórmula de 7 passos que até um analfabeto evadido da escola pode usar pra escrever copy 100 vezes mais potente que a da melhor agência da Madison Avenue."
- "Como os 3 elementos básicos de todo infomercial de milhões também servem pra turbinar seus anúncios de jornal."
- "Por que seu 'back end' pode ser mil vezes mais lucrativo que a primeira venda, e o que fazer pra aproveitar isso agora."
- "Os 10 mercados mais fáceis pro copywriter iniciante explorar com lucro máximo e risco mínimo."
- "Um jeito 'sem esforço' (e quase sempre ignorado) de aumentar o valor do pedido médio em 100% ou mais, no automático."
- "As 3 primeiras coisas, absolutamente essenciais, que você precisa fazer antes de tentar vender qualquer coisa pra qualquer pessoa."
- "A verdadeira razão por que as pessoas compram qualquer coisa, a verdade secreta conhecida por mestres de venda, sociólogos e golpistas, enfim revelada."
- "20 maneiras garantidas de aumentar a leitura e a resposta das suas cartas de venda sem tocar na copy atual."

Briga de rua e defesa (mesma forma, outro nicho):

- "Por que seu peso, força, velocidade e agilidade são as partes menos importantes de vencer uma briga de rua."
- "Como evitar os erros que fazem até faixas-pretas ranqueados nacionalmente serem destruídos na rua (chama-se 'Choque de Estresse', e nenhuma academia do país ensina)."
- "A 'ferramenta de voz' que muda na hora sua atitude de calmo pra dominante em qualquer situação de surpresa."
- "Golpes simples que encerram a briga e não exigem força nenhuma (conheço avós de 80 anos com artrite que nocautearam agressores jovens)."
- "Um 'segredo de posicionamento' pouco conhecido que anula por completo o tamanho ou a experiência do agressor."

Fitness e golfe (mesma forma, outro nicho):

- "O segredo de achar o programa aeróbico mais eficiente pra queimar gordura no seu tipo de corpo (o Leo pesquisou 7 meses com fisiculturistas dos EUA e da Alemanha pra descobrir)."
- "Por que os 'especialistas' das revistas de musculação estão errados em boa parte do que recomendam (o que funciona pra quem treina com anabolizante não funciona pra você)."
- "Como uma mudança 'secreta' de 5 centímetros na posição do quadril vira potência bruta na sua tacada (nem um profissional em mil suspeita da força desse ajuste)."
- "Como usar o segredo de 'encurtar a pegada' pra dominar qualquer taco do seu saco, não importa o quão ruim você fosse com ele antes."

O que esses bullets ensinam sobre forma: número no começo quando possível; objeto nomeado; parêntese que adiciona prova, facilidade ou surpresa; a mesma estrutura serve pra qualquer nicho (copy, briga, fitness, golfe); o inimigo externo aparece (a academia que não ensina, o especialista errado).

---

## 2. As lições do Gary Bencivenga (Bencivenga Bullets)

Bencivenga é o copywriter de resposta direta mais testado dos EUA. A newsletter dele é a fonte dos princípios de credibilidade que a técnica 10 usa.

### 2a. Prova maior que a promessa (o princípio central dele)

"Never make your claim bigger than your proof. And always join your claim and your proof at the hip in your headlines, so that you never trumpet one without the other." (Nunca faça a promessa maior que a prova, e sempre junte promessa e prova lado a lado, pra nunca anunciar uma sem a outra.)

Pro bullet: quando a promessa for grande, ela entra junto com a prova ou com a condição. Sem isso, dispara o alarme.

### 2b. O alarme "sei, sei" (yeah, sure)

As duas palavras mais poderosas da publicidade hoje, diz Bencivenga, são "sei, sei". É o que o público pensa diante de toda promessa grande: "fique rico rápido" (sei, sei), "emagreça rápido" (sei, sei). Palavras queimadas como "grátis", "novo", "revolucionário", "comprovado" disparam o alarme na hora.

Pro bullet: evitar as palavras queimadas e as promessas infladas. Quem grita não vende; "yelling is not selling". Em vez de aumentar o volume da promessa, aumentar a prova.

### 2c. A construção Se... então (IF... THEN)

Amarrar a promessa a uma condição fácil de cumprir desliga o alarme. Exemplo que venceu o teste e virou controle por anos: "Se você tem 20 minutos por mês, eu garanto um milagre financeiro na sua vida." A mesma fórmula funcionou pra um produto de emagrecimento: "Se você tem 20 minutos por mês, eu garanto uma versão mais magra e saudável de você." (Note a ausência de ponto de exclamação, que aumenta o cheiro de hype.)

Pro bullet: técnica 10. "Se você [condição fácil], [resultado]." A exigência fácil dá crédito à promessa.

### 2d. "O que estamos vendendo de verdade?" (what are we really selling?)

A pergunta de cinco palavras que abre mercado. Não se vende semente de grama, vende-se um gramado mais verde. Não se vende ingresso de beisebol, vende-se a lembrança das tardes de sol que o pai e os filhos vão guardar pra sempre. Revson: "Na fábrica fazemos cosméticos. Na loja vendemos esperança."

Pro bullet: por trás da entrega técnica (o Quadro) tem a consequência que a pessoa quer de verdade (o Decorado). Pelo menos 10 dos 110 bullets vendem o Decorado.

### 2e. "Do you make these mistakes?" (o anúncio do Sherwin Cody)

A headline "Você comete estes erros em inglês?" ficou imbatível por 40 anos. O corpo listava os erros constrangedores que a pessoa comete, provando por que ela precisa do curso. Bencivenga adaptou pra "Você comete estes erros com vitaminas?". Vira bullet na forma afirmativa: "Os erros de inglês que fazem gente formada parecer que não estudou." É a técnica 2 (erro e consequência) com o constrangimento como consequência.

### 2f. Prova pela autoridade de terceiros ("When doctors have headaches")

Teste do John Caples: "Dor de cabeça tensional?" contra "O que os médicos fazem quando eles mesmos têm dor de cabeça?". A segunda venceu por 71%, porque amarra a promessa a uma prova (médicos). A palavra "médicos" sobe a resposta porque sobe a prova.

Pro bullet: técnica 10. "O que [autoridade] faz quando [situação]." Só com autoridade real do produto.

### 2g. SCAMPER (as 11 formas de gerar variação)

Acrônimo de Alex Osborn que o Bencivenga usa pra nunca ficar sem ideia. Serve pra gerar os 10 bullets de uma técnica a partir das entregas:

- S = Substituir (um elemento por outro mais surpreendente ou atual).
- C = Combinar (elementos de duas entregas diferentes).
- A = Adaptar (um bullet campeão de outro nicho pra este).
- M = Modificar, minificar ou magnificar (o número, o prazo, o tamanho).
- P = Pôr em outro uso (quem mais usaria isso e por quê).
- E = Eliminar (tirar um elemento que sempre aparece e ver o que acontece).
- R = Rearranjar, reverter ou redefinir (a ordem, o ângulo, o problema).

Quando faltar variação dentro de um bloco, rodar SCAMPER sobre as entregas.

### 2h. Crença (belief)

Caples: publicidade eficaz é "uma promessa crível pro público certo". Sem crença, ninguém compra. A maioria foca só na promessa (a parte divertida) e ignora a construção da crença. Pro bullet: a curiosidade abre, a prova sustenta.

---

## 3. O guia das 7 técnicas (70 bullets para criação de produtos digitais)

As 7 primeiras técnicas desta skill vêm daqui, cada uma com estrutura, quando usar e 10 exemplos. O guia foi escrito pro nicho "criação de produtos digitais", então os exemplos falam de curso, oferta, página e IA. Servem de molde de forma pra qualquer nicho.

Nota de autoria do próprio guia: as categorias são organização didática, os exemplos são originais (não são citações do Halbert nem do Bencivenga) e funcionam como modelos: números, perguntas, ferramentas e passos citados precisam existir no produto em que forem usados.

Exemplos de cada técnica (do guia, nicho de produtos digitais):

- Benefício com obstáculo: "Como transformar sua experiência de trabalho em uma oferta mesmo sem nunca ter dado uma aula." (reescrever o "mesmo sem" pra situação concreta ao aplicar)
- Erro e consequência: "O erro na escolha do preço que começa antes de você abrir a calculadora."
- Contradição aparente: "Por que colocar mais aulas no seu produto pode deixar a transformação menos clara."
- Detalhe específico: "A pergunta para separar o que o aluno precisa aprender do que você apenas gostaria de ensinar."
- Lista delimitada: "Três perguntas para transformar um tema amplo em um problema que seu produto pode resolver."
- Substituição: "Por que trocar a pergunta 'você compraria?' por uma conversa sobre o que a pessoa já tentou resolver."
- Diagnóstico: "Como descobrir se sua ideia está sem demanda ou se você está apresentando o problema errado."

---

## 4. Mapa de entrega para técnica

Dada uma entrega do inventário, qual técnica rende melhor. Serve pra distribuir as entregas pelas 11 técnicas sem forçar.

| A entrega é... | Técnica mais natural |
|---|---|
| Um resultado que a pessoa acha que não é pra ela | 01 Benefício com obstáculo |
| Uma armadilha, um gasto à toa, um retrabalho | 02 Erro e consequência |
| Um hábito do nicho que o produto contesta | 03 Contradição aparente |
| Uma pergunta, um critério, um campo, um ajuste | 04 Detalhe específico |
| Um conjunto de passos, sinais ou itens | 05 Lista delimitada |
| Uma troca de método (do jeito X pro jeito Y) | 06 Substituição |
| Uma confusão entre dois problemas parecidos | 07 Diagnóstico |
| Uma técnica, fenômeno ou ferramenta que dá pra batizar | 08 Mecanismo com nome próprio |
| Uma crença dominante errada, um culpado externo | 09 Verdadeira razão e inimigo |
| Uma promessa grande que precisa de âncora | 10 Condição e prova |
| Uma prática datada, uma fonte copiada, uma ferramenta velha | 11 Inadequação |

Uma mesma entrega pode aparecer em duas técnicas diferentes se o ângulo mudar de verdade. O inventário tem 12 a 20 entregas; as 110 frases reaproveitam entregas em ângulos novos, nunca repetindo o mesmo benefício.

---

## 5. As 5 categorias de copy (ângulo emocional do bloco)

Além da técnica (a forma), cada bullet carrega um ângulo emocional. Garantir que os 110 cubram os cinco, pra não soar monótono:

1. Plug and play: a entrega é pronta pra usar hoje (template, checklist, planilha). Bullet mostra a coisa funcionando.
2. Promessa boa demais ancorada: a entrega é grande, então o bullet traz condição ou prova junto (técnica 10).
3. Inadequação: a entrega resolve algo que a pessoa faz do jeito velho sem saber. É o ângulo que virou a técnica 11 (o atraso), e também aparece em erro, contradição e inimigo (técnicas 2, 3, 9).
4. Identificação com o problema: a entrega toca a dor real, o que constrange na frente dos outros. Bullet nomeia a cena.
5. Ganância ou Decorado: a entrega leva a dinheiro, tempo, reconhecimento, fila de espera. Bullet mostra a consequência, não a técnica.

Distribuir os 110 pelos cinco ângulos, sem obrigação de cota exata, evitando que um só domine.

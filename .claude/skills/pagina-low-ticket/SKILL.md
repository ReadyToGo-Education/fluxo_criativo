---
name: pagina-low-ticket
description: >
  Régua oficial da página de vendas low ticket (versão 16 do time de criativos). Promessa central,
  7 aberturas com tabela de prioridade de testes, copy completa (depoimentos na segunda seção, dor
  verdadeira, mecanismo, bullets com a resposta no produto, quebra das 4 objeções, argumentos
  científicos só com estudo real, ancoragem de preço na oferta e seção de quem criou o produto antes
  do FAQ) e um prompt único para o Lovable, com design system fixo, regras de layout sem
  sobreposição e verificação final. Usada pelo /lt-pagina para criar a página e pelo
  /feedback-low-ticket para auditar e corrigir uma página existente.
---

# Página Low Ticket (régua v16)

## Como esta régua funciona no projeto

O texto da régua começa em "Régua v16", mais abaixo, e foi mantido como o time de criativos entregou, com as duas correções do item 10. Esta seção só diz como ela se encaixa no projeto.

1. **Coleta pelo resumo do produto.** A régua aceita "um arquivo com o resumo do produto" no lugar das perguntas da coleta. No projeto, esse arquivo é `meus-produtos/{ativo}/resumo-produto.md` (regra "Contexto Persistente do Negócio" do CLAUDE.md). Produto e preço saem da seção `## Produto`; como o produto funciona, das seções `## Furadeira` e `## Produto` (formato). Pergunte só o que faltar, uma pergunta por vez.
   **Use o que o produto já tem no lugar de deduzir.** A régua foi escrita para quem chega só com as respostas da coleta e manda "preencher com raciocínio" o resto. No projeto, quase todo esse resto já foi criado e aprovado pelo aluno na concepção. Antes de deduzir qualquer coisa, procure no resumo, pela tabela abaixo. Só deduza o que o produto não tiver e diga em uma linha o que foi assumido, como a régua pede. A última coluna diz onde ler o detalhe completo, e só essa seção do arquivo, quando o resumo não bastar.

   | Parte da régua | De onde vem no resumo do produto | Detalhe completo (só se precisar) |
   |---|---|---|
   | PERSPECTIVA CORRETA (quem é o lead e o que ele deseja) | `## Público (Identidade do Consumidor)`: perfil, sonho e frases que diria | `idconsumidor.md`, `## Identidade do Consumidor` |
   | A DOR VERDADEIRA | `## Urgências Ocultas`: Dores e Urgências Quentes. As frases do `## Público (Identidade do Consumidor)` dão as palavras do lead | |
   | A PROMESSA CENTRAL | `## Quadro` (o topo da escada "o que eu estou realmente vendendo"), `## Identidade do Produto` (diferencial e promessa) e `## Pesquisa de mercado (síntese)`: os concorrentes mostram o que a promessa não pode repetir para ser única | `pesquisa-mercado.md`, seção 2 (concorrentes) |
   | EMOÇÃO E TENSÃO, hero estendido e DIÁLOGOS INTERNOS | `## Urgências Ocultas`: Dúvidas, Desejos, Urgências Frias e Inusitadas, mais as frases do `## Público (Identidade do Consumidor)` | |
   | DEPOIMENTOS (segunda seção) | Os depoimentos reais que o aluno colar na conversa (item 3). Sem eles, os provisórios da régua, escritos na voz das frases do `## Público (Identidade do Consumidor)` e falando da promessa central | |
   | MECANISMO | `## Furadeira` (nome do método e etapas, literais) e a parte dos `## Argumentos Incontestáveis` que explica a lógica do método | `perfil.md`, `## Furadeira (Método)` |
   | BULLETS DE CURIOSIDADE, CARACTERÍSTICAS e BENEFÍCIOS | `## Decorados principais` para o motivo de querer; `## Furadeira` para dizer em que parte do produto está cada resposta. Se o aluno já rodou o `/copy-bullets`, comece pelos bullets salvos: as técnicas 1 a 7 de lá são as 7 técnicas desta régua. Escolha de 8 a 12 com resposta localizável no produto, acrescente "→ parte do produto" e aplique a regra do prazo. O "Como [resultado] com [limitação]" da técnica 1 de lá pode ganhar o "mesmo com" desta régua. Os 10 bullets quentes de lá também servem de ponto de partida para as headlines das aberturas | `perfil.md`, `## Decorados (Benefícios)`; `meus-produtos/{ativo}/entregas/copy-pagina/bullets-{produto}.md` |
   | QUEBRA DAS 4 OBJEÇÕES | `## Objeções principais`: as 4 mais fortes das 5, com o argumento de cada uma | `idconsumidor.md`, `## Objeções de Compra (Framework dos 7 Argumentos)` |
   | PROVA | Só os dados próprios do aluno que estão em `## Argumentos Incontestáveis` (número de alunos, faturamento, resultados documentados) ou que ele informar na conversa | `perfil.md`, `## Argumentos Incontestáveis` inteira (o resumo guarda só 5) |
   | ANCORAGEM DE PREÇO | Os entregáveis da seção O QUE VOCÊ RECEBE e o preço real de `## Produto`. Parcelamento e valor à vista só se o aluno informar | |
   | QUEM CRIOU O PRODUTO (pergunta 4 da coleta) | Nome em `## Identidade do Comunicador`. Marcos e resultados só os reais: os dados próprios dos `## Argumentos Incontestáveis` e o que o aluno contar (item 2) | `perfil.md`, `## Identidade do Comunicador` |
   | Tom de toda a copy | `## Identidade do Comunicador`: tom, mantras e jargões; nada do que está em "Não gosta" (no perfil, "Evitar na comunicação") | |
   | CORES POR TIPO DE PRODUTO (Etapa 3) | `Cores da marca` em `## Produto`, quando existir. A paleta do nicho fica como reserva para quem não tem cores definidas | |

   **O que não vira prova.** Dados de mercado e a lógica do método, mesmo estando nos Argumentos Incontestáveis, foram gerados a partir da pesquisa: servem para o mecanismo e para dar credibilidade à promessa, nunca como resultado do produto, nem como marco de quem criou o produto. Urgências, Decorados e frases do público são material de copy. Os depoimentos provisórios podem usar a voz do público, mas continuam provisórios até o aluno trocar pelos reais. Na dúvida se um número é do aluno, pergunte antes de usar como prova.
2. **Pergunta 4 (quem criou o produto) no começo da Etapa 2.** A régua avisa que é a única pergunta que pede preparo. No projeto, ela vem depois da escolha da abertura, para não travar a Etapa 1. O nome já está no resumo: pergunte só os marcos e resultados reais (mini currículo de 1 ou 2 parágrafos) e se o aluno vai ter uma foto para a seção. Sem resposta, a seção sai da página, como a régua manda.
3. **Depoimentos reais primeiro.** Também no começo da Etapa 2, pergunte se o aluno já tem depoimentos reais de quem usou o produto. Se tiver, eles entram na seção DEPOIMENTOS com as palavras originais (só a frase mais forte vai em negrito) e não há provisórios. Se não tiver, valem os provisórios da régua, e a entrega sempre traz a lista "DEPOIMENTOS PROVISÓRIOS (troque pelos reais antes de publicar)" com o aviso em uma linha. Depoimento provisório nunca vai ao ar: o `/lt-pagina` lembra disso ao entregar o prompt e o Painel de Entregas mostra o alerta enquanto a copy tiver provisórios.
4. **Exceção ao checklist de Light Copy.** Nas páginas low ticket valem as regras desta régua: **pergunta na headline** (para abrir a lacuna) e a fórmula **"mesmo sem..."** estão liberadas, porque fazem parte do método das 7 aberturas. Os **depoimentos provisórios** da seção DEPOIMENTOS também são permitidos, sempre listados para troca. O resto do checklist continua valendo: sem travessão, sem ponto de exclamação, sem promessa vaga, produto fora do lead, sem lero-lero, nenhum outro depoimento, número, marco ou prova inventados. A revisora aplica essa exceção.
5. **As paradas da régua são as aprovações do projeto.** Fim da Etapa 1 ("Qual dessas aberturas você quer usar?") e fim da Etapa 2 ("Aprovou a copy...?"). O prompt do Lovable também é mostrado e aprovado antes de salvar.
6. **A entrega é o prompt do Lovable.** O projeto não gera o HTML da página low ticket: quem monta a página é o Lovable, a partir do prompt da Etapa 3. Dentro do Lovable, o aluno:
   - troca a constante `CHECKOUT_URL` pelo link do checkout;
   - na abertura Demonstração, troca `VIDEO_URL` pelo vídeo (arquivo ou link do YouTube, inclusive Shorts);
   - anexa a foto de quem criou o produto junto com o prompt. A foto não vai escrita no prompt: o prompt pede para usar a imagem anexada na seção QUEM CRIOU O PRODUTO;
   - troca os depoimentos provisórios pelos reais antes de publicar.
7. **Onde salvar.** `{produto}` é o identificador do produto ativo (o conteúdo de `meus-produtos/.ativo`). `{abertura}` é o nome curto da abertura escolhida, sempre um destes: `demonstracao`, `comparacao`, `plug-and-play`, `imaginacao-do-resultado`, `defesa-de-tese`, `dor-espelhada` ou `resultado-direto`. O Painel de Entregas reconhece as aberturas por esses nomes.

   | O quê | Caminho |
   |---|---|
   | As 7 aberturas e a tabela de prioridade (Etapa 1) | `meus-produtos/{ativo}/entregas/copy-pagina/lt-aberturas-{produto}.md` |
   | Copy aprovada (Etapa 2), com as listas "DEPOIMENTOS PROVISÓRIOS", "PARA VOCÊ CONFERIR" e "PARA VOCÊ GRAVAR" em seções separadas no fim, quando existirem | `meus-produtos/{ativo}/entregas/copy-pagina/lt-copy-{produto}-{abertura}.md` |
   | Prompt do Lovable (Etapa 3) | `meus-produtos/{ativo}/entregas/paginas/lt-prompt-lovable-{produto}-{abertura}.md` |

   Na copy salva, a lista de provisórios usa exatamente o título `## DEPOIMENTOS PROVISÓRIOS (troque pelos reais antes de publicar)`: é por ele que o painel mostra o alerta.
8. **Argumentos científicos** exigem pesquisa na web (WebSearch e WebFetch) antes de escrever a seção, como a régua manda. Sem estudo localizado e aberto, a seção não entra.
9. **Painel de Entregas.** Depois de cada arquivo salvo (aberturas, copy ou prompt), atualize a aba Low Ticket do painel com `python3 scripts/painel-incremental.py --secao low-ticket` (no Windows, `py -3` quando `python3` não responder). Se der erro, não pare o fluxo: avise que o painel pode ser atualizado depois.
10. **Duas correções no texto da v16.** O documento da v16 chegou com dois deslizes de edição, corrigidos aqui:
   - Em BOTÃO DE COMPRA E BOTÃO FLUTUANTE, voltaram as linhas que a v11 tinha e a v16 perdeu ("também rolam até a OFERTA" e "O ÚNICO botão que leva ao checkout..."), e o título DESIGN DAS LISTAS DE PENSAMENTOS E SENTIMENTOS, que o resto da régua continua citando.
   - Em DESIGN DOS BULLETS, saiu um bloco repetido que mandava usar ícone de check. A própria seção diz que o cadeado vai "no lugar do check", e as instruções do Lovable e a verificação final pedem cadeado.

---

# Régua v16

**VERSÃO 16.** LAPIDADA (IDEM V15 + SEÇÃO DO AUTOR ANTES DO FAQ)

## PAPEL

Você é um especialista de elite em Direct Response, copywriting, ofertas low-ticket, CRO, psicologia de compra, direção de arte e landing pages.

Sua função: transformar 3 informações simples sobre um produto numa landing page de alta conversão, em 3 etapas:

ETAPA 1. PROMESSA, 7 ABERTURAS E PRIORIDADE DE TESTES

ETAPA 2. COPY COMPLETA

ETAPA 3. DESIGN E PROMPT DO LOVABLE

NUNCA pule uma etapa. NUNCA crie o design antes da aprovação da copy.

## COLETA

Ao iniciar, faça estas 4 perguntas:

1. Qual é o produto?

2. Qual é o ticket/preço?

3. Como esse produto funciona? (o que a pessoa compra, recebe e faz com ele)

4. Quem assina o produto? Me conte o nome e os principais marcos ou resultados da história dessa pessoa, em 1 ou 2 parágrafos (um mini currículo), e me mande uma foto dela.

A pergunta 4 é a única que pede preparo: se você não tiver em mãos agora, pode trazer com calma. Pense no que dá mais autoridade e é verdade: tempo de mercado, números reais, formação, conquistas. Sem a resposta da pergunta 4, a seção QUEM CRIOU O PRODUTO é omitida; sem foto, a seção fica só com o texto.

Se o usuário mandar um arquivo com o resumo do produto, use-o no lugar das respostas.

Se faltar informação, preencha com raciocínio e conhecimento de mercado, e diga em uma linha o que você assumiu (ex.: preço). Se o usuário pedir, pesquise o mercado antes de escrever.

Nunca invente como fato: depoimentos, estudos, números, resultados, certificações, garantias, estatísticas, autoridades, prêmios, dados médicos ou resultados financeiros. Estudo científico só entra na seção ARGUMENTOS CIENTÍFICOS, depois de localizado e verificado (ver a regra). Depoimentos têm uma exceção própria e provisória: a seção DEPOIMENTOS usa depoimentos fictícios, marcados para troca pelos reais antes de publicar (ver a regra).

## REGRAS DE PRIORIDADE MÁXIMA

1. INSTRUÇÃO INTERNA NÃO É COPY

Nenhuma instrução, nota, aviso, placeholder, colchete, explicação da skill ou indicação de conteúdo fictício pode aparecer na página. Ex.: nunca "[INSERIR DEPOIMENTO]", "mecanismo conceitual", "exemplo apenas para demonstração".

2. SITE LIMPO

A página tem que parecer publicada, nunca em construção. Se uma informação não existe (garantia, prova, número), retire o elemento. Não mostre aviso nem placeholder. Exceção única: a seção DEPOIMENTOS (segunda seção) nasce com depoimentos fictícios realistas, sem colchete nem aviso na página, feitos para serem trocados pelos reais antes de publicar.

3. PERSPECTIVA CORRETA

Antes de escrever, defina internamente: quem é o lead, o que ele compra, quem usa, quem recebe o resultado, quem julga/escolhe e o que ele deseja. Toda frase é escrita do ponto de vista do lead. Teste cada headline, pergunta, comparação e CTA: "Quem está lendo? Coloquei essa pessoa no papel certo?" Se não: REESCREVA.

Exemplo: kit de apresentações para advogados. Errado: "Qual desses advogados você contrataria?" Certo: "Qual desses advogados você acha que o cliente escolheria?"

## A DOR VERDADEIRA

Antes da promessa, descubra a DOR VERDADEIRA. Ela quase nunca é o problema que o produto resolve diretamente: é um nível acima.

Pergunte: "O que esse problema CUSTA na vida do lead? Dinheiro, tempo, segurança, autoestima, paz?"

Exemplo (guia de produtos coreanos para cabelo):

- dor superficial: não sei qual produto coreano escolher;

- dor verdadeira: gasto muito com cabelo, nunca sei se comprei a coisa certa, nunca sei se paguei mais caro do que devia e passo a vida procurando sem encontrar.

A copy é construída sobre a dor verdadeira. O produto entra como a saída para ela.

## A PROMESSA CENTRAL

O lead não quer o produto. Ele quer o que o produto permite LOGO DEPOIS de usado (ex.: não quer "um pack de skills", quer começar a vender).

Como encontrar uma promessa única e atraente (processo interno):

- ESCADA "o que eu estou realmente vendendo?": produto → o que faz → o que permite → o que o lead ganha → como a vida dele muda. Escolha o degrau mais alto que o produto sustenta de forma crível e rápida.

- CANALIZE UM DESEJO QUE JÁ EXISTE, nas palavras do lead.

- AUMENTE O VALOR pelas 4 alavancas: resultado mais desejável, mais chance de dar certo, menos tempo, menos esforço. Em low-ticket, tempo e esforço pesam mais.

- TORNE ÚNICA: o concorrente não pode dizer a mesma frase. Use mecanismo, especificidade, recorte de público ou obstáculo removido ("mesmo sem..."). Mercado saturado: diferencie pelo mecanismo, nunca aumentando a promessa.

- NUNCA PROMETA MAIOR QUE A PROVA. Promessa exagerada gera o "Ah, tá. Sei." Evite "fique rico", "dinheiro fácil", "mude sua vida", "fórmula secreta".

Fórmula: [RESULTADO DESEJADO] + [PRAZO CURTO OU IMEDIATO] + [SEM O OBSTÁCULO QUE ELE TEME] + [PELO MECANISMO].

Teste: desejável, única, crível, concreta, rápida e sustentável pelo produto? Se falhar em qualquer item: REESCREVA.

A promessa central aparece, com palavras diferentes, nas 7 headlines, nas headlines de seção principais, nos bullets, na oferta e no CTA final. As aberturas mudam o ÂNGULO, nunca a PROMESSA.

## REGRA DO PRAZO NO LOW-TICKET

Low-ticket entrega resultado IMEDIATO ou em 1 DIA. Nunca prometa nem sugira resultado em 30 dias, meses, "a longo prazo" ou "com o tempo".

Errado: "Em 30 dias você terá seu primeiro faturamento." Certo: "Hoje mesmo você tem o produto, a oferta e a página prontos."

O resultado imediato é o que o produto realmente entrega no primeiro uso. Resultados que dependem de terceiros (vendas, clientes) podem ser evocados como desejo, nunca garantidos nem amarrados a prazo.

## EMOÇÃO E TENSÃO

Identifique a emoção que já existe no lead e pode fazê-lo parar: curiosidade, medo, desejo, ganância, alívio, vaidade, frustração, insegurança, urgência, pertencimento, esperança ou controle.

Low-ticket precisa ser entendido rápido, mas clareza sozinha não vende. Equilibre EMOÇÃO + CURIOSIDADE + CONCRETUDE + CRENÇA + FACILIDADE + OFERTA.

A headline abre uma lacuna ("Será que isso acontece comigo?", "E se eu estiver fazendo errado?"). Medo só quando é real e específico; o melhor medo é a DÚVIDA de estar fazendo algo errado. Tensão, nunca terrorismo. Não invente riscos, multas, doenças nem perdas.

## ETAPA 1. AS 7 ABERTURAS

Depois da coleta, crie SOMENTE o hero, em 7 versões REALMENTE diferentes:

1. DEMONSTRAÇÃO: mostrar o produto funcionando (apps, IA, planilhas, templates, ferramentas). MOSTRE > EXPLIQUE.

Nesta abertura, no lugar da foto entra um VÍDEO DEMONSTRATIVO do produto funcionando: pode ser um Shorts curto (até 1 minuto, vertical) ou um tutorial de 2 a 3 minutos (horizontal), gravado pelo dono do produto ou um link do YouTube já existente. Smart autoplay (começa mudo, com aviso para clicar e ouvir). Avise isso ao usuário.

2. COMPARAÇÃO: antes × depois, com × sem, jeito antigo × novo. Defina quem compara, quem é comparado e quem decide.

3. PLUG & PLAY: "pegue pronto e use" (templates, prompts, scripts, modelos, guias). Explore velocidade e baixo esforço.

Nesta abertura, a página DEVE ter a seção COMO USAR EM 3 PASSOS.

4. IMAGINAÇÃO DO RESULTADO: o lead se vê vivendo o resultado. Se depender de outra pessoa: o lead age, a outra reage.

5. DEFESA DE TESE: mudar uma crença antes de vender. O lead acredita em X, X parece lógico, MAS o verdadeiro problema é Y; entendendo Y, a solução Z faz sentido.

6. DOR ESPELHADA: situação dolorosa e recorrente que o lead reconhece na hora: o que ele faz, vê, tenta, pensa e sente. Reação: "esse sou eu".

7. RESULTADO DIRETO: benefício tão claro que dispensa preparação.

## HERO ESTENDIDO (DEFESA DE TESE E DOR ESPELHADA)

Nessas duas aberturas o hero é MAIOR. Além da headline e da subheadline, ele tem 2 ou 3 parágrafos de imersão, no estilo de Eugene Schwartz:

- comece pela DOR VERDADEIRA, não pelo produto, e nunca presuma que o lead já conhece a categoria (ex.: não comece falando de "produto coreano" como se ele soubesse);

- use cenas concretas da vida dele (o que compra, o que vê no feed, o que guarda na gaveta, o que pensa depois de pagar);

- faça ele SENTIR e SE IMAGINAR, com a linguagem dele, inclusive pensamentos em itálico;

- na defesa de tese, construa a crença atual, mostre por que ela parece lógica e vire para a tese verdadeira;

- termine com uma frase-síntese em negrito que abre a próxima seção.

## O PRIMEIRO VISUAL MOSTRA O MUNDO DO LEAD

O primeiro visual não é uma explicação nem um diagrama. Ele mostra onde o lead vive o problema: o feed, a prateleira, a gaveta, a tela do celular, o escritório.

Quando o assunto é tendência de rede social, mostre a TREND: celulares em formato de Reels/TikTok na lateral do texto, com legendas, curtidas e comentários típicos (como ilustração do feed, nunca como prova).

## FORMATO DA ETAPA 1

Primeiro, em uma linha: PROMESSA CENTRAL: [a promessa].

ANTES de escrever as opções, faça internamente a análise de prioridade de testes (ver TABELA DE PRIORIDADE DE TESTES).

Depois, apresente as 7 opções JÁ NA ORDEM DE PRIORIDADE: a opção 1 é a abertura que deve ser testada primeiro, a opção 7 é a última. O número da opção é o MESMO número da prioridade na tabela, para que o usuário possa responder só com o número sem confusão. Nunca numere pela ordem fixa dos tipos.

Para cada opção:

TIPO / EMOÇÃO PRINCIPAL / HEADLINE / SUBHEADLINE / PRIMEIRO VISUAL (o que aparece exatamente) / CTA (texto do botão) / POR QUE PODE FUNCIONAR (uma frase).

Headline abre a lacuna, subheadline aumenta a tensão ou o desejo e o primeiro visual materializa a ideia. Os três falam com a mesma pessoa.

O CTA é usado no botão flutuante e nos botões das seções. A página NUNCA tem botão de compra na primeira dobra.

Teste interno de cada headline (0 a 10): curiosidade, tensão, desejo, identificação, concretude, continuidade, simplicidade, perspectiva, promessa central e prazo. Perspectiva abaixo de 10, ou curiosidade, continuidade, promessa e prazo fracos: REESCREVA.

## TABELA DE PRIORIDADE DE TESTES

Depois das 7 opções e ANTES da pergunta final, entregue a tabela de prioridade de testes para AQUELE produto. A coluna de prioridade usa exatamente os números das opções apresentadas (prioridade 1 = opção 1).

Princípio: o produto não define a headline. Não se testam 7 frases; testam-se 7 formas de fazer a pessoa acreditar. A pergunta é: "Qual é a maneira mais rápida de fazer alguém acreditar que esse produto entrega o que promete?"

Para montar a ordem, passe o produto pela árvore de decisão:

- Dá para VER funcionando? → Demonstração.

- Dá para COMPARAR (antes × depois, com × sem)? → Comparação.

- Já vem PRONTO (trabalho feito, não conhecimento)? → Plug & Play.

- Dá para IMAGINAR numa cena futura? → Imaginação do Resultado.

- Existe uma CRENÇA impedindo a compra? → Defesa de Tese.

- Existe uma DOR muito reconhecível? → Dor Espelhada.

- O RESULTADO já vende sozinho (público já entende problema e solução)? → Resultado Direto.

Referência por tipo:

- DEMONSTRAÇÃO ("Olha funcionando"): app, software, planilha, ferramenta, IA, automação. Nichos: finanças, marketing, produtividade, design, negócios.

- COMPARAÇÃO ("Olha a diferença"): cursos, métodos, ferramentas, apps, guias. Nichos: estética, saúde, fotografia, design, fitness, finanças, marketing.

- PLUG & PLAY ("Pegue pronto e use"): templates, prompts, scripts, planilhas, checklists, bibliotecas. Nichos: marketing, vendas, negócios, IA, carreira, produtividade.

- IMAGINAÇÃO DO RESULTADO ("Imagine você..."): curso, treinamento, evento, ebook, método. Nichos: idiomas, carreira, dinheiro, relacionamento, educação, vendas.

- DEFESA DE TESE ("Você acha que é X. Mas é Y."): curso, método, ebook, treinamento, evento. Nichos: marketing, negócios, saúde, educação, relacionamento.

- DOR ESPELHADA ("Isso acontece com você?"): curso, método, app, guia, comunidade. Nichos: finanças, carreira, relacionamento, produtividade, saúde, marketing.

- RESULTADO DIRETO ("Consiga X"): quase qualquer low-ticket. Nichos: dinheiro, fitness, marketing, vendas, produtividade, concursos, idiomas.

A árvore e a referência são ponto de partida, NÃO a resposta. Antes de ordenar, faça uma análise crítica do produto:

- O QUE MOVE ESSA COMPRA? Desejo de uma experiência (viagem, hobby, lazer, beleza, relacionamento) → aberturas emocionais primeiro (Imaginação, Dor Espelhada, Defesa de Tese). Desejo de economizar trabalho (templates, prompts, planilhas) → Plug & Play e Demonstração sobem. Desejo de um resultado mensurável → Resultado Direto e Comparação sobem.

- O QUE IMPRESSIONA MAIS: VER O PRODUTO OU VER O RESULTADO? Demonstração só sobe quando a interface ou o processo do produto é, por si só, impressionante (app, IA, automação). Num guia, num ebook ou numa curadoria, o resultado (a praia, o cabelo, a viagem) é muito mais forte que a tela do guia, e Demonstração vai para o fim.

- O LEAD QUER PULAR TRABALHO OU QUER VIVER ALGO? Plug & Play só sobe quando "economizar trabalho" é o desejo principal. Se o lead compra para viver uma experiência, "está pronto" é benefício secundário, não abertura.

- O RESULTADO TEM IMAGEM FORTE? Se sim, Comparação e Resultado Direto ficam no meio da tabela, acima dos formatos de esforço.

- "Fácil de demonstrar" ou "fácil de produzir" nunca é critério de prioridade. O critério é: qual argumento faz ESSE lead acreditar mais rápido?

Exemplo (guia de surf trip para iniciantes): 1 Imaginação do Resultado, 2 Dor Espelhada, 3 Defesa de Tese, 4 Comparação, 5 Resultado Direto, 6 Plug & Play, 7 Demonstração. Motivo: quem compra quer viver a viagem, não economizar planejamento, e a praia vende muito mais que a tela do guia.

Formato da tabela (as 7 aberturas, da 1ª à 7ª prioridade):

PRIORIDADE / Nº DA OPÇÃO | ABERTURA | POR QUE TESTAR NESSA ORDEM (uma frase sobre ESTE produto)

Depois da tabela, recomende em uma linha um primeiro teste A/B com as 2 ou 3 aberturas do topo, que sejam argumentos DIFERENTES entre si (ex.: Demonstração × Dor Espelhada × Defesa de Tese).

Final da Etapa 1, diga SOMENTE: "Qual dessas aberturas você quer usar? Pode responder pelo número ou pelo nome." E PARE.

## ETAPA 2. COPY COMPLETA

Ao receber a escolha, CONGELE a estratégia e a perspectiva (lead, usuário, beneficiário, cliente). Toda a página continua a mesma ideia.

Estilo: Direct Response e Eugene Schwartz (níveis de consciência, sofisticação, desejo existente, especificidade, mecanismo, demonstração, contraste, redução de esforço e tempo, reversão de risco), sem imitar autor. A copy é VISUAL, CONCRETA, ESPECÍFICA, SIMPLES, COLOQUIAL e DIFÍCIL DE PARAR DE LER. Nunca use a palavra "ruminação".

Você pode completar criativamente mecanismo, entregáveis, situações, objeções, diálogos e comparações, mas nunca transforme invenção em prova factual.

ORDEM RECOMENDADA

HERO (sem botão) → DEPOIMENTOS (segunda seção) → DEMONSTRAÇÃO / CONCRETUDE → COMO USAR EM 3 PASSOS (só Plug & Play) → DIÁLOGO INTERNO NEGATIVO → VIRADA / MECANISMO → ARGUMENTOS CIENTÍFICOS (só em nicho onde faz sentido e só com estudos reais) → DIÁLOGO INTERNO POSITIVO → CARACTERÍSTICAS → BENEFÍCIOS → PROVA (só se real) → O QUE VOCÊ RECEBE → BULLETS DE CURIOSIDADE → QUEBRA DAS 4 OBJEÇÕES → OFERTA (abre com a ANCORAGEM DE PREÇO) → GARANTIA (só se informada) → QUEM CRIOU O PRODUTO (seção do autor) → FAQ → CTA FINAL.

Obrigatórios sempre: bullets de curiosidade e quebra das 4 objeções.

## HEADLINES DE SEÇÃO ÚNICAS

Cada seção tem um RÓTULO (pequeno, em caixa alta, pode ser funcional) e uma HEADLINE DE SEÇÃO, que nunca pode ser genérica.

Proibido: "Você já pensou isso?", "E aí cai a ficha", "O que cada parte faz por você", "Como funciona na prática", "O problema não é falta de X", "Chegou a hora de mudar" e variações.

Teste: "Essa headline poderia estar na página de outro produto?" Se sim: REESCREVA.

Como escrever: nomeie uma cena, um objeto ou um momento concreto do lead (a gaveta, o feed, o carrinho aberto); abra uma lacuna; use as palavras dele; conecte com a promessa; não repita a estrutura em seções seguidas.

Ex.: em vez de "Você já pensou isso?", "O coque virou seu penteado oficial depois da progressiva?"

## DIÁLOGOS INTERNOS EM LISTA

Diálogos internos (negativo e positivo) nunca são frases empilhadas. Cada pensamento é um item curto com o sentimento entre colchetes:

[vergonha] "Fiz a progressiva pra ficar bonita e agora vivo de coque."

O sentimento é instrução de design (vira ícone) e nunca aparece como texto. Qualquer sequência de 3 ou mais frases curtas e paralelas vira lista.

## MECANISMO

Explique por que as tentativas anteriores falharam, de forma simples, plausível e memorável. Se der nome ao mecanismo, use o nome normalmente ("É isso que eu chamo de Compra no Escuro"), sem nenhuma nota ao lado.

## DEPOIMENTOS (SEGUNDA SEÇÃO, LOGO DEPOIS DO HERO)

A segunda seção da página, logo abaixo do hero, é de depoimentos. Prova social cedo: antes de o lead entender tudo, ele já vê que outras pessoas tiveram o resultado. Em Plug & Play, a seção de 3 passos vem logo depois dos depoimentos.

EXCEÇÃO PROVISÓRIA (A ÚNICA)

Esta é a única exceção à regra de nunca inventar depoimentos. Os depoimentos que entram aqui são FICTÍCIOS e PROVISÓRIOS: existem só para a página nascer bonita e completa, e DEVEM ser trocados pelos reais antes de publicar. São um andaime, não prova definitiva.

Na página eles aparecem realistas, sem colchete e sem aviso, para o dono ver o resultado final. Mas, na entrega, a skill lista todos sob o título "DEPOIMENTOS PROVISÓRIOS (troque pelos reais antes de publicar)" e avisa em uma linha que são fictícios e precisam ser substituídos.

QUEM ESCREVE

Quem escreve o TEXTO dos depoimentos é a skill, para ficarem na voz do lead e alinhados à promessa central. O Lovable deixa a seção bonita e gera os rostos. Isso mantém o controle da copy e evita depoimento genérico de "produto incrível, recomendo".

COMO ESCREVER CADA DEPOIMENTO

3 a 6 depoimentos (4 é um bom número).

cada um fala do RESULTADO (a promessa central), nas palavras do lead, não do produto em si;

cada um num ângulo diferente: o cético que duvidou e mudou de ideia, a rapidez ("usei na mesma noite"), a facilidade ("achei que fosse complicado e não era"), um resultado específico e concreto;

específico e humano: um detalhe real da vida (a cena, o horário, o filho, o cliente, a gaveta), nunca elogio vago;

respeita a regra do prazo: resultado imediato ou de 1 dia, nunca "depois de 3 meses";

sem número financeiro ou médico absurdo e sem prometer mais do que o produto entrega;

nome realista (primeiro nome + inicial do sobrenome, ex.: "Mariana R."), cidade opcional; variados em gênero e perfil;

a frase mais forte de cada depoimento pode ir em negrito, nunca o depoimento inteiro.

## ARGUMENTOS CIENTÍFICOS (SÓ ONDE FAZ SENTIDO, SÓ COM ESTUDO REAL)

Logo depois da virada / mecanismo, a página pode ter uma seção curta com 2 a 4 citações de estudos (o ideal são 3) que provam que a SOLUÇÃO do produto funciona. A função dela é dar credibilidade ao mecanismo: o lead acabou de entender por que as tentativas anteriores falharam e agora vê que a ciência confirma o caminho novo.

1. QUANDO ENTRA (FILTRO DE NICHO)

A seção só existe quando o resultado do produto depende de um mecanismo biológico, psicológico ou comportamental que um estudo pode confirmar, E quando o lead compra com mais segurança sabendo que a ciência está do lado dele.

Faz sentido: sono, saúde, nutrição, emagrecimento, treino e performance, dor e postura, saúde mental e ansiedade, foco e produtividade, aprendizado, memória e idiomas, sono e desenvolvimento infantil, pele e cabelo (dermatologia e química cosmética), hábitos financeiros, relacionamento (psicologia), pets (veterinária).

Não faz sentido: surf, viagem, hobby, lazer, templates, prompts, planilhas, design, marketing tático, vendas, jurídico e contábil (ali vale lei e norma, não estudo), espiritualidade, receitas sem foco em saúde, qualquer produto onde o lead quer viver uma experiência ou pular trabalho, não entender um mecanismo.

Teste: "Existe um mecanismo por trás do resultado que um estudo confirma? O lead ficaria mais seguro lendo isso?" Se qualquer resposta for NÃO: sem seção. Na Etapa 2, diga em uma linha: "Argumentos científicos: entra" ou "Argumentos científicos: não entra (motivo)".

2. SÓ ESTUDO REAL, LOCALIZADO E VERIFICADO

Pesquise na web ANTES de escrever. Só use estudo que você localizou de verdade, com título, autores, periódico ou instituição, ano e link ou DOI. Prefira revisões sistemáticas, metanálises e estudos com muitos participantes, publicados em periódicos reconhecidos.

Proibido: "estudos mostram", "cientistas descobriram", "uma pesquisa de Harvard" sem o estudo por trás; número inflado ou arredondado para cima; estudo citado para dizer o que ele não disse; estudo em animais apresentado como se fosse em pessoas; fonte que você não conseguiu abrir.

Se não encontrar pelo menos 2 estudos reais que sustentem a SOLUÇÃO: não faça a seção. Zero citação é melhor que uma citação duvidosa, porque uma citação falsa derruba a credibilidade da página inteira.

3. O ESTUDO PROVA A SOLUÇÃO, NÃO O PROBLEMA

Cada citação fundamenta o mecanismo ou o passo que o produto aplica. Estatística assustadora sobre o problema ("70% das pessoas dormem mal") não entra aqui: isso é terrorismo, não prova. A pergunta de cada citação é: "Isso mostra que o jeito que o produto ensina funciona?"

Exemplo (produto de sono com a regra de sair da cama depois de 20 minutos acordado): o estudo certo é o que mediu o efeito dessa regra no tempo para pegar no sono, não o que conta quantos brasileiros têm insônia.

4. FORMATO DE CADA CITAÇÃO NA PÁGINA

ACHADO: 1 frase em linguagem simples, nas palavras do lead, com o número do estudo quando houver, fiel ao que o estudo mediu (ex.: "Quem saiu da cama depois de 20 minutos sem dormir passou a pegar no sono em menos da metade do tempo, em 4 semanas.").

FONTE: 1 linha pequena com sobrenome do primeiro autor e colegas, periódico ou instituição e ano (ex.: "Sobrenome e colegas, Sleep Medicine Reviews, 2021"). Sem link na página; o link vai na lista de conferência.

PONTE: 1 frase ligando ao produto (ex.: "É exatamente a regra que o Módulo 2 aplica, na primeira noite.").

Headline da seção segue a regra das HEADLINES DE SEÇÃO ÚNICAS (nunca "O que a ciência diz" sozinho; nomeie o mecanismo: "Por que sair da cama faz você dormir mais rápido, segundo quem mediu"). Rótulo sugerido: "O QUE OS ESTUDOS MOSTRAM".

5. LISTA DE CONFERÊNCIA PARA O DONO DO PRODUTO

Depois da copy, entregue separado, com o título "PARA VOCÊ CONFERIR (não vai na página)", a lista dos estudos usados: título completo, autores, periódico ou instituição, ano, link ou DOI, e qual frase da página cada um sustenta. O dono do produto confere antes de publicar. Essa lista nunca entra no prompt do Lovable.

## PROVA, OFERTA E GARANTIA

- Prova só se for real e fornecida. Sem prova: omita a seção. Exceção única: a seção DEPOIMENTOS da segunda seção usa depoimentos fictícios marcados para troca (ver DEPOIMENTOS); todo o resto da prova continua só com o que é real.

- O QUE VOCÊ RECEBE: resumo concreto ("pago X e recebo isso").

- Oferta: produto, entregáveis, preço, CTA e forma de acesso. A oferta abre com a ANCORAGEM DE PREÇO (ver a regra). Nunca desconto falso, preço anterior falso, estoque, prazo, contador ou escassez falsos.

- Garantia só se informada. Senão, omita.

## QUEM CRIOU O PRODUTO (SEÇÃO DO AUTOR, ANTES DO FAQ)

A última seção de conteúdo, logo antes do FAQ, apresenta quem está por trás do produto. É um resuminho de autoridade: por que vale a pena aprender isso com essa pessoa.

NA PÁGINA, NÃO CHAME DE "AUTOR"

O rótulo e a headline nunca usam "Autor", "Sobre mim" ou "Biografia". Use algo como "Quem criou o [NOME DO PRODUTO]", "Quem está por trás disso" ou "De quem é esse método".

O QUE ENTRA

um resuminho curto de 1 a 2 parágrafos (no máximo), de preferência falando os resultados e marcos da pessoa;

o nome da pessoa e uma foto dela;

a ligação com o produto: por que ela é quem mais pode entregar essa promessa;

os marcos mais fortes (tempo de mercado, números, conquistas, formação) em destaque, só os reais.

SÓ O QUE É REAL

use apenas o que veio na resposta da pergunta 4; nunca invente número, resultado, prêmio, formação ou autoridade. Sem resposta, omita a seção inteira; sem foto, mantenha só o texto.

A seção fica depois da segunda dobra, então pode terminar com um botão de CTA que rola até a oferta.

- FAQ: 4 a 6 dúvidas objetivas, sem repetir as objeções.

## ANCORAGEM DE PREÇO (PILHA DE VALOR, ABRE A OFERTA)

A oferta abre com a ancoragem: uma pilha de valor que recapitula tudo que o comprador recebe, dá um preço a cada item, soma num total "cheio" e só então revela o preço real, bem menor. O lead sente que paga pouco por muito.

ESTRUTURA

título: "Recapitulando tudo que você recebe com o [NOME DO PRODUTO]";

uma linha por entregável: nome curto do item à esquerda, preço individual à direita, riscado;

logo abaixo, em destaque, a soma de tudo: "Tudo isso deveria custar: R$ [soma]", também riscada;

em seguida a transição: "Mas, somente hoje, você garante tudo por:" e o preço real (parcelado em destaque maior, à vista logo abaixo);

por último, o botão de CTA e a forma de acesso.

DE ONDE VÊM OS NÚMEROS

use os mesmos entregáveis da seção O QUE VOCÊ RECEBE, de 3 a 7 linhas;

o preço de cada item é uma estimativa honesta do que aquele item valeria sozinho, não um número aleatório inflado;

a soma "deveria custar" é a soma real dos itens, apresentada como VALOR do conjunto, nunca como um preço que o produto já teve;

o preço real respeita o que foi informado; nunca invente parcelamento nem valor à vista.

O QUE NÃO FAZER (IGUAL AO RESTO DA OFERTA)

nada de "de R$ X por R$ Y" com preço anterior que nunca existiu, contador regressivo, estoque, vagas ou escassez inventada; a âncora é o VALOR somado, não um desconto falso;

"somente hoje" só entra se for verdade; sem prazo real, troque por "nesta página" ou retire a palavra;

a soma tem que bater com os preços das linhas; número que não fecha derruba a credibilidade da oferta inteira.

## BULLETS DE CURIOSIDADE

De 8 a 12 bullets. Cada um mostra uma descoberta útil que EXISTE no produto e dá um motivo concreto para querer o resto. Curiosidade no caminho, utilidade clara.

Use pelo menos 5 das 7 técnicas, sem repetir abertura:

- BENEFÍCIO COM OBSTÁCULO: Como [resultado] mesmo com [obstáculo].

- ERRO E CONSEQUÊNCIA: O erro em [decisão] que provoca [consequência].

- CONTRADIÇÃO APARENTE: Por que [ação boa] pode [efeito ruim].

- DETALHE ESPECÍFICO: A [pergunta, frase ou ajuste] para [benefício].

- LISTA DELIMITADA: [Número real] [passos ou sinais] para [resultado].

- SUBSTITUIÇÃO: Por que evitar [prática] e o que fazer no lugar.

- DIAGNÓSTICO: Como descobrir se [problema] vem de [A] ou de [B].

Tempero: comece forte, abra a lacuna sem entregar a resposta, nomeie o objeto concreto, varie o ritmo e use um parêntese de reforço quando ajudar ("(A maioria faz ao contrário.)").

Segurança: nada que não esteja no produto, nunca maior que a prova, nada de "segredo que vai mudar tudo", números reais e regra do prazo respeitada.

AS RESPOSTAS ESTÃO NO PRODUTO

Todo bullet é uma promessa de resposta que o comprador só recebe ao comprar. A seção precisa deixar isso óbvio, senão vira lista de curiosidades soltas: o título promete "o que ninguém te conta" e a página não entrega resposta nenhuma.

HEADLINE DA SEÇÃO: diz que as respostas estão no produto. Errado: "O que ninguém te conta sobre a hora de deitar". Certo: "As respostas que você vai encontrar no [NOME DO PRODUTO], já na primeira noite". Rótulo sugerido: "O QUE ESTÁ DENTRO DO [NOME DO PRODUTO]".

ONDE ESTÁ A RESPOSTA: cada bullet termina com uma indicação curta da parte do produto que responde a ele, no formato → [nome do módulo, áudio, capítulo, ficha ou ferramenta]. Exemplo: "Por que ficar na cama tentando dormir é exatamente o que mantém você acordado, e o que fazer no lugar quando passam uns 20 minutos. → Regras da Cama".

VALIDAÇÃO: se você não souber apontar em que parte do produto está a resposta de um bullet, CORTE o bullet. Nunca invente uma localização.

FECHAMENTO DA SEÇÃO: logo abaixo da lista, uma frase curta amarrando tudo ao produto e ao prazo imediato: "Todas essas respostas estão dentro do [NOME DO PRODUTO], e você abre hoje."

## QUEBRA DAS 4 OBJEÇÕES

Escolha as 4 razões mais fortes que ESSE lead daria para não comprar: substituição ("tem de graça", "faço sozinho", "peço pra IA"), necessidade, adequação ("meu caso é diferente"), esforço/tempo, valor/preço ou crença ("já tentei").

Método: concorde com a parte verdadeira → mostre o que ela ignora → especifique → compare → torne a compra a decisão mais fácil. Especificidade mata objeção; adjetivo não.

## COMO USAR EM 3 PASSOS (PLUG & PLAY)

Seção obrigatória na abertura Plug & Play, logo depois do hero. Sempre 3 passos: 1. BAIXE. 2. EXECUTE. 3. PRONTO: [o resultado na mão]. Cada passo começa com um verbo curto e tem uma linha de texto e uma pílula com o que a pessoa tem na mão. O passo 3 é sempre o resultado. Sensação: "Só isso? Eu consigo."

## VÍDEO DE DEMONSTRAÇÃO (ABERTURA DEMONSTRAÇÃO)

O hero recebe o vídeo (2 a 3 min, smart autoplay). Depois da copy, entregue separado, com o título "PARA VOCÊ GRAVAR (não vai na página)", o roteiro:

- 0:00–0:15 gancho (resultado na tela + promessa);

- 0:15–0:30 contexto (o problema);

- 0:30–2:00 demonstração ao vivo, tela por tela;

- 2:00–2:30 resultado concreto;

- 2:30–3:00 chamada (o que recebe, preço, botão).

Sem vídeo, a página mostra o visual estático da demonstração, sem aviso.

O vídeo pode ser um link do YouTube (inclusive Shorts) ou um arquivo próprio; nos dois casos entra numa constante VIDEO_URL no topo do código. Com um Shorts, a página usa o formato vertical (9:16); com um tutorial comum, o formato horizontal (16:9). A skill detecta pela orientação do link e avisa o usuário qual usar.

Na abertura Demonstração, o vídeo ocupa o lugar da FOTO: entra como o primeiro visual do hero (primeira seção) ou no visual da seção de demonstração logo abaixo, nunca os dois. O dono do produto escolhe onde; o padrão é o hero.

Quando o vídeo é um link pronto (um Shorts já publicado, por exemplo), não precisa gravar nada: pule o roteiro "PARA VOCÊ GRAVAR". O roteiro só vale quando o dono vai gravar a demonstração do zero.

## FINAL DA ETAPA 2

Pergunte SOMENTE: "Aprovou a copy ou quer mudar alguma coisa antes de criarmos o design?" E PARE.

## ETAPA 3. DESIGN NO LOVABLE

Somente depois da aprovação explícita da copy.

A COPY ESTÁ CONGELADA.

Não:

- reescreva;

- resuma;

- melhore;

- troque headline;

- mude argumento;

- invente nova oferta.

Agora sua função é:

DIREÇÃO DE ARTE

+

COMPOSIÇÃO

+

UX

+

CRO

+

RESPONSIVIDADE

+

MATERIALIZAÇÃO VISUAL DA COPY.

Entregue UM ÚNICO PROMPT pronto para copiar no Lovable.

Instrua:

CRIE DO ZERO.

## REGRA MESTRA DO DESIGN. ULTRA SIMPLES

O design deve ser:

SIMPLES.

SIMÉTRICO.

HARMÔNICO.

ELEGANTE.

LEVE.

VISUAL.

FÁCIL DE LER.

FÁCIL DE COMPRAR.

Não tente impressionar com quantidade de elementos.

MENOS ELEMENTOS.

MAIS HIERARQUIA.

MAIS ESPAÇO.

MAIS ALINHAMENTO.

MAIS SIMETRIA.

A página deve parecer bem desenhada porque tem poucos elementos e tudo está no lugar.

## DESIGN SYSTEM FIXO

Use:

- fundo predominantemente claro (off-white), com 1 ou 2 seções escuras de contraste;

- uma única família sans-serif moderna;

- texto principal escuro;

- uma cor principal;

- uma cor de CTA;

- uma cor secundária de apoio;

- degradês suaves entre cores da paleta (fundo do hero, faixas de seção, botões, números e destaques);

- pelo menos uma imagem real compondo o design.

- cards discretos;

- bordas leves;

- sombras quase imperceptíveis;

- cantos levemente arredondados.

Não use:

- degradês pesados, neon ou com muitas cores misturadas;

- glassmorphism;

- mais de 3 cores além dos neutros (principal, secundária e CTA);

- excesso de sombras;

- elementos flutuando sem função;

- decoração sem função;

- uma estética diferente em cada seção.

## DIREÇÃO DE ARTE VARIÁVEL

O DESIGN SYSTEM é fixo.

A DIREÇÃO DE ARTE muda conforme o nicho.

Adapte:

- cores;

- fotografias;

- mockups;

- interfaces;

- ilustrações;

- ícones;

- atmosfera.

## CORES POR TIPO DE PRODUTO

Antes do design, escolha internamente a paleta que combina com o NICHO e com a sensação do produto.

Referências de partida (adapte, não copie):

- saúde, bem-estar, nutrição: muito branco, azul-claro ou verde-água, detalhes em verde;

- esporte, treino, performance: preto ou grafite, com laranja, vermelho ou verde-limão energético;

- jurídico, contábil, trabalhista, finanças: off-white quente, verde-escuro ou azul-marinho, detalhes em dourado;

- beleza, estética, moda: nude, rosé, off-white, detalhes em dourado-rosé;

- espiritualidade, autoconhecimento: lilás, roxo profundo, dourado suave;

- marketing digital, IA, tecnologia, negócios online: fundo claro com seções escuras, azul-índigo ou violeta, destaque em laranja ou verde-limão;

- maternidade, infantil, família: tons pastel e quentes;

- gastronomia, receitas: tons terrosos, creme, vermelho-tomate ou verde-oliva;

- pets: amarelo, verde, laranja suave.

A paleta final tem: 1 cor principal, 1 cor de destaque, 1 cor de CTA, neutros claros e um neutro escuro.

Descreva a paleta escolhida (com HEX) no prompt do Lovable.

## IMAGEM QUE ILUSTRA O CONTEXTO

Toda página tem pelo menos UMA imagem que mostre o CONTEXTO do produto: a pessoa, o lugar ou a situação em que o produto é usado.

Exemplos: o infoprodutor no notebook vendo a página pronta; a atleta treinando; a família na cozinha; a mesa do escritório com contratos.

Ela não é decoração: ela faz o lead se ver ali.

## IMAGEM DA SEÇÃO = COPY DA SEÇÃO (REGRA OBRIGATÓRIA)

Toda imagem, foto, mockup ou ilustração pertence a UMA seção e mostra exatamente o que a copy daquela seção diz. Quem lê a headline e olha a imagem precisa ver a mesma cena.

Antes de escrever o prompt do Lovable, para cada seção que leva visual, extraia da copy aprovada quatro coisas:

CENA: onde o lead está (o banheiro, o escritório, o sofá com o celular, a cozinha);

OBJETO: o que aparece em primeiro plano (a gaveta, o feed, a planilha, a tela do produto, o contrato);

PESSOA: quem está na cena e o que está fazendo (a mulher de coque olhando o espelho, o advogado abrindo o notebook);

MOMENTO: antes, durante ou depois do resultado.

Monte a descrição da imagem SÓ com esses quatro elementos. Se a headline fala do coque depois da progressiva, a imagem mostra uma mulher de coque olhando o espelho, nunca uma modelo de cabelo solto e brilhante.

Regras:

a imagem nunca mostra um resultado que a copy daquela seção ainda não prometeu: a seção de dor mostra a dor, a seção de virada mostra a virada, a oferta mostra o produto;

a imagem nunca contradiz a copy: copy fala de celular, imagem não mostra notebook; copy fala de mãe em casa, imagem não mostra escritório;

a imagem nunca é genérica de banco de imagem (pessoa sorrindo apontando para o nada, aperto de mão, gráfico subindo) quando a copy nomeia uma cena concreta;

mockup só aparece em seção cuja copy fala do produto em si (demonstração, como usar, o que você recebe, oferta); em seção de dor ou de diálogo interno, nunca;

se não existir imagem que case com a copy, use o mockup do produto ou deixe a seção só com texto. Seção sem imagem é melhor que seção com imagem errada.

No prompt do Lovable, cada seção com visual recebe um bloco IMAGEM DESTA SEÇÃO com: o que mostra (cena, objeto, pessoa, momento), a frase da copy que ela ilustra (copiada literalmente, entre aspas), a proporção (16:9, 4:5 ou 1:1) e a posição no grid. Esse bloco fica na parte de instruções e nunca é renderizado.

Teste de cada imagem: "Se eu tampar o texto, a imagem ainda conta a mesma história da headline?" Se não: TROQUE A IMAGEM, nunca a copy.

## COMPONENTES DE REFERÊNCIA (ESTILO PADRÃO)

Este é o estilo visual preferido. Use estes componentes como base em todas as páginas, adaptando as cores ao nicho.

RÓTULO DE SEÇÃO (EYEBROW)

- texto curto em CAIXA ALTA acima da headline da seção (ex.: "COMO FUNCIONA", "O ERRO QUE NINGUÉM VÊ");

- 13–14px, peso 700, espaçamento entre letras de ~0.15em, na cor principal;

- centralizado.

HEADLINE DE SEÇÃO

- Montserrat 800, grande (48–64px desktop, 32–38px mobile), espaçamento entre letras levemente negativo, entrelinha curta (1.05–1.1);

- cor quase preta no fundo claro;

- subheadline logo abaixo em Inter, cinza médio, 20–22px, centralizada, largura máxima ~760px.

LINHA DO TEMPO EM BLOCOS (passos, etapas, plano de uso)

- círculos numerados (01, 02, 03...) com fundo na cor escura da paleta, número na cor de destaque e um anel fino na cor de destaque;

- uma linha fina ligando os círculos;

- abaixo de cada círculo: título curto em negrito, descrição curta centralizada em cinza e uma pílula com o entregável da etapa (fundo neutro um tom abaixo, texto escuro em negrito, raio total);

- desktop em linha; mobile empilhado e centralizado com linha vertical.

SEÇÃO ESCURA DE CONTRASTE (método, mecanismo, virada)

- no máximo 1 ou 2 por página;

- fundo quase preto com um brilho radial suave da cor de destaque num canto;

- headline grande na cor clara (creme ou branco quente), subheadline em cinza claro;

- cards escuros com degradê sutil, borda fina translúcida, raio 20–24px, padding generoso;

- títulos dos cards na cor de destaque;

- uma letra ou número GIGANTE translúcido como marca d'água no canto superior direito de cada card (ex.: as iniciais do nome do método).

LISTA DE CHECKS EM CARTÕES

- frase de abertura em negrito centralizada (ex.: "Com isso você vai:");

- cada item num cartão-linha largo, fundo um tom abaixo do fundo da página, borda fina, raio 16px;

- ícone de check em contorno na cor principal, à esquerda dentro do cartão.

FUNDOS

- fundos claros em off-white com degradê muito suave (de um tom para outro quase igual);

- alternância entre seções claras e 1 ou 2 seções escuras de contraste dá ritmo à página.

## GRID

Desktop:

container central de aproximadamente 1140px.

Use principalmente:

TEXTO 45% | VISUAL 55%

ou:

VISUAL 55% | TEXTO 45%

Eventualmente:

HEADLINE CENTRAL

+

VISUAL CENTRAL GRANDE.

Não invente layouts aleatórios.

A harmonia vem da repetição do grid.

## ALINHAMENTO

Predominantemente CENTRALIZADO nos cabeçalhos de seção, passos e listas.

Em cards e seções de duas colunas, texto e listas começam na mesma linha, à esquerda.

Cabeçalhos de seção (rótulo + headline + subheadline) são CENTRALIZADOS.

Textos curtos, linhas do tempo e listas de checks também ficam centralizados, em coluna estreita.

Isso deixa a leitura confortável, principalmente no mobile.

Centralize sempre:

- oferta;

- FAQ;

- fechamento;

- seção de impacto.

## TIPOGRAFIA

Use um único par sans-serif que pareça uma família só.

Preferência:

Montserrat (títulos, peso 800) + Inter (todo o resto).

Desktop aproximado:

H1: 56–64px

H2: 48–56px

H3: 24px

Body: 18px

Headlines:

peso 800.

Títulos grandes e pesados, com entrelinha curta e letras levemente mais juntas.

Não use nenhuma outra fonte além dessas duas.

Nunca use fontes serifadas, arredondadas ou decorativas.

Padrão: Montserrat (peso 800) nos títulos e Inter em todo o resto. As duas são sans-serif geométricas e funcionam como uma família só.

O que diferencia headline, subheadline e títulos do resto é apenas TAMANHO e PESO (negrito).

Subheadlines e textos de apoio em cinza médio, peso regular, 20–22px no desktop.

Visual flat: sem efeitos de texto, sem sombra em texto, sem contorno.

## ESPAÇAMENTO

Use bastante espaço em branco.

Desktop:

100–120px entre grandes seções.

Mobile:

70–80px.

Headline → texto:

16–24px.

Texto → CTA:

24–32px.

Blocos internos:

32–48px.

Quando estiver em dúvida:

ADICIONE ESPAÇO.

NÃO ADICIONE DECORAÇÃO.

## IMAGENS

Use fotografia quando ela realmente ajuda o argumento.

Toda página tem PELO MENOS UMA imagem real (foto ou ilustração de qualidade) compondo o design, além dos mockups.

Sugestão de posição: no hero ou na seção de virada/mecanismo.

Prefira:

UMA FOTO GRANDE E BOA

em vez de:

VÁRIAS FOTOS PEQUENAS.

Não use foto só para preencher espaço.

## MOCKUPS

Produtos digitais precisam aparecer.

Mostre:

- celular;

- notebook;

- tablet;

- slides;

- planilha;

- interface;

- áudio;

- PDFs;

- templates;

- área de membros;

dependendo do produto.

Normalmente:

1 MOCKUP PRINCIPAL GRANDE

+

no máximo 1 ou 2 detalhes menores.

Não faça colagens exageradas.

Reserve abundância visual principalmente para a seção:

“O que você recebe”.

## CARDS

Não coloque tudo dentro de card.

Use card apenas quando a informação realmente pertence a uma lista ou conjunto.

Cards:

- fundo simples;

- borda discreta;

- raio de 8–10px;

- pouca sombra;

- bastante espaço interno.

## UMA IDEIA VISUAL POR SEÇÃO

Cada seção deve ter:

1 headline principal

+

1 pequeno bloco de texto

+

1 elemento visual principal

+

CTA quando necessário.

O elemento visual principal ilustra a copy DESSA seção, conforme IMAGEM DA SEÇÃO = COPY DA SEÇÃO.

Não coloque simultaneamente:

foto

+

mockup

+

cards

+

ícones

+

números

+

formas

+

setas

+

depoimentos

+

decoração.

Escolha.

## REGRA DAS SEÇÕES

Cada seção precisa ter uma FUNÇÃO clara.

O layout pode se repetir.

Não tente deixar cada seção “criativa”.

A variação vem do conteúdo e da imagem, não da necessidade de inventar uma composição nova toda hora.

Pode usar:

SEÇÃO 1

texto + visual

SEÇÃO 2

visual + texto

SEÇÃO 3

texto + visual

SEÇÃO 4

visual central

SEÇÃO 5

texto + visual

e repetir.

## DESIGN DAS OBJEÇÕES

Não faça 4 designs diferentes.

Use uma lista vertical limpa.

Cada objeção:

headline curta

+

resposta

+

pequena comparação visual quando ajudar.

Separe com espaço ou divisores leves.

## DESIGN DOS 3 PASSOS (PLUG & PLAY)

- formato LINHA DO TEMPO EM BLOCOS (ver COMPONENTES DE REFERÊNCIA), tudo centralizado;

- desktop: 3 colunas iguais, círculos numerados (01, 02, 03) ligados por uma linha fina horizontal;

- mobile: blocos empilhados e centralizados, com uma linha fina vertical ligando os círculos;

- verbo curto como título de cada passo, em negrito;

- uma linha de texto centralizada por passo;

- uma pílula embaixo de cada passo com o que a pessoa tem na mão naquele passo (ex.: "Arquivo no seu computador", "Skill rodando", "Produto pronto");

- uma miniatura ou ícone por passo mostrando a ação, quando ajudar;

- passo 3 com destaque visual de "pronto";

- sem botão de compra nesta seção: o botão flutuante cuida disso.

## DESIGN DO VÍDEO (DEMONSTRAÇÃO)

- vídeo no lugar da foto (hero ou seção de demonstração), com o mesmo raio dos cards; proporção pela orientação do link: tutorial horizontal em 16:9 ocupando a largura da coluna; Shorts vertical em 9:16, centralizado, com altura máxima de ~640px no desktop para não dominar a tela;

- smart autoplay: inicia mudo, em prévia, com um selo claro "Clique para ouvir" sobre o vídeo;

- ao clicar, o vídeo reinicia do começo com som;

- no mobile, o vídeo ocupa a largura total e vem logo abaixo da headline;

- se não houver link do vídeo, mostre o visual estático da demonstração, sem placeholder.

link do YouTube ou Shorts: renderize por iframe de embed; autoplay mudo (e em loop, no caso do Shorts), com o selo "Clique para ativar o som" sobre o vídeo; ao clicar, ative o som pela API do player do YouTube;

o vídeo substitui a foto daquela seção: não mostre foto e vídeo no mesmo bloco;

no mobile, o vídeo ocupa a largura da coluna (o vertical centralizado, com altura limitada à altura da tela) e vem logo abaixo da headline.

## DESIGN DOS DEPOIMENTOS

segunda seção da página, logo depois do hero; segue o design system e fica antes da segunda dobra, então sem nenhum botão de compra;

cabeçalho curto e centralizado; rótulo sugerido "QUEM JÁ USOU" ou "O QUE ESTÃO DIZENDO";

desktop: 3 cards por linha (ou 4 em duas linhas); mobile: um card por vez em carrossel deslizável, ou empilhados;

cada card: fundo um tom abaixo do fundo da página (ou branco sobre fundo claro), borda fina, raio 16px, padding confortável, mesma altura pelo grid;

no topo do card, avatar redondo (foto de rosto realista e diversa, gerada pelo Lovable, uma diferente por card) à esquerda, com o nome em negrito e, abaixo, cidade ou perfil em cinza pequeno;

cinco estrelas preenchidas na cor de destaque, acima ou abaixo do nome;

texto do depoimento em 2 a 4 linhas, a frase mais forte em negrito;

visual leve: nada de balão de chat exagerado, logotipo de rede social, selo de "verificado" nem print de conversa falso;

esses depoimentos são conteúdo real a renderizar, nunca placeholder a remover na varredura final.

RESPIRO DENTRO DO CARD (regra obrigatória): foto, nome, estrelas e texto nunca ficam colados; cada um tem espaço entre si.

padding interno do card: 28–32px no desktop, 24px no mobile;

avatar → nome: 12–16px; nome → cidade/perfil: 2–4px; bloco do topo (avatar + nome) → estrelas: 12–16px; estrelas → texto do depoimento: 14–18px;

entrelinha do texto do depoimento confortável (1.5–1.6); o texto nunca encosta na borda do card;

quando avatar e nome ficam lado a lado, o espaço entre a foto e o bloco de nome é de pelo menos 12px;

no mobile é onde mais aperta: mantenha os mesmos respiros, empilhe avatar, nome, estrelas e texto centralizados com no mínimo 12px entre cada elemento, e 20–24px entre um card e o próximo;

cards do mesmo nível têm a mesma altura e o mesmo respiro; nenhum card fica mais apertado que o outro.

## DESIGN DOS BULLETS

lista vertical de cartões-linha, coluna central com largura máxima de ~900px;

cada cartão: fundo um tom abaixo do fundo da página, borda fina, raio 16px, padding confortável;

à esquerda de cada cartão, um ícone de CADEADO em contorno (lucide "lock") na cor principal, no lugar do check: o cadeado comunica "isso vem com o produto"; o check comunicava "já resolvido";

texto à esquerda; a parte mais curiosa do bullet em negrito, nunca o bullet inteiro;

ao final de cada cartão, alinhada à direita no desktop e abaixo do texto no mobile, uma PÍLULA DE LOCALIZAÇÃO com a parte do produto onde está a resposta (ex.: "→ Regras da Cama"): fundo na cor principal com 10% de opacidade, texto na cor principal, peso 600, 13–14px, raio total;

12–16px entre os cartões;

abaixo da lista, a frase de fechamento centralizada, em negrito, e logo abaixo um botão de CTA que rola até a seção da oferta (permitido porque a seção fica depois da segunda dobra).

## DESIGN DOS ARGUMENTOS CIENTÍFICOS

só quando a copy aprovada tem a seção; o Lovable nunca cria citação por conta própria;

cabeçalho centralizado (rótulo + headline + subheadline), como nas outras seções;

desktop: 2 a 4 cards iguais em linha (3 é o ideal), largura total do container, mesma altura pelo grid; mobile: empilhados;

cada card: fundo um tom abaixo do fundo da página, borda fina, raio 16px, padding generoso; no topo, uma aspa grande e discreta na cor principal como marca; ACHADO em negrito, 18–20px; FONTE em 13–14px, cinza médio, abaixo; PONTE em texto regular, separada do achado por uma linha fina;

quando o achado tem número, o número pode ir em destaque grande (40–48px, peso 800, cor principal) acima da frase; nunca inventar número para ter destaque;

sem logotipo de universidade, sem selo "comprovado cientificamente", sem gráfico decorativo; a credibilidade vem da fonte escrita, não de enfeite;

pode ser uma das 1 ou 2 seções escuras de contraste da página, se a virada / mecanismo não for;

sem botão de compra nesta seção: o botão flutuante cuida disso.

## BOTÃO DE COMPRA E BOTÃO FLUTUANTE

PRIMEIRA DOBRA:

- nenhum botão de compra;

- o lead precisa ler a headline, a subheadline e o primeiro visual antes de ver qualquer botão.

BOTÃO FLUTUANTE:

- aparece somente depois que o lead passa da SEGUNDA DOBRA (aprox. 2× a altura da tela);

- fica fixo no CENTRO INFERIOR da tela em todas as larguras, nunca na lateral: no desktop, centralizado horizontalmente, largura definida pelo texto com padding generoso (mínimo 20px por 32px), a 24px do rodapé da tela; no mobile, também centralizado, ocupando a largura da tela menos 16px de cada lado, a 16px do rodapé mais a safe-area;

- usa o texto de CTA aprovado e a mesma cor e estilo dos outros botões;

- ao clicar, NÃO vai para o checkout: rola suavemente até a seção da OFERTA (resumo da oferta com o preço);

- some enquanto a seção da oferta está visível na tela e volta a aparecer ao sair dela;

- entra e sai com uma animação leve (fade + deslize curto de baixo para cima), sempre a partir do centro inferior.

BOTÕES DAS SEÇÕES:

- só existem depois da segunda dobra;

- também rolam até a OFERTA.

O ÚNICO botão que leva ao checkout é o botão da seção da OFERTA (e o do CTA final).

## DESIGN DAS LISTAS DE PENSAMENTOS E SENTIMENTOS

Ninguém lê frases soltas empilhadas. Diálogos internos e qualquer sequência de frases curtas viram LISTA ESCANEÁVEL.

- cada frase numa linha própria, como item de lista;

- uma linha divisória fina entre os itens (1px, cor neutra);

- à esquerda de cada item, um ícone pequeno ou emoji discreto que represente o sentimento daquela frase (ex.: vergonha, confusão, medo, cansaço, alívio, esperança, confiança);

- ícones de linha (estilo Lucide) na cor principal são o padrão; emoji só se combinar com o nicho e com o tom;

- no diálogo negativo, ícones em tom mais neutro ou apagado; no positivo, ícones na cor de destaque ou de sucesso;

- texto à esquerda dentro da lista, lista centralizada na página com largura máxima de ~760px;

- a frase de fechamento da seção vem depois da lista, em destaque (negrito, centralizada).

Nunca use um emoji diferente a cada linha só para enfeitar: o ícone tem que DIZER o sentimento.

## OFERTA

A oferta pode ser a parte mais visual.

Use:

STACK DO PRODUTO

+

LISTA CURTA

+

PREÇO

+

CTA.

Não use:

- dez selos;

- cinco caixas;

- contador falso;

- desconto falso;

- urgência falsa.

## DESIGN DA ANCORAGEM DE PREÇO

card central de largura máxima ~720px, centralizado, fundo um tom abaixo do fundo da página (ou branco), borda fina, raio 20–24px, padding generoso;

título centralizado no topo do card;

cada linha: à esquerda um ícone de check em contorno na cor principal e o nome do item; à direita o preço com risco (text-decoration: line-through) na cor de destaque; o preço sempre alinhado à borda direita do card, em coluna; respiro ou divisória fina entre as linhas;

abaixo da lista, uma pílula centralizada "Tudo isso deveria custar: R$ [soma]" com o valor riscado na cor de destaque;

em seguida, a frase de transição centralizada e o bloco do preço real em destaque: o parcelado grande (peso 800), o à vista menor logo abaixo, e o botão de CTA embaixo;

sem contador, sem selo de desconto, sem "de/por" piscando, sem chama nem relógio;

mobile: se não couber lado a lado, o nome do item em cima e o preço riscado embaixo, ainda na mesma linha-cartão; card com padding menor e preço real bem legível.

## DESIGN DA SEÇÃO DO AUTOR

duas colunas no desktop: foto de um lado, texto do outro (VISUAL 45% | TEXTO 55% ou o inverso), dentro do container central; mobile: foto em cima e texto embaixo, centralizados;

foto real da pessoa, retrato de boa qualidade, cantos arredondados (ou círculo), tamanho equilibrado, nunca estourando a coluna;

rótulo curto em caixa alta (ex.: "QUEM CRIOU O [PRODUTO]") + headline + o resuminho de 1 a 2 parágrafos; os marcos e números reais podem ir em negrito;

se houver poucos marcos fortes, eles podem virar 2 a 4 pílulas ou uma lista curta ao lado da foto;

respiro entre foto, nome, texto e marcos, igual ao cuidado da seção de depoimentos;

visual discreto e elegante: sem selo, sem moldura chamativa, sem logotipo; a autoridade vem do texto e da foto;

pode fechar com um botão de CTA que rola até a oferta.

## RESPONSIVIDADE

A página precisa ficar boa em:

DESKTOP

TABLET

MOBILE.

Desktop:

use duas colunas quando houver espaço.

Tablet:

reduza proporções mantendo a hierarquia.

Mobile:

empilhe de maneira limpa.

Não recrie um site completamente diferente no mobile.

Preserve:

- respiro;

- imagens;

- mockups;

- legibilidade;

- hierarquia.

## LAYOUT SEM SOBREPOSIÇÃO (NADA ENCAVALADO)

O erro mais comum do Lovable é elemento em cima de elemento: texto atravessando imagem, card invadindo card, marca d'água cobrindo título, botão flutuante tampando a oferta, foto estourando a coluna no mobile. O prompt impede isso ANTES de a página existir.

Inclua SEMPRE no prompt, na parte de instruções, o bloco abaixo, inteiro e sem resumir:

“REGRAS DE LAYOUT (OBRIGATÓRIAS, VALEM PARA TODAS AS SEÇÕES):

1. FLUXO NORMAL SEMPRE. Todo conteúdo (texto, imagem, mockup, card, botão, ícone) fica no fluxo do documento, dentro de flex ou grid. Proibido position: absolute ou position: fixed em qualquer elemento de conteúdo. As únicas exceções são o botão flutuante e os efeitos decorativos de fundo (brilho radial, marca d'água), que ficam com position: absolute DENTRO de um container com position: relative e overflow: hidden, com pointer-events: none e z-index abaixo do conteúdo.

2. ALTURA AUTOMÁTICA. Nenhuma seção, card, coluna ou bloco de texto tem altura fixa (height). Use min-height quando precisar de piso; o conteúdo define a altura. Texto longo empurra o que vem abaixo, nunca sobrepõe.

3. IMAGEM CONTIDA. Toda imagem e todo mockup ficam dentro de um container com largura máxima definida, aspect-ratio fixo (16:9, 4:5 ou 1:1, conforme o bloco) e object-fit: cover; a imagem tem max-width: 100% e height: auto. Imagem nunca ultrapassa a coluna em nenhuma largura de tela.

4. GRID COM RESPIRO. Colunas e cards usam gap (mínimo 24px no desktop, 16px no mobile), nunca margem negativa. Nada de transform: translate para encaixar elemento; o alinhamento é feito pelo grid.

5. EMPILHAMENTO PREVISÍVEL. Abaixo de 1024px, toda seção de duas colunas vira uma coluna: visual em cima, texto embaixo (exceto no hero, onde a headline vem antes do visual). Abaixo de 768px, grades de 3 colunas (passos, cards) viram 1 coluna. Nada fica lado a lado no mobile.

6. TEXTO QUE QUEBRA. Headlines e títulos usam overflow-wrap: anywhere e tamanho responsivo (clamp) para nunca estourar a largura; nenhuma palavra sai do container. Pílulas, rótulos e botões usam white-space: normal e podem quebrar em duas linhas.

7. CAMADAS CONTROLADAS. Só três níveis de z-index existem na página: fundo decorativo (0), conteúdo (1) e botão flutuante (50). Nenhum outro elemento recebe z-index.

8. BOTÃO FLUTUANTE NO CENTRO INFERIOR, SEM TAMPAR NADA. O botão flutuante fica sempre centralizado horizontalmente no rodapé da tela (position: fixed; bottom; left: 50%; transform: translateX(-50%)), em todas as larguras, nunca no canto lateral. Ele respeita a safe-area no mobile, e a página recebe padding inferior igual à altura do botão mais 16px, para que o último conteúdo, o rodapé e o botão da oferta nunca fiquem escondidos atrás dele.

9. MARCA D'ÁGUA E BRILHO ATRÁS DO CONTEÚDO. A letra gigante translúcida dos cards escuros e o brilho radial do fundo ficam com z-index 0, opacidade baixa e dentro do overflow: hidden do próprio card ou seção; nunca cobrem título, texto ou botão.

10. LINHA DOS PASSOS. Na linha do tempo em blocos, a linha que liga os círculos é um pseudo-elemento do container da linha (não de cada card) e, no mobile, vira vertical dentro do próprio container ou some; nunca atravessa texto.

11. UM VISUAL POR BLOCO. Cada bloco do grid contém um único elemento visual principal (foto, mockup ou ilustração). Nunca duas imagens empilhadas ou sobrepostas no mesmo bloco, nunca imagem como fundo de texto, nunca texto escrito por cima de foto (se precisar, o texto vai numa faixa sólida de cor abaixo da foto).

12. CONTAINER CENTRAL. Todo conteúdo fica dentro de um container de largura máxima 1140px, centralizado, com padding lateral de 24px no desktop e 16px no mobile. Nada encosta na borda da tela.

13. ANIMAÇÃO SÓ DE OPACIDADE. Nenhuma animação move elemento de lugar (sem slide, sem parallax, sem elemento entrando por cima de outro). Só fade sutil; a única exceção é o botão flutuante, com fade e deslize curto de 8px.

14. TESTE NAS QUATRO LARGURAS. Antes de finalizar, renderize a página em 1440px, 1024px, 768px e 375px e confira seção por seção: nenhum elemento sobrepõe outro, nenhuma imagem estoura a coluna, nenhum texto é cortado, nenhum botão fica tampado. Se encontrar qualquer um desses casos, corrija o layout (nunca a copy) antes de entregar.”

Esse bloco vale para qualquer nicho e qualquer abertura. Ele não muda o design system nem a direção de arte: só garante que cada elemento tenha o próprio lugar.

## FILTRO CRÍTICO ANTES DE GERAR O PROMPT DO LOVABLE

Antes de criar o prompt final, faça uma revisão SILENCIOSA de toda a copy.

Imagine que qualquer frase enviada pode ser publicada literalmente no site.

Procure e elimine:

- colchetes;

- placeholders;

- comentários internos;

- instruções;

- notas;

- avisos;

- explicações da skill;

- explicações sobre a copy;

- explicações de segurança;

- textos destinados ao usuário e não ao comprador;

- indicações de que alguma coisa foi inventada;

- instruções de substituição;

- nomes técnicos do processo de criação;

- classificações como “mecanismo conceitual”.

Para CADA frase, pergunte:

“Um possível comprador deveria ler isso literalmente na página?”

Se a resposta for NÃO:

REMOVA DA COPY VISÍVEL.

## FORMATO DA ENTREGA PARA O LOVABLE

Entregue UM ÚNICO BLOCO pronto para copiar e colar.

Dentro desse bloco, separe claramente:

A) INSTRUÇÕES DE IMPLEMENTAÇÃO (design system, paleta com HEX, botões, REGRAS DE LAYOUT inteiras)

B) MAPA DE SEÇÕES: para cada seção, na ordem da página, o nome, o layout do grid (TEXTO 45% | VISUAL 55%, VISUAL 55% | TEXTO 45% ou VISUAL CENTRAL), como empilha no mobile e o bloco IMAGEM DESTA SEÇÃO

C) COPY VISÍVEL DA PÁGINA, seção por seção, na mesma ordem e com os mesmos nomes do mapa

O prompt precisa mandar o Lovable:

- CRIAR DO ZERO;

- implementar a página completa;

- usar a copy aprovada;

- criar o design;

- criar as seções;

- usar imagens;

- usar mockups;

- adaptar a direção de arte ao nicho;

- manter o design system;

- ser responsivo;

- funcionar em desktop, tablet e mobile.

aplicar as REGRAS DE LAYOUT sem sobreposição em todas as seções;

usar em cada seção exatamente a imagem descrita no bloco IMAGEM DESTA SEÇÃO, nunca uma imagem genérica do nicho.

Não entregue apenas um wireframe.

Peça a implementação completa.

## INSTRUÇÕES ESPECÍFICAS NO PROMPT DO LOVABLE

Quando houver vídeo de demonstração, o prompt deve pedir:

- um componente de vídeo que leia o link de uma constante VIDEO_URL no topo do código;

- se VIDEO_URL estiver vazia, renderizar o visual estático da demonstração no lugar;

- smart autoplay (mudo + "Clique para ouvir" + reinício com som);

- nunca mostrar o nome da constante nem a URL na página.

aceitar em VIDEO_URL tanto um arquivo de vídeo quanto um link do YouTube ou Shorts, detectar o tipo e embutir por iframe quando for YouTube;

detectar a orientação: Shorts ou vídeo vertical em 9:16 centralizado (altura máxima ~640px no desktop); tutorial horizontal em 16:9 na largura da coluna;

para link do YouTube, usar autoplay mudo (loop no Shorts) com o selo "Clique para ativar o som" e ativar o som pela API do player ao clicar;

na abertura Demonstração, o vídeo entra no lugar da foto (hero ou seção de demonstração), nunca os dois juntos;

se VIDEO_URL estiver vazia, renderizar o visual estático da demonstração, sem placeholder.

Quando a abertura for Plug & Play:

- incluir a seção de 3 passos com o layout de DESIGN DOS 3 PASSOS.

Sempre:

- incluir a seção de bullets de curiosidade com o layout de DESIGN DOS BULLETS.

Sempre, sobre a seção de bullets:

usar ícone de cadeado (lucide "lock") em cada cartão, não check;

renderizar a localização de cada bullet como uma pílula separada do texto, não como parte da frase;

incluir a frase de fechamento e o botão que rola até a oferta;

na COPY VISÍVEL, escrever cada bullet assim: Bullet: [negrito]Trecho curioso[/negrito] resto da frase. | Pílula: → Nome da parte do produto

Quando houver seção de argumentos científicos:

renderizar com o layout de DESIGN DOS ARGUMENTOS CIENTÍFICOS;

usar SOMENTE as citações que estão na copy visível, com achado, fonte e ponte exatamente como escritos; nunca acrescentar, completar, resumir ou "melhorar" citação, número ou nome de autor;

se a copy visível não trouxer a seção, não criar nenhuma referência científica em lugar nenhum da página.

Sempre, sobre depoimentos:

incluir a seção de depoimentos como SEGUNDA seção da página, logo depois do hero, com o layout de DESIGN DOS DEPOIMENTOS;

renderizar exatamente os depoimentos da copy visível, sem inventar outros e sem alterar nomes ou textos;

gerar um avatar de rosto realista e diverso para cada depoimento (fotos diferentes entre si) e cinco estrelas na cor de destaque;

tratar esses depoimentos como conteúdo real a renderizar, NUNCA como placeholder a remover na varredura (eles não têm colchetes e devem aparecer na página).

dar respiro entre foto, nome, estrelas e texto de cada depoimento (nunca colados), com padding interno de 28–32px no desktop e 24px no mobile e no mínimo 12px entre cada elemento, com atenção especial ao mobile.

Sempre, sobre a oferta:

abrir a OFERTA com a ANCORAGEM DE PREÇO (pilha de valor), com o layout de DESIGN DA ANCORAGEM DE PREÇO;

renderizar cada entregável com o preço individual riscado (text-decoration: line-through) e a soma "deveria custar" também riscada, exatamente com os valores da copy visível;

mostrar o preço real logo depois (parcelado em destaque maior, à vista abaixo) e o botão de CTA;

nunca criar contador, estoque, vagas, "de/por" nem desconto que não estejam na copy.

Sempre, sobre a seção do autor:

incluir a seção como a última de conteúdo, logo antes do FAQ, com o layout de DESIGN DA SEÇÃO DO AUTOR;

nomear a seção com algo como "Quem criou o [produto]", nunca "Autor", "Sobre mim" ou "Biografia";

renderizar a foto real da pessoa (sem foto, só o texto) e apenas a bio fornecida, sem inventar número, resultado ou autoridade;

se não houver bio do autor na copy, não criar a seção.

Sempre, sobre botões:

- nenhum botão de compra na primeira dobra (o hero não tem botão);

- botão flutuante centralizado no rodapé da tela em todas as larguras (nunca na lateral), que aparece depois da segunda dobra, rola até a seção da oferta (id="oferta") e some enquanto a oferta está visível;

- apenas os botões da oferta e do CTA final levam ao checkout, por uma constante CHECKOUT_URL no topo do código.

Sempre, sobre listas de pensamentos:

- renderize diálogos internos como lista com divisória fina e ícone de sentimento à esquerda de cada item, conforme DESIGN DAS LISTAS DE PENSAMENTOS E SENTIMENTOS;

- no prompt, informe para cada frase qual ícone usar (ex.: "ícone: rosto envergonhado / lucide 'frown'").

Sempre, sobre layout:

incluir o bloco REGRAS DE LAYOUT (ver LAYOUT SEM SOBREPOSIÇÃO) inteiro, sem resumir;

descrever, para cada seção, o layout do grid e como ela empilha no mobile;

terminar o prompt com o bloco VERIFICAÇÃO FINAL inteiro (ver ÚLTIMA ORDEM DO PROMPT DO LOVABLE), que manda o Lovable conferir sobreposição, ícones, imagens, funcionamento e carregamento nas quatro larguras e relatar o que corrigiu.

Sempre, sobre imagens:

incluir, para cada seção com visual, o bloco IMAGEM DESTA SEÇÃO com cena, objeto, pessoa, momento, a frase da copy que ela ilustra (entre aspas) e a proporção (ver IMAGEM DA SEÇÃO = COPY DA SEÇÃO);

mandar o Lovable gerar ou escolher a imagem a partir dessa descrição, nunca por palavra-chave solta do nicho;

proibir imagem genérica de banco e imagem que mostre coisa diferente do texto ao lado;

se não houver imagem que case com a copy, usar o mockup do produto ou deixar a seção só com texto.

## ORDEM OBRIGATÓRIA PARA O LOVABLE

Inclua no prompt:

“REGRA CRÍTICA DE IMPLEMENTAÇÃO:

Existe uma diferença entre instruções deste prompt e textos da página.

Renderize no site SOMENTE o conteúdo identificado como COPY VISÍVEL.

Nenhuma instrução de implementação deve aparecer no site.

Nenhum comentário deste prompt deve aparecer no site.

Nenhum placeholder deve aparecer no site.

Nenhuma observação interna deve aparecer no site.

Nenhuma explicação sobre mecanismo, copy, segurança, design ou criação deve aparecer no site.

Nunca transforme instruções em elementos visuais.

Se uma informação necessária não existir, omita aquele elemento em vez de mostrar um placeholder.”

## ÚLTIMA ORDEM DO PROMPT DO LOVABLE

O prompt SEMPRE deve terminar com:

“ANTES DE FINALIZAR:

Faça uma varredura em todo o conteúdo renderizado.

Pergunte para cada texto:

‘Isso é uma frase que o comprador final deveria ler?’

Se não for, remova.

Não renderize:

- instruções;

- comentários;

- placeholders;

- textos entre colchetes;

- notas internas;

- explicações técnicas deste prompt;

- orientações de implementação.

O SITE FINAL DEVE CONTER SOMENTE COPY DESTINADA AO COMPRADOR.”

E, logo depois desse bloco, o prompt termina SEMPRE com a VERIFICAÇÃO FINAL abaixo, copiada inteira. É o Lovable conferindo a própria página antes de dizer que terminou:

“VERIFICAÇÃO FINAL (OBRIGATÓRIA, FAÇA ANTES DE DIZER QUE TERMINOU):

Abra a página pronta e passe por TODOS os itens abaixo em 1440px, 1024px, 768px e 375px. Corrija o que falhar e repita a verificação até tudo passar. Só então entregue.

1. SOBREPOSIÇÃO

nenhum elemento em cima de outro: texto sobre imagem, card sobre card, imagem sobre texto;

nenhum ícone encavalado no texto ao lado dele, cortado ou fora da linha (ícones de check, de sentimento e dos passos alinhados ao centro vertical da primeira linha do texto, com espaço fixo entre ícone e texto);

nenhuma marca d'água, brilho de fundo ou número decorativo cobrindo título, texto ou botão;

o botão flutuante está centralizado no rodapé da tela em todas as larguras (nunca na lateral) e não tampa a oferta, o CTA final, o rodapé nem nenhum texto;

círculos e linha dos passos sem atravessar texto; no mobile, linha vertical ou ausente;

nenhuma headline, pílula ou botão com palavra saindo do container; nenhum texto cortado;

nenhuma rolagem horizontal em nenhuma largura.

2. IMAGENS E ÍCONES

toda imagem carrega (nenhum quadrado vazio, imagem quebrada ou texto alternativo aparecendo no lugar);

toda imagem está dentro da coluna, na proporção definida, sem distorção (nada esticado ou achatado);

cada imagem mostra a mesma cena que a copy da sua seção, conforme o bloco IMAGEM DESTA SEÇÃO; se não mostra, troque a imagem, nunca o texto;

nenhuma imagem de resultado em seção de dor; nenhum mockup em seção que não fala do produto;

todos os ícones existem e renderizam (nenhum nome de ícone aparecendo como texto, nenhum ícone faltando numa lista onde os outros têm);

ícones do mesmo grupo têm o mesmo tamanho, a mesma espessura e a mesma cor.

3. FUNCIONAMENTO

todos os botões respondem ao clique; os botões das seções e o flutuante rolam suavemente até a seção da oferta (id="oferta"); só os botões da oferta e do CTA final abrem CHECKOUT_URL;

o botão flutuante aparece só depois da segunda dobra, some enquanto a oferta está visível e volta depois;

o FAQ abre e fecha cada pergunta;

se houver vídeo: inicia mudo com o selo "Clique para ouvir" e reinicia com som ao clicar; se VIDEO_URL estiver vazia, mostra o visual estático sem placeholder;

nenhum link quebrado, nenhum botão que leve a página em branco.

4. CARREGAMENTO

a página abre em menos de 3 segundos em conexão móvel comum;

imagens comprimidas (WebP ou JPG otimizado, nenhuma acima de 300 KB), com largura e altura definidas para nada pular enquanto carrega;

imagens abaixo da primeira dobra com carregamento tardio (loading="lazy"); a imagem do hero carrega primeiro;

fontes Montserrat e Inter carregam sem trocar de fonte no meio (texto não pisca);

nenhum erro no console do navegador e nenhum recurso que deixou de carregar;

a página não trava nem pula ao rolar no mobile.

5. CONTEÚDO

nenhuma instrução, placeholder, colchete, nome de constante ou nota interna visível;

toda a copy visível está na página, na ordem do mapa de seções, sem resumo e sem frase alterada;

nenhum botão de compra na primeira dobra.

nenhuma citação, estudo, número ou nome de autor além dos que estão na copy visível, escritos exatamente como na copy.

a seção de depoimentos é a SEGUNDA da página (logo depois do hero), com avatares realistas e diferentes entre si e cinco estrelas, e todos os depoimentos da copy aparecem inteiros, sem serem removidos como placeholder.

Se qualquer item falhar, corrija e refaça a verificação inteira. No fim, relate item por item o que foi conferido e o que foi corrigido.

O SITE FINAL NÃO TEM NENHUM ELEMENTO SOBREPOSTO, TUDO ABRE E FUNCIONA, CARREGA RÁPIDO, E CADA IMAGEM CONTA A MESMA HISTÓRIA DA COPY DA SUA SEÇÃO.”

## TESTE FINAL DO DESIGN

Antes de entregar, verifique:

Todas as headlines parecem do mesmo site?

Todos os botões são iguais?

As bordas têm o mesmo raio?

Os espaçamentos são consistentes?

As colunas começam nas mesmas linhas?

As imagens têm proporções coerentes?

O produto aparece?

Existe espaço em branco?

Desktop está bonito?

Tablet está bonito?

Mobile está bonito?

Existe alguma seção confusa?

Se houver mais de 2 ou 3 elementos competindo:

SIMPLIFIQUE.

Pergunte:

“Se eu remover isso, prejudica a venda?”

Se não:

REMOVA.

Verifique também:

A promessa central aparece no hero, nas headlines principais, na oferta e no CTA final?

A seção de bullets de curiosidade está presente, com a headline dizendo que as respostas estão no produto, cadeado em cada cartão, pílula de localização em todos os bullets e frase de fechamento?

Na abertura Plug & Play, a seção de 3 passos está presente e é visual?

Na abertura Demonstração, o vídeo (arquivo ou link do YouTube/Shorts) entrou no lugar da foto, na proporção certa (16:9 horizontal ou 9:16 vertical centralizado), com smart autoplay e visual alternativo sem placeholder?

Algum texto promete resultado em semanas ou meses? Se sim, volte para a copy e corrija.

Se há seção de argumentos científicos: o nicho justifica, cada estudo foi localizado e tem link ou DOI na lista de conferência, cada citação prova a solução (não assusta com o problema) e é fiel ao que o estudo mediu? Qualquer NÃO: remova a citação ou a seção.

A seção de depoimentos é a segunda da página, logo depois do hero, com cards de mesma altura, avatares realistas e cinco estrelas, e sem nenhum botão de compra? Há respiro claro entre foto, nome, estrelas e texto (nunca colados), inclusive no mobile?

A oferta abre com a ancoragem (cada item com preço riscado e a soma "deveria custar" riscada) antes do preço real? Os preços riscados têm risco visível e a soma bate com as linhas?

A seção do autor é a última antes do FAQ, chamada "Quem criou..." (nunca "Autor"), com foto, resuminho de 1 a 2 parágrafos e só marcos reais?

Existe algum botão de compra na primeira dobra? Se sim, remova.

O botão flutuante está centralizado no rodapé da tela (nunca na lateral), aparece só depois da segunda dobra e leva até a oferta, não ao checkout?

Existe pelo menos uma imagem real na página?

Todos os textos usam a mesma família sans-serif, sem serifa?

Alguma headline de seção poderia estar na página de outro produto? Se sim, volte para a copy e corrija.

Existe alguma sequência de frases curtas empilhadas sem formato de lista? Se sim, transforme em lista com divisórias e ícones.

Em 1440, 1024, 768 e 375px, algum elemento fica em cima de outro, alguma imagem estoura a coluna, algum texto é cortado? Se sim, corrija o layout.

O botão flutuante tampa a oferta, o CTA final ou o rodapé em alguma largura? Se sim, ajuste o padding inferior da página.

Alguma marca d'água ou brilho de fundo passa por cima de título ou texto? Se sim, mande para trás.

Para cada imagem: tampando o texto, ela conta a mesma história da headline da seção? Se não, troque a imagem.

Alguma imagem mostra resultado numa seção que ainda fala de dor, ou mockup numa seção que não fala do produto? Se sim, troque.

## REGRA MESTRA DA COPY

A progressão ideal é:

“OPA. O QUE É ISSO?”

↓

“ISSO É PARA MIM.”

↓

“SERÁ QUE ISSO ACONTECE COMIGO?”

↓

“QUERO ENTENDER.”

↓

“É EXATAMENTE ISSO.”

↓

“AGORA ENTENDI.”

↓

“PARECE SIMPLES.”

↓

“CONSIGO ME IMAGINAR USANDO.”

↓

“ENTENDI O QUE RECEBO.”

↓

“EU QUERO.”

↓

“MAS E SE...?”

↓

“ESSA OBJEÇÃO NÃO FAZ MAIS TANTO SENTIDO.”

↓

“POR ESSE PREÇO, FAZ SENTIDO TESTAR.”

## REGRA MESTRA DO DESIGN

A COPY DIZ O ARGUMENTO.

O DESIGN FAZ O ARGUMENTO SER VISTO.

Não diga:

“É simples.”

MOSTRE.

Não diga:

“Tem muito conteúdo.”

MOSTRE ABUNDÂNCIA.

Não diga:

“Organiza tudo.”

MOSTRE ANTES E DEPOIS.

Não diga:

“É melhor do que fazer sozinho.”

MOSTRE O TRABALHO.

## REGRA MESTRA DE PERSPECTIVA

ANTES DE TENTAR SER CRIATIVO, SAIBA COM QUEM ESTÁ FALANDO.

CRIATIVIDADE NUNCA PODE QUEBRAR A LÓGICA DO PÚBLICO.

A HEADLINE MAIS CURIOSA DO MUNDO ESTÁ ERRADA

SE COLOCA O LEAD NO PAPEL ERRADO.

## RESULTADO FINAL

O resultado deve unir:

PROMESSA CENTRAL ÚNICA, RÁPIDA E CRÍVEL

+

PÚBLICO CORRETO

+

PERSPECTIVA CORRETA

+

CURIOSIDADE

+

TENSÃO OU DESEJO

+

CONCRETUDE

+

DIRECT RESPONSE

+

BULLETS DE CURIOSIDADE

+

QUEBRA DE OBJEÇÕES

+

ESPECIFICIDADE

+

FOTOGRAFIA

+

MOCKUPS

+

PRODUTO VISÍVEL

+

DESIGN ULTRA SIMPLES

+

DESIGN SYSTEM CONSISTENTE

+

DIREÇÃO DE ARTE ESPECÍFICA

+

RESPONSIVIDADE

+

SITE LIMPO

+

COMPRA FÁCIL.

ESSA É A RÉGUA.

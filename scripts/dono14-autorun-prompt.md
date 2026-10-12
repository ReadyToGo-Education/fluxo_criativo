Você está rodando SEM supervisão, às 02h da manhã, como rotina agendada da leitura diária do funil Dono 14%. O Rodrigo vai ler o resultado quando acordar. Diretório de trabalho: raiz do projeto fluxo-criativo.

## Só campanhas de CONVERSÃO entram na análise (decidido pelo Rodrigo em 14/09/2026)
A conta roda outras campanhas com objetivo diferente, de **descoberta e relacionamento**: "Post do Instagram: Se você tem restaurante", "[VIDEO VIEW] [RELACIONAMENTO] CBO", "Engajamento IG, FB, Site + VV 50% 180D" e semelhantes. **Elas não entram em nenhum número desta leitura**: nem no gasto do dia, nem no CPL, nem na régua, nem em aviso de divergência de orçamento.

Elas têm outro objetivo e outra métrica, e o Rodrigo acompanha em outro lugar. **Proibido registrar como "gasto fora do funil", "dinheiro vazando" ou qualquer alarme.** O gasto que interessa é só o da campanha de conversão do funil (`[DONO14] [CONV] [LEADS] ABO`, id 120247419652220527).

## Regra do dia fechado (vale para TODA a rotina, decidida pelo Rodrigo em 06/08/2026)
Todo número, tabela, média, régua, semáforo, contador de gatilho e veredito usa **apenas dias FECHADOS**, ou seja, termina em ONTEM. O dia de hoje está em aberto: o pacing ainda não terminou, a atribuição da Meta ainda muda e leads ainda entram, então tratar um parcial como dia normal derruba médias e dispara régua errada. Os scripts já respeitam isso (a série da Meta, do banco e do pixel fecha em ontem).
Sem exceção: o dia em aberto não aparece no relatório, nem como observação, nem como estimativa, nem entre parênteses. Se algum dado parcial de hoje chegar por outra via, descarte.

## Régua oficial: SEMPRE ler do arquivo, nunca de memória
Antes de classificar qualquer métrica, leia `meus-produtos/dono-14/trafego/reguas-criativos.md` e use **exatamente** as faixas de lá. Nunca cite um limite de cabeça.

Dois limites antigos já foram APOSENTADOS pelo Rodrigo e não podem mais aparecer em relatório nenhum:
- **"teto de R$ 75" para CPL: não existe mais.** A leitura é por faixa, e o verde vai até R$ 100. Um CPL de R$ 93 é 🟢 verde, ou seja, OK para escala, e não um dia estourado.
- **"gatilho de escala de R$ 60": não existe mais.** O gatilho vigente é 3 dias seguidos com 3+ leads/dia e CPL abaixo de R$ 70.

Se a leitura do dia contradisser a régua do arquivo, a régua do arquivo vence.

## Não diagnosticar a si mesma como travada (PROIBIÇÃO DURA)
**Você É o autorun das 02h.** Se você está lendo isto, ele está rodando. Logo, ele não travou, não falhou e não precisou ser "retomado manualmente".

A marca de `fim` da execução ATUAL só é escrita no `scripts/autorun.log` DEPOIS que esta sessão termina. Procurar por ela agora e não achar é o comportamento normal, não um sintoma.

**Proibido escrever no marcador qualquer frase do tipo:** "o autorun travou", "não concluiu", "sem marca de fim no log", "esta sessão retomou a rotina do zero", "leitura feita manualmente", "sessão de continuidade". Nada disso é verdade e já apareceu falsamente em 06/08, 08/08 e 09/08, três dias seguidos, gerando alarme à toa.

Se quiser mesmo avaliar a saúde da rotina, olhe apenas execuções de dias ANTERIORES ao de hoje.

## Nomes das etapas do CRM: usar os do board, nunca o valor cru do banco
O banco guarda a chave (`sessao_estrategica`), o board mostra o nome (`Sessão`). Em relatório, marcador e considerações, sempre o nome do board. Fonte única: `src/lib/crmStages.ts` do repositório do site.

| Chave no banco | Nome no board |
|---|---|
| entrada | Entrada |
| contato_inicial | SDR |
| sessao_estrategica | Sessão |
| recuperacao | Recuperação |
| contrato | **Fechamento** (é pipeline, não receita) |
| ganho | **Ganhos** (só isto é venda) |
| perdido | Perdidos |

Chaves legadas: `abordagem_passiva`, `abordagem_ativa` e `painel` viraram SDR; `no_show` virou Recuperação.

## Passo 0. Trava de duplicação
Verifique se já existe o marcador `meus-produtos/dono-14/trafego/analise/diario/{AAAA-MM-DD de HOJE}.md`. Se existir, encerre imediatamente sem fazer nada (a leitura do dia já foi feita).

## Passo 1. Meta + VSL
Rode `py -3 scripts/dono14-diario.py` (lê o token do .env sozinho).

## Passo 2. Leads reais pelo banco (fonte de verdade)
Rode `py -3 scripts/dono14-banco.py` (consulta o Supabase DIRETO via chave no .env, sem depender de conector; devolve leads por dia, funil A/B, eventos dedup, nomes de ontem/hoje e stages do CRM). **Este é o caminho principal da madrugada.**
Se o script falhar (ex.: SUPABASE_SERVICE_KEY ausente ou erro de rede), tente a ferramenta `execute_sql` do Supabase (projeto `sizhdcrnfylimhsdfdnf`) com a consulta da skill `/dono14-diario`, SEMPRE com `count(distinct event_id)`. Se ambos falharem, siga com os números da Meta e marque em destaque: "RECONCILIAÇÃO COM O BANCO PENDENTE, conferir na sessão interativa".
Regra de leitura: leads reais = `contact_submissions`; atenção a ressubmissões (mesmo nome/telefone já existente conta como reengajamento, não lead novo).

## Como contar lead: CAPTAÇÃO é o número oficial (decidido pelo Rodrigo em 16/08/2026)

O `dono14-banco.py` devolve duas contagens por dia. Use cada uma no seu lugar:

- **CAPTAÇÃO** (coluna `CAPTACAO`): cadastros que a mídia entregou. **Inclui ressubmissão**, porque o anúncio pagou por aquele preenchimento e o reengajamento tem valor real. **Exclui falso e spam** (lista em `meus-produtos/dono-14/trafego/cadastros-falsos.json`). **É o número oficial: manda no CPL real, na régua, no gatilho de escala e na série `leads_banco` do contexto.**
- **lead_novo**: pessoas únicas no dia. Serve para projeção comercial e CAC, e para dizer quantas pessoas novas entraram no funil. Nunca usar para CPL.

Quando os dois diferirem, diga isso no marcador em uma linha, sem tratar como problema. Exemplo real de 15/08: captação 3, pessoas novas 2, porque o Lúcio (lead de 02/08, hoje em Fechamento) preencheu de novo e o Rodrigo unificou. CPL do dia é R$ 61,11 pela captação, não R$ 91,67.

**Evento órfão não é divergência.** O `dono14-banco.py` agora tem a coluna `orfaos`: eventos em `lead_events` sem lead correspondente em `contact_submissions`, casados por prefixo de hash do e-mail. Isso acontece quando o Rodrigo apaga um cadastro falso ou unifica dois cadastros do mesmo lead e remove o duplicado: a linha sai da tabela de leads, o evento fica. **Não abrir investigação, não pedir consulta extra, não registrar como pendência.** Basta escrever no marcador, em uma linha, quantos órfãos houve e a causa. O número oficial é sempre `leads_banco`. Casos conhecidos: 10/08 (cadastro falso do João Silva) e 15/08 (unificação do Lúcio).

**Cadastro falso não conta como lead.** Quando o Rodrigo identifica um, ele apaga do banco, e a partir daí os scripts já param de contar sozinhos. O que NÃO se corrige sozinho é a série `leads_banco` do `.contexto.json`, que guarda o número do dia em que o falso ainda existia. Se o total do `.contexto.json` divergir do que o `dono14-banco.py` devolve, **o banco vence**: corrija o dia no contexto e registre a correção no marcador. Casos já tratados: Bryan (23/07) e João Silva (10/08, apagado em 11/08, o dia caiu de 3 para 2 leads).

## Reentrada herda o criativo do PRIMEIRO cadastro (descoberto em 18/09/2026)
O site grava o `utm_content` pelo cookie de atribuicao, que guarda o primeiro toque por 90 dias. Quem ja tinha cadastro e volta por outro anuncio fica creditado ao criativo ANTIGO, mesmo que ele nem esteja no ar. Em 17/09 isso fez o A47 aparecer com 1 lead (CPL R$ 114) quando teve 3 (CPL R$ 38).

A correcao fica em `meus-produtos/dono-14/trafego/reatribuicoes.json`, que os scripts de analise por criativo ja leem sozinhos. **Em toda leitura, conferir:** algum lead do dia fechado foi creditado a um criativo que NAO entregou impressao no dia? Se sim, registrar em AVISOS EM DESTAQUE com nome, criativo gravado e os criativos que tiveram lead na Meta naquele dia. **Nao incluir na lista pela madrugada**: a inclusao exige prova (quebra horaria da Meta ou um unico criativo com lead no dia) e e feita na sessao interativa.

**Reentrada nao e cadastro falso.** Nao chamar de suspeito quem ja tinha cadastro anterior, mesmo com faturamento declarado estranho.

## Passo 2b. Comercial detalhado (venda, valor e pipeline)
Rode `py -3 scripts/dono14-comercial.py` (autorizado na allowlist desde 08/08). Ele traz cada card com stage, valor de contrato, tags e os motivos de perda.

**Regra dura de contagem, não confie na linha pronta do script:** a linha "Vendas com tag 'Dono 14%'" conta TODO card que carrega a tag, incluindo perdidos e em negociação, e por isso infla a receita. **Venda confirmada é somente `stage=ganho`.** Some você mesmo o `valor` dos cards em `ganho` para chegar na receita real. Cards em `contrato` são pipeline, nunca receita.

Registre no marcador: quantas vendas em ganho, a receita somada, e o pipeline em contrato (valor e nomes). Se o número de ganhos mudou desde a leitura anterior, isso é o fato mais importante do dia e vai no topo do resumo, com nome e valor.

## Passo 2c. Orçamento real da conta
Rode `py -3 scripts/dono14-orcamento.py`. Ele devolve o orçamento diário dos conjuntos ATIVOS e compara com o plano combinado.

**Use esse número para julgar o gasto do dia**, nunca o plano de memória. E **nunca mais escreva "não foi possível confirmar o orçamento via API"**: esse aviso falso se repetiu de 24 a 27/08 porque a chamada era feita inline e barrada pelo detector do terminal. O script resolve isso. Se ele próprio falhar, aí sim registre o erro real que apareceu.

## Vigia da conversao de visita em cadastro (aberto em 07/09/2026)

Calcular sempre, no relatorio e no marcador: **cadastros do banco / visitas (landing_page_view) da semana**. A base historica, de 27/07 a 30/08, e **11,7%** (86 cadastros em 732 visitas).

A semana de 31/08 a 06/09 fechou em **6,8%** (10 em 146). Isso fica a 1,84 sigma da base, ou seja, 3,3% de chance de ser so acaso. **Nao e prova, e suspeita.** A pagina `/sessao` nao e alterada desde 10/08 (conferido no repositorio) e foi testada ao vivo em 07/09: dobra correta, CTA apontando para `/sessao-cadastro`, formulario com os 4 campos, sem erro de console. O mix de trafego (idade, genero, aparelho) tambem nao mudou.

**Regra:** se a semana seguinte (07/09 a 13/09) fechar **abaixo de 9%**, sao duas semanas seguidas fora da faixa e a suspeita vira caso a investigar a fundo, com AVISO EM DESTAQUE. Se voltar para a casa dos 11%, foi oscilacao e o vigia se encerra, registrando isso.

**Nao tratar a taxa de UM dia como sinal.** Com 20 visitas por dia, um dia de 5% e um dia de 15% sao ambos normais. So a semana fechada tem tamanho para julgar.

## CPL de perfil: a régua de topo adotada em 24/09/2026

A partir de 24/09/2026 (decisão do Rodrigo), todo julgamento de criativo usa uma **escada de três degraus**, nesta ordem. Nunca pular degrau e nunca declarar vencedor pelo primeiro sozinho.

1. **CPL de perfil** julga o TOPO. Gasto do criativo dividido só pelos cadastros que declararam de **R$ 100 mil a R$ 1 milhão** de faturamento. Régua: 💚 abaixo de R$ 120 · 🟢 R$ 120 a 170 · 🟡 R$ 170 a 260 · 🔴 acima de R$ 260.
2. **Sessão sobre cadastro de perfil** julga o MEIO. Foi onde o A47 (67%) se separou do A48 (0%).
3. **CAC real** julga o FUNDO, e segue sendo o único juiz de venda.

**Por que existe.** Das 9 vendas, as 5 com formulário preenchido declararam R$ 130 mil ou mais. Das Sessões agendadas, 38 vieram de quem declarou R$ 100 mil ou mais e só 4 de baixo disso.

**O que ela NÃO faz.** O A40 fechou com 65% de perfil, CPL de perfil de R$ 89 (o melhor da conta) e 17 Sessões, e não vendeu nada. Ela não separa quem compra. Nunca usar sozinha.

**Higiene obrigatória (sem isso o número mente):**
- Cadastro falso não conta (`cadastros-falsos.json`; os falsos já saem de `contact_submissions`, o arquivo cobre o evento que sobra).
- Reentrada conta no criativo CORRIGIDO (`reatribuicoes.json`), nunca no gravado.
- Faturamento declarado **acima de R$ 1 milhão não entra como perfil** até o SDR confirmar. Já apareceu duas vezes em cadastro aleatório (R$ 5.154.000 em 25/08 e R$ 5.000.000 da Edvirgens em 20/09, os dois em perdido).

**Base mínima para veredito: 5 cadastros de perfil** (cerca de R$ 700 gastos). Abaixo disso o script marca "sem veredito" e a leitura reporta o número sem concluir.

A régua oficial está em `meus-produtos/dono-14/trafego/reguas-criativos.md` e o cálculo já sai pronto no `dono14-analise-profunda.py`. **Ler do arquivo, nunca de memória.**

## Marco de 09/10/2026: Pixel e LP novos, monitorar antes x depois

Em 09/10/2026 o Rodrigo publicou mudanca no **Pixel** e na **LP /sessao**. A foto do ANTES esta em `meus-produtos/dono-14/trafego/site/baseline-09-10-antes.json` (ler sempre de la, nunca de memoria). Regras a partir desta data:

1. **09/10 e dia de transicao.** Reportar os numeros, sem veredito, sem acionar recuo de ancora nem gatilho por causa dele.
2. **FEITO em 11/10 (sessão interativa):** a foto do depois está gravada em `pagina_depois` do baseline. Pixel igual (223799232011558), Lead para todo cadastro, `dcal_attr_last` NÃO subiu. Não repetir esta conferência; só reabrir se a página mudar de novo.
2-antigo. **Primeira leitura depois do deploy (10/10 ou a primeira em que a pagina mudou):** conferir na /sessao ao vivo se `last_modified` mudou, qual e o `pixel_id` (antes 223799232011558), quais eventos `fbq` o HTML dispara (antes so PageView e ViewContent) e se existe `dcal_attr_last`. Gravar o DEPOIS no mesmo arquivo de baseline, campo `pagina_depois`. Se nao der para abrir a pagina na rotina, deixar a pendencia explicita para a sessao interativa.
3. **Se o pixel_id mudou,** a serie de PageView/ViewContent/Lead do pixel recomeca do zero: nao comparar com a janela anterior e avisar que a serie do dashboard quebrou ali.
4. **Comparacao oficial: 7 dias fechados depois (10 a 16/10) contra 7 antes (02 a 08/10).** Tres numeros: conversao de visita em cadastro (antes 7%, faixa saudavel 8% a 15%), taxa de perfil dos cadastros (antes 42%) e Lead do Pixel contra cadastros do banco no mesmo dia (antes o Pixel contava em dobro). Antes de 7 dias, so reportar; veredito so em 17/10.
5. **Recuo de ancora nesse periodo:** a regua de 3 dias de volume foi calibrada para a pagina antiga; com pagina nova, sinalizar mas rotular como "regua em recalibracao", sem pedir acao.
6. **Dia zerado logo depois do deploy** pode ser pagina quebrada, nao criativo: conferir Clarity (dead/rage click na /sessao e /sessao-cadastro) e o formulario antes de concluir qualquer coisa.

## Passo 3. Clarity
Rode `py -3 scripts/dono14-clarity.py` (Data Export API direto, token no .env; devolve sessões, scroll médio, tempo ativo e dead/rage clicks por URL do último dia). **UMA execução só: a API aceita no máximo 10 chamadas/dia.** Use o resultado para o placar de engajamento das páginas da Sessão.

**Como ler o scroll (mudou em 12/08/2026):** a dobra da `/sessao` foi revisada e publicada pelo Rodrigo, e o CTA principal agora nasce DENTRO da primeira tela do celular (y=388 num viewport de 812). Antes ele ficava em y=872, fora da tela. Portanto **scroll baixo deixou de ser sintoma de "não chega ao botão"**: a pessoa pode converter sem rolar. Reportar o número, sim; tratar 13% ou 15% como problema automático, não. E **não cobrar mais a revisão da dobra como pendência**, ela está feita.
Se o script falhar (token ausente/erro), tente as ferramentas MCP do Clarity se disponíveis; senão, anote "Clarity pendente". Gravações de sessão (jornadas individuais) não saem pela API: ficam para a sessão interativa da manhã, quando necessário.

## Passo 4. Atualizar o contexto
Atualize `meus-produtos/dono-14/trafego/analise/diario/.contexto.json`:
- **NUNCA trunque o mapa `leads_banco`**: ele guarda a série completa desde 09/06. Apenas acrescente o dia FECHADO novo. Não grave o dia corrente parcial na série (regra do dia fechado).
- Leads reais = banco. Exclusões conhecidas: a submissão falsa de 23/07 (Bryan) conta 0.
- Atualize `comercial` com os stages do CRM (venda = só stage ganho).
- Escreva `consideracoes` com julgamento, respeitando o plano vigente (atualizado em 10/08/2026):
  - **ATUALIZAÇÃO 09/10/2026 (vale acima de tudo o que está abaixo): A50 e A51 em teste de 7 dias, de 10/10 00h01 a 16/10 23h59.** Um anúncio por conjunto, R$ 60/dia cada, mesma configuração do A47 (Brasil, 25 a 55, Público Advantage+ desligado, Feed e Reels). Conta em **R$ 280/dia** de 10/10 a 16/10 (A39 R$ 100 + A47 R$ 60 + A50 R$ 60 + A51 R$ 60) e de volta a R$ 160 em 17/10. Já está no `PLANO_POR_DATA`; não alarmar divergência. **Todo teste de criativo dura 7 dias (decisão do Rodrigo): não propor estender nem tirar a data de fim.** Avisar na leitura de 15/10 que os dois vencem em 16/10, e fechar o veredito na leitura de 17/10.
  - **Régua do teste do A50 e do A51:** no dia 7, vermelho em duas ou mais métricas de topo (CTR abaixo de 1%, CPC acima de R$ 15, custo por visita acima de R$ 23) reprova. Fora isso, ler o perfil: metade ou mais dos cadastros com R$ 100 mil ou mais, custo por lead de perfil até R$ 170 e pelo menos 1 Sessão agendada. Com menos de 5 cadastros de perfil, reportar o número e dizer que é sinal, não veredito. O A50 tem 80 segundos (acima do teto de 60), com pílula "DONO DE RESTAURANTE" na tela nos 3 primeiros segundos, "fatura R$ 160.000 por mês" aos 9,1s como descrição do caso e o filtro direto aos 71,7s; o A51 tem 49 segundos e fala o filtro direto aos 10,3s e de novo aos 27,1s.
  - **Regime de eventos novo desde 09/10/2026 às 12h14:** o Lead voltou a disparar em TODO cadastro (R$ 15.000 acima da régua, R$ 931,12 abaixo), e quem passa da régua dispara também `LeadMentoria`. Portanto `eventos_dedup` de Lead **volta a bater com a captação do dia**, como era até 23/09. De 24/09 a 08/10 a diferença era esperada (Lead só para o perfil) e não deve ser reaberta. Se a partir de 10/10 não bater, aí sim registrar em AVISOS EM DESTAQUE. **Não comparar o custo por lead da Meta de antes e depois de 09/10: a régua do que conta como Lead mudou.**
  - **Página /sessao desde 09/10/2026 às 12h42:** o filtro de R$ 100 mil saiu da caixa do botão e virou frase discreta abaixo dele. É marco novo do funil: a conversão de visita em cadastro de 30/09 a 09/10 (caixa dourada, cerca de 6%) não serve de base para o que vem depois.
  - **PLANO VIGENTE desde 05/09/2026: RODIZIO DE 4 CRIATIVOS a R$ 60/dia cada, total R$ 240/dia.** A39 (baixado de R$ 140 para R$ 60), A42, A43 e A44. Decisao do Rodrigo: recuperar volume de lead e achar o proximo campeao, porque o A39 sozinho nao sustenta o funil. A43 e A44 comecam em 06/09 00h01. Conferir sempre pelo `dono14-orcamento.py`, nunca de memoria.
  - **ATUALIZACAO 18/09/2026 (decisao do Rodrigo, teto de caixa R$ 200/dia):** o conjunto do A47 ficou so com o A47, **R$ 100/dia e SEM data de fim** (A48 e A49 pausados dentro dele). O A39 caiu para **R$ 40/dia**. O A48 e o A49 foram para conjuntos proprios, em **teste sequencial a R$ 60/dia**: **A48 de 19/09 00h01 a 25/09 23h59**, **A49 de 26/09 00h01 a 02/10 23h59**. Programado: R$ 140 em 18/09, R$ 200 de 19/09 a 02/10, R$ 140 a partir de 03/10. Tudo isso esta no `PLANO_POR_DATA`; nao alarmar divergencia.
  - **Regua de corte do teste sequencial:** com cerca de 20 visitas (3 a 4 dias), conversao de visita em cadastro de 8% ou mais segue; abaixo disso, sinalizar para o Rodrigo. **Nao julgar venda dentro da janela.** Avisar na leitura de 24/09 que o A48 vence em 25/09, e na de 01/10 que o A49 vence em 02/10.
  - **Motivo de manter o A39 no ar:** e o unico criativo com venda comprovada (4 contratos, R$ 67.600). O A47 tem o melhor comeco da historia da conta (CPL R$ 31 e 21% de conversao em 17 e 18/09), mas ainda sem venda. Lembrar do A40: CPL mais barato da conta e zero venda.
  - **ATUALIZACAO 17/09/2026: entraram A47, A48 e A49, os tres criativos gerados a partir do briefing de 12/09.** Estao num conjunto unico, "A47+A48+A49 - Frio Adv+ 25-55 - Feed+Reels", R$ 100/dia, inicio 17/09 00h01, **fim 23/09 23h59**. O A39 subiu para R$ 100/dia. O A40 saiu. **Conta em R$ 200/dia.** Nao tratar A47, A48 ou A49 como desconhecidos. Temas: A47 (62s) "Ele compra todo dia e nao sabe quanto gasta"; A48 (80s) "Cada corte que voce faz tira um cliente", a consequencia no dono; A49 (67s) "Ele achava que tinha 12% de lucro. Eram 2%". Janela de teste de 7 dias fecha em 23/09. **Avisar na leitura de 22/09** que o conjunto vence no dia seguinte.
  - **Pipeline com card manual:** desde 15/09 o comercial cria card direto no CRM, sem `submission_id` (Luna Octavia Moura Vilao, Renato Viana Junior, Flavia, Diego Sousa). Esses cards nao vieram do formulario da midia paga. O `dono14-comercial.py` so nomeia card com valor preenchido e o `pipeline.py` usa o campo `nome` do proprio card: sempre identificar o pipeline pelo `crm_cards.nome`, nunca reportar "card sem nome".
  - **ATUALIZACAO 12/09/2026: o conjunto Lookalike foi LIGADO pelo Rodrigo e comeca em 13/09 00h01.** R$ 90/dia, publicos "Morno - LL 1% - VV 50% - 180D" e "Morno - LL 1% - Site - Dono14 + Sessao - 180D" (a pendencia do semelhante da origem quente foi resolvida). Anuncios A40, A39 e A43. **O A44 NAO esta nesse conjunto**, entao ele sai do ar por completo quando o conjunto proprio dele vencer em 12/09 23h59.
  - **Conjunto que ainda nao comecou nao conta no programado do dia.** A API devolve `effective_status: ACTIVE` para conjunto com `start_time` no futuro, e isso inflou o programado em R$ 90 em 12/09, gerando alarme falso. O `dono14-orcamento.py` foi corrigido em 12/09 para ler `start_time` e `end_time` e listar esses conjuntos a parte. **O plano agora e por data** (`PLANO_POR_DATA` no script): 11/09 R$ 300, 13/09 R$ 270, 17/09 R$ 210, 18/09 R$ 150. Confiar no que o script devolve e nao alarmar divergencia sem conferir a data.
  - **ATUALIZACAO 11/09/2026: o A46 e do Rodrigo, e e um teste de duracao do A45.** Criado por ele em 10/09 as 15h15, inicio 11/09 00h01, fim 17/09 23h59, R$ 60/dia. Mesmo tema do A45 ("O melhor mes do ano, e 58% sem lucro"), mas outro video: **A46 tem 57 segundos, A45 tem 94**, com segundo titulo e texto diferentes. Nao e duplicata e nao e conjunto desconhecido. Na leitura, comparar os dois lado a lado como teste de duracao.
  - **Conta em R$ 300/dia desde 11/09:** A39 + A43 + A44 + A45 + A46, R$ 60 cada. `PLANO_ATUAL` = 300.
  - **Conjunto de lookalike criado em 11/09 (outra sessao, decisao do Rodrigo por VOLUME):** "LAL 1% VV50 + Site - Frio 25-55 - Feed+Reels", R$ 90/dia, inicio programado 13/09 00h01, anuncios A40, A39 e A43, PAUSADO ate o Rodrigo ligar. Ver a memoria dono14-volume-para-sdr-novo-e-lal: nao re-litigar o A40 nem a semente; julgar esse conjunto por volume e CPL, separando os leads dele pelo `utm_term` (nome do conjunto).
  - **Esperado a partir de 13/09:** A43 e A44 vencem em 12/09 23h59. Se o LAL for ligado, programado = **R$ 270/dia** (A39 + A45 + A46 + LAL). Se nao for ligado, **R$ 180/dia**. Qualquer um dos dois e plano conhecido: reportar o valor, sem alarme de conjunto desconhecido.
  - **ATUALIZACAO 10/09/2026: o A45 entrou e ocupou a vaga do A42.** Subiu em 10/09 00h01, R$ 60/dia, com fim programado em 16/09 23h59. O A42 venceu o cronograma em 08/09 23h59 e parou de entregar de fato (zero gasto e zero impressao em 09/09 em diante). **Conta em R$ 240/dia: A39 + A43 + A44 + A45.** Nao tratar o A45 como conjunto desconhecido nem como divergencia.
  - **Conjunto com cronograma vencido nao conta no programado.** A API continua devolvendo `effective_status: ACTIVE` para conjunto cujo `end_time` ja passou, e isso gerou alarme falso de "R$ 300/dia divergente" em 10/09. O `dono14-orcamento.py` foi corrigido em 10/09 para ler o `end_time` e tirar esses conjuntos da soma, listando-os a parte. Confiar no que o script devolve.
  - **Fim programado dos conjuntos novos:** A42 termina em 08/09 23h59, A43 e A44 em 12/09 23h59. Sem acao do Rodrigo, o programado cai sozinho para R$ 180/dia em 09/09 e para R$ 60/dia (so o A39) em 13/09. **Avisar com um dia de antecedencia**, na leitura de 08/09 e na de 12/09.
  - **Janela de teste dos criativos novos (A42, A43, A44): 7 dias cheios, sem veredito antes.** A R$ 60/dia, cada um acumula cerca de R$ 420 na janela, o que da poucas unidades de lead. Isso basta para julgar topo e ponte (CTR, CPC, CPV, connect) e para pegar CPL extremo, mas **nao basta para julgar venda**. Nao declarar criativo vencedor nem perdedor por numero de fechamento nessa janela.
  - **Nao chamar o A39 de criativo saturado.** A frequencia dele ficou entre 1,05 e 1,16 por sete semanas e o CTR semanal nao caiu (1,33% na primeira semana, 1,45% na ultima). O que subiu foi o CPL: R$ 83 nas quatro primeiras semanas contra R$ 132 nas tres ultimas. Reportar como encarecimento do lead, nao como fadiga de criativo.
  - **SÓ A DUPLA ÂNCORA, A39 + A40, a R$ 100/dia cada. Programado: R$ 200/dia.** Aplicado pelo Rodrigo em 11/08 às 09h24 (subiu de R$ 85), confirmado no registro de atividades da conta. Não comparar com R$ 204 nem com R$ 230, que são planos antigos.
  - **A41 foi PAUSADO em 11/08 às 09h23**, ao fim dos 7 dias de teste (04/08 a 10/08). Fechou com 3 leads reais, CPL real R$ 139, 1 sessão e nenhum fechamento. Não citar como campanha zerada nem cobrar decisão sobre ele: está encerrado. A cauda de atribuição dele pode pingar por alguns dias.
  - **PLANO VIGENTE desde 31/08 (aplicado pelo Rodrigo às 09h58 e 09h59, conferido no registro da conta): SÓ O A39, a R$ 120/dia. O A40 foi PAUSADO.** Fecha o mês com 48 leads, 11 sessões e ZERO venda, contra 3 vendas e R$ 51.000 do A39.
  - **O A42 entra em 01/09.** Criativo novo, sem histórico: os primeiros dias não têm base de comparação. Trate como janela de teste, do mesmo jeito que foi o A41 (7 dias cheios antes de veredito), e **não dispare régua de recuo sobre ele antes disso**. Quando ele subir, o programado passa a ser R$ 120 mais o que for definido para o A42; confirme sempre pelo `dono14-orcamento.py`, nunca de memória.
  - **Degrau de R$ 100 para R$ 120 no A39 em 31/08.** Os dias 31/08 e 01/09 são transição: reportar números, sem veredito sobre o criativo.
  - **A cauda de atribuição do A40 ainda pode pingar** por alguns dias depois da pausa. Lead atribuído a ele agora é resíduo, não entrega nova.
  - **PLANO NOVO desde 24/08 (decisão do Rodrigo): A39 e A40 a R$ 80/dia cada, total R$ 160/dia.** Ele baixou o orçamento para liberar caixa e foco no desenvolvimento de criativos novos. A41 segue pausado. **Confira o valor real na conta antes de comparar gasto com programado**: se ainda estiver em R$ 100, use R$ 200 e registre que a redução não foi aplicada.
  - **Com R$ 160/dia, o volume de leads cai junto, e isso é esperado, não é piora de criativo.** Proporcionalmente são cerca de 20% menos leads por dia. **Não tratar queda de volume como fadiga nem disparar régua de recuo por causa dela.** O que continua valendo é o CPL: se o custo por lead se mantiver na faixa verde com menos verba, o criativo está saudável.
  - **O gatilho de escala fica mais difícil de bater** (exige 3+ leads/dia) simplesmente porque há menos verba. Sinalize isso quando a contagem não avançar, em vez de sugerir que o funil piorou.
  - **Degrau para baixo também reabre aprendizado.** Os 2 primeiros dias após a redução (24 e 25/08) são transição: reportar os números, sem veredito sobre criativo.
  - **A decisão sobre o A40 foi substituída por esta.** Ele NÃO foi pausado: segue no ar com orçamento menor, enquanto o Rodrigo produz criativo novo. Não cobrar de novo a decisão de pausar.
  - **CONGELADO ATÉ DOMINGO 23/08 (decisão do Rodrigo em 18/08).** A janela de julgamento fechou em 17/08 com a dupla âncora APROVADA (16 leads, CPL médio R$ 63,92). O Rodrigo está em treinamento esta semana e não consegue gravar criativo novo, então **nada muda na conta até domingo**: A39 e A40 seguem a R$ 100/dia cada, A41 pausado.
    **Não cobrar decisão sobre o A40 nas leituras de 19 a 22/08.** Ele já sabe do quadro (30 leads, CPL R$ 55, 10 sessões e zero fechamento, CTR entrando no vermelho). Repetir isso todo dia é ruído. Reportar os números normalmente, sem pedir ação.
    **Na leitura de domingo 23/08**, trazer o balanço consolidado do A40 desde 11/08 (leads, CPL, sessões, fechamentos, CTR por semana) para ele decidir com o quadro fechado.
  - **Janela combinada: 11/08 a segunda-feira 17/08**, só com as duas âncoras. **Ler o resultado pela janela de 13 a 17**, descartando 11 e 12 como transição do degrau, porque mudança de orçamento reabre aprendizado. Dizer isso no relatório em vez de tratar 12/08 como veredito.
  - **Atenção ao efeito do degrau:** no dia em que o orçamento subiu (09/08), o gasto foi a R$ 296,52 e o CPL real saltou de R$ 44,58 para R$ 148,26. Um dia não prova, mas mexer em orçamento reabre aprendizado. Sempre olhar 2 ou 3 dias depois de um degrau antes de julgar o criativo.
  - **Gatilho de escala:** 3 dias seguidos com 3+ leads/dia e CPL real abaixo de R$ 70 (só sinalizar, nunca executar).
  - **Recuo de âncora:** 3 dias seguidos com CPL acima de R$ 100 ou CTR abaixo de 1%.
  - **Leitura por criativo vem do BANCO** (`utm_content`), não da atribuição da Meta. A atribuição da plataforma já errou quatro vezes nesta conta e em 08/08 apontou o A40 como vencedor quando o A39 é quem produziu a venda e os três contratos. Citar número da Meta só como contraste, sempre rotulado.
  - **CBO Vencedores foi desativada** e saiu do monitoramento. Não voltar a citá-la como campanha zerada.
- Atualize `linha_do_tempo` se houve fato relevante.

## Passo 5. Dashboard
Rode `py -3 scripts/dono14-dashboard.py`. NÃO abra o navegador (é madrugada, ninguém está olhando).

## Passo 5b. Análise profunda (DETERMINÍSTICA, por script)
Rode `py -3 scripts/dono14-analise-profunda.py`. O script gera `analise-profunda-leads-{AAAA-MM-DD}.html` sozinho, com dados REAIS da Meta em nível de anúncio (funil de vídeo por conjunto), leads do banco com CRM, régua semanal e a seção de considerações lida do `.contexto.json`.

**FORMATO PADRÃO, aprovado pelo Rodrigo em 08/08/2026.** O script já entrega tudo isto sozinho. Nunca gerar o HTML à mão e nunca aceitar versão sem estes itens:
1. Janela GLOBAL de cada criativo, da primeira aparição até o dia fechado (o ciclo comercial é mais longo que 7 dias).
2. Lupa comercial por criativo, com leads do banco casados por `utm_content`: leads reais, CPL real, sessões agendadas, fechamentos, **a divisão por produto em TRÊS linhas (Dono 14%, Projeto 14% e Painel do Dono) mais os sem classificação**, receita, CAC e ROAS. A separação dos três é obrigatória desde 22/09/2026: antes disso o script procurava só o número "14" solto e contava todo card de Projeto 14% como Dono 14%.
3. Colunas de freq e CPM na tabela, além de leads do banco e CPL real por período.
4. Filtro "Por dia" e "Por semana", com linha de TOTAL da vida do criativo.
5. **Análise do criativo fechando cada cartão** (texto determinístico: topo, retenção, ponte, lead, comercial, tendência e veredito pela régua). Substituiu o gráfico semanal, removido em 11/08 por decisão do Rodrigo.
6. Etapas do CRM com o nome do board, nunca a chave crua.

Se o arquivo sair sem algum desses blocos, registre em AVISOS EM DESTAQUE no marcador em vez de tentar remendar o HTML.
**Por isso a ORDEM importa: o Passo 4 (atualizar o .contexto.json com as considerações e o plano vigente) precisa vir ANTES deste passo**, porque o script publica esse texto no relatório.
Se o script falhar, registre o erro no marcador e NÃO tente recriar o HTML manualmente (as versões manuais da madrugada saíam com estimativas; o conserto é da manhã). Não abra no navegador.

## Passo 6. Marcador
**TRAVA: só execute este passo se o arquivo da análise profunda do Passo 5b já existir no disco. O marcador é o carimbo de "leitura concluída"; salvá-lo sem a análise profunda é entrega incompleta (aconteceu 2 vezes; não repita).**
Salve `meus-produtos/dono-14/trafego/analise/diario/{AAAA-MM-DD de HOJE}.md` com a leitura completa: placar do dia fechado, CPL real, tabela âncora x teste, Clarity (ou pendência), comercial, veredito e AVISOS EM DESTAQUE se houver algo crítico (gasto diário acima de R$ 200, CPL estourado, evento zerado com gasto alto, campanha que não deveria estar ativa). Caminhos de arquivo sempre absolutos e completos.

## Passo 7. Sincronizar o projeto com o repositório do Workshop
**Só execute depois do Passo 6.** A atualização vem por último de propósito: se algo der errado no repositório, a leitura do dia já está salva e entregue.

Rode `py -3 scripts/sincronizar-repo.py`. O script é determinístico e cuida de tudo sozinho: busca novidades do Workshop, guarda seu trabalho em aberto, junta, devolve o trabalho e espelha no fork pessoal.

**REGISTRO OBRIGATÓRIO, SEMPRE.** O marcador do dia precisa ter uma seção "Sincronização do projeto" com o resultado, **inclusive quando não houver novidade nenhuma**. Silêncio não é aceitável: sem a linha escrita, não há como saber se o passo rodou ou foi pulado (aconteceu em 08/08). O passo também entra numerado na lista "Passos executados", com o mesmo critério dos demais.

Como interpretar a saída e o que escrever:
- **"EM DIA"** (código 0): escreva "Sincronização: em dia, nenhuma novidade do Workshop."
- **"ATUALIZADO com sucesso"** (código 0): escreva "Sincronização: atualização recebida", listando os commits que chegaram (o script os imprime em "Chegando:").
- **"PARADO"** (código 2): houve conflito que exige decisão humana. O script já desfez tudo e devolveu o trabalho, então **nada foi perdido e nada ficou pela metade**. Registre em AVISOS EM DESTAQUE do marcador, nomeando os arquivos em conflito, e siga em frente.
- **Passo não executado por qualquer motivo:** escreva isso explicitamente no marcador, com o motivo.

**O script também faz BACKUP AUTOMÁTICO** (desde 10/08/2026): commita sozinho o que mudou em `scripts/`, `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, `.claude/skills/`, `.claude/settings.json`, `CLAUDE.md` e `ARQUITETURA.md`, e envia para o fork pessoal. Registre no marcador o que ele disser:
- **"BACKUP: N arquivo(s) salvos"**: escreva quantos e siga.
- **"BACKUP: nada novo para salvar"**: escreva isso mesmo.
- **"BACKUP ABORTADO: o conteúdo parece conter credencial"**: isso é grave. Vai em **AVISOS EM DESTAQUE**, dizendo que algum arquivo tem algo parecido com token escrito nele e que o backup do dia não aconteceu. Não tente contornar, não commite à mão, não edite o arquivo para "limpar". A conferência é do Rodrigo.

Nada fora dessa lista de pastas é commitado, de propósito, para lixo de terminal e arquivo temporário nunca entrarem no repositório.

**Proibido tentar resolver o conflito na madrugada.** Sem o Rodrigo para escolher entre as duas versões, a decisão não é sua. A única resolução automática permitida é a do `.gitignore` (união dos dois blocos), e ela já está dentro do script.

Nunca use `git reset`, `git checkout --`, `git clean`, rebase ou push forçado, nem aqui nem em nenhum outro passo.

## Regras absolutas
- Esta rotina é SOMENTE LEITURA na conta Meta. Proibido criar, pausar, ativar ou alterar qualquer campanha, conjunto, anúncio ou orçamento. Mudanças são decisão do Rodrigo, no chat, durante o dia.
- Português brasileiro com acentuação correta. Proibido travessão.
- Nunca exibir tokens.
- Se um passo falhar, siga para o próximo e registre a falha no marcador; o objetivo é o Rodrigo acordar com o máximo de leitura possível e a lista clara do que ficou pendente.

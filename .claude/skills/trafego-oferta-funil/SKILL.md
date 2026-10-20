---
name: trafego-oferta-funil
description: >
  Diagnóstico pós-clique, leitura de página e análise de oferta para Meta Ads, a partir dos números
  do funil. Preenche a lacuna que as outras skills apontam mas não resolvem: "o problema é na página,
  mas não sei o que está errado lá." 6 sub-skills: leitura pós-clique (funil por etapa via
  /trafego-insights), leitura da página (Claude in Chrome primeiro, WebFetch depois, ou texto colado),
  congruência anúncio x página, diagnóstico de oferta (nota de 0 a 100 cruzada com a conversão, usando
  o Quadro e a Furadeira reais do resumo-produto.md), diagnóstico de checkout (eventos da Meta,
  sem backend) e plano de correção do funil. Upsell e downsell opcionais. Nunca executa ação na conta,
  nunca modifica páginas e não substitui a auditoria de copy: as correções vão para /feedback-pagina,
  /feedback-low-ticket, /pagina-checkout, /pagina-ajuste, /pagina-performance, /copy-pagina e
  /lt-pagina. Use quando o aluno pedir "por que minha página não converte?", "o anúncio e a página
  estão alinhados?", "a oferta é forte?", "checkout está quebrando?", "o problema é no tráfego ou na
  página?", ou quando /trafego-otimizar, /trafego-criativos ou /trafego-diagnostico identificarem
  gargalo fora do Meta.
---

# Tráfego Oferta Funil. Diagnóstico Pós-Clique e Leitura de Página

Você é um consultor de oferta e funil que protege o dinheiro do aluno. Seu papel é descobrir se o problema está no tráfego ou na página/oferta, ler a página real, comparar com o anúncio e apontar onde a oferta falha. Você **não executa ação na conta Meta** e **não modifica páginas**.

**Posicionamento no ecossistema:**
- `/trafego-otimizar` detecta gargalo "página/checkout" e encaminha para esta skill.
- `/trafego-criativos` detecta `falha_pos_clique` e encaminha para esta skill.
- `/trafego-diagnostico` classifica a hipótese `oferta_funil` e encaminha para esta skill.
- `/trafego-oferta-funil` é o que vem **depois**: lê a página real e diz onde o funil quebra, **a partir dos números**.
- As **correções** saem de outras skills: `/feedback-pagina` e `/feedback-low-ticket` (auditoria completa de copy, estrutura e design), `/copy-pagina` e `/lt-pagina` (refazer a copy), `/pagina-ajuste` (ajuste pontual numa página do Severino), `/pagina-performance` (velocidade) e `/pagina-checkout` (ligação com o checkout).

**Regra de ouro:** esta skill diagnostica, não gera copy nova nem modifica páginas. Aponta problemas e recomenda testes. A nota da oferta (seção 6 e sub-skill `diagnostico-oferta.md`) é uma leitura estrutural cruzada com a conversão, **não** a auditoria de copy: essa é do `/feedback-pagina` (ou do `/feedback-low-ticket`, em página low ticket).

---

## 🔌 Passo 0. Contexto, conexão e entrevista de entrada

O fluxo de entrada segue o **padrão compartilhado** da `.claude/skills/trafego-diagnostico/SKILL.md`, Passos 0.1 a 0.9 (qualquer mudança nele deve ser feita nas três skills de investigação), com o escopo da `/trafego-criativos` e dois passos próprios (URL e upsell). Uma pergunta por mensagem, com opções numeradas.

### 0.1. Produto ativo e resumo do produto
Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (gerar conforme o CLAUDE.md se não existir). Guardar sem perguntar:
- **Ticket** (Preço) e **tipo** (Low, Middle ou High Ticket): definem a faixa de benchmark (seção 3.5) e a skill de correção (low ticket vai para `/feedback-low-ticket` e `/lt-pagina`).
- **Quadro e Furadeira literais:** a promessa e o mecanismo que a página deveria mostrar (seção 6).
- **Objeções principais, Urgências Ocultas, Decorados e público:** para avaliar FAQ, dor atacada, prova e para quem a página fala.

### 0.2. Conexão Meta
Ler `META_AUTH_MODO` (`grep "^META_AUTH_MODO=" .env | cut -d= -f2-`). Vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP` (inclusive o legado `HIBRIDO`): acionar `/trafego-conexao` e aguardar, sem adivinhar nem cair em fallback. `MCP_CONECTOR`: confirmar tool terminada em `ads_get_ad_entities` e que `FB_AD_ACCOUNT_ID` tem valor (`grep -q "^FB_AD_ACCOUNT_ID=." .env`; se faltar, a opção "Validar" do `/trafego-conexao` completa). Conta não liberada no conector: avisar e oferecer o modo App pelo `/trafego-conexao`. `APP`: confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` têm valor com `grep -q "^NOME=." .env` (o ponto faz a linha vazia contar como ausente). Skill 100% leitura, sem bloco 🛡️.

### 0.3. Selecionar conta
Mesma lógica das demais skills.

### 0.4 e 0.5. Filtros de status e de objetivo
Iguais aos da `/trafego-diagnostico`. No objetivo, as opções aqui são só 1 (vendas), 2 (captação) e 3 (vendas + captação, recomendado): campanha sem conversão não tem funil pós-clique para diagnosticar.

### 0.55. Escopo
```
Quer analisar toda a conta ou campanhas específicas?

1. Conta completa
2. Campanhas específicas

Digite o número:
```

### 0.6 a 0.9. Produtos, meta, mapeamento, margem e período
Iguais aos da `/trafego-diagnostico`: o produto ativo vem do resumo; só se pergunta se há outros produtos na conta, a meta de CPA/CPL, a confirmação do mapeamento campanhas → produtos, a margem (exatamente 3 taxas: plataforma, reembolso e imposto, ou pular) e o período (7d, 14d ou 30d, com o anterior calculado automaticamente).

### 0.95. URL da página de vendas

```
Qual é o endereço (URL) da sua página de vendas principal?
(ex: https://seusite.com.br/oferta)

Se tiver mais de uma página, me diga a principal agora.
As outras eu descubro pelos anúncios.
```

Se o aluno não souber, a skill extrai o link do criativo pela API (seção 4.1). Se a página foi criada no Severino, a versão local em `meus-produtos/{ativo}/entregas/paginas/` serve só de apoio: o diagnóstico vale para a página que está no ar (o link do anúncio).

### 0.97. Upsell e downsell (opcional)

```
Depois da compra, você oferece algum upsell ou downsell?
(uma segunda oferta que só quem já comprou enxerga)

1. Tenho upsell e/ou downsell, vou passar os links
2. Não tenho (pular)

Digite o número:
```

Se **1:** pedir as URLs, uma por mensagem (qual é o upsell, qual é o downsell). Seguir para a leitura na seção 4.6.
Se **2** (ou se o produto não tem): pular sem insistir. **Ausência de upsell/downsell não é problema, é escolha de modelo.** Não penalizar o diagnóstico, não tentar adivinhar.

---

## 1. Menu principal

```
╔══════════════════════════════════════════════════════════════╗
║  TRÁFEGO OFERTA FUNIL. Diagnóstico Pós-Clique e Página       ║
╚══════════════════════════════════════════════════════════════╝

Qual análise de oferta e funil você quer rodar?

[1]  DIAGNÓSTICO COMPLETO        roda os 6 módulos e consolida
                                 (pós-clique → página → congruência →
                                  oferta → checkout → plano)

[2]  LEITURA PÓS-CLIQUE          onde o funil quebra? (métricas)

[3]  LEITURA DA PÁGINA           o que tem na página?

[4]  CONGRUÊNCIA ANÚNCIO-PÁGINA  anúncio e página estão alinhados?

[5]  DIAGNÓSTICO DE OFERTA       a oferta é forte? (nota de 0 a 100)

[6]  DIAGNÓSTICO DE CHECKOUT     a etapa final funciona?

[7]  PLANO DE CORREÇÃO           que teste fazer na página agora?

Digite o número:
```

### Entradas por linguagem natural

| O que o aluno diz | Módulo acionado |
|-------------------|-----------------|
| "por que minha página não converte?" | Diagnóstico completo |
| "o problema é no tráfego ou na página?" | Leitura pós-clique + diagnóstico de oferta |
| "o anúncio e a página estão alinhados?" | Congruência anúncio-página |
| "a oferta é forte?" | Diagnóstico de oferta |
| "checkout está quebrando?" | Diagnóstico de checkout |
| "o que testar na página?" | Plano de correção |
| "CTR bom mas CPA ruim" | Leitura pós-clique + congruência |

---

## 2. Fluxo do Diagnóstico Completo (opção 1)

```
🔍 Próximo passo: rodar o diagnóstico completo de oferta e funil (6 módulos). Tempo estimado: 3 a 5 minutos.

⏳ Passo 1/7: funil pós-clique.
⏳ Passo 2/7: leitura da página de vendas.
⏳ Passo 3/7: comparação do anúncio com a página.
⏳ Passo 4/7: força da oferta.
⏳ Passo 5/7: checkout.
⏳ Passo 6/7: plano de correção.
⏳ Passo 7/7: consolidação do relatório.
```

**Inteligência cruzada:**
- Se o pós-clique mostra connect rate abaixo de 70%: a leitura da página busca sinais de problema técnico (abaixo de 70%, a primeira hipótese é técnica; régua na seção 3.5).
- Se a congruência é baixa: o diagnóstico de oferta recebe o alerta "desalinhamento com o anúncio".
- Se o checkout mostra fricção: o plano prioriza o briefing de checkout.
- Se a página tem nota alta mas as métricas são ruins: o problema pode ser preço, público ou checkout, não a página.

---

## 3. Dados via `/trafego-insights`

Consumir `funil_por_campanha()`, as métricas derivadas e a `serie_diaria`. NÃO duplicar.

**Funil completo: SEMPRE tentar puxar antes de declarar limitação.** O funil pós-clique (visita à página, carrinho, checkout iniciado, compra) é o coração desta skill. A disponibilidade depende do modo de conexão:

| Modo (`META_AUTH_MODO`) | Como puxar o funil | Limitação real |
|---|---|---|
| `APP` | Graph API (`curl` em `.../insights?fields=actions`, `v25.0`, token mascarado na tela). O array `actions` traz `landing_page_view`, `add_to_cart`, `initiate_checkout`, `purchase`, `omni_landing_page_view`. **Funil 100% disponível.** | Nenhuma; só faltam os dados do gateway (cartão recusado, Pix) |
| `MCP_CONECTOR` | Pedir no `ads_get_ad_entities` os campos de funil conferidos na conta real: `link_click`, `landing_page_view`, `omni_initiated_checkout` e `omni_purchase` (lista completa abaixo). Visita à página, checkout iniciado e compra saem direto deles. Carrinho (`add_to_cart` ou equivalente omni) só entra depois de confirmar com `ads_get_field_context`. | Métrica sem evento volta `null`: a conta não registra aquele evento. Só para a visita ou o checkout que faltar, seguir para a alternativa abaixo (o carrinho tem regra própria, logo depois dela) |

**Quando o MCP não trouxer visita ou checkout** (campo `null`):
1. **Leitura guiada no Gerenciador de Anúncios** (sem mexer em nada da conta). Passo a passo para o aluno:
   1. Abrir o Gerenciador de Anúncios e selecionar as campanhas do escopo.
   2. Ajustar o período para o mesmo da análise.
   3. Clicar em "Colunas" → "Personalizar colunas".
   4. Marcar "Visualizações da página de destino", "Adições ao carrinho", "Finalizações de compra iniciadas" e "Compras".
   5. Aplicar e mandar os números aqui (ou um print da tabela).

   Se a coluna de visitas à página ou de checkout iniciado também vier vazia no Gerenciador (ou a de compras, havendo venda no período na Hotmart ou na Kiwify), o pixel não registra esse evento: encaminhar para `/trafego-pixel`. Carrinho vazio é comum em checkout de plataforma (Hotmart, Kiwify) e não indica pixel com defeito.
2. Se o aluno preferir seguir sem esses números: usar CPA/ROAS como substitutos, **declarando** que o funil está incompleto (impressões → cliques → [lacuna] → conversões).

**Carrinho fora do gatilho:** carrinho não confirmado no `ads_get_field_context` (ou `null`) não abre a alternativa acima. O funil segue visita à página → checkout iniciado → compra, com uma linha dizendo ao aluno que o carrinho não veio pelo conector e que, se ele quiser, dá para ler a coluna "Adições ao carrinho" no Gerenciador.

Limitação do conector nunca vira troca para o modo App: o App é só para conta que a Meta ainda não liberou no conector (Passo 0.2).

**Campos no `ads_get_ad_entities` (contrato do conector: `.claude/skills/trafego-insights/SKILL.md` §10.1 "Contrato do conector da Meta (MCP)", conferido na conta real em 09/10/2026):** `amount_spent` (não `spend`), `impressions`, `reach`, `link_click`, `landing_page_view`, `omni_initiated_checkout`, `omni_purchase`, `offsite_conversion_fb_pixel_purchase_values` (sem ele, valor = `purchase_roas × amount_spent`), `purchase_roas`, `results`, `name`, `effective_status`, `campaign_id` e `adset_id`. Métrica sem evento volta `null`. CTR de link, CPM e frequência saem da conta: `link_click ÷ impressions`, `amount_spent ÷ impressions × 1000` e `impressions ÷ reach`. Não pedir `actions`, `action_values` nem `inline_link_clicks` crus: estão fora do contrato (a forma conferida é `link_click` e os campos `omni_*`). Carrinho e qualquer outro campo de ação: confirmar com `ads_get_field_context` antes.

**Métricas derivadas do funil completo:** connect rate = visitas à página ÷ cliques no link; conversão da página = compras ÷ visitas; taxa de checkout = checkout iniciado ÷ visitas; conclusão de checkout = compras ÷ checkout iniciado.

---

## 3.5 Benchmark de conversão por faixa de ticket

> Régua de mercado para dizer se a conversão está boa ou ruim. **A conversão cai conforme o ticket sobe** (lei verificada em fontes independentes: Firework, Baymard, Lucky Orange). Selecionar a faixa pelo **ticket do resumo do produto** (Passo 0.1) ou, em multi-produto, pelo ticket de cada produto. Contexto das faixas: tráfego frio de rede social, infoproduto, Brasil. Apresentar SEMPRE com a etiqueta de confiança ao lado do número. Mostrar no output final só a faixa do aluno, não as cinco.
>
> **Régua única do Severino para a conclusão de checkout** (compras ÷ checkouts iniciados): a `/trafego-otimizar`, a `/trafego-analise` e as demais skills apontam para esta tabela em vez de usar um limiar fixo. Crítico (fricção provável) só abaixo da metade do piso da faixa (sub-skill `diagnostico-checkout.md`).

**Fases sensíveis ao preço** (a régua muda por faixa):

| Faixa de ticket | Conversão da página (visita → compra) | Conclusão de checkout (checkout iniciado → compra) |
|---|---|---|
| até R$ 297 (impulso) | 1,5% a 4% | 25% a 45% |
| até R$ 500 | 1% a 2,5% | 18% a 35% |
| até R$ 1.000 | 0,7% a 1,8% | 12% a 25% |
| até R$ 2.500 (alto) | 0,4% a 1,2% | 7% a 18% |
| acima de R$ 2.500 | 0,3% a 1% | 5% a 15% |

**Confiança por número (obrigatório exibir):**
- Conversão da página: 🟢 **alta nas pontas** (low e high ticket ancorados em fonte direta: abaixo de US$ 50 = 3% a 5%, high ticket acima de US$ 1.000 = 0,5% a 1,5%), 🟡 **baixa a média no meio** (R$ 500 e R$ 1.000 são interpolação, sem fonte direta).
- Conclusão de checkout: 🔴 **estimativa em todas as faixas.** Só a direção (cai com o preço) e o teto da faixa alta (luxo conclui cerca de 18% a 22%, Baymard) têm lastro. Os percentuais exatos são extrapolação. **Nunca apresentar como dado fechado.**

**Fases NÃO sensíveis ao preço** (régua fixa, porque a pessoa ainda não viu o preço quando clica e quando a página carrega):
- CTR no link: campanhas de venda no Meta, cerca de 1,4%; e-commerce, 1,5% a 3%.
- Connect rate (visitas à página ÷ cliques no link): saudável 80% ou mais, atenção de 60% a 79%, crítico abaixo de 60%. Abaixo de 70%, a primeira hipótese é técnica (página lenta, link errado, redirecionamento): conferir com `/pagina-performance` e a congruência anúncio-página antes de mexer no anúncio.

**Ressalva obrigatória do checkout (sempre exibir junto do número):** o evento `initiate_checkout` da Hotmart e da Kiwify pode disparar mais "solto" que o "adicionar ao carrinho" dos estudos de e-commerce. Se conta mais gente na entrada, a conclusão de checkout do aluno fica artificialmente baixa contra o benchmark. Tratar a comparação de checkout como aproximação, nunca como prova de checkout quebrado.

**Como usar:** colocar a faixa do ticket do aluno ao lado dos números reais dele. Quando a conversão da página estiver abaixo da faixa mas houver campanhas com zero venda no conjunto, declarar que é "média envenenada" (distribuição), não necessariamente página ruim.

Fontes: Firework, Fetchfunnel, Baymard, Lucky Orange, LanderLab, HeroSpark (low ticket Brasil).

---

## 4. Fluxo de leitura da página

### 4.1. Obter a URL da página

Ordem de prioridade:
1. URL informada pelo aluno no Passo 0.95.
2. Extrair do criativo (só leitura):
   - `MCP_CONECTOR`: `ads_get_creatives` (ou o campo de criativo do `ads_get_ad_entities`, confirmado com `ads_get_field_context`).
   - `APP`: `curl -g` em `/{ad_id}?fields=creative{id,object_story_spec,asset_feed_spec,call_to_action_type}`.
   - Criativo clássico: `object_story_spec.link_data.link`. Advantage+: `asset_feed_spec.link_urls[0].website_url`.

### 4.2. Ler a página (regra 10 do CLAUDE.md)

Ordem fixa, sem pedir nada ao aluno:
1. **Claude in Chrome** (`read_page`): renderiza a página completa, inclusive o que carrega por JavaScript.
2. **Se o Claude in Chrome não estiver disponível** (ferramenta ausente ou erro de conexão): `WebFetch` da URL.
3. Nunca travar a conversa pedindo para "conectar o Chrome" ou "instalar algo". Simplesmente usar a alternativa e seguir.

**Esta skill não mexe em configuração.** Não edita o `settings.local.json`, não adiciona domínio a lista de permissões e não muda nenhuma configuração permanente. Se o Claude Code pedir autorização para ler o domínio, é a janela de permissão do próprio Claude Code, e quem decide é o aluno.

Com o conteúdo em mãos, extrair os elementos conforme a sub-skill `leitura-pagina.md`.

### 4.3. Alternativa quando a leitura falha

Se as duas leituras falharem (página só em JavaScript sem o Chrome, página com senha, erro, HTML vazio):
```
Não consegui ler a página automaticamente (pode ser uma página
que carrega por JavaScript ou que exige login).

Você pode me ajudar de 2 formas:

1. Abrir a página no navegador, selecionar todo o texto (Ctrl+A),
   copiar e colar aqui
2. Descrever os principais elementos: headline, promessa,
   garantia, preço, CTA

Digite o número:
```

### 4.4. Deduplicação de URLs

Se vários anúncios apontam para a mesma URL: ler a página uma vez só. Somar as métricas dos anúncios que usam essa URL.

Se o mesmo produto tem URLs diferentes: listar e analisar cada uma separadamente. Oferecer comparação.

### 4.5. Leitura de upsell/downsell e estimativa de take rate

Só roda se o aluno informou links no Passo 0.97. As páginas de upsell/downsell são pós-compra: **só quem comprou as enxerga.** Isso muda a leitura: não é tráfego frio, é base 100% qualificada.

**Passo a passo:**
1. Ler cada URL na mesma ordem da seção 4.2 (Claude in Chrome, depois WebFetch), com a mesma alternativa da 4.3 se falhar (página protegida, JavaScript, texto colado).
2. Ler a oferta da página (mesmos elementos do diagnóstico de oferta: promessa, mecanismo, preço, CTA). Avaliar se o upsell **complementa** a oferta principal ou **compete** com ela.

**Estimativa de take rate (quantos compradores aceitam a segunda oferta):**
- Take rate = compras do upsell ÷ compras da oferta principal. Quem chega na página de upsell é exatamente quem comprou, então o denominador é o total de compras da principal.
- **Só dá para calcular pelo Meta se o upsell tiver evento próprio distinguível:** conversão personalizada separada, ou produto/pixel separado. Como achar e contar, por modo:
  - `APP`: listar com `GET /act_<id>/customconversions` e contar, no array `actions` dos insights, a entrada `offsite_conversion.custom.<id>` (`curl -g`, token só por substituição dentro do comando, mascarado na tela).
  - `MCP_CONECTOR`: listar com `ads_get_customconversions`. Depois, conferir com `ads_get_field_context` se o `ads_get_ad_entities` aceita um campo de ação para essa conversão (por exemplo `actions:offsite_conversion.custom.<id>`). Nunca pedir `actions` cru (seção 3). Se o campo não existir, marcar `fonte_take_rate: "indisponivel_no_mcp"` e usar o relatório da Hotmart ou da Kiwify.
- **Se o upsell dispara o MESMO evento `purchase` da principal, o Meta não separa as duas compras.** Nesse caso, declarar: "o take rate real só sai do relatório da plataforma (Hotmart, Kiwify); o pixel não distingue." **Nunca inventar o número.**

**Benchmark de take rate (verificado em fonte, com etiqueta de confiança):**

| Oferta | Onde aparece | Take rate de mercado | Confiança |
|---|---|---|---|
| Order bump | no checkout, 1 clique | 15% a 37% (saudável 15% a 25%; bem configurado até cerca de 38%, Statista/Hotmart) | 🟢 média a alta |
| Upsell pós-compra | página depois do pagamento | 3% a 15% (típico 3% a 8%; bem otimizado 8% a 15%) | 🟢 média a alta |
| Downsell | depois do upsell recusado | 2% a 8% (sempre abaixo do upsell; preço 40% a 60% menor que ele) | 🟡 média |

**Cuidado com os nomes (o aluno costuma misturar):** *order bump* fica no checkout (preço baixo, 1 clique, taxa alta); *upsell pós-compra* é a página que só o comprador vê depois de pagar (taxa bem menor). Os links que o aluno passa no Passo 0.97 normalmente são upsell/downsell pós-compra, não order bump. Saúde do upsell pós-compra: abaixo de 2% = algo errado; 3% a 8% = típico; acima de 8% = bem otimizado.

Fontes: Focus Digital, CartHook, Growth Suite, Hotmart (order bump), Ensinio.

**Quando o produto não tem upsell/downsell:** pular limpo. Ausência não penaliza o diagnóstico.

---

## 5. Texto do anúncio via API

Para a congruência anúncio-página, buscar o texto do anúncio (só leitura):
- `MCP_CONECTOR`: `ads_get_creatives` (opcional: `ads_get_ad_preview` para ver a prévia).
- `APP`: `curl -g` em `/{ad_id}?fields=creative{id,name,object_story_spec,asset_feed_spec,call_to_action_type}`.

| Campo lógico | Criativo clássico | Advantage+ |
|-------------|-------------------|------------|
| Texto principal | `object_story_spec.link_data.message` | `asset_feed_spec.bodies[0].text` |
| Headline | `object_story_spec.link_data.name` | `asset_feed_spec.titles[0].text` |
| Descrição | `object_story_spec.link_data.description` | `asset_feed_spec.descriptions[0].text` |
| Link | `object_story_spec.link_data.link` | `asset_feed_spec.link_urls[0].website_url` |
| CTA | `call_to_action_type` | `call_to_action_type` |

**Quando o criativo é vídeo sem transcrição:** declarar "congruência avaliada apenas com os campos de texto do anúncio. O vídeo pode ter promessas adicionais não analisadas." Reduzir a confiança.

---

## 6. Integração VTSD no diagnóstico de oferta

A régua é o produto real do aluno, lido do `resumo-produto.md`, nunca um exemplo genérico:

| Elemento da página | Conceito VTSD | Pergunta de avaliação |
|--------------------|---------------|----------------------|
| Headline / promessa | Quadro na Parede | A promessa da página é o **Quadro registrado no resumo** (literal ou fiel a ele)? O aluno se vê naquele quadro? |
| Mecanismo único | Furadeira | A página apresenta a **Furadeira do resumo** (nome do método e macroetapas)? Está claro que é ela que entrega o Quadro? |
| Prova social | Decorados | Os depoimentos mostram a transformação e os Decorados (o que mudou na vida), não só elogio ao material? |
| Urgência/escassez | Urgência Oculta | A urgência está ligada a uma Urgência Oculta real do resumo (o custo de não agir), ou é "últimas vagas" genérico? |
| CTA | Identidade do Consumidor | O CTA fala com o público do resumo, na linguagem dele? |
| FAQ | Objeções principais | O FAQ responde às 5 objeções principais do resumo? |
| Bônus | Caixa Rápido | Os bônus entregam resultado rápido e resolvem objeções específicas, ou são empilhamento genérico? |

**Esta tabela não é a auditoria de copy.** Ela mede se a página carrega o produto que foi concebido e cruza isso com os números. Revisão frase a frase, Light Copy, estrutura 8D e design são do `/feedback-pagina` (ou do `/feedback-low-ticket`).

---

## 7. Urgência do funil

| Nível | Critério |
|-------|----------|
| `critica` | 0 conversões com gasto alto. Página quebrada ou oferta completamente desalinhada. |
| `alta` | Connect rate abaixo de 60% OU conversão da página abaixo de 0,5% com volume. Dinheiro queimando no clique. (Nota: a `/trafego-otimizar` usa 70% como limiar de gargalo técnico; aqui, 60% é o limiar de urgência alta.) |
| `media` | Conversão abaixo do benchmark, mas não crítica. Congruência parcial. |
| `baixa` | Funil funcional, oportunidade de melhoria. Nota da oferta de 60 a 79. |
| `monitorar` | Funil saudável. Nota da oferta 80 ou mais. |

> Os limiares de conversão da página acima são o piso geral. Para julgar de fato se a conversão está baixa, cruzar com a faixa do ticket (seção 3.5): 0,5% pode ser ruim para ticket baixo e normal para ticket alto. O limiar fixo é o piso; o benchmark por faixa é a régua fina.

---

## 8. Confiança da análise

| Fator | Efeito |
|-------|--------|
| Página lida pelo Claude in Chrome (renderizada) | + confiança |
| Página lida pelo WebFetch (HTML completo) | + confiança, com a ressalva de JavaScript |
| Leitura falhou e o aluno colou o conteúdo | confiança média |
| Página só com VSL (pouco texto) | confiança baixa para a oferta |
| Funil pós-clique completo (visita + checkout + compra; carrinho quando vier) | + confiança |
| MCP sem campo de visita ou de checkout, e sem leitura guiada | confiança baixa para o funil |
| Criativo em vídeo sem transcrição | confiança baixa para a congruência |
| Menos de 7 dias ou menos de 100 visitas à página | confiança baixa |

---

## 9. Anti-padrões

| Conclusão proibida | Por que está errada | Forma correta |
|--------------------|---------------------|---------------|
| "A página é ruim porque o CPA é alto" | CPA alto pode ser criativo, público ou leilão | Cruzar: CTR e visitas boas + conversão da página baixa = aí sim, provável causa na página |
| "A página carrega devagar porque o connect rate é baixo" | Pode ser redirecionamento, link errado, celular | "Connect rate baixo SUGERE possível problema de carregamento ou redirecionamento" |
| "O ROAS da Meta prova que a oferta funciona" | Atribuição não é lucro real | Qualificar como "ROAS atribuído" |
| "Essa página não converte porque não tem VSL" | Página sem vídeo pode converter bem | Avaliar pelos elementos que ela TEM |
| "Vi a página, sei tudo sobre a oferta" | A leitura não assiste vídeo e o WebFetch não roda JavaScript | Declarar as limitações explicitamente |
| "O checkout está quebrando por cartão recusado" | Sem dados do gateway | "Possível fricção final. Conferir na plataforma (Hotmart, Kiwify)." |
| "A nota da oferta é a revisão da página" | A nota é leitura estrutural cruzada com números | Auditoria completa de copy no `/feedback-pagina` ou `/feedback-low-ticket` |

---

## 10. Limitações declaradas (sempre no output)

- "Análise baseada no HTML público." Quando a leitura foi pelo WebFetch: "Elementos carregados por JavaScript podem não estar visíveis."
- "Sem dados de velocidade de carregamento. Connect rate baixo SUGERE, não confirma." (Velocidade de verdade: `/pagina-performance`.)
- "Tenho o evento de checkout iniciado (pixel), então meço a TAXA de conclusão de checkout (compras ÷ checkout iniciado). Mas sem dados do gateway (cartão, Pix, boleto) não confirmo a CAUSA do abandono. A taxa é dado; a causa é hipótese."
- "ROAS é atribuído pela Meta, não é lucro real."
- Quando há VSL: "A página contém vídeo. A análise cobre os elementos de texto, não o conteúdo do vídeo."
- Quando há vídeo no anúncio: "Congruência avaliada com os campos de texto do anúncio."
- Páginas protegidas (login, área de membros, obrigado): "Não consigo acessar. Descreva manualmente."

---

## 11. Estrutura do relatório humano (7 seções)

```
1. CONTEXTO RESUMIDO
   Período, escopo, URL(s) analisada(s), nível de confiança, limitações.

2. DIAGNÓSTICO REAL
   O que os dados + a página dizem.
   O que NÃO dizem (sem backend, sem JavaScript, sem vídeo).
   Erro comum a evitar.

3. HIPÓTESE CENTRAL
   Onde o funil provavelmente quebra (pós-clique, página, oferta ou checkout).

4. ALAVANCAS DE MAIOR IMPACTO
   Prioridade: página > oferta > congruência > checkout > orçamento.

5. RISCOS E ARMADILHAS
   Onde dá para perder dinheiro.
   Onde os dados podem enganar.

6. TESTES INTELIGENTES
   Testes de página rápidos e baratos.
   Cada teste com hipótese, critério de sucesso, critério de morte.

7. DECISÃO RECOMENDADA
   O que fazer agora na página (e com qual skill do Severino).
   O que NÃO fazer (não mexer no tráfego se o problema é na página).
   O que fazer SOMENTE SE.
```

**Inclusões obrigatórias no relatório (sincronizadas com as sub-skills):**
- Benchmark da faixa de ticket ao lado das taxas reais, com etiqueta de confiança (seção 3.5).
- Justificativa elemento por elemento da nota da oferta, em tabela `Elemento | Nota | Por que essa nota` (seção 12).
- Checkout julgado pela faixa do ticket, com a ressalva da Hotmart e da Kiwify, nunca por um limiar fixo de 30%.
- Quando houver upsell/downsell, o take rate (quando o upsell tem evento próprio) ou o aviso de que ele só sai do relatório da Hotmart ou da Kiwify (seção 4.5 e sub-skill `upsell-downsell.md`).

---

## 12. Explicação obrigatória (regra dura)

Todo número, gráfico, nota e achado DEVE ter texto explicativo em linguagem natural. Gráfico sem explicação é proibido.

**Caso específico, o gráfico de notas da oferta (seção 6):** o gráfico de barras com as notas dos elementos (Promessa, Mecanismo, Prova social, Garantia, Bônus, CTA, Urgência, Preço) NUNCA aparece sozinho. Ele vem **sempre** acompanhado da leitura **elemento por elemento**, em quadro próprio (tabela ou lista) logo abaixo ou ao lado, respondendo para cada nota: **por que essa nota e o que tirou pontos.** Nota sem justificativa não comunica nada: a pessoa não sabe o que é "Furadeira" nem por que tirou 80. Formato recomendado: tabela `Elemento | Nota | Por que essa nota`. Fechar o quadro com o lembrete de método: as notas cobrem só o que foi lido da página (texto), não o vídeo/VSL; e é leitura estrutural, não a auditoria de copy (que é do `/feedback-pagina`). Vale no chat e no export HTML.

---

## 13. Handoffs

### Da oferta-funil para outras skills

| Situação | Handoff para |
|----------|-------------|
| Página de vendas (middle ou high ticket) com problema de copy, estrutura ou prova | `/feedback-pagina` (auditoria completa e correção) |
| Página low ticket com problema de copy, estrutura ou design | `/feedback-low-ticket` |
| Copy da página precisa ser refeita do zero | `/copy-pagina` (vendas 8D) ou `/lt-pagina` (low ticket) |
| Ajuste pontual numa página criada no Severino (headline, bloco, CTA) | `/pagina-ajuste` |
| Connect rate baixo ou página lenta | `/pagina-performance` |
| Checkout: link, plataforma ou passagem da página para o pagamento | `/pagina-checkout` |
| Pixel sem disparar compra ou checkout | `/trafego-pixel` (diagnóstico) e `/pagina-pixel` (instalação) |
| Problema confirmado no criativo (não na página) | `/trafego-criativos` |
| Criativo com falha que precisa de ação na conta | `/trafego-otimizar` |
| Funil saudável e oferta forte | `/trafego-diagnostico` (falso vencedor) e depois `/trafego-escalar` |

### De outras skills para a oferta-funil

| Skill | Momento | Handoff |
|-------|---------|---------|
| `/trafego-otimizar` | Gargalo técnico, página ou checkout | `/trafego-oferta-funil` |
| `/trafego-criativos` | `falha_pos_clique` | `/trafego-oferta-funil` |
| `/trafego-diagnostico` | Hipótese `oferta_funil` | `/trafego-oferta-funil` |

---

## 14. Histórico de análises

Registrar no `meus-produtos/{ativo}/entregas/trafego/oferta-funil/INDEX.md` (formato: `| YYYY-MM-DD HH:MM | modulo | act_<id> | URL | nota da oferta | urgencia | [link](arquivo.html) |`; sem export, a última coluna fica `chat`). Comparar com a análise anterior quando houver (nota da oferta, urgência, etapa de quebra).

---

## 15. Export HTML

Ao final de qualquer módulo, oferecer o export. Reutiliza o design system da `/trafego-analise` e o `.claude/skills/trafego-analise/scripts/trafego_chart_geom.py`, no tema escolhido pelo aluno (Escuro, Terra ou Claro Neutro: pergunta com opções na primeira vez, depois `EXPORT_TEMA` do `.env`, conforme a seção 1 do `.claude/skills/trafego-analise/sub-skills/_export-html.md`). Salva em `meus-produtos/{ativo}/entregas/trafego/oferta-funil/`.

### 15.1. Abrir no navegador (OBRIGATÓRIO)

> Depois de gravar o arquivo HTML, **escrever o arquivo e mostrar o link não conclui o export.** É obrigatório abrir o arquivo no navegador padrão do aluno antes de declarar "concluído". Mesma mecânica da `/trafego-analise` e da `/trafego-otimizar`.

Sequência obrigatória depois de gravar o HTML (e depois de o checklist de conformidade passar):

1. Montar o caminho absoluto: `{RAIZ_PROJETO}/meus-produtos/{ativo}/entregas/trafego/oferta-funil/{slug}-{timestamp}.html`.
2. Abrir no navegador padrão com o script compartilhado do projeto, com o interpretador detectado na sessão (`{PY}` = `python3` ou `py -3`):
   ```
   {PY} "{RAIZ_PROJETO}/scripts/abrir-html.py" "{caminho-absoluto}"
   ```
   O próprio script tenta os comandos nativos de cada sistema e, se nada funcionar, imprime a instrução de abertura manual.
3. **Sempre** devolver o caminho absoluto no chat, com o navegador aberto ou não.

---

## 16. Princípios que esta skill nunca viola

1. **Nunca executar ação na conta Meta.** Diagnóstico + recomendação.
2. **Nunca modificar páginas nem configurações.** Aponta o que está errado, não reescreve. Não edita `settings.local.json`.
3. **Nunca gerar copy nova.** Diagnosticar não é gerar. A correção vai para `/feedback-pagina`, `/feedback-low-ticket`, `/copy-pagina`, `/lt-pagina` ou `/pagina-ajuste`.
4. **Nunca afirmar causa de checkout sem dados do gateway.** Só "possível fricção".
5. **Nunca tratar o ROAS da Meta como lucro real.**
6. **Sempre declarar limitações.** Leitura da página, VSL, JavaScript, backend.
7. **Dados pós-clique via `/trafego-insights`.** Nunca duplicar.
8. **Comparação temporal obrigatória.** Funil atual vs anterior.
9. **Explicação obrigatória em todo output.**
10. **Uma pergunta por mensagem nas perguntas iniciais.** E nunca perguntar o que o resumo do produto já tem.
11. **Margem: 3 campos, nunca mais.** Taxa da plataforma + reembolso + imposto.
12. **Connect rate baixo não prova página lenta.** Pode ser redirecionamento, link errado, celular.
13. **Quadro e Furadeira reais.** A régua da oferta é o que está no `resumo-produto.md`, nunca um exemplo genérico.
14. **Nota da oferta não é auditoria de copy.** É leitura estrutural cruzada com os números; a auditoria completa é do `/feedback-pagina`.

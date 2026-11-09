# Sub-skill. Diagnóstico Criativo

Cruza atenção + intenção + conversão + consistência para identificar **onde exatamente** cada criativo quebra. Diferente do Fadiga Map do output [3] (que mede fadiga com score 0-5), esta sub-skill faz diagnóstico em 4 camadas com 7 veredictos possíveis.

## Contexto multi-produto

Roda **por produto**. Cada produto tem benchmarks diferentes (Hook Rate aceitável para high ticket ≠ low ticket).

## Quando é acionado

- Opção [5] do menu principal
- Automaticamente na Inteligência Completa (quarto módulo)
- Quando o aluno pergunta "onde exatamente o criativo quebra?"

## Dados necessários

Todas as métricas dos módulos 1-3 + adicionais:
- `serie_diaria` das métricas-norte (CPA/CPL) via `/trafego-insights`
- `frequency` por anúncio
- `created_time` dos ads (para idade do criativo)
- Mínimo 7 dias de dados e 1.000 impressões por criativo para diagnóstico confiável

## Diagnóstico em 4 camadas

Para cada criativo, avaliar 4 camadas em sequência:

| Camada | O que avalia | Métricas | OK se... | FAIL se... |
|--------|-------------|----------|----------|-----------|
| 1. Atenção | Captura e sustenta? | Hook Rate, Hold Rate | Hook ≥ 25% E Hold ≥ 35% | Hook < 15% OU Hold < 30% |
| 2. Intenção | Gera ação? | CTR, Click-to-LPV Rate | CTR ≥ benchmark E LPV Rate ≥ 80% | CTR < benchmark × 0.7 OU LPV Rate < 60% |
| 3. Conversão | Gera venda/lead? | CPA, ROAS, Purchase Rate | CPA ≤ target × 1.3 | CPA > target × 1.5 |
| 4. Consistência | Sustenta no tempo? | CV diário, tendência, frequência | CV < 0.40 E freq < 3.0 E tendência estável | CV > 0.60 OU freq > 4.0 OU tendência piorando |

**Nota sobre zona cinza:** valores entre OK e FAIL (ex: Hook 15-24%, Hold 30-34%, LPV 60-79%) são `zona_cinza`. Não diagnosticar como FAIL nem como OK. Marcar a camada como "atenção" com ressalva.

**Visita à página baixa começa pela página:** o LPV Rate (Click-to-LPV) é a mesma conta do connect rate (visitas à página ÷ cliques no link). Abaixo de 70%, a primeira hipótese é técnica (página lenta, link errado, redirecionamento): conferir com `/pagina-performance` e a congruência com `/trafego-oferta-funil` antes de mexer no anúncio. Só depois de descartar a causa técnica, ler como curiosidade vazia do criativo.

**Referência de thresholds:** esses limiares são os de diagnóstico. As faixas do Hook Rate (crítico abaixo de 15%, atenção de 15% a 25%, saudável 25% ou mais) e do LPV Rate (saudável 80% ou mais, atenção de 60% a 79%, crítico abaixo de 60%) são as mesmas de todas as skills de tráfego do Severino. Os perfis da `leitura-atencao.md` usam limiares de classificação (mais granulares). A `dna-criativo.md` deriva thresholds dos dados reais da conta (podem ser mais altos ou mais baixos). Os do diagnóstico são o padrão geral.

**Zona cinza** (entre OK e FAIL): marcar como `atencao` e incluir ressalva.

## Os 7 diagnósticos possíveis

| Diagnóstico | Padrão | Onde quebra | Ação |
|------------|--------|------------|------|
| `falha_gancho` | Camada 1 FAIL no hook (Hook Rate < 15%) | Primeiros segundos | Testar novo gancho. Manter corpo e CTA. |
| `falha_sustentacao` | Camada 1 FAIL no hold (Hook OK, Hold < 30%) | Meio do vídeo | Reescrever desenvolvimento. Gancho funciona. |
| `falha_intencao` | Camadas 1 OK, Camada 2 FAIL (CTR baixo ou LPV baixo) | Transição atenção → clique | Se CTR baixo: fortalecer CTA e urgência. Se CTR alto + LPV baixo: primeiro conferir a causa técnica (página lenta, link errado, redirecionamento) com `/pagina-performance` e a congruência com `/trafego-oferta-funil`, sem mexer no anúncio; descartada a causa técnica, é curiosidade vazia: alinhar promessa com destino em `/copy-anuncio`. |
| `falha_qualificacao` | Camadas 1-2 OK, Camada 3 FAIL com CTR e LPV bons | Tráfego qualificado chega mas não compra | Problema pode ser oferta, preço, prova ou checkout. Testar CTA mais direto ou âncora de preço no criativo. |
| `falha_pos_clique` | Camadas 1-2 OK, Camada 3 FAIL com Offer Rate muito baixo (< 2%) | Página/checkout, NÃO o criativo | NÃO pausar criativo. Rodar `/trafego-oferta-funil` para ler a página e diagnosticar a oferta. |
| `criativo_equilibrado` | 4 camadas OK | Nenhuma (candidato a escala) | Criar variações. Para escalar: `/trafego-diagnostico` (falso vencedor e score) e depois `/trafego-escalar`. |
| `dados_insuficientes` | < 1.000 impressões OU < 7 dias OU < 3 conversões | N/A | Aguardar mais dados. |

## Árvore de prioridade entre veredictos

Quando múltiplas camadas falham simultaneamente, aplicar esta ordem de prioridade (o primeiro match vence):

1. **`dados_insuficientes`**: sempre prevalece. Se não há dados, não diagnosticar.
2. **`falha_gancho`**: se Camada 1 FAIL no hook, parar aqui. Sem atenção, avaliar intenção e conversão é irrelevante.
3. **`falha_sustentacao`**: se hook OK mas hold FAIL, parar. O público não chega ao CTA.
4. **`falha_intencao`**: se atenção OK mas Camada 2 FAIL (CTR ou LPV baixos). Inclui curiosidade vazia (CTR alto + LPV baixo), que só vale depois de descartar a causa técnica da página (LPV abaixo de 70%: `/pagina-performance` e `/trafego-oferta-funil` primeiro).
5. **`falha_pos_clique`**: se atenção e intenção OK, conversão FAIL **e** Offer Rate < 2% (problema fora do criativo: página, checkout, oferta). Prevalece sobre falha_qualificacao quando Offer Rate é muito baixo.
6. **`falha_qualificacao`**: se atenção e intenção OK, conversão FAIL com tráfego qualificado (LPV bom) **e** Offer Rate ≥ 2% (o tráfego chega e demonstra algum interesse, mas não fecha).
7. **`criativo_equilibrado`**: só quando TODAS as 4 camadas estão OK.

**Regra:** nunca atribuir dois veredictos ao mesmo criativo. O primeiro match na árvore é o veredicto final. Se houver falha menor em outra camada, mencionar como "ressalva" no relatório, não como segundo diagnóstico.

---

## Score de confiança por criativo

Adaptado da lógica da `/trafego-diagnostico`:

| Variável | 0 pts | 5 pts | 10 pts |
|----------|-------|-------|--------|
| Impressões | < 1.000 | 1.000-10.000 | > 10.000 |
| Conversões | 0-2 | 3-10 | > 10 |
| Dias com dado | 1-3 | 4-6 | 7+ |
| CV diário CPA | > 0.60 | 0.30-0.60 | < 0.30 |
| Frequência | > 4.0 | 2.0-4.0 | < 2.0 |

Score = soma (0 a 50). Faixas: alta (40+), média (25-39), baixa (10-24), insuficiente (0-9).

## Explicação obrigatória

Cada diagnóstico DEVE ter explicação completa:

```
AD "Polêmica - 15s": FALHA DE INTENÇÃO (visita à página baixa) ⚠️

O que está acontecendo: esse criativo captura atenção (Hook 35%)
e gera muitos cliques (CTR 2.8%), mas o Click-to-LPV Rate é
apenas 38%: a maioria dos cliques não chega na página. E quem
chega não compra (CPA R$ 280, quase 2× a meta).

Onde quebra: entre o clique e a chegada à página. Com 38% de
visita (abaixo de 70%), a primeira hipótese é técnica: página
lenta, link errado ou redirecionamento.

Por que provavelmente é isso: primeiro, a causa técnica. Se a
página estiver em ordem, a leitura passa a ser curiosidade
vazia: a promessa "descubra o segredo" atrai curiosos, não
compradores. O clique é de "quero saber", não de "quero comprar".

O que NÃO fazer: não escalar pelo CTR alto. Não pausar sem
testar variação (o gancho é forte).

O que fazer: primeiro, descartar a causa técnica. Com 38% de
visita, conferir se a página carrega rápido e se o link e o
redirecionamento estão certos (/pagina-performance) e se a página
continua a promessa do anúncio (/trafego-oferta-funil), sem mexer
no anúncio. Com a página em ordem, testar variação da promessa
mais conectada ao Quadro do produto. Em vez de "descubra o
segredo", uma premissa concreta com resultado e prazo reais
(nada inventado), escrita em /copy-anuncio.

Confiança: 38/50 (média). Para subir: +5 conversões e +3 dias.
```

## Output YAML

```yaml
diagnostico_criativo:
  produto: "Produto A"
  total_analisados: 8

  criativos:
    - ad_id: "<id>"
      ad_name: "<nome>"
      formato: video | imagem
      camadas:
        atencao: OK | FAIL | zona_cinza
        intencao: OK | FAIL | zona_cinza
        conversao: OK | FAIL | zona_cinza
        consistencia: OK | FAIL | zona_cinza
      diagnostico: falha_gancho | falha_sustentacao | falha_intencao | falha_qualificacao | falha_pos_clique | criativo_equilibrado | dados_insuficientes
      score_confianca: 38
      faixa_confianca: alta | media | baixa | insuficiente
      acao_recomendada: "<texto>"
      nao_fazer: "<texto>"
```

## Tratamento sem vídeo (imagem only)

Quando o criativo é imagem estática:
- Camada 1 (Atenção): avaliada apenas por CTR e CPC como proxies. Hook Rate, Hold Rate → `nao_aplicavel_formato_imagem`. FAIL se CTR < benchmark × 0.5. OK se CTR ≥ benchmark.
- Camada 2 (Intenção): funciona normalmente (Click-to-LPV independe de formato).
- Camada 3 (Conversão): funciona normalmente.
- Camada 4 (Consistência): funciona normalmente.
- Declarar no output: "Diagnóstico de atenção limitado a CTR/CPC (sem dados de retenção de vídeo)."

Veredictos possíveis para imagem: `falha_intencao`, `falha_qualificacao`, `falha_pos_clique`, `criativo_equilibrado`, `dados_insuficientes`. Os veredictos `falha_gancho` e `falha_sustentacao` são exclusivos de vídeo (dependem de Hook/Hold).

**Imagem com atenção reprovada:** em imagem, camada 1 FAIL (CTR < benchmark × 0.5) entra na posição 2 da árvore (no lugar de `falha_gancho`) e vira `falha_intencao` com o texto "a imagem não para a rolagem: CTR {X}%, menos da metade do benchmark". Ação: nova peça em `/criativo-estatico`, mantendo a oferta. Nesse caso, não usar a frase "captura atenção" do template (variante de imagem no template de `falha_intencao`).

## Templates de explicação por veredicto

Cada veredicto DEVE usar o template correspondente:

### falha_gancho
```
{nome}: FALHA NO GANCHO

O que está acontecendo: o público não para de scrollar nos
primeiros 3 segundos. Hook Rate de {X}% (saudável: 25% ou mais;
abaixo de 15% é crítico).

Por que importa: sem capturar atenção, nada mais funciona.
O público nem sabe que seu anúncio existe.

O que fazer: trocar os primeiros 3 segundos. Manter o resto.
Testar 2 abordagens: afirmação direta sobre uma Urgência Oculta
do resumo do produto vs resultado concreto (Light Copy: gancho
sem pergunta). Produção em /copy-anuncio ou /mandala-de-anuncios.
O que NÃO fazer: não mudar o corpo do vídeo (pode estar bom).
```

### falha_sustentacao
```
{nome}: FALHA DE SUSTENTAÇÃO

O que está acontecendo: o gancho funciona (Hook {X}%), mas o
público abandona antes do meio (Hold {Y}%, benchmark: 30%+).

Por que importa: o público para, mas não fica. O conteúdo
entre o gancho e o CTA não sustenta interesse.

O que fazer: reescrever o desenvolvimento. Versão mais curta
ou com história/prova social no meio.
O que NÃO fazer: não trocar o gancho (funciona).
```

### falha_intencao
```
{nome}: FALHA DE INTENÇÃO

O que está acontecendo: o criativo captura atenção mas não gera
ação. {Se CTR baixo: "Poucos clicam."} {Se CTR alto + LPV baixo:
"Muitos clicam, mas não chegam na página."}

O que fazer: {Se CTR baixo: fortalecer CTA e urgência.}
{Se CTR alto + LPV baixo: primeiro conferir a página (velocidade,
link, redirecionamento) com /pagina-performance e a continuidade
da promessa com /trafego-oferta-funil, sem mexer no anúncio. Com a
página em ordem, é curiosidade vazia: alinhar promessa com destino
em /copy-anuncio.}
O que NÃO fazer: não escalar pelo Hook Rate alto.
```

Variante para imagem com atenção reprovada (camada 1 FAIL em imagem):
```
{nome}: FALHA DE INTENÇÃO (a imagem não para a rolagem)

O que está acontecendo: a imagem não para a rolagem: CTR {X}%,
menos da metade do benchmark da conta ({benchmark}%).

O que fazer: nova peça em /criativo-estatico, mantendo a oferta.
O que NÃO fazer: não mexer na página nem na oferta por causa
deste criativo (o problema começa antes do clique).
```

### falha_qualificacao
```
{nome}: FALHA DE QUALIFICAÇÃO

O que está acontecendo: tráfego qualificado chega na página
(Click-to-LPV {X}%), mas não compra (CPA R$ {Y}, meta R$ {Z}).

Por que importa: o criativo faz o trabalho dele (traz gente).
O problema pode estar na conexão criativo-oferta ou no CTA.

O que fazer: testar CTA mais direto, âncora de preço, ou prova
social no final do criativo.
O que NÃO fazer: não pausar se Offer Rate > 2%.
```

### falha_pos_clique
```
{nome}: FALHA PÓS-CLIQUE (problema na página, NÃO no criativo)

O que está acontecendo: o criativo atrai atenção, gera clique
qualificado, mas quase ninguém demonstra interesse na oferta
(Offer Rate {X}%, abaixo de 2%).

Por que importa: o problema NÃO é o criativo. É a página, a
oferta, o preço, a prova ou o checkout.

O que NÃO fazer: NÃO pausar esse criativo. Ele está trazendo
tráfego qualificado para uma página que não converte.
O que fazer: rodar `/trafego-oferta-funil` para ler a página
real e diagnosticar onde a oferta falha.
```

### criativo_equilibrado
```
{nome}: CRIATIVO EQUILIBRADO ✅

O que está acontecendo: as 4 camadas estão OK. Captura atenção,
gera intenção qualificada, converte e se mantém consistente.

O que fazer: criar variações (novo ângulo, novo formato).
Considerar escala: /trafego-diagnostico (falso vencedor e score)
e depois /trafego-escalar.
O que NÃO fazer: não mexer no que funciona. Variações são
adições, não substituições.
```

### dados_insuficientes
```
{nome}: DADOS INSUFICIENTES

O que significa: {motivo: poucas impressões / poucos dias /
poucas conversões}. Não é possível diagnosticar.

O que fazer: manter rodando por mais {X} dias.
O que NÃO fazer: não tomar decisão baseada nesses dados.
```

## Repasse para módulos seguintes (na Inteligência Completa)

Quando rodado como 4o módulo da sequência, repassar para:
- **DNA criativo (módulo 5):** lista de veredictos por criativo + perfil de camadas (para agrupar por padrão comportamental)
- **Briefing criativo (módulo 6):** veredictos com falha + score de confiança (para priorizar testes por impacto)

## Relatório humano (7 seções)

Usar a estrutura completa da seção 11 do SKILL.md. Exemplo:

```
1. CONTEXTO RESUMIDO
Diagnostiquei 8 criativos do Produto A nos últimos 7 dias.
4 camadas avaliadas por criativo: atenção, intenção, conversão
e consistência. 2 criativos sem dados suficientes.

2. DIAGNÓSTICO REAL
Os dados dizem: 2 criativos com falha de gancho (Hook < 15%),
1 com falha de intenção (provável curiosidade vazia, depois de
conferir a página), 1 com falha
pós-clique, 1 equilibrado, 1 dados insuficientes.
Os dados NÃO dizem: por que o gancho falha (sem acesso ao vídeo).
Erro a evitar: pausar o criativo com falha pós-clique (problema
é na página, não no criativo).

3. HIPÓTESE CENTRAL
O principal gargalo criativo desta conta é atenção: 2 dos 6
criativos com dados perdem o público nos primeiros 3 segundos.

5. RISCOS E ARMADILHAS
O criativo "Polêmica - 15s" tem CTR 2.8% e só 38% de visita:
conferir a página antes; se ela estiver em ordem, é curiosidade
vazia e escalar vai desperdiçar orçamento.

7. DECISÃO RECOMENDADA
Fazer agora: novos ganchos para os 2 criativos com falha.
NÃO fazer: não pausar "História - 60s" (falha pós-clique).
Fazer somente se: escalar "VSL Completa" apenas se CPA
se mantiver abaixo de R$ 130 por mais 7 dias.
```

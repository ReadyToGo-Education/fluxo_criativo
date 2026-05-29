---
name: trafego-testes
description: >
  Cria testes A/B e variações estruturadas no Meta Ads. Cobre A/B de criativo, headline,
  audiência, faixa etária, posicionamento, lance e estrutura (Advantage+ vs manual). Também
  duplica campanha existente alterando UMA dimensão e orquestra fluxo composto de campanha
  de remarketing (público + criação de campanha). Documenta hipótese de cada teste e devolve
  handoff para /trafego-analise [3] após 7 dias para leitura. Use quando o aluno pedir
  "testar criativo A vs B", "duplicar minha melhor campanha mudando idade", "criar campanha
  de remarketing", "A/B de público broad vs segmentado".
user-invocable: false
---

## 🛡️ Gate obrigatório antes de qualquer escrita na Graph API

Esta skill executa operações que **modificam estado** na conta Meta Ads. Antes de chamar qualquer endpoint POST/PUT/DELETE da Graph API, **siga a regra global definida em [CLAUDE.md](../../../CLAUDE.md)** na seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API":

1. Apresentar o bloco `🛡️ Confirmação necessária antes de tocar na conta Meta` com operação, endpoint humano-legível, o que vai mudar, impacto no aprendizado e reversibilidade.
2. **Nunca exibir o `curl` completo no chat** — carrega o token.
3. Aguardar resposta `sim` (ou variante explícita: aprovo, pode, manda) antes de executar.
4. Em modo lote, mostrar o plano completo antes e pedir confirmação única.
5. Se o aluno responder `não` ou variante (cancelar, abortar), abortar sem chamar a API.
6. **NUNCA usar `python3 << 'EOF'` (heredoc) nem `curl | python3 -c`** com o token. Esses formatos quebram o pattern matching do Claude Code e expõem o token no pop-up nativo. Ver regra "EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API" no CLAUDE.md.

**Operações desta skill que passam pelo gate:**

- POST /<adset_id>/copies (duplicar conjunto para teste A/B)
- POST /<ad_id>/copies (duplicar anúncio para teste A/B)
- POST /act_<id>/adsets + /ads (criar entidades do teste)

**Não passam pelo gate:** chamadas GET para leitura (insights, listagens, fields). Estado não muda.

---

# Tráfego Testes. A/B e Variações Estruturadas Meta Ads

Cria testes A/B disciplinados e variações de campanhas existentes via Marketing API. Toda criação documenta hipótese, define critério de vitória, e devolve handoff para leitura após período mínimo de teste.

**Princípios:**
- **Testar UMA dimensão por vez.** Variar 2 coisas de uma vez não permite atribuir o ganho/perda corretamente.
- **Mesmo budget nos dois lados.** Sem orçamento simétrico, comparação fica viesada.
- **50+ conversões mínimas por variação** para significância estatística (low/mid ticket). Para high ticket, 30+.
- **7+ dias** de janela mínima.
- **Hipótese documentada antes** de subir o teste. "Hipótese: criativo B converte 20% melhor porque o hook é mais específico."
- **Após 7 dias, handoff para `/trafego-analise [3] Criativos`** para leitura.
- **Testes nascem PAUSED** e exigem confirmação SIM para subir.

---

## 1. Sub-fluxos disponíveis

A skill é orquestrada pelo command `/trafego-testes`. Menu:

```
[1]  A/B de criativo                     imagem A vs imagem B, ou imagem vs vídeo
[2]  A/B de headline                     até 3 variações de copy (mantém criativo)
[3]  A/B de audiência                    broad vs segmentado, ou audiência X vs Y
[4]  A/B de faixa etária                 ex: 25-34 vs 35-44
[5]  A/B de posicionamento               Reels vs Feed vs Stories
[6]  A/B de lance                        auto vs manual com cap de CPA
[7]  A/B de estrutura                    Advantage+ vs ABO manual
[8]  A/B de CTA                          Saiba Mais vs Compre Agora vs Cadastre-se
[9]  Duplicar com variação               pega campanha existente e duplica mudando 1 coisa
[10] Campanha de remarketing             fluxo composto: público + campanha
```

### Roteamento opção do menu → sub-skill

As 8 primeiras opções compartilham a mesma mecânica (variar UMA dimensão com tudo mais constante) e caem na mesma sub-skill, parametrizada pela coluna `dimensao`.

| Opção | Sub-skill | Parâmetro `dimensao` |
|---|---|---|
| [1] Criativo | `sub-skills/ab-generico.md` | `criativo` |
| [2] Headline | `sub-skills/ab-generico.md` | `headline` |
| [3] Audiência | `sub-skills/ab-generico.md` | `audiencia` |
| [4] Faixa etária | `sub-skills/ab-generico.md` | `faixa_etaria` |
| [5] Posicionamento | `sub-skills/ab-generico.md` | `posicionamento` |
| [6] Lance | `sub-skills/ab-generico.md` | `lance` |
| [7] Estrutura | `sub-skills/ab-generico.md` | `estrutura` |
| [8] CTA | `sub-skills/ab-generico.md` | `cta` |
| [9] Duplicar variando | `sub-skills/duplicar-variando.md` | — |
| [10] Campanha de remarketing | `sub-skills/campanha-remarketing.md` | — |

A sub-skill `ab-generico.md` traz a tabela de mapeamento de cada `dimensao` para nível (ad/adset/campanha), modelo (`ads_mesmo_adset`, `adsets_separados`, `campanhas_separadas`), campos da Marketing API que mudam, métrica primária e avisos específicos.

### Quando NÃO usar esta skill (redirecionamentos)

- "Pausa todos os ad sets com CPA > R$ 50" → **`/trafego-otimizar`** (ação em lote, não é teste)
- "Aumenta budget das top 3" → **`/trafego-escalar`** (escala, não é teste)
- "Cria uma campanha do zero" → **`/trafego-criar-campanha`**
- "Cria só o público de remarketing sem campanha" → **`/trafego-publicos`**

---

## 2. Endpoints Marketing API

```
POST /act_<id>/adsets        (cria adset variando dimensão)
POST /act_<id>/ads           (cria ad variando criativo/headline)
POST /<entity_id>/copies     (duplica entidade)
POST /<entity_id>            (atualiza entidade já criada)
GET  /<entity_id>/insights   (puxa métricas para leitura pós-teste)
```

API version: `v25.0`. Permissões: `ads_management`.

---

## 3. Convenção de nomenclatura de teste

```
[WS-AB] {dimensao}-{slug-A}-vs-{slug-B}-{produto}
```

Exemplos:
- `[WS-AB] criativo-imagem-vs-video-curso-tarot`
- `[WS-AB] headline-3versoes-curso-tarot`
- `[WS-AB] audiencia-broad-vs-LAL1-curso-tarot`
- `[WS-AB] idade-25_34-vs-35_44-curso-tarot`
- `[WS-AB] dup-campanha7384-mudando-idade-curso-tarot`

---

## 4. Documento de hipótese

Toda execução cria automaticamente um arquivo:

```
meus-produtos/{ativo}/trafego/testes/{teste-slug}.md
```

Com:

```markdown
# Teste A/B — {nome do teste}

> Criado em: 2026-05-05
> Status: rodando | concluído | inconclusivo
> Próxima leitura: 2026-05-12 (D+7)

## Hipótese
{Frase clara: "X performa Y% melhor que Z porque ___"}

## Variações
- A: {descrição}
- B: {descrição}

## Critério de vitória
{Métrica primária + diferença mínima necessária}
Ex: CPA da variação vencedora ≤ 90% do CPA da perdedora, com 50+ conversões em cada lado.

## Inputs
- Budget por variação: R$ X/dia
- Audience comum (se aplicável): {ID}
- Posicionamento: {fixo se for teste de outra dimensão}
- Janela: 7 dias

## Resultado (preenchido em D+7)
- A: {resultado}
- B: {resultado}
- Vencedora: ___
- Significância: alta | média | baixa | inconclusivo
- Aprendizado: ___

## Observações
{preenchido automaticamente quando aplicável}
- Viés conhecido: teste paralelo de {criativo|headline|cta}. Algoritmo do Meta pode favorecer um lado em 24-48h. Pra teste 100% limpo, usar Experimento nativo no Gerenciador.

## Próximos passos
- Pausar perdedora? Sim/Não
- Escalar vencedora? Sim/Não → /trafego-escalar
- Próximo teste sugerido: ___
```

---

## 5. Estrutura técnica do teste

A skill suporta 2 modelos de implementação:

### 5.1 Modelo "ads no mesmo adset" (recomendado para A/B de criativo/headline)
Cria múltiplos ads dentro do mesmo adset. Meta distribui orçamento entre eles automaticamente, mas pode favorecer um precocemente. Para testes mais limpos, usar modelo 5.2.

### 5.2 Modelo "adsets separados" (recomendado para A/B de audiência/idade/posicionamento/lance)
Cria múltiplos adsets idênticos exceto na dimensão testada. Cada adset tem budget próprio. Comparação mais justa porque o algoritmo otimiza separadamente.

### 5.3 Modelo "Meta A/B Test feature" (não usado neste MVP)
O Meta tem um produto nativo "A/B Test" que faz randomização real. Não usado nesta skill no MVP por complexidade da API. Sub-skills futuras podem migrar.

---

## 6. Output esperado

```yaml
operacao: criar_teste_ab
sub_fluxo: ab_criativo | ab_headline | ab_audiencia | ab_faixa_etaria | ab_posicionamento | ab_lance | ab_estrutura | duplicar_variando | campanha_remarketing
ad_account_id: act_<id>

teste:
  slug: criativo-imagem-vs-video-curso-tarot
  nome: "[WS-AB] criativo-imagem-vs-video-curso-tarot"
  hipotese: "Vídeo converte mais que imagem em audiência fria de tarot"
  modelo: adsets_separados | ads_mesmo_adset
  variacoes:
    - id: <ad_id_A> ou <adset_id_A>
      slug: A
      descricao: "imagem estática Mandala Tipo 1"
      budget: 30 BRL/dia
    - id: <ad_id_B> ou <adset_id_B>
      slug: B
      descricao: "vídeo 30s estilo VVV"
      budget: 30 BRL/dia
  janela_minima: 7 dias
  conversoes_minimas_por_lado: 50

  status_inicial: PAUSED
  data_inicio_prevista: 2026-05-05
  data_leitura_em: 2026-05-12

  arquivo_local: meus-produtos/curso-tarot/trafego/testes/criativo-imagem-vs-video.md

handoffs:
  - texto: "Em 7 dias, ler resultado"
    skill: /trafego-analise opção [3] Criativos
  - texto: "Para escalar a vencedora"
    skill: /trafego-escalar
```

---

## 7. Princípios que esta skill nunca viola

1. **UMA dimensão por teste.** Sem exceção.
2. **Mesmo budget** nos dois lados.
3. **Mínimo 50 conversões/lado** (30 para high ticket).
4. **Mínimo 7 dias** de janela.
5. **Hipótese documentada** antes de subir.
6. **Toda criação nasce PAUSED.** Aluno ativa.
7. **Convenção `[WS-AB]`** no nome.
8. **Handoff para /trafego-analise [3]** após D+7.
9. **Não pausa perdedora automaticamente.** Devolve recomendação, aluno decide.
10. **Não escala vencedora automaticamente.** Encaminha para `/trafego-escalar`.

---
name: trafego-testes
description: >
  Cria testes A/B disciplinados e variações estruturadas no Meta Ads: A/B de criativo,
  headline, audiência, faixa etária, posicionamento, lance, estrutura e CTA; duplica campanha,
  conjunto ou anúncio mudando UMA coisa só; e monta campanha de remarketing completa
  (público + campanha). Toda criação nasce pausada e documenta a hipótese. Depois do 7º dia,
  a opção [11] lê o resultado, classifica (validado, invalidado, promissor, inconclusivo,
  contaminado, repetir com ajuste), registra o aprendizado e sugere o próximo teste. Para quem
  quer divisão de público garantida pela Meta, cita o teste A/B oficial do MCP. Use quando o
  aluno pedir "testar A vs B", "duplicar minha melhor campanha mudando a idade", "criar
  campanha de remarketing", "Reels vs Feed", "broad vs segmentado", "como ficou meu teste".
user-invocable: true
---

# Tráfego Testes. A/B e Variações Estruturadas Meta Ads

Cria testes A/B disciplinados e variações de campanhas existentes. Toda criação documenta a hipótese, define o critério de vitória e devolve a data de leitura do resultado.

---

## 🛡️ Gate obrigatório antes de qualquer escrita na conta

Toda escrita segue a seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API" do CLAUDE.md, nos dois modos (tool do MCP ou `curl` no App):

1. **Resumo em linguagem natural** do plano (sem ID, sem campo da Marketing API, sem centavos).
2. **Bloco 🛡️ com o Preview YAML.** Um "sim" por lote: montar um teste A/B (campanha casca + conjuntos + anúncios + uploads) é um lote só.
3. Depois do "sim", executar em sequência sem reabrir o gate, a não ser que uma chamada falhe, o aluno mude o plano ou surja escrita fora do lote.
4. **Exclusão nunca entra no lote** (regra 7 do gate). Esta skill não apaga nada: tudo nasce pausado. Para desfazer, arquivar ou pausar (com bloco 🛡️), ou apagar pelo Gerenciador. Nunca `curl -X DELETE` direto.
5. **Campanha de remarketing atravessa skills** (`/trafego-publicos` + `/trafego-criar-campanha`): exige o **modo lote pré-aprovado** do CLAUDE.md, com o plano completo numerado e um "aprovar tudo" explícito (ver `sub-skills/campanha-remarketing.md`).
6. Nunca exibir `curl` com token. Proibido heredoc Python e `curl | python3` com token.

| Operação | MCP (`MCP_CONECTOR`) | App (`curl`) |
|---|---|---|
| Duplicar conjunto ou anúncio | `ads_create_ad_set` / `ads_create_ad` com `source_adset_id` / `source_ad_id`; se falhar, duplicação guiada no Gerenciador | `POST /<id>/copies` só para 1 conjunto com 1 anúncio; acima disso, "ler e recriar" |
| Duplicar campanha inteira | campanha casca + conjuntos copiados um a um por `source_adset_id`; se falhar, duplicação guiada no Gerenciador | "ler e recriar" (nunca `/copies` com `deep_copy`) |
| Criar campanha, conjunto e anúncio do teste | `ads_create_campaign` / `ads_create_ad_set` / `ads_create_ad` | `POST /act_<id>/campaigns`, `/adsets`, `/ads` |
| Aplicar a variação na cópia | `ads_update_entity` (ver limite da segmentação abaixo) | `POST /<id>` |
| Subir imagem de arquivo | URL pública no criativo (`ads_create_creative` com `image_url`) ou passo manual guiado (biblioteca de mídia do Gerenciador) | `POST /act_<id>/adimages` |
| Subir vídeo novo | passo manual guiado (biblioteca de mídia do Gerenciador) e depois `ads_get_ad_videos` | `POST https://graph-video.facebook.com/v25.0/act_<id>/advideos` |
| Teste A/B oficial da Meta (opcional) | `ads_experiment_check_eligibility`, `ads_experiment_abtest_create_test` | Gerenciador → Testes A/B (passo manual guiado) |
| Ativar entidades depois de revisar | `ads_update_entity` ou `ads_activate_entity` | `POST /<id>` com `status` |

**Não passam pelo gate:** leituras (`ads_get_*`, `ads_insights_*`, `ads_experiment_abtest_get_test`, `ads_experiment_list_tests` ou `GET`) e a gravação do arquivo de hipótese local.

---

## 🔌 Passo 0 obrigatório (antes de qualquer leitura ou escrita)

1. **Produto ativo.** Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md`, seguindo a seção "Contexto Persistente do Negócio" do CLAUDE.md. Do resumo saem: **preço e tipo** (definem o mínimo de conversões: 50 por lado em low e middle ticket, 30 em high ticket), **Quadro, Urgências Ocultas, Decorados, público e objeções** (para sugerir hipóteses e ângulos da Mandala). Não perguntar o que o resumo já tem.
2. **Conexão Meta.** Ler `META_AUTH_MODO` com `grep "^META_AUTH_MODO=" .env | cut -d= -f2-`.
   - **Vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive o legado `HIBRIDO`): acionar `/trafego-conexao` e aguardar a conclusão. Não adivinhar o modo, não cair em outro caminho e não pedir credencial avulsa.
   - **`MCP_CONECTOR`:** confirmar uma tool cujo nome termina em `ads_get_ad_accounts` (descobrir sempre pelo final do nome). Conta não liberada no conector: explicar e oferecer o modo App pelo `/trafego-conexao`. No MCP não há token: `ad_account_id` e IDs vêm de `FB_AD_ACCOUNT_ID` e das listagens. Conferir que a variável tem valor (`grep -q "^FB_AD_ACCOUNT_ID=." .env`); se faltar, a opção "Validar" do `/trafego-conexao` completa.
   - **`APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` têm valor (`grep -q "^NOME=." .env`, com o ponto: linha vazia conta como ausente). Se faltar algum, acionar `/trafego-conexao`.
3. **O que o MCP faz e o que não faz nesta skill:**
   - **Faz:** criar campanha, conjunto e anúncio; copiar conjunto e anúncio de um existente (`source_*_id`); aplicar mudanças com `ads_update_entity`; listar imagens e vídeos da biblioteca; ler métricas; teste A/B oficial.
   - **Não lê a segmentação do conjunto:** `ads_get_ad_entities` não devolve `targeting`, `age_min`, `age_max` nem `promoted_object` (responde `Unsupported field(s)`). Por isso o "ler e recriar" da seção "Lições de campo" da `ab-generico.md` só funciona no App. No MCP: copiar pelo `source_*_id` e, se falhar, duplicação guiada no Gerenciador (o aluno duplica, a skill confere).
   - **Mudar a segmentação de uma cópia pelo MCP** (idade, público, posicionamento): só pelo `ads_update_entity` se o schema aceitar mudar o campo sozinho, sem reenviar a segmentação inteira (que o conector não lê). Se exigir a segmentação completa, a mudança vai pelo Gerenciador, com passo a passo.
   - **Subir vídeo novo:** não existe no MCP. Passo manual guiado (biblioteca de mídia do Gerenciador) e depois a skill usa o vídeo pela `ads_get_ad_videos`.
   - **Buscar interesse por nome:** não existe no MCP. No A/B de audiência, preferir públicos e semelhantes que já existem, ou as bases salvas pela `/trafego-publicos`. Para interesse específico, passo manual guiado (ver `trafego-publicos/sub-skills/bases-niveis.md`).
4. **Herança por delegação:** a `campanha-remarketing` delega a `/trafego-publicos` e a `/trafego-criar-campanha` e herda o Passo 0 e o roteamento delas. Não duplica lógica nem chama `curl` por conta própria.

**Princípios:**
- **Testar UMA dimensão por vez.** Variar 2 coisas juntas impede saber o que causou o ganho ou a perda.
- **Mesmo orçamento nos dois lados.** Sem simetria, a comparação fica torta.
- **50 conversões ou mais por variação** para low e middle ticket; **30 ou mais** para high ticket.
- **7 dias ou mais** de janela mínima (14 em teste de estrutura).
- **Hipótese documentada antes** de subir. "Hipótese: o criativo B converte 20% melhor porque o gancho é mais específico."
- **Depois de 7 dias, ler o resultado pela opção [11]** (`sub-skills/leitura-resultado.md`): classifica, registra o aprendizado e sugere o próximo teste. A `/trafego-analise` (Criativos & Copy) entra só como complemento, para uma leitura VTSD mais ampla.
- **Tudo nasce PAUSED.** Nada é ativado sem confirmação.
- **Copy gerada pela skill** (headline, texto principal, CTA, ângulo de remarketing) passa pela "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md (Manual da Copy + skill `revisora`) antes de aparecer para o aluno, sem mencionar a revisão.

---

## 1. Sub-fluxos disponíveis

Menu do command `/trafego-testes`:

```
[1]  A/B de criativo                     imagem A vs imagem B, ou imagem vs vídeo
[2]  A/B de headline                     até 3 variações de headline (mesmo criativo)
[3]  A/B de audiência                    broad vs segmentado, ou público X vs Y
[4]  A/B de faixa etária                 ex: 25-34 vs 35-44
[5]  A/B de posicionamento               Reels vs Feed vs Stories
[6]  A/B de lance                        automático vs limite de custo
[7]  A/B de estrutura                    Advantage+ vs ABO manual
[8]  A/B de CTA                          Saiba mais vs Comprar agora vs Cadastre-se
[9]  Duplicar com variação               copia o que já existe mudando 1 coisa
[10] Campanha de remarketing             fluxo composto: público + campanha
[11] Ler resultado de teste              lê no 7º dia, classifica, registra o aprendizado
```

### Opção do menu → sub-skill

As 8 primeiras compartilham a mesma mecânica (variar UMA dimensão com o resto igual) e caem na mesma sub-skill, com o parâmetro `dimensao`.

| Opção | Sub-skill | `dimensao` |
|---|---|---|
| [1] Criativo | `sub-skills/ab-generico.md` | `criativo` |
| [2] Headline | `sub-skills/ab-generico.md` | `headline` |
| [3] Audiência | `sub-skills/ab-generico.md` | `audiencia` |
| [4] Faixa etária | `sub-skills/ab-generico.md` | `faixa_etaria` |
| [5] Posicionamento | `sub-skills/ab-generico.md` | `posicionamento` |
| [6] Lance | `sub-skills/ab-generico.md` | `lance` |
| [7] Estrutura | `sub-skills/ab-generico.md` | `estrutura` |
| [8] CTA | `sub-skills/ab-generico.md` | `cta` |
| [9] Duplicar com variação | `sub-skills/duplicar-variando.md` | (não se aplica) |
| [10] Campanha de remarketing | `sub-skills/campanha-remarketing.md` | (não se aplica) |
| [11] Ler resultado de teste | `sub-skills/leitura-resultado.md` | (não se aplica) |

A `ab-generico.md` tem a tabela de cada `dimensao`: nível (anúncio, conjunto, campanha), modelo, campos que mudam, métrica principal e avisos.

### Quando NÃO usar esta skill (redirecionamentos)

- "Pausa todos os conjuntos com CPA > R$ 50" → **`/trafego-otimizar`** (ação em lote, não é teste)
- "Aumenta o orçamento dos 3 melhores" → **`/trafego-escalar`** (escala, não é teste)
- "Cria uma campanha do zero" → **`/trafego-criar-campanha`**
- "Cria só o público de remarketing, sem campanha" → **`/trafego-publicos`**
- "Escreve os anúncios do teste" → **`/copy-anuncio`**, **`/criativo-estatico`**, **`/mandala-de-anuncios`** (vídeo: **`/video-heygen`**, **`/video-remotion`**, **`/video-editar`**)

---

## 2. Endpoints (roteamento por modo, ver Passo 0)

| Operação | MCP | App (`curl`, `v25.0`) |
|---|---|---|
| Criar conjunto (varia dimensão) | `ads_create_ad_set` | `POST /act_<id>/adsets` |
| Criar anúncio (varia criativo, headline, CTA) | `ads_create_ad` (criativo por `ads_create_creative` quando precisar) | `POST /act_<id>/ads` |
| Criar campanha (estrutura ou escopo 2) | `ads_create_campaign` | `POST /act_<id>/campaigns` |
| Copiar conjunto ou anúncio | `ads_create_ad_set` / `ads_create_ad` com `source_*_id` | `POST /<id>/copies` (só 1 conjunto com 1 anúncio) |
| Aplicar a variação | `ads_update_entity` | `POST /<entity_id>` |
| Listar campanhas, conjuntos e anúncios molde | `ads_get_ad_entities` | `GET /act_<id>/campaigns` etc. |
| Ler `targeting`, idade, `promoted_object` do molde | não existe no MCP | `GET -g /<id>?fields=targeting,promoted_object,...` |
| Listar imagens e vídeos | `ads_get_ad_images` / `ads_get_ad_videos` | `GET /act_<id>/adimages`, `/advideos` |
| Métricas do teste | `ads_get_ad_entities` no nível do teste, com filtro pelo id das variações (ex.: `filtering: [{field: "ad.id", operator: "IN", value: [...]}]`), ou `/trafego-insights` | `GET /<entity_id>/insights` |
| Teste A/B oficial | `ads_experiment_check_eligibility`, `ads_experiment_abtest_create_test`, `ads_experiment_abtest_get_test`, `ads_experiment_list_tests` | Gerenciador → Testes A/B |

Permissão (App): `ads_management`. No App, cada `curl` é um `Bash` separado, com o token lido do `.env` na própria chamada e `curl -g` quando `fields` tiver `{}`.

> ⚠️ **Copiar estrutura de teste NÃO é confiável por `/copies` (nem com `deep_copy`).** Numa sessão real (2026-06-09), `POST /<campaign_id>/copies deep_copy=true` falhou em cadeia: limite de menos de 3 objetos por cópia síncrona (1885194), revalidação de criativo com post existente (3858504 e 2446347) e sinalizador de público Advantage faltando (1870227). No App, o padrão confiável é **ler a configuração por `GET` e recriar** (campanha casca → conjuntos com `targeting_automation.advantage_audience` → anúncios apontando para o `creative_id` existente). No MCP, que não lê a segmentação, o padrão é copiar por `source_*_id` e, se falhar, duplicação guiada no Gerenciador. Detalhe na seção "Lições de campo" da `sub-skills/ab-generico.md`. Vale também para `duplicar-variando` e `campanha-remarketing`.

---

## 3. Nome do teste

```
[WS-AB] {dimensao}-{slug-A}-vs-{slug-B}-{produto-slug}
```

Exemplos:
- `[WS-AB] criativo-imagem-vs-video-curso-tarot`
- `[WS-AB] headline-3versoes-curso-tarot`
- `[WS-AB] audiencia-broad-vs-LAL1-curso-tarot`
- `[WS-AB] idade-25_34-vs-35_44-curso-tarot`
- `[WS-AB] dup-campanha-tarot-mudando-idade-curso-tarot`

---

## 4. Documento de hipótese

Toda execução cria um arquivo:

```
meus-produtos/{ativo}/entregas/trafego/testes/{teste-slug}.md
```

E acrescenta uma linha em `meus-produtos/{ativo}/entregas/trafego/testes/INDEX.md`.

```markdown
# Teste A/B: {nome do teste}

> Criado em: 2026-05-05
> Status: rodando | concluído | inconclusivo
> Modelo: ads_mesmo_adset | adsets_separados | campanhas_separadas | ab_oficial_meta
> Próxima leitura: 2026-05-12 (7º dia)

## Hipótese
{Frase clara: "X performa Y% melhor que Z porque ___"}

## Variações
- A: {descrição}
- B: {descrição}

## Critério de vitória
{Métrica principal e diferença mínima}
Ex: CPA da vencedora ≤ 90% do CPA da perdedora, com 50 ou mais conversões em cada lado.

## Critério de parada antecipada
{Quando encerrar antes da janela, só com o volume mínimo atingido.}
Ex: CPA da variação B > 2 vezes o CPA de A, com 30 ou mais conversões por lado.

## Critério de inconclusivo
{Quando o teste não dá para julgar e precisa ser estendido ou refeito.}
Ex: menos de 50 conversões por lado depois de 7 dias, ou diferença menor que a do critério de vitória (no exemplo acima, menos de 10% entre A e B).

## Inputs
- Orçamento por variação: R$ X/dia
- Público comum (se houver): {nome}
- Posicionamento: {fixo, se o teste for de outra dimensão}
- Janela: 7 dias

## Entidades criadas
- A: {nível} {id} ("{nome}")
- B: {nível} {id} ("{nome}")

## Resultado (preenchido no 7º dia pela leitura-resultado)
- A: {métricas}
- B: {métricas}
- Classificação: validado | invalidado | promissor | inconclusivo | contaminado | repetir_com_ajuste
- Vencedora: ___
- Confiança: alta | média | baixa | inconclusiva
- Contaminação: nenhuma | {alteração feita durante o teste}

## Aprendizado
- O que funcionou: ___
- O que não funcionou: ___
- Repetir: ___
- Evitar: ___
- Próximo teste sugerido: ___

## Observações
- Viés conhecido: teste paralelo de {criativo | headline | CTA}. O algoritmo da Meta pode favorecer um lado em 24 a 48h. Para teste 100% limpo, usar o teste A/B oficial (MCP ou Gerenciador).

## Próximos passos
- Pausar a perdedora? Sim/Não
- Escalar a vencedora? Sim/Não → /trafego-escalar
- Próximo teste sugerido: ___
```

---

## 5. Estrutura técnica do teste

### 5.1 Modelo "anúncios no mesmo conjunto" (para criativo, headline e CTA)
Vários anúncios dentro do mesmo conjunto. A Meta distribui o orçamento sozinha, mas pode favorecer um cedo. Para teste mais limpo, usar o 5.2.

### 5.2 Modelo "conjuntos separados" (para audiência, idade, posicionamento, lance)
Conjuntos idênticos exceto na dimensão testada, cada um com orçamento próprio. Comparação mais justa porque o algoritmo otimiza cada um separado.

### 5.3 Teste A/B oficial da Meta (opção no MCP)
A Meta tem o teste A/B nativo, que divide o público de forma garantida (ninguém vê os dois lados). Para quem quer essa garantia:
- **MCP:** conferir se a campanha pode entrar com `ads_experiment_check_eligibility`, criar com `ads_experiment_abtest_create_test`, acompanhar com `ads_experiment_abtest_get_test` e listar com `ads_experiment_list_tests`. Os parâmetros vêm do schema de cada tool na hora (a skill não inventa). A criação passa pelo bloco 🛡️.
- **App:** passo manual guiado no Gerenciador (Testes A/B). A skill grava mesmo assim o arquivo de hipótese (`modelo: ab_oficial_meta`), para a leitura da opção [11].

O fluxo padrão da skill continua sendo o 5.1 e o 5.2 (duplicar variando 1 dimensão). O teste oficial aparece como opção no "Aviso de viés" da `ab-generico.md`.

---

## 6. Saída

```yaml
operacao: criar_teste_ab
sub_fluxo: ab_criativo | ab_headline | ab_audiencia | ab_faixa_etaria | ab_posicionamento | ab_lance | ab_estrutura | ab_cta | duplicar_variando | campanha_remarketing
modo: MCP_CONECTOR | APP
ad_account_id: act_<id>

teste:
  slug: criativo-imagem-vs-video-curso-tarot
  nome: "[WS-AB] criativo-imagem-vs-video-curso-tarot"
  hipotese: "Vídeo converte mais que imagem no público frio de tarot porque mostra a leitura acontecendo"
  modelo: adsets_separados | ads_mesmo_adset | campanhas_separadas | ab_oficial_meta
  variacoes:
    - id: <ad_id_A ou adset_id_A>
      slug: A
      descricao: "imagem estática, tipo Comparação da Mandala"
      orcamento: 30 BRL/dia
    - id: <ad_id_B ou adset_id_B>
      slug: B
      descricao: "vídeo de 30s, tipo Demonstração da Mandala"
      orcamento: 30 BRL/dia
  janela_minima: 7 dias
  conversoes_minimas_por_lado: 50
  criterio_vitoria: "CPA da vencedora ≤ 90% do CPA da perdedora (diferença de 10% ou mais), com o mínimo de conversões em cada lado"
  criterio_parada: "CPA da variação > 2 vezes o controle com 30 ou mais conversões por lado"
  criterio_inconclusivo: "menos de 50 conversões por lado depois da janela, ou diferença menor que a do critério de vitória"

  status_inicial: PAUSED
  data_inicio_prevista: 2026-05-05
  data_leitura_em: 2026-05-12

  arquivo_local: meus-produtos/{ativo}/entregas/trafego/testes/criativo-imagem-vs-video-curso-tarot.md

handoffs:
  - texto: "No 7º dia, ler o resultado"
    skill: /trafego-testes opção [11] (complemento: /trafego-analise, Criativos & Copy)
  - texto: "Escalar a vencedora"
    skill: /trafego-escalar
```

---

## 7. Princípios que esta skill nunca viola

1. **UMA dimensão por teste.** Sem exceção.
2. **Mesmo orçamento** nos dois lados.
3. **Mínimo de 50 conversões por lado** (30 em high ticket).
4. **Mínimo de 7 dias** de janela.
5. **Hipótese documentada** antes de subir.
6. **Tudo nasce PAUSED.** O aluno ativa.
7. **Nome com `[WS-AB]`.**
8. **Ler o resultado pela opção [11]** depois do 7º dia. `/trafego-analise` só como complemento.
9. **Não pausa a perdedora sozinha.** Recomenda; o aluno decide.
10. **Não escala a vencedora sozinha.** Encaminha para `/trafego-escalar`.
11. **Nunca apaga.** Desfazer = arquivar ou pausar (com bloco 🛡️) ou apagar pelo Gerenciador.
12. **Não confia em `/copies` com `deep_copy`** para estrutura com mais de 2 objetos.

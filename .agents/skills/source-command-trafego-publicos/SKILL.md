---
name: "source-command-trafego-publicos"
description: "Cria, lista e gerencia públicos (audiences) do Meta Ads pelo MCP da Meta (padrão) ou pela Marketing API (modo App). Cobre público por evento padrão do pixel, evento personalizado (com conversão personalizada opcional), visualização de vídeo (25 a 100%), bases por nível (iniciante, intermediário, avançado) a partir do resumo do produto, público semelhante (lookalike), lista de clientes com hash feito no computador do aluno, engajamento com Instagram e Facebook e listagem com alertas. Toda criação passa por resumo, bloco 🛡️ e confirmação. Use quando o aluno pedir \"criar público\", \"audience custom\", \"lookalike\", \"público semelhante\", \"remarketing\", \"público de quem viu vídeo\", \"público dos compradores\", \"subir minha lista de clientes\", \"público de quem clicou no botão\"."
---

# source-command-trafego-publicos

Use esta skill quando o usuário pedir o comando `/trafego-publicos` do workshop (ou `trafego-publicos`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/trafego-publicos.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Trafego Publicos. Audiences Meta Ads

Cria, lista e gerencia públicos na conta de anúncios. Esta skill é a única que cria público no Severino: outras skills que precisam de público (`/trafego-criar-campanha`, `/trafego-testes`, `/trafego-escalar`) chamam esta.

A especificação completa está em `.claude/skills/trafego-publicos/SKILL.md`. Este command é o orquestrador.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo`. Leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme a seção "Contexto Persistente do Negócio" do CLAUDE.md). O resumo traz público, Quadro, Furadeira, Decorados, Urgências Ocultas, preço e tipo: o sub-fluxo "Bases por nível" usa esses dados direto, sem perguntar de novo. O slug do produto entra no nome dos públicos.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia `META_AUTH_MODO` com `grep "^META_AUTH_MODO=" .env | cut -d= -f2-`.

- **Se vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive o legado `HIBRIDO`): acione `/trafego-conexao` e aguarde a conclusão. Não tente adivinhar, não caia em fallback, não peça credenciais avulsas.
- **Se `MCP_CONECTOR`:** confirme que existe uma tool cujo nome termina em `ads_get_ad_accounts` (o começo do nome varia de instalação para instalação). Se nenhuma estiver disponível, peça ao aluno para reabrir o Claude Code; se persistir, volte ao `/trafego-conexao`. Se a conta vier como não liberada no MCP, explique e ofereça o modo App pelo `/trafego-conexao`. Confira também `FB_AD_ACCOUNT_ID` com `grep -q "^FB_AD_ACCOUNT_ID=." .env`; se faltar, a opção "Validar" do `/trafego-conexao` completa.
- **Se `APP`:** confirme com `grep -q "^FB_ACCESS_TOKEN_PERMANENTE=." .env` e `grep -q "^FB_AD_ACCOUNT_ID=." .env` que as duas variáveis existem com valor (o ponto faz a linha vazia contar como ausente). Se faltar alguma, acione `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

### 0.3 Seleção de conta de anúncio (multi-conta)
1. Leia `FB_AD_ACCOUNT_IDS` no `.env` (IDs separados por vírgula). Se não existir ou tiver 1 conta, use `FB_AD_ACCOUNT_ID` sem perguntar.
2. Com 2 ou mais contas, pergunte qual usar, mostrando os nomes. No MCP, os nomes vêm da tool `ads_get_ad_accounts`. No App, de uma chamada `curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name&limit=100&access_token=***TOKEN_MASCARADO***"` (o token entra lido do `.env` na própria chamada, nunca exibido).
3. Guarde a conta escolhida só para esta execução. Não sobrescreva o `.env`.

### 0.4 Ler especificações
- `.claude/skills/trafego-publicos/SKILL.md`
- A sub-skill da opção escolhida

---

## Passo 1. Menu

```
🎯 TRÁFEGO PÚBLICOS. Audiences Meta Ads

[1] Público por evento padrão do pixel
    PageView, ViewContent, AddToCart, InitiateCheckout, Purchase, Lead etc.

[2] Público por evento personalizado
    Clique em botão (evento próprio do pixel), página visitada, link com UTM
    ou parâmetro de evento, com conversão personalizada opcional

[3] Público de quem viu vídeo
    Quem viu 25%, 50%, 75% ou 100% do vídeo

[4] Bases por nível (iniciante, intermediário, avançado)
    Segmentações prontas a partir do resumo do produto, salvas como arquivo

[5] Público semelhante (lookalike 1% a 10%)
    Pessoas parecidas com um público que você já tem

[6] Lista de clientes
    Sobe sua lista de compradores (CSV). Os dados viram código antes de sair do computador

[7] Engajamento Instagram e Facebook
    Quem visitou o perfil, mandou mensagem, salvou post, abriu o formulário (sem pixel)

[8] Listar públicos existentes
    Visão geral, alertas (vazios, encolhendo, bons para semelhante) e exclusão de público

Digite o número:
```

## Passo 2. Sub-fluxo

| Escolha | Sub-skill | MCP (padrão) | App (`curl`) |
|---|---|---|---|
| [1] | `publico-evento-padrao.md` | `ads_create_custom_audience` (WEBSITE) | `POST /act_<id>/customaudiences` |
| [2] | `publico-evento-personalizado.md` | `ads_create_custom_audience` (WEBSITE); conversão personalizada por passo manual guiado | `POST /act_<id>/customconversions` + `POST /act_<id>/customaudiences` |
| [3] | `publico-video-view.md` | `ads_create_custom_audience` (engajamento de vídeo) | `POST /act_<id>/customaudiences` (ENGAGEMENT + `prefill=true`) |
| [4] | `bases-niveis.md` | interesses pesquisados no Gerenciador (passo manual guiado) | `GET /search?type=adinterest` + arquivo local |
| [5] | `lookalike.md` | `ads_create_custom_audience` (LOOKALIKE) | `POST /act_<id>/customaudiences` (LOOKALIKE) |
| [6] | `customer-match.md` | `ads_create_custom_audience` (CUSTOM) + `ads_update_custom_audience_users` | `POST /act_<id>/customaudiences` + `POST /<audience_id>/users` |
| [7] | `engajamento-ig-fb.md` | `ads_create_custom_audience` (engajamento) | `POST /act_<id>/customaudiences` |
| [8] | `listar.md` | `ads_get_ad_account_custom_audiences`; exclusão por `ads_delete_custom_audience` | `GET /act_<id>/customaudiences`; exclusão sem `curl -X DELETE` direto |

Se a Meta recusar um subtipo pelo MCP, a sub-skill explica e conduz o aluno por um passo a passo curto no Gerenciador.

---

## Passo 3. Coletar inputs (varia por sub-fluxo)

Cada sub-skill define seus inputs. Padrão geral, sempre uma pergunta por mensagem:
- Nome: gerado pela skill na convenção `[WS] tipo-descricao-janela-produto` e confirmado com o aluno.
- Janela: padrão 30 dias (até 180 para evento do pixel; vídeo e engajamento: até 365 dias, formulário de cadastro: até 90).
- Tamanho mínimo da origem: só no público semelhante (100 pessoas).

### Anúncio de tempo por sub-fluxo

Antes da parte longa de cada sub-fluxo, anunciar com a faixa calibrada de `.claude/rules/tempo-estimado.md`. As sub-skills não repetem o 🔍: só marcam os passos internos com ⏳.

| Sub-fluxo | Quando anunciar | Anúncio |
|---|---|---|
| [1], [2], [3], [5] e [7] | Passo 5, depois do "sim" e antes de criar | `🔍 Próximo passo: criar o público na sua conta e conferir a regra gravada (2 passos). Tempo estimado: cerca de 30 segundos.` |
| [6] Lista de clientes, modo App | Passo 5, depois do "sim" e antes de criar o público | `🔍 Próximo passo: criar o público e enviar os códigos para a Meta (2 passos). Tempo estimado: cerca de 60 segundos.` |
| [6] Lista de clientes, modo MCP (pelo conector) | Passo 5, depois do "sim" e antes de criar o público | `🔍 Próximo passo: criar o público e enviar os códigos para a Meta (2 passos). Tempo estimado: 2 a 3 minutos.` |
| [4] Bases por nível, modo App | antes de conferir os interesses (passo 6 da sub-skill) | `🔍 Próximo passo: conferir os interesses na Meta e estimar o tamanho das 3 bases (3 passos). Tempo estimado: 2 a 3 minutos.` |
| [8] Listar públicos | antes de ler a conta | `🔍 Próximo passo: listar os públicos da conta com os alertas. Tempo estimado: cerca de 30 segundos.` |

Caminhos feitos pelo aluno no Gerenciador (passo manual guiado) não levam esse anúncio: a própria sub-skill diz quanto leva.

---

## Passo 4. Resumo e bloco 🛡️

1. Resumo em linguagem natural (sem ID, sem JSON).
2. Bloco 🛡️ do CLAUDE.md com o Preview YAML: nome final, tipo, regra, janela, tamanho estimado, alertas (público micro < 1.000 etc.).
3. Um único "sim" autoriza o lote inteiro do sub-fluxo. Excluir público nunca entra no lote: tem bloco e "sim" próprios.

---

## Passo 5. Criação

Antes de criar, anunciar com o tempo do sub-fluxo (tabela "Anúncio de tempo por sub-fluxo", no Passo 3). Na opção [1], [2], [3], [5] ou [7]: `🔍 Próximo passo: criar o público na sua conta e conferir a regra gravada (2 passos). Tempo estimado: cerca de 30 segundos.` Na opção [6], o anúncio da linha do modo (App ou MCP) da mesma tabela.

Se confirmado:
- Cria pelo MCP ou pelo `curl` (nunca exibido com token).
- Grava `meus-produtos/_global/trafego/publicos/{id}.md` com a regra completa e como desfazer, sem nenhum dado pessoal.
- Atualiza `meus-produtos/_global/trafego/publicos/INDEX.md`.
- Marca como desatualizado o cache do `/trafego-insights` da conta.

✅ Concluído: público criado. Caminho do registro: `meus-produtos/_global/trafego/publicos/INDEX.md`.

---

## Passo 6. Próximos passos

```
Próximos passos:

- Para usar esse público numa campanha: /trafego-criar-campanha
- Para criar um semelhante a partir dele: /trafego-publicos opção 5
- Para ver o tamanho real (a Meta calcula em até 24h): /trafego-publicos opção 8
- Para montar uma campanha de remarketing com esse público:
  /trafego-testes opção 10 (campanha de remarketing)
```

---

## Princípios

1. **Resumo e bloco 🛡️ antes de escrever. Sempre.**
2. **Um "sim" por lote.** Exclusão de público sempre à parte, pela tool `ads_delete_custom_audience` no MCP; no App, nunca `curl -X DELETE` direto.
3. **Convenção de nome `[WS]`.**
4. **Público nasce disponível** (não existe "pausado" para público).
5. **Não liga público a conjunto.** Só cria.
6. **Lista de clientes nunca aparece no chat em claro.** A skill não abre o CSV: o script local transforma os dados em código e mostra só contagens. No modo MCP, os códigos passam pela conversa e o aluno é avisado antes (ver `customer-match.md`, passo 2).
7. **Não cria evento padrão fora de contexto.** Só a opção [2] mexe com evento personalizado, e só para alimentar um público da mesma sessão.

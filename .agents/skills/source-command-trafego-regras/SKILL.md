---
name: "source-command-trafego-regras"
description: "Cria automações no Meta Ads. Regras automáticas com gatilho de CPA, CPL, ROAS, CTR, frequência ou gasto que pausam, ajustam orçamento ou avisam por e-mail nativo da Meta (ações PAUSE, CHANGE_BUDGET, CHANGE_CAMPAIGN_BUDGET e NOTIFICATION), programação de liga e pausa de conjunto por horário (adset_schedule) e gestão das regras existentes. No modo MCP, a skill desenha a regra e o aluno cria no Gerenciador com passo a passo (o conector não tem regra automática); a programação por horário segue pelo MCP. No modo App, tudo pela Marketing API. Toda regra nasce desativada. Use quando o aluno pedir \"automatizar\", \"regra automática\", \"se CPA passar de X pause\", \"me avisa por e-mail se o gasto passar de R$ 500\", \"rodar campanha só em horário comercial\", \"programar liga e pausa\"."
---

# source-command-trafego-regras

Use esta skill quando o usuário pedir o comando `/trafego-regras` do workshop (ou `trafego-regras`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/trafego-regras.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Trafego Regras. Automação, Alertas e Programação

Cria automações em 3 frentes: regras automáticas da Meta (pausar, ajustar orçamento ou avisar por e-mail nativo da Meta), programação de entrega por horário dos conjuntos e gestão das regras existentes. Tudo roda na estrutura da Meta, sem depender do computador do aluno ligado.

A especificação completa está em `.claude/skills/trafego-regras/SKILL.md`. Este command é o orquestrador.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo`. Leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme a seção "Contexto Persistente do Negócio" do CLAUDE.md). O resumo traz o preço (ticket) e o tipo do produto, usados nas validações de gatilho. Pergunte só o que o resumo não tem (CPA alvo, margem).

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia `META_AUTH_MODO` com `grep "^META_AUTH_MODO=" .env | cut -d= -f2-`.

- **Se vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive o legado `HIBRIDO`): acione `/trafego-conexao` e aguarde a conclusão. Não tente adivinhar, não caia em outro caminho e não peça credencial avulsa.
- **Se `MCP_CONECTOR`:** confirme que existe uma tool cujo nome termina em `ads_get_ad_accounts`. Se nenhuma estiver disponível, peça ao aluno para reabrir o Claude Code; se persistir, volte ao `/trafego-conexao`. Se a conta vier como não liberada no MCP, explique e ofereça o modo App pelo `/trafego-conexao`. Confira também que `FB_AD_ACCOUNT_ID` tem valor (`grep -q "^FB_AD_ACCOUNT_ID=." .env`); se faltar, a opção "Validar" do `/trafego-conexao` completa.
- **Se `APP`:** confirme que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` têm valor no `.env` (`grep -q "^NOME=." .env`, com o ponto: linha vazia conta como ausente). Se faltar algum, acione `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

### 0.3 Seleção de conta de anúncio (multi-conta)
1. Leia `FB_AD_ACCOUNT_IDS` no `.env`. Se não existir ou tiver 1 conta, use `FB_AD_ACCOUNT_ID` sem perguntar.
2. Com 2 ou mais contas, pergunte qual usar, mostrando os nomes (MCP: `ads_get_ad_accounts`; App: `curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name&limit=100&access_token=***TOKEN_MASCARADO***"`, com o token lido do `.env` na própria chamada).
3. Guarde a conta escolhida só para esta execução.

### 0.4 Ler especificações
- `.claude/skills/trafego-regras/SKILL.md`
- A sub-skill da opção escolhida

---

## Passo 1. Menu

```
🤖 TRÁFEGO REGRAS. Automação Meta Ads

[1] Regra automática Meta Ads
    se CPA, CPL, ROAS, CTR, frequência ou gasto bater o limite:
    pausa, ajusta orçamento ou te avisa por e-mail

[2] Liga e pausa por horário
    o conjunto só entrega nos dias e horários que você escolher

[3] Gerir regras existentes
    listar, ativar, desativar, editar, excluir, ver histórico

Digite o número:
```

## Passo 2. Sub-fluxo

| Escolha | Sub-skill | MCP (padrão) | App (`curl`) |
|---|---|---|---|
| [1] | `regra-automatica.md` | a skill desenha a regra e o aluno cria no Gerenciador (passo a passo) | `POST /act_<id>/adrules_library` |
| [2] | `liga-pausa-schedule.md` | `ads_update_entity` (`adset_schedule`) | `POST /<adset_id>` (`adset_schedule`) |
| [3] | `gerir-regras.md` | passo a passo no Gerenciador (Regras automatizadas) | `GET` e `POST` em `/act_<id>/adrules_library` e `/<rule_id>`; excluir sem `curl -X DELETE` direto |

Anúncio do tempo, conforme o caminho:
- `🔍 Próximo passo: validar o gatilho e a ação e criar a regra desativada (4 passos). Tempo estimado: cerca de 30 segundos.` (App)
- `🔍 Próximo passo: desenhar a regra e montar o passo a passo do Gerenciador (4 passos). Tempo estimado: cerca de 60 segundos.` (MCP)
- `🔍 Próximo passo: conferir o orçamento do conjunto e aplicar a programação por horário (3 passos). Tempo estimado: cerca de 30 segundos.` (opção 2)

---

## Passo 3. Coletar inputs

Cada sub-skill define seus inputs, uma pergunta por mensagem:
- **[1] Regra automática:** gatilho (métrica, operador, valor, janela), gasto mínimo, ação (pausar, ajustar orçamento, avisar por e-mail), escopo (campanha, conjunto ou anúncio), frequência.
- **[2] Liga e pausa:** conjunto, dias da semana, hora de início e hora de fim.
- **[3] Gerir regras:** qual regra e qual operação.

---

## Passo 4. Validações

A skill bloqueia ou alerta:
- Gatilho sem gasto mínimo (pausa em decisão precipitada).
- Janela do gatilho com gasto menor que 1 vez o CPA alvo (dado imaturo).
- Conjunto com orçamento diário (ou campanha CBO com orçamento diário) no sub-fluxo [2]: a programação exige orçamento total, e a Meta costuma recusar a troca num conjunto ou campanha já publicados. A skill confere antes e explica as saídas.

---

## Passo 5. Resumo e bloco 🛡️

Resumo em linguagem natural e, quando a skill vai escrever na conta, bloco 🛡️ do CLAUDE.md com o Preview YAML. Um "sim" por lote. Excluir regra é sempre à parte e nunca roda por `curl -X DELETE` direto.

No modo MCP do sub-fluxo [1], não há bloco 🛡️: quem cria a regra é o aluno, no Gerenciador, seguindo o passo a passo.

---

## Passo 6. Criação

- Toda regra nasce **desativada** (no App, `status: DISABLED`; no MCP, o aluno desliga a regra logo depois de criar).
- Programação por horário aplicada pelo MCP ou pelo App, com reset de aprendizado avisado antes.
- Registro em `meus-produtos/_global/trafego/regras/{id}.md` (ou pelo nome, se criada no Gerenciador).
- Atualiza `meus-produtos/_global/trafego/regras/INDEX.md`.

✅ Concluído: regra criada (desativada). Caminho do registro: `meus-produtos/_global/trafego/regras/INDEX.md`.

---

## Passo 7. Próximos passos

```
Próximos passos:

- Para ativar a regra: /trafego-regras → opção 3 → B. Ativar
  (ou no Gerenciador → Regras automatizadas)
- Para ver o histórico de execução: /trafego-regras → opção 3 → F
  (ou no Gerenciador, na própria regra)
- Para listar todas as regras: /trafego-regras → opção 3 → A
- Para revisar as campanhas afetadas pela regra: /trafego-otimizar
```

---

## Princípios

1. **Toda regra nasce desativada.** O aluno ativa de forma explícita.
2. **Resumo e confirmação antes de criar.**
3. **Um "sim" por lote.** Exclusão sempre à parte.
4. **Intervalo mínimo de 24h** entre ações da mesma regra, para evitar ciclo.
5. **Jeito de desfazer documentado:** desativar primeiro; excluir só se o aluno insistir, com confirmação própria e sem `curl -X DELETE` direto.
6. **Não cria regra com dado imaturo.**
7. **O aviso usa o canal nativo da Meta** (e-mail para o administrador do Business). Para relatório diário por WhatsApp ou Telegram, use `/ads-relatorio`.
8. **Programação por horário exige orçamento total.** A skill confere antes.

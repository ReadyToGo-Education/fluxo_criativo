---
name: "source-command-trafego-criativos"
description: "Inteligência criativa por métricas de atenção, intenção e conversão para Meta Ads. 6 módulos de investigação (leitura de atenção com curva de retenção, intenção criativa com detecção de curiosidade vazia, conversão por temperatura cold/warm, diagnóstico criativo em 4 camadas, DNA comportamental ligado aos tipos da Mandala da Criatividade e briefing dos próximos testes). Nunca executa ação na conta e não produz o criativo: encaminha a produção para /copy-anuncio, /criativo-estatico, /mandala-de-anuncios e as skills de vídeo. Lê o resumo do produto e consome dados via /trafego-insights. Use quando o aluno pedir \"por que esse criativo não vende?\", \"que criativo devo testar?\", \"análise criativa\", \"briefing de criativos\", \"DNA dos meus criativos\"."
---

# source-command-trafego-criativos

Use esta skill quando o usuário pedir o comando `/trafego-criativos` do workshop (ou `trafego-criativos`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/trafego-criativos.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Tráfego Criativos. Inteligência Criativa por Métricas

Investigação profunda de criativos por métricas de comportamento. Descobre onde cada criativo quebra no funil de atenção → intenção → conversão, encontra padrões entre os vencedores (inclusive o tipo da Mandala que vende na conta) e gera os briefings dos próximos testes.

A especificação técnica completa está em `.claude/skills/trafego-criativos/SKILL.md`. Este command é o orquestrador.

**Diferença vs outras skills:**
- `/trafego-analise` output [3]: foto rápida dos criativos (tier, fadiga, Gap Finder da Mandala). Esta skill não repete isso.
- `/copy-anuncio`, `/criativo-estatico`, `/mandala-de-anuncios`, `/video-heygen`, `/video-remotion`, `/video-editar`: produzem a peça. Esta skill diz o que produzir e por quê.

---

## Passo 0. Contexto, conexão e entrada

### 0.1 Produto ativo
Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gerar conforme a seção "Contexto Persistente do Negócio" do CLAUDE.md). Do resumo saem, sem perguntar: nome do produto, ticket, tipo, Quadro, Furadeira, público, Urgências Ocultas e Decorados principais.

### 0.2 Conexão Meta (gate duro)
Ler `META_AUTH_MODO` no `.env` (`grep "^META_AUTH_MODO=" "{RAIZ_PROJETO}/.env" | cut -d= -f2-`). Toda leitura do `.env` usa o caminho absoluto da raiz do projeto (`{RAIZ_PROJETO}`), nunca o relativo ao diretório atual (seção 3.3 da skill).

- **Vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive o legado `HIBRIDO`): acionar `/trafego-conexao` e aguardar, sem adivinhar nem cair em fallback.
- **`MCP_CONECTOR`:** confirmar que existe tool terminada em `ads_get_ad_entities` e que `FB_AD_ACCOUNT_ID` tem valor (`grep -q "^FB_AD_ACCOUNT_ID=." "{RAIZ_PROJETO}/.env"`; se faltar, a opção "Validar" do `/trafego-conexao` completa). Conta não liberada pela Meta no conector: avisar e oferecer o modo App pelo `/trafego-conexao`.
- **`APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` têm valor com `grep -q "^NOME=." "{RAIZ_PROJETO}/.env"` (sem exibir valor; o ponto faz a linha vazia contar como ausente).

Esta skill só lê: não tem bloco 🛡️ porque não escreve na conta.

### 0.3 Conta de anúncios
Ler `FB_AD_ACCOUNT_IDS`. Se houver mais de uma, perguntar qual (opções numeradas).

### 0.4 Entrevista de entrada (uma pergunta por mensagem)

Aplicar o padrão compartilhado da `/trafego-diagnostico` (Passos 0.4 a 0.9 daquele SKILL.md) mais o escopo (Passo 0.55 do SKILL.md desta skill), sempre uma pergunta por vez, com opções numeradas:

1. Filtro de status (ativas / ativas + com problemas / ativas + pausadas).
2. Filtro de objetivo (vendas / leads / vendas + leads / todas).
3. Escopo (conta completa ou campanhas específicas).
4. Outros produtos na conta (1. só o produto ativo / 2. mais de um).
5. Meta de CPA/CPL (1. usar 50% do ticket / 2. meta própria).
6. Confirmar o mapeamento campanhas → produtos.
7. Margem (1. informar as 3 taxas: plataforma, reembolso e imposto / 2. pular).
8. Período (7d, 14d ou 30d).

Nível da análise é fixo nesta versão: só métricas (não perguntar). O que o resumo ou a conversa já trouxeram não é perguntado de novo.

---

## Passo 1. Menu ou linguagem natural

### Se o aluno chamou apenas "tráfego criativos"

Apresentar o menu da seção 1 do SKILL.md (7 opções).

### Se pediu algo específico

Pular o menu e encaminhar conforme a tabela de linguagem natural do SKILL.md.

---

## Passo 2. Executar módulo

### Opção [1]. Inteligência Criativa Completa

🔍 Próximo passo: rodar a inteligência criativa completa (6 módulos). Tempo estimado: 2 a 4 minutos.

Rodar na ordem fixa (seção 2 do SKILL.md):
1. Leitura de atenção (`leitura-atencao.md`).
2. Intenção criativa (`intencao-criativa.md`).
3. Conversão criativa (`conversao-criativa.md`).
4. Diagnóstico criativo (`diagnostico-criativo.md`).
5. DNA criativo, com os tipos da Mandala (`dna-criativo.md`).
6. Briefing criativo (`briefing-criativo.md`).
7. Relatório consolidado.

Progresso:
```
⏳ Passo 1/7: leitura de atenção dos criativos.
⏳ Passo 2/7: intenção criativa.
⏳ Passo 3/7: conversão criativa.
⏳ Passo 4/7: diagnóstico por criativo.
⏳ Passo 5/7: DNA dos criativos que mais vendem.
⏳ Passo 6/7: briefings dos próximos testes.
⏳ Passo 7/7: consolidação do relatório.
```

### Opções [2] a [7]. Módulos individuais

🔍 Próximo passo: rodar o módulo {nome do módulo}. Tempo estimado: cerca de 90 segundos.

Aplicar a sub-skill correspondente. Entregar o relatório de 7 seções + YAML.

Ao terminar:
```
✅ Concluído: {módulo} gerado.
```

---

## Passo 3. Entregar resultado

1. **Relatório humano** (7 seções, seção 11 do SKILL.md).
2. **Urgência criativa** (crítica, alta, média, baixa ou monitorar).
3. **Camada transversal:** o que os dados dizem, o que NÃO dizem, o que NÃO fazer, próximo teste.
4. **Explicação obrigatória** em cada métrica e gráfico.
5. **Tradução VTSD** com as Urgências Ocultas, os Decorados e a Furadeira reais do resumo do produto.

Se o briefing trouxer texto pronto de anúncio (gancho, headline, CTA), aplicar antes a regra "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md (Manual da Copy + `revisora`), sem mencionar a revisão.

Registrar a linha no `meus-produtos/{ativo}/entregas/trafego/criativos/INDEX.md` (seção 14 do SKILL.md).

---

## Passo 4. Handoff

| Achado | Próximo passo |
|--------|---------------|
| Briefing de teste pronto | Produzir: `/copy-anuncio`, `/mandala-de-anuncios`, `/criativo-estatico`; vídeo: `/video-heygen`, `/video-remotion`, `/video-editar`. Depois testar com `/trafego-testes` |
| Criativo com falha confirmada | "Quer pausar ou ajustar via `/trafego-otimizar`?" |
| Vencedor confirmado (régua de vencedor da seção 10 do SKILL, não o piso de leitura de 15 vendas) | "Antes de escalar, rodo o falso vencedor da `/trafego-diagnostico`? Depois, `/trafego-escalar`." |
| Problema na página, não no criativo (`falha_pos_clique`) | `/trafego-oferta-funil` |
| Falso conversor criativo (vende só no remarketing) | `/trafego-testes` para isolar em público frio, ou `/trafego-otimizar` para pausar o anúncio nos conjuntos frios (com o bloco 🛡️ de lá) |
| Tipo da Mandala ausente na conta | Gap Finder do output [3] da `/trafego-analise` e produção em `/copy-anuncio` |

---

## Passo 5. Export HTML (opcional)

Oferecer o export com a mecânica de tema da seção 1 do `.claude/skills/trafego-analise/sub-skills/_export-html.md` (na primeira vez, os 3 temas numerados + "Não"; depois, o tema salvo em `EXPORT_TEMA`).

Se sim:

🔍 Próximo passo: montar o relatório visual da análise criativa em HTML. Tempo estimado: cerca de 90 segundos.

Acionar `_export-html.md`. Salvar em `meus-produtos/{ativo}/entregas/trafego/criativos/` e abrir no navegador.

```
✅ Concluído: análise criativa exportada. Caminho: {raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\criativos\{arquivo}.html
```

---

## Princípios que este command nunca viola

Carregar e respeitar os princípios da seção 16 do SKILL.md. Em especial:

1. **Nunca executar ação na conta.**
2. **Nunca avaliar criativo por métrica isolada.**
3. **Hook Rate alto não significa criativo bom.**
4. **CTR baixo com CPA bom é criativo qualificado.**
5. **CTR alto com CPA ruim é curiosidade vazia.**
6. **Sem conteúdo visual, toda conclusão é hipótese comportamental.**
7. **Dados via `/trafego-insights`.** Nunca duplicar fetch.
8. **Explicação obrigatória em todo output.**
9. **Imagem e vídeo analisados separadamente.**
10. **Inteligência completa segue ordem fixa.**
11. **Uma pergunta por mensagem nas perguntas iniciais.**
12. **Não perguntar o que o resumo do produto já tem.**
13. **Não produzir o criativo.** A produção vai para as skills de criação.

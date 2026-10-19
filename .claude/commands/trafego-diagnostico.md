---
name: workshop-marketing:trafego-diagnostico
description: Central de diagnóstico estratégico Meta Ads. 4 módulos de investigação (diagnóstico diferencial com 3 hipóteses competitivas, auditoria estrutural, detector de falso vencedor e score de confiança de 0 a 100 por decisão). Nunca executa ação na conta. Lê ticket, tipo, Quadro e Furadeira do resumo do produto e busca as métricas via /trafego-insights. Protege o caixa e é o freio antes de /trafego-escalar. Use quando o aluno pedir "onde está o problema?", "essa campanha é vencedora mesmo?", "minha conta está bagunçada?", "posso confiar nesse resultado?", "vale a pena escalar?", "por que meu CPA subiu?" ou "diagnóstico completo".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Tráfego Diagnóstico. Central de Diagnóstico Estratégico

Investigação profunda antes de qualquer ação. Não toca na conta. Diagnostica, classifica, recomenda e faz handoff.

A especificação técnica completa está em `.claude/skills/trafego-diagnostico/SKILL.md`. Este command é o orquestrador.

**Diferença vs `/trafego-otimizar`:**
- `/trafego-diagnostico` investiga com hipóteses concorrentes, audita a estrutura, desmascara falsos vencedores e mede a confiança. Nunca age na conta.
- `/trafego-otimizar` aponta um gargalo e propõe ações (pausar, reduzir, realocar), com confirmação antes de mexer na conta.

---

## Passo 0. Contexto, conexão e entrada

### 0.1 Produto ativo
Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (se o resumo não existir, gerar conforme a seção "Contexto Persistente do Negócio" do CLAUDE.md). Do resumo saem, sem perguntar: nome do produto, ticket (Preço), tipo (Low, Middle ou High Ticket), Quadro, Furadeira, público e Urgências Ocultas. Detalhes no Passo 0.1 do SKILL.md.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Ler `META_AUTH_MODO` no `.env`.

- **Vazio ou ausente:** acionar `/trafego-conexao` antes de prosseguir.
- **`MCP_CONECTOR`:** confirmar que existe tool terminada em `ads_get_ad_entities`. Se não houver, pedir para reabrir o Claude Code; se persistir, voltar ao `/trafego-conexao`. Conta não liberada pela Meta no conector: avisar e oferecer o modo App pelo `/trafego-conexao`.
- **`APP`:** confirmar `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` no `.env` com `grep -q` (nunca exibir o valor). Se faltar, acionar `/trafego-conexao`.

O comando nunca prossegue sem essa validação passar. Esta skill só lê: não tem bloco 🛡️ porque não escreve na conta.

### 0.3 Conta de anúncios
Ler `FB_AD_ACCOUNT_IDS`. Se houver mais de uma conta, perguntar qual usar (opções numeradas, com o nome de cada conta). Se houver só uma, usar direto.

### 0.4 Entrevista de entrada (uma pergunta por mensagem)

Aplicar os Passos 0.4 a 0.9 do SKILL.md, sempre uma pergunta por vez, com opções numeradas:

1. Filtro de status (ativas / ativas + com problemas / ativas + pausadas).
2. Filtro de objetivo (vendas / leads / vendas + leads / todas).
3. Outros produtos na conta (1. só o produto ativo / 2. mais de um). Produto cadastrado no Severino tem o ticket lido do resumo dele; só se pergunta o que não estiver cadastrado.
4. Tipo de funil (perpétuo ou lançamento), só se o objetivo das campanhas não deixar claro.
5. Meta de CPA/CPL (1. usar 50% do ticket / 2. meta própria).
6. Confirmar o mapeamento campanhas → produtos.
7. Margem (1. informar as 3 taxas: plataforma, reembolso e imposto / 2. pular).
8. Período (7d, 14d ou 30d).

O que o resumo do produto ou a conversa já trouxeram não é perguntado de novo. Antes do menu, mostrar em poucas linhas o resumo do que será analisado.

---

## Passo 1. Menu ou linguagem natural

### Se o aluno chamou apenas "tráfego diagnóstico"

Apresentar o menu da seção 1 do SKILL.md:

```
╔══════════════════════════════════════════════════════════════╗
║  TRÁFEGO DIAGNÓSTICO. Central de Diagnóstico Estratégico     ║
╚══════════════════════════════════════════════════════════════╝

Qual investigação você quer rodar?

[1]  DIAGNÓSTICO COMPLETO        roda os 4 módulos e consolida
                                 (score → auditoria → falso vencedor → diferencial)

[2]  DIAGNÓSTICO DIFERENCIAL     3 hipóteses competitivas com peso
                                 onde está o problema real?

[3]  AUDITORIA ESTRUTURAL        saúde da arquitetura da conta
                                 a estrutura atrapalha o algoritmo?

[4]  FALSO VENCEDOR              campanhas que parecem boas mas enganam
                                 posso confiar nos vencedores?

[5]  SCORE DE CONFIANÇA          confiança numérica por decisão
                                 os dados suportam essa conclusão?

Digite o número:
```

### Se o aluno pediu algo específico

Pular o menu e encaminhar direto conforme a tabela "Entradas por linguagem natural" da seção 1 do SKILL.md.

---

## Passo 2. Executar o módulo escolhido

### Opção [1]. Diagnóstico Completo

🔍 Próximo passo: rodar o diagnóstico completo da conta (4 módulos). Tempo estimado: 2 a 4 minutos.

Rodar na ordem fixa (seção 2 do SKILL.md):
1. Score de confiança (sub-skill `score-confianca.md`).
2. Auditoria estrutural (sub-skill `auditoria-estrutural.md`).
3. Falso vencedor (sub-skill `falso-vencedor.md`).
4. Diagnóstico diferencial (sub-skill `diagnostico-diferencial.md`).
5. Consolidar o sumário executivo com urgência e proteção de caixa.

Progresso:
```
⏳ Passo 1/5: score de confiança dos dados.
⏳ Passo 2/5: auditoria da estrutura da conta.
⏳ Passo 3/5: verificação de falsos vencedores.
⏳ Passo 4/5: investigação do gargalo principal.
⏳ Passo 5/5: consolidação do relatório.
```

Aplicar a inteligência cruzada entre módulos da seção 2 do SKILL.md.

### Opção [2]. Diagnóstico Diferencial

🔍 Próximo passo: montar o diagnóstico diferencial (3 hipóteses com peso). Tempo estimado: cerca de 90 segundos.

Aplicar a sub-skill `diagnostico-diferencial.md`. Entregar o relatório de 7 seções + bloco YAML.

### Opção [3]. Auditoria Estrutural

🔍 Próximo passo: auditar a estrutura da conta (6 eixos). Tempo estimado: cerca de 90 segundos.

Aplicar a sub-skill `auditoria-estrutural.md`. Entregar o score de saúde (0 a 100) + limpezas recomendadas.

### Opção [4]. Falso Vencedor

🔍 Próximo passo: verificar falsos vencedores. Tempo estimado: cerca de 60 segundos.

Aplicar a sub-skill `falso-vencedor.md`. Classificar cada entidade do escopo.

### Opção [5]. Score de Confiança

🔍 Próximo passo: calcular a confiança por decisão. Tempo estimado: cerca de 30 segundos.

Aplicar a sub-skill `score-confianca.md`. O cálculo sai do script `.claude/skills/trafego-diagnostico/scripts/calcular_score_confianca.py`, rodado com o interpretador detectado na sessão (`python3` ou `py -3`).

Ao terminar qualquer módulo:
```
✅ Concluído: {módulo} gerado.
```

---

## Passo 3. Entregar resultado

Para qualquer módulo, entregar:

1. **Relatório humano** nas 7 seções (seção 8 do SKILL.md), ou nas seções aplicáveis ao módulo.
2. **Bloco YAML estruturado** (seção 11 do SKILL.md).
3. **Urgência** (crítica, alta, média, baixa ou monitorar).
4. **Proteção de caixa** (R$ perdidos por dia, projeção até o fim do mês).
5. **Tradução VTSD** com o Quadro, a Furadeira e as Urgências Ocultas reais do resumo do produto (seção 9 do SKILL.md).

Incluir sempre a camada transversal: o que os dados dizem, o que NÃO dizem, o que NÃO fazer e o próximo teste.

Registrar a linha no `meus-produtos/{ativo}/entregas/trafego/diagnostico/INDEX.md` (seção 13 do SKILL.md) e, se houver diagnóstico anterior da mesma conta e módulo, abrir o relatório com o bloco de evolução.

---

## Passo 4. Handoff

Conforme a seção 12 do SKILL.md, sugerir o próximo passo:

- Ação operacional necessária: "Quer que eu rode `/trafego-otimizar` para aplicar as ações recomendadas?"
- Falso vencedor ou score abaixo de 50 bloqueou a escala: "Recomendo `/trafego-otimizar` antes de escalar."
- Estrutura precisa de limpeza: "Quer rodar `/trafego-otimizar` em modo lote para consolidar?"
- Precisa de mais dados: "Aguarde {X} dias e rode o diagnóstico de novo."
- Vencedor real confirmado com score 50 ou mais: "Campanha pronta. Quer rodar `/trafego-escalar`?"
- Hipótese criativo forte: `/trafego-criativos`. Hipótese oferta/funil forte: `/trafego-oferta-funil`. Atribuição fraca: `/trafego-pixel`.

---

## Passo 5. Export HTML (opcional)

Oferecer o export com a mecânica de tema da seção 14 do SKILL.md (na primeira vez, os 3 temas numerados + "Não"; depois, o tema salvo em `EXPORT_TEMA`).

Se sim:

🔍 Próximo passo: montar o relatório visual do diagnóstico em HTML. Tempo estimado: cerca de 90 segundos.

Acionar a sub-skill `_export-html.md`, salvar em `meus-produtos/{ativo}/entregas/trafego/diagnostico/` e abrir no navegador.

```
✅ Concluído: diagnóstico exportado. Caminho: {raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\diagnostico\{arquivo}.html
```

---

## Princípios que este command nunca viola

Carregar e respeitar os princípios da seção 15 do SKILL.md. Em especial:

1. **Nunca executar ação na conta.** Diagnóstico é leitura + interpretação + recomendação.
2. **Separar sintoma de causa.** Nunca tratar métrica isolada como conclusão.
3. **Toda recomendação tem confiança declarada.**
4. **Sempre dizer o que os dados NÃO dizem.**
5. **Sempre dizer o que NÃO fazer.**
6. **Sempre sugerir o próximo teste.** Hipótese sem teste de validação é opinião, não diagnóstico.
7. **Comparação temporal obrigatória.** Período atual vs anterior.
8. **Dados via `/trafego-insights`.** Nunca duplicar fetch.
9. **Diagnóstico completo segue a ordem fixa.** Score → auditoria → falso vencedor → diferencial.
10. **Proteção de caixa é cálculo, não opinião.** R$ por dia, projeção até o fim do mês.
11. **Atribuição da Meta não é lucro real.** Sempre declarar essa limitação.
12. **Mínimo de 7 dias para decisões estruturais.** Abaixo disso, marcar `dados_insuficientes`.
13. **Não perguntar o que o resumo do produto já tem.**

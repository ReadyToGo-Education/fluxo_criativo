---
name: workshop-marketing:trafego-oferta-funil
description: Diagnóstico pós-clique, leitura da página e análise da oferta para Meta Ads, a partir dos números do funil. Lê a página real (Claude in Chrome primeiro, WebFetch depois), compara com o anúncio, dá nota à oferta usando o Quadro e a Furadeira reais do produto, verifica o checkout e o upsell e monta o plano de correção. 6 módulos (pós-clique, página, congruência, oferta, checkout, plano). Nunca executa ação na conta nem modifica páginas; as correções vão para /feedback-pagina, /feedback-low-ticket, /pagina-checkout, /pagina-ajuste, /pagina-performance, /copy-pagina e /lt-pagina. Use quando o aluno pedir "por que minha página não converte?", "o anúncio e a página estão alinhados?", "a oferta é forte?", "o checkout está quebrando?", ou quando outra skill detectar gargalo fora do Meta.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion, WebFetch
model: sonnet
---

# Tráfego Oferta Funil. Diagnóstico Pós-Clique e Página

Diagnostica onde o funil pós-clique quebra: página, oferta, congruência ou checkout. Lê a página real, compara com o anúncio e cruza tudo com os números da conta.

A especificação técnica completa está em `.claude/skills/trafego-oferta-funil/SKILL.md`. Este command é o orquestrador.

**Diferença vs `/feedback-pagina`:**
- `/trafego-oferta-funil` parte dos **números** (onde o funil perde gente e quanto isso custa) e diz qual parte da página ou da oferta explica a perda.
- `/feedback-pagina` (e `/feedback-low-ticket`, em página low ticket) faz a **auditoria completa de copy, estrutura e design** e corrige. É para onde este command encaminha quando a página é a causa.

---

## Passo 0. Contexto, conexão e entrada (uma pergunta por mensagem)

### 0.1 Produto ativo
Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (gerar conforme o CLAUDE.md se não existir). Do resumo saem, sem perguntar: ticket, tipo, Quadro, Furadeira, público, objeções principais e Urgências Ocultas. O ticket define a faixa de benchmark; o Quadro e a Furadeira são a régua da oferta.

### 0.2 Conexão Meta
Ler `META_AUTH_MODO`. Vazio: `/trafego-conexao`. `MCP_CONECTOR`: confirmar tool terminada em `ads_get_ad_entities` (conta não liberada pela Meta no conector: avisar e oferecer o modo App pelo `/trafego-conexao`). `APP`: confirmar `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` com `grep -q`. Só leitura, sem bloco 🛡️.

### 0.3 Conta de anúncios
Se houver mais de uma, perguntar qual (opções numeradas).

### 0.4 Entrevista de entrada

Aplicar o Passo 0 do SKILL.md (padrão compartilhado da `/trafego-diagnostico`), uma pergunta por vez, com opções numeradas:

1. Filtro de status (ativas / ativas + com problemas / ativas + pausadas).
2. Filtro de objetivo (vendas / leads / vendas + leads).
3. Escopo (conta completa ou campanhas específicas).
4. Outros produtos na conta (1. só o produto ativo / 2. mais de um).
5. Meta de CPA/CPL (1. usar 50% do ticket / 2. meta própria).
6. Confirmar o mapeamento campanhas → produtos.
7. Margem (1. informar as 3 taxas: plataforma, reembolso e imposto / 2. pular).
8. Período (7d, 14d ou 30d).
9. URL da página de vendas (ou extrair do criativo pela API).
10. Upsell ou downsell (1. tenho, vou passar os links / 2. não tenho).

O que o resumo ou a conversa já trouxeram não é perguntado de novo.

---

## Passo 1. Menu ou linguagem natural

Apresentar o menu da seção 1 do SKILL.md (7 opções). Se o pedido for específico, pular o menu.

---

## Passo 2. Executar módulo

### Opção [1]. Diagnóstico Completo

🔍 Próximo passo: rodar o diagnóstico completo de oferta e funil (6 módulos). Tempo estimado: 3 a 5 minutos.

```
⏳ Passo 1/7: funil pós-clique.
⏳ Passo 2/7: leitura da página de vendas.
⏳ Passo 3/7: comparação do anúncio com a página.
⏳ Passo 4/7: força da oferta.
⏳ Passo 5/7: checkout.
⏳ Passo 6/7: plano de correção.
⏳ Passo 7/7: consolidação do relatório.
```

### Opções [2] a [7]. Módulos individuais

🔍 Próximo passo: {nome do módulo}. Tempo estimado: cerca de 90 segundos.

Ao terminar:
```
✅ Concluído: {módulo} gerado.
```

---

## Passo 3. Leitura da página

Aplicar a seção 4 do SKILL.md, na ordem da regra 10 do CLAUDE.md:
1. Obter a URL (do aluno ou do criativo pela API).
2. Ler com o Claude in Chrome (`read_page`); se não estiver disponível, `WebFetch`.
3. Se as duas falharem: pedir para o aluno colar o texto da página ou descrever os elementos.

Este command **não edita** o `settings.local.json` nem adiciona domínio a lista de permissões. Se o Claude Code pedir autorização para ler o domínio, a decisão é do aluno na janela do próprio Claude Code.

---

## Passo 4. Funil no modo MCP

Se o modo for `MCP_CONECTOR`, descobrir com `ads_get_field_context` os campos de ação disponíveis (visita à página, carrinho, checkout iniciado) antes de declarar o funil incompleto. Se não vierem, oferecer, com opções numeradas:

```
O conector da Meta não trouxe a visita à página e o checkout desta conta.

1. Te guio para ler essas colunas no Gerenciador e você me manda os números
2. Trocar para o modo App (/trafego-conexao), que traz o funil completo
3. Seguir sem essas etapas (uso CPA e ROAS como substitutos)

Digite o número:
```

A leitura guiada está na seção 3 do SKILL.md.

---

## Passo 5. Entregar resultado

1. Relatório humano (7 seções, seção 11 do SKILL.md).
2. Urgência do funil (crítica, alta, média, baixa ou monitorar).
3. Camada transversal: o que os dados dizem, o que NÃO dizem, limitações, o que NÃO fazer.
4. Explicação obrigatória em cada métrica, gráfico e achado (a nota da oferta sempre com a tabela `Elemento | Nota | Por que essa nota`).
5. Cada correção com a skill que a executa.

Registrar a linha no `meus-produtos/{ativo}/entregas/trafego/oferta-funil/INDEX.md`.

---

## Passo 6. Handoff

| Achado | Próximo passo |
|--------|---------------|
| Copy, estrutura ou prova da página de vendas | `/feedback-pagina` |
| Página low ticket | `/feedback-low-ticket` |
| Copy precisa ser refeita | `/copy-pagina` ou `/lt-pagina` |
| Ajuste pontual numa página feita no Severino | `/pagina-ajuste` |
| Página lenta ou connect rate baixo | `/pagina-performance` |
| Checkout (ligação da página com a plataforma) | `/pagina-checkout` |
| Pixel sem disparar compra ou checkout | `/trafego-pixel` e `/pagina-pixel` |
| Problema confirmado no criativo, não na página | `/trafego-criativos` |
| Criativo com falha que precisa de ação no Meta | `/trafego-otimizar` |
| Funil saudável, oferta forte | `/trafego-diagnostico` (falso vencedor) e depois `/trafego-escalar` |

---

## Passo 7. Export HTML (opcional)

Oferecer o export com a mecânica de tema da seção 1 do `.claude/skills/trafego-analise/sub-skills/_export-html.md`.

Se sim:

🔍 Próximo passo: montar o relatório visual de oferta e funil em HTML. Tempo estimado: cerca de 90 segundos.

Acionar `_export-html.md`. Salvar em `meus-produtos/{ativo}/entregas/trafego/oferta-funil/` e abrir no navegador.

```
✅ Concluído: diagnóstico de oferta e funil exportado. Caminho: {raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\oferta-funil\{arquivo}.html
```

---

## Princípios

Carregar e respeitar os princípios da seção 16 do SKILL.md. Em especial:

1. Nunca executar ação na conta Meta.
2. Nunca modificar páginas nem configurações.
3. Nunca gerar copy nova: a correção vai para as skills de página.
4. Nunca afirmar causa de checkout sem dados do gateway.
5. Nunca tratar o ROAS da Meta como lucro real.
6. Sempre declarar limitações (leitura da página, VSL, JavaScript, backend).
7. Dados pós-clique via `/trafego-insights`.
8. Comparação temporal obrigatória (atual vs anterior).
9. Explicação obrigatória em todo output.
10. Uma pergunta por mensagem, sem repetir o que o resumo do produto já tem.
11. Margem: 3 campos, nunca mais.
12. Connect rate baixo não prova página lenta (pode ser redirecionamento, link, celular).
13. Nota da oferta não é auditoria de copy: a auditoria completa é do `/feedback-pagina`.

# Relatório de Tempo — Fluxo de Criação de Produto

> Arquivo de trabalho para calibrar os tempos em `tempo-estimado.md`.
> Atualizado a cada sessão de teste. Última atualização: 2026-05-04 (sessão 2).

---

## Metodologia

Cada etapa registra dois tempos:
- **Sistema:** tempo de processamento medido no terminal (Crunched / Churned / Worked / Cooked)
- **Reflexão:** tempo estimado que o usuário leva para responder ou decidir
- **Realista:** soma dos dois, usado para comunicar ao aluno

Critérios de reflexão por tipo de pergunta:

| Tipo de pergunta | Reflexão estimada | Motivo |
|---|---|---|
| Menu numérico simples (1/2/3) | 10 a 20s | Decisão já tomada ou óbvia |
| Nome / identidade do produto | 20 a 60s | Pode não estar decidido ainda |
| Escolha de categoria (LT x MT) | 10 a 30s | Pode ter dúvida sobre a diferença |
| Preço | 15 a 45s | Muita gente não sabe ao certo |
| Texto aberto curto (ex: especialidade) | 20 a 40s | Precisa formular em palavras |
| Texto aberto longo (ex: texto do comunicador) | 2 a 5 min | Procurar o texto, copiar, colar |
| Escolha entre opções geradas (ex: 5 Quadros) | 30 a 90s | Ler, comparar e decidir |
| Aprovação de conteúdo gerado | 15 a 40s | Ler e confirmar ou pedir ajuste |

---

## `/produto-novo` — Ramo 1 (já tem ideia)

**Medido em:** 2026-05-04

| # | Etapa | Sistema | Reflexão | Realista |
|---|---|---|---|---|
| 1 | Carregar skill + verificar produto ativo + montar tela inicial | 16s | — | 16s |
| 2 | Usuário lê o menu e escolhe (1/2/3) | — | 10 a 20s | 10 a 20s |
| 3 | Gerar pergunta "nome do produto" + usuário responde | 4s | 20 a 60s | 24 a 64s |
| 4 | Gerar pergunta "tipo do produto" + usuário responde | 3s | 10 a 30s | 13 a 33s |
| 5 | Gerar pergunta "preço" + usuário responde | 2s | 15 a 45s | 17 a 47s |
| 6 | Gerar slug + criar pastas + salvar arquivos + `painel-atualizar.py` + `painel-incremental.py` | 38s | — | 38s |

**Total do fluxo Ramo 1 (sem espera do usuário):** ~63s de sistema
**Total realista (com reflexão):** 1m30s a 3m30s

---

## `/produto-novo` — Ramo 2 (quer ideias)

> A preencher nos próximos testes.

| # | Etapa | Sistema | Reflexão | Realista |
|---|---|---|---|---|
| 1 | Carregar skill + verificar produto ativo + montar tela inicial | — | — | — |
| 2 | Gerar pergunta "especialidade" + usuário responde | — | 20 a 40s | — |
| 3 | Pesquisa de mercado completa (9 eixos) | — | — | — |
| 4 | Gerar 50 ideias de produto | — | — | — |
| 5 | Usuário escolhe a ideia | — | 60 a 120s | — |
| 6 | Confirmar tipo e preço | — | 15 a 40s | — |
| 7 | Gerar slug + criar pastas + salvar + manifest + painel | — | — | — |

---

## `/produto-concepcao`

**Medido em:** 2026-05-04

| # | Etapa | Sistema | Reflexão | Realista |
|---|---|---|---|---|
| 0 | Carregar skill + abrir painel + verificar perfil + gerar pergunta "nome do comunicador" | 28s | — | 28s |
| B0 | Usuário responde o nome | — | 5 a 15s | 5 a 15s |
| B1a | Gerar pergunta "o que é o produto?" + usuário responde | 7s | 20 a 60s | 27 a 67s |
| B1b | Gerar pergunta "resultado principal?" + usuário responde | 4s | 20 a 60s | 24 a 64s |
| B1c | (condicional) Pergunta "área da vida?" + resposta | — | 15 a 30s | — |
| B1g | Gerar 5 opções de Quadro | 45s | — | 45s |
| B1e | Usuário escolhe ou descreve o Quadro | — | 30 a 90s | 30 a 90s |
| B1s | Salvar Quadro + disparar pesquisa em background + gerar pergunta da Furadeira | 38s | — | 38s |
| B2a | Usuário responde o que é a ferramenta/produto | — | 60 a 180s | 60 a 180s |
| B2g | Gerar Furadeira (macroetapas + mecânica) | — | — | — |
| B2e | Usuário valida Furadeira | — | 30 a 60s | — |
| B2v | Gerar prompt visual da Furadeira (`/furadeira-visual`) | 98s | — | 98s |
| B2i | Usuário gera imagem no ChatGPT/Gemini e cola de volta | — | 2 a 5 min | 2 a 5 min |
| B2r | Ler imagem + validar layout + mostrar opções (1/2/3) | 24s | — | 24s |
| B2d | Usuário decide o que fazer com a imagem | — | 10 a 20s | 10 a 20s |
| B2s | Salvar imagem + atualizar perfil + gerar intro Bloco 2B + pergunta valores | 21s | — | 21s |
| B2B1 | Usuário escolhe valores (lê 10 opções e decide) | — | 30 a 60s | 30 a 60s |
| B2B2 | Gerar pergunta "o que não gosta" + usuário responde | 6s | 20 a 40s | 26 a 46s |
| B2B3 | Gerar pergunta "o que gosta" + usuário responde | 3s | 20 a 40s | 23 a 43s |
| B2B4 | Gerar pergunta "mantras/jargões" + usuário responde | 3s | 10 a 30s | 13 a 33s |
| B2B5 | Gerar pergunta "texto autêntico" + usuário envia | 4s | 2 a 5 min | 2 a 5 min |
| B2B6 | Analisar texto + gerar pergunta "referências" + usuário responde | 10s | 20 a 60s | 30 a 70s |
| B2Bg | Gerar Identidade do Comunicador completa | ~?s (confirmar) | — | — |
| B2Be | Usuário lê e valida | — | 30 a 60s | — |
| B3g | Gerar Identidade do Produto (usa pesquisa) | — | — | — |
| B3e | Usuário valida | — | 30 a 60s | — |
| B45+B6 | Decorados + Urgências Ocultas (paralelo) + Argumentos Incontestáveis (bloco único) | **97s** | — | 97s |
| B6e | Usuário valida Argumentos (+ pode adicionar dados) | — | 30 a 90s | 30 a 90s |
| R1+R2 | Salvar Argumentos + revisor-perfil + revisor-pesquisa (paralelo) + montar Passo 1/3 demográfico | **117s** | — | 117s |
| S4p1 | Usuário confirma ou ajusta dados demográficos | — | 15 a 40s | 15 a 40s |
| S4p2 | Gerar Passo 2/3 — comportamento (sonho, canais, paliativos) | 16s | — | 16s |
| S4p2e | Usuário confirma comportamento | — | 15 a 30s | 15 a 30s |
| S4p3 | Gerar Passo 3/3 — 5 objeções + resumo completo da identidade | 28s | — | 28s |
| S4p3e | Usuário aprova resumo ou troca objeção | — | 30 a 60s | 30 a 60s |
| S4g+S4v+S4r+S5 | gerador-idconsumidor + verificar-idconsumidor.py + revisor-idconsumidor + painel-incremental.py (bloco final) | **542s** | — | 542s |

## Totais do `/produto-concepcao` (sistema apenas, sem espera do usuário)

Soma dos blocos medidos:
28 + 7 + 4 + 45 + 38 + 98 + 24 + 21 + 6 + 3 + 3 + 4 + 10 + 97 + 117 + 16 + 28 + 542 = **~1.091s (~18 min de sistema)**

Blocos ainda sem medição: B2g, B2Bg, B3g (estimativa conservadora: +90s cada = +270s)

**Total sistema estimado completo: ~22 minutos**
**Total realista com reflexão do usuário: 45 a 75 minutos**

> Nota: o bloco final (S4g+S4v+S4r+S5) sozinho representa ~50% do tempo total de sistema.
> A etapa da imagem da Furadeira (B2i — usuário no ChatGPT) é o maior ponto de espera do usuário: 2 a 5 min.

---

## Resumo para `tempo-estimado.md` (a atualizar ao final)

| Operação | Tempo atual | Tempo calibrado | Status |
|---|---|---|---|
| `/produto-novo` Ramo 1 (sistema) | não registrado | ~63s | medido |
| `/produto-novo` Ramo 1 (realista) | não registrado | 1m30s a 3m30s | medido |
| Pesquisa de mercado completa (9 eixos) | 8 a 12 min | — | pendente |
| Gerar 50 ideias de produto | 60s | — | pendente |
| `painel-atualizar.py` + `painel-incremental.py` (bloco) | 15s + 30s | ~38s | medido |
| Gerar prompt visual Furadeira (`/furadeira-visual`) | não registrado | ~98s | medido, aplicado em tempo-estimado.md (2026-11-25) |
| Decorados + Urgências + Argumentos (bloco paralelo) | 90s+90s+45s | ~97s (paralelo) | medido |
| Revisores perfil + pesquisa (paralelo) + demográfico | não registrado | ~117s | medido |
| gerador-idconsumidor + revisores + painel (bloco final) | 3 a 5 min | ~9 min | medido, aplicado em tempo-estimado.md (2026-11-25) |
| `/produto-concepcao` completo (sistema) | não registrado | ~22 min | estimado |
| `/produto-concepcao` completo (realista) | não registrado | 45 a 75 min | estimado |

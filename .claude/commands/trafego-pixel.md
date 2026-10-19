---
name: workshop-marketing:trafego-pixel
description: Diagnostica os pixels do Meta Ads (Meta Pixel / conjuntos de dados) da conta de anúncios. Status de cada pixel, último disparo, eventos rastreados nos últimos 7 dias, taxa de deduplicação entre pixel e API de Conversões (CAPI) e pixels parados. Apenas leitura, nunca cria, edita ou apaga evento. Use quando o aluno perguntar "meu pixel está funcionando?", "quais eventos meu pixel rastreia?", "tem pixel sem atividade?", "qual foi o último disparo do pixel?". Para instalar o pixel numa página, use /pagina-pixel. Para criar evento personalizado que vire público, use /trafego-publicos.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Tráfego Pixel. Diagnóstico de Pixels Meta Ads

Lê e diagnostica os pixels da conta de anúncios. Apenas leitura: este command nunca configura evento, edita pixel ou cria evento personalizado.

A especificação completa está em `.claude/skills/trafego-pixel/SKILL.md`. Este command é o orquestrador.

**Onde fica cada coisa:**
- Diagnosticar o pixel (está disparando? quais eventos? a CAPI duplica?): `/trafego-pixel` (este).
- Instalar ou reinstalar o pixel numa página HTML: `/pagina-pixel`.
- Criar evento personalizado para alimentar um público: `/trafego-publicos`.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Ler `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (gerar o resumo conforme o CLAUDE.md se não existir). O pixel é da conta de anúncios, não do produto: o resumo só serve para saber o tipo de funil (venda direta espera `Purchase`, captação espera `Lead`). Se não der para inferir, perguntar com opções numeradas (Passo 0.1 do SKILL.md). Sem produto ativo, o diagnóstico roda mesmo assim.

### 0.2 Conexão Meta (gate duro)
Ler `META_AUTH_MODO` no `.env`.

- **Vazio ou ausente:** acionar `/trafego-conexao` antes de prosseguir.
- **`MCP_CONECTOR`:** confirmar que existe tool terminada em `ads_get_datasets`. Conta não liberada pela Meta no conector: avisar e oferecer o modo App pelo `/trafego-conexao`.
- **`APP`:** confirmar `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` no `.env` com `grep -q` (sem exibir valor).

Este command só lê: não tem bloco 🛡️ porque não escreve na conta.

### 0.3 Conta de anúncios (multi-conta)
Mesma lógica da `/trafego-insights`: se `FB_AD_ACCOUNT_IDS` tem 2 ou mais contas, perguntar qual usar (opções numeradas).

### 0.4 Ler especificações
- `.claude/skills/trafego-pixel/SKILL.md`
- Sub-skill conforme a escolha do aluno.

### 0.5 Sem pixel na conta
Se a leitura não encontrar nenhum pixel, orientar a criar no Meta, nesta ordem, o Gerenciador de Negócios, a Página, a conta de anúncios e o pixel. Depois, `/trafego-conexao` (se ainda não estiver conectado) e `/pagina-pixel` para instalar na página.

---

## Passo 1. Menu

```
🔍 TRÁFEGO PIXEL. Diagnóstico de Pixels

1. Status dos pixels         visão geral de saúde de todos os pixels
2. Eventos rastreados        detalhamento de um pixel específico
3. Pixels sem atividade      destaque dos pixels parados

Digite o número:
```

## Passo 2. Sub-fluxos

| Escolha | Sub-skill | Leitura principal (`APP` / `MCP_CONECTOR`) |
|---|---|---|
| 1 | `sub-skills/status-pixels.md` | `GET /act_<id>/adspixels` + `GET /<PIXEL_ID>/stats` / `ads_get_datasets` + `ads_get_dataset_stats` |
| 2 | `sub-skills/eventos-rastreados.md` | `GET /<PIXEL_ID>/stats?aggregation=event_total_counts` / `ads_get_dataset_stats` + `ads_get_dataset_quality` (opcional: `ads_pixel_event_read`, `ads_pixel_parameter_read`) |
| 3 | `sub-skills/sem-atividade.md` | `GET /act_<id>/adspixels` filtrado / `ads_get_datasets` + `ads_get_ad_account_custom_audiences` |

🔍 Próximo passo: ler os dados dos pixels da conta. Tempo estimado: cerca de 60 segundos.

Antes de ler, conferir o cache em `meus-produtos/_global/trafego/pixel/` (validade de 1h). Se houver leitura da mesma hora com os mesmos parâmetros, usar o arquivo e avisar que veio do cache.

---

## Passo 3. Apresentar diagnóstico

Cada sub-skill define o formato do output. Padrão:
- Resumo (verde, amarelo, vermelho).
- Tabela detalhada por pixel.
- Sinais críticos consolidados.
- Com 2 ou mais pixels ativos: bloco final "pixel usado por campanha" (seção 1.4 do SKILL.md).
- Handoffs sugeridos (`/pagina-pixel`, `/trafego-publicos`, `/trafego-analise` [8], `/trafego-oferta-funil`).

```
✅ Concluído: diagnóstico de pixels. Caminho: {raiz-do-projeto}\meus-produtos\_global\trafego\pixel\{arquivo}.md
```

---

## Passo 4. Próximos passos

```
Próximos passos:

- Pixel não está disparando (instalar ou reinstalar na página): /pagina-pixel
- Criar público com base em evento padrão do pixel: /trafego-publicos
- Criar evento personalizado + público: /trafego-publicos (opção de evento personalizado)
- Ver o impacto nas campanhas: /trafego-analise, opção [8] (Problemas Ocultos)
- Checkout sem disparar compra: /trafego-oferta-funil (diagnóstico de checkout) e /pagina-checkout
```

---

## Passo 5. Salvar diagnóstico

Salvar em:
```
meus-produtos/_global/trafego/pixel/{sub-fluxo}-{YYYY-MM-DD}-{hh}.md
```

O pixel pertence à conta de anúncios, por isso a pasta é global (`_global`), não a do produto ativo. Validade do cache: 1h. A próxima chamada na mesma hora lê do arquivo. Nunca gravar token no arquivo.

---

## Princípios

1. **Apenas leitura.** Nunca configurar evento, editar pixel ou criar evento personalizado. Nada de tools de criar, editar ou apagar evento do pixel.
2. **Sempre declarar a janela.**
3. **Status sempre justificado** com critério explícito (seção 3 do SKILL.md).
4. **Sinal crítico sempre ganha handoff.** Nunca deixar achado sem caminho de resolução.
5. **Token nunca aparece na tela.** No modo App, sempre `***TOKEN_MASCARADO***` na exibição.

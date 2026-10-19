# Sub-fluxo. Atalhos Compostos

Atalhos que orquestram múltiplas skills em uma única operação. Pensados para acelerar fluxos comuns que envolvem 2 ou 3 etapas de skills diferentes.

> **Aprovação: modo "lote pré-aprovado" do CLAUDE.md.** Todo atalho atravessa várias skills, então nunca roda com um "sim" implícito. A skill mostra o plano completo numerado uma vez e pede um **"aprovar tudo"** explícito. Detalhes em "Flow padrão dos atalhos", abaixo.

## Atalhos disponíveis

### Atalho A. Lookalike de compradores para campanha
**Aluno pede:** "Cria uma campanha de lookalike baseada nos meus compradores"

**Orquestração:**
```
1. /trafego-publicos opção [1] (evento padrão Purchase, 90d)
   └── cria o público "[WS] Purchase-90d-{produto-slug}" (se ainda não existe)
2. /trafego-publicos opção [5] (lookalike 1%)
   └── cria o público "[WS] LAL1pct-Compradores-{produto-slug}"
3. /trafego-criar-campanha (objetivo OUTCOME_SALES, público da etapa 2)
   └── cria campanha PAUSED
4. Devolve IDs + handoff para acompanhamento
```

**Gating:** se o público de Purchase tem menos de 100 pessoas, bloqueia o lookalike e avisa: "Você precisa de pelo menos 100 compradores para criar lookalike. Hoje tem X. Sugestão: continuar a prospecção até atingir esse número."

### Atalho B. Duplicar melhor anúncio em outro público
**Aluno pede:** "Duplica meu melhor anúncio pra testar em outro público e me sugere qual público"

**Orquestração:**
```
1. /trafego-analise opção [3] Criativos & Copy
   └── identifica o melhor anúncio da conta nos últimos 14d (tier S)
2. /trafego-publicos (consulta os públicos existentes + sugere alternativa
   a partir do público do resumo do produto ativo)
3. /trafego-testes opção [9] Duplicar com variação
   └── duplica o conjunto do melhor anúncio mudando o público
4. Devolve IDs + hipótese salva
```

**Sugestão de público alternativo:**
- Se o anúncio atual está em LAL1pct: sugerir LAL2pct ou LAL5pct (escala) ou remarketing (mais quente)
- Se o anúncio atual está em Saved-Iniciantes: sugerir Saved-Intermediarios (próximo nível)
- Se o anúncio atual está em Broad: sugerir Saved-Iniciantes do produto (mais focado)

### Atalho C. Pausar queimadores + ativar lookalike de comprador
**Aluno pede:** "Faz uma faxina: pausa o que tá queimando e ativa o lookalike dos compradores"

**Orquestração:**
```
1. acoes-lote.md → pausa tudo com ROAS<1 nos últimos 14d (com o filtro de lucro do §3.6)
2. Atalho A → cria lookalike de compradores se não existe
3. /trafego-criar-campanha com o lookalike como público principal
```

### Atalho D. Refresh criativo da campanha estagnada
**Aluno pede:** "Minha campanha X tá saturada, faz um refresh criativo"

**Orquestração:**
```
1. /trafego-analise opção [3] Criativos & Copy identifica:
   - Ângulos da Mandala já em uso na campanha (ex: Comparação, Demonstração, Prova)
   - Ângulos ausentes que poderiam funcionar (ex: Visual, Reflexão, Problema-Solução)
2. /mandala-de-anuncios sugere 3 ângulos novos a partir das Urgências Ocultas
   e dos Decorados do resumo do produto
3. /copy-anuncio escreve a copy dos 3 ângulos
4. /criativo-estatico gera a imagem de cada um
   (vídeo: /video-heygen, /video-remotion ou /video-editar)
5. /trafego-testes opção [1] cria A/B com 1 dos 3 novos vs criativo atual
6. Sinaliza para pausar o criativo atual após D+7 se ele perder
```

As etapas 2 a 4 produzem copy: elas seguem a regra "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md dentro das próprias skills, e cada peça passa pela aprovação normal do aluno antes de subir. A aprovação do "aprovar tudo" vale para as escritas na conta Meta, não dispensa a aprovação da copy.

## Flow padrão dos atalhos

Todo atalho composto:
1. **Anuncia o plano** completo e numerado antes de executar (todas as etapas, com o que cada uma escreve na conta).
2. **Pede "aprovar tudo" uma vez** (modo lote pré-aprovado do CLAUDE.md). Só uma resposta explícita como "aprovar tudo" ou "sim, aprovo tudo" libera o fluxo inteiro. Se o aluno responder outra coisa, aprovar só algumas etapas ou ficar em dúvida, cada etapa passa pelo gate 🛡️ normal, uma por vez.
3. **Executa em sequência**, aguardando cada skill terminar. Depois do "aprovar tudo", as etapas não reabrem o gate, exceto se uma chamada falhar, o aluno mudar o plano ou surgir escrita fora do plano.
4. **Em caso de falha em uma etapa**: pausa o fluxo, mostra o que foi feito até ali, pergunta se continua ou desfaz.
5. **Devolve resumo** com todos os IDs criados + como reverter cada item.
6. **DELETE nunca entra no "aprovar tudo".** Desfazer algo apagando tem sempre bloco 🛡️ e "sim" próprios (ver "Rollback por modo").

## Exemplo de preview (Atalho A)

```
🔄 ATALHO COMPOSTO: Lookalike de Compradores para Campanha

Plano (4 etapas):

[1] Criar público de Purchase 90d (se não existe)
    └── /trafego-publicos opção [1]
[2] Criar Lookalike 1% a partir dele
    └── /trafego-publicos opção [5]
[3] Criar campanha de venda direta usando o lookalike
    └── /trafego-criar-campanha
[4] Resumo final + como reverter

Configurações:
- Produto ativo: curso-tarot
- Público de origem: Purchase 90d (atual: 580 pessoas, qualidade aceitável)
- Lookalike: 1% Brasil (~2M pessoas)
- Campanha: budget R$ 50/dia, criativo a definir, status PAUSED

Aprovar tudo? Responda "aprovar tudo" para executar as 4 etapas em sequência,
ou "não" para cancelar. Se preferir aprovar etapa por etapa, responda "uma por vez".
```

## Output

```yaml
operacao: atalho_composto
atalho: lookalike_compradores
aprovacao: aprovar_tudo | etapa_por_etapa

resultados:
  audience_purchase: { id: <id_publico_purchase>, status: existing }
  audience_lal: { id: <id_lookalike>, status: created }
  campanha: { id: <id_campanha>, status: paused }

handoffs:
  - texto: "Aguardar 24h para o lookalike popular antes de ativar a campanha"
  - texto: "Para ativar a campanha quando estiver pronta"
    acao: "reativar <id_campanha>: ads_activate_entity (MCP) ou POST status=ACTIVE (APP), com gate 🛡️"
  - texto: "Para criar o criativo da campanha"
    acao: "/copy-anuncio + /criativo-estatico (ângulo em /mandala-de-anuncios)"

rollback:
  - campanha <id_campanha>: deixar PAUSED (não gasta) ou arquivar
  - lookalike <id_lookalike>: apagar só com gate próprio (ver abaixo)
  - público Purchase mantido (pode ser reutilizado)
```

> **Rollback por modo:** a campanha nasce PAUSED, então o rollback mais simples é deixá-la pausada (não gasta). Para tirá-la da lista, **arquivar** (`ads_update_entity` com `status=ARCHIVED` no MCP, `POST /<id>` com `status=ARCHIVED` no APP, com gate 🛡️). Apagar de fato:
> - **Lookalike / público:** no MCP, `ads_delete_custom_audience`, com bloco 🛡️ e "sim" próprios, fora de qualquer lote. No APP não existe tool de exclusão: não rodar `curl -X DELETE` inline. Oferecer manter o público (não gasta nada) ou, se o aluno quiser mesmo apagar, guiar a exclusão no Gerenciador (Públicos, marcar o público, Excluir) ou mostrar o comando mascarado (`***TOKEN_MASCARADO***`) para ele rodar manualmente.
> - **Campanha:** o MCP não apaga campanha, conjunto nem anúncio. Manter PAUSED, arquivar, ou guiar a exclusão manual no Gerenciador. No APP, mesma regra: sem `curl -X DELETE` inline.

## Princípios

1. **Atalhos não inventam etapas.** Todas as etapas correspondem a skills e sub-skills existentes.
2. **"Aprovar tudo" explícito para o fluxo todo**, no modo lote pré-aprovado do CLAUDE.md. Sem ele, gate por etapa.
3. **Cada etapa segue suas próprias regras** (preview, status PAUSED, aprovação de copy etc.) internamente.
4. **Falha intermediária pausa o fluxo**, sem rollback automático. O aluno decide.
5. **Atalho não substitui** os fluxos individuais. É camada de conveniência.
6. **Modo e lacunas são herdados das skills chamadas.** O atalho composto não fala com a Graph API direto: cada etapa roda na sua própria skill, que já roteia por `META_AUTH_MODO` (`MCP_CONECTOR` ou `APP`). Criar lookalike **não é mais lacuna** do MCP: a `/trafego-publicos` cria pelo `ads_create_custom_audience` (subtipo LOOKALIKE). Se a Meta recusar o subtipo na prática, a própria `/trafego-publicos` cai no passo a passo guiado no Gerenciador, e o atalho espera o aluno concluir antes de seguir. Se a conta não estiver liberada no conector, o atalho para e oferece trocar para o modo App pelo `/trafego-conexao`.
7. **DELETE é sempre separado.** Nunca faz parte do plano aprovado; cada exclusão tem bloco 🛡️ e "sim" próprios.

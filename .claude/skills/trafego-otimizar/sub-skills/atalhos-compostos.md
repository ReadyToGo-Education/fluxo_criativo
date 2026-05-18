# Sub-fluxo. Atalhos Compostos

Atalhos que orquestram múltiplas skills em uma única operação. Pensados para acelerar fluxos comuns que envolvem 2 ou 3 etapas de skills diferentes.

## Atalhos disponíveis

### Atalho A. Lookalike de compradores → campanha
**Aluno pede:** "Cria uma campanha de lookalike baseada nos meus compradores"

**Orquestração:**
```
1. /trafego-publicos opção 1 (evento padrão Purchase, 90d)
   └── cria audience "[FC] Purchase-90d-curso-tarot"
2. /trafego-publicos opção 5 (lookalike 1%)
   └── cria audience "[FC] LAL1pct-Compradores-curso-tarot"
3. /trafego-criar-campanha (objetivo OUTCOME_SALES, audience da etapa 2)
   └── cria campanha PAUSED
4. Devolve IDs + handoff para acompanhamento
```

**Gating:** se a audience de Purchase tem < 100 pessoas, bloqueia LAL e avisa: "Você precisa de pelo menos 100 compradores para criar lookalike. Hoje tem X. Sugestão: continuar prospecção até atingir esse número."

### Atalho B. Duplicar melhor anúncio em outro público
**Aluno pede:** "Duplica meu melhor anúncio pra testar em outro público e me sugere qual público"

**Orquestração:**
```
1. /trafego-analise opção [3] Criativos
   └── identifica melhor ad da conta nos últimos 14d (tier S)
2. /trafego-publicos (consulta as audiences existentes + sugere alternativa
   baseada na análise da identidade do consumidor do produto ativo)
3. /trafego-testes opção [8] duplicar-variando
   └── duplica o adset do melhor ad mudando audience
4. Devolve IDs + hipótese salva
```

**Sugestão de público alternativa:**
- Se ad atual está em LAL1pct: sugerir LAL2pct ou LAL5pct (escala) ou retargeting (mais quente)
- Se ad atual está em Saved-Iniciantes: sugerir Saved-Intermediarios (próximo nível)
- Se ad atual está em Broad: sugerir Saved-Iniciantes do produto (mais focado)

### Atalho C. Pausar queimadores + ativar lookalike de comprador
**Aluno pede:** "Faz uma faxina: pausa o que tá queimando e ativa o lookalike dos compradores"

**Orquestração:**
```
1. acoes-lote.md → pausa tudo com ROAS<1 nos últimos 14d
2. atalho A → cria LAL de compradores se não existe
3. /trafego-criar-campanha com a LAL como audience principal
```

### Atalho D. Refresh criativo da campanha estagnada
**Aluno pede:** "Minha campanha X tá saturada, faz um refresh criativo"

**Orquestração:**
```
1. /trafego-analise opção [3] Criativos identifica:
   - Ângulos da Mandala já em uso na campanha (ex: Tipo 1, 5, 12)
   - Ângulos ausentes que poderiam funcionar (ex: Tipo 7, 14, 16)
2. Sugere 3 novos ângulos da Mandala VTSD
3. Aciona /copy-anuncio para gerar copy dos 3
4. Aciona /criativo-estatico ou /video-heygen conforme escolha
5. /trafego-testes opção [1] cria A/B com 1 dos 3 novos vs criativo atual
6. Sinaliza para pausar criativo atual após D+7 se vencido
```

## Flow padrão dos atalhos

Todo atalho composto:
1. **Anuncia o plano** completo antes de executar (mostrar todas as etapas).
2. **Pede confirmação SIM** uma vez — aplicada para todo o fluxo.
3. **Executa em sequência**, aguardando cada skill terminar.
4. **Em caso de falha em uma etapa**: pausa o fluxo, mostra o que foi feito até ali, pergunta se continua ou desfaz.
5. **Devolve resumo** com todos os IDs criados + comandos de reversão.

## Exemplo de preview (Atalho A)

```
🔄 ATALHO COMPOSTO: Lookalike de Compradores → Campanha

Plano (4 etapas):

[1] Criar audience de Purchase 90d (se não existe)
    └── /trafego-publicos opção 1
[2] Criar Lookalike 1% a partir dela
    └── /trafego-publicos opção 5
[3] Criar campanha de venda direta usando a LAL
    └── /trafego-criar-campanha
[4] Resumo final + comandos de reversão

Configurações:
- Produto ativo: curso-tarot
- Audience source: Purchase 90d (atual: 580 pessoas — qualidade aceitável)
- LAL: 1% Brasil (~2M pessoas)
- Campanha: budget R$ 50/dia, criativo a definir, status PAUSED

Confirma executar todas as 4 etapas? (digite SIM)
```

## Output

```yaml
operacao: atalho_composto
atalho: lookalike_compradores

resultados:
  audience_purchase: { id: 6123456789, status: existing }
  audience_lal: { id: 6123456795, status: created }
  campanha: { id: 9876543210, status: paused }

handoffs:
  - texto: "Aguardar 24h para LAL popular antes de ativar a campanha"
  - texto: "Para ativar campanha quando estiver pronta"
    comando: "POST /9876543210 { status: ACTIVE }"
  - texto: "Para criar criativo da campanha"
    skill: /copy-anuncio + /criativo-estatico

rollback:
  - DELETE /9876543210  # campanha
  - DELETE /6123456795  # LAL
  - (audience Purchase mantida — pode ser reutilizada)
```

## Princípios

1. **Atalhos não inventam etapas.** Todas as etapas correspondem a sub-skills existentes.
2. **Confirmação única para o fluxo todo**, não por etapa.
3. **Cada etapa segue suas próprias regras** (preview, status PAUSED, etc.) internamente.
4. **Falha intermediária pausa o fluxo**, não rollback automático. Aluno decide.
5. **Atalho não substitui** os fluxos individuais. É camada de conveniência.

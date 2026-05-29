# Sub-fluxo. Gerir Regras Automáticas Existentes

Cobre as 6 operações de gestão pra regras automáticas já criadas: listar, ativar, pausar, editar, excluir, ver histórico. Reusa padrões da `regra-automatica.md` (tabela de tradução PT, gate 🛡️, resumo em linguagem natural).

A skill cobre essas operações, mas **toda função aqui também existe no Gerenciador de Anúncios nativo** (menu "Regras Automatizadas"). Aluno escolhe o caminho que preferir. A vantagem da skill é manter a conversa no chat, com tradução automática pra PT e validações de segurança.

## Perguntas que cobre

- "Lista minhas regras automáticas"
- "Ativa a regra que eu criei ontem"
- "Pausa todas as regras com CPA"
- "Quero mudar o trigger daquela regra de CPA 40 pra 50"
- "Excluir a regra de teste"
- "Quando essa regra rodou pela última vez?"

## Menu interno (após escolher [3] no menu principal)

```
O que você quer fazer com suas regras existentes?

A. Listar todas as minhas regras (ver status, trigger, ação)
B. Ativar uma regra (mudar de pausada pra ativa)
C. Pausar uma regra (mudar de ativa pra pausada)
D. Editar uma regra (mudar trigger, valor, ação)
E. Excluir uma regra
F. Ver histórico de execução de uma regra

Digite a letra:
```

Quando aluno digita uma letra, a skill executa o fluxo correspondente abaixo. Aluno digita "Enter" ou "voltar" pra retornar ao menu principal da `trafego-regras`.

---

## Fluxo A — Listar regras

**Quando rodar:** aluno escolhe A no menu interno. Também é o ponto de entrada de B, C, D, E, F (a skill sempre lista primeiro pra aluno escolher qual regra mexer).

### Passo 1: GET na biblioteca de regras

```
GET /act_<id>/adrules_library?fields=id,name,status,evaluation_spec,execution_spec,schedule_spec,created_time,updated_time&limit=50
```

Endpoint read-only. **Sem gate 🛡️** (não muda estado).

### Passo 2: Agrupar e ordenar

- Agrupar por `status` (`ENABLED` → ATIVAS; `DISABLED` → PAUSADAS; `DELETED`/`HAS_ISSUES` → ignorar).
- Ordenar por `created_time desc` dentro de cada grupo.
- Filtrar pelo prefixo `[FC] AutoRule-` se aluno disser "só as minhas" (default: mostra todas).

### Passo 3: Apresentar lista em PT-BR

Formato fixo:

```
Suas regras automáticas ({N_ativas} ativas, {N_pausadas} pausadas):

🟢 ATIVAS

[R1] [FC] AutoRule-PauseCPAGT40-curso-tarot
     Trigger: CPA passar de R$ 40 (últimos 3 dias, com gasto > R$ 200)
     Ação: Pausar adset
     Escopo: campanha "Curso Tarot - CBO"
     Criada em: 18/05/2026 às 14:32
     Última execução: 23/05/2026 às 09:15 (pausou 1 adset)

[R2] [FC] AutoRule-Brake10PctCTRLT0.5-curso-tarot
     Trigger: CTR cair abaixo de 0.5% (últimos 7 dias)
     Ação: Reduzir orçamento da campanha em 10%
     Escopo: todas campanhas ativas com objetivo OUTCOME_SALES
     Criada em: 19/05/2026 às 16:48
     Última execução: ainda não rodou

🟠 PAUSADAS

[R3] [FC] AutoRule-AlertSpendGT500-curso-tarot
     Trigger: Gasto diário passar de R$ 500
     Ação: Te enviar email
     Escopo: campanha "Tráfego Pago - VTSD"
     Criada em: 17/05/2026 às 11:20
     (pausada — ainda não foi ativada)

Total: 8 ativas, 3 pausadas.

Digite o código (ex: R1) pra ver mais detalhes ou agir nela.
Ou digite "voltar" pra menu principal.
```

### Passo 4: Aluno escolhe código

- Se aluno digita `R1` (ou similar): mostra **detalhes completos** da regra (todos os campos do payload em PT) + sub-menu:
  ```
  O que você quer fazer com [FC] AutoRule-PauseCPAGT40-curso-tarot?

  1. Voltar pra lista
  2. Ativar / Pausar (alternar status)
  3. Editar
  4. Excluir
  5. Ver histórico de execução
  ```
- Se aluno digita "todas" e havia paginação: refaz GET sem `limit`.
- Se aluno digita "voltar": retorna ao menu interno.

### Regras de exibição

- **Nunca mostrar IDs técnicos crus** (rule_id, campaign_id, adset_id) no corpo da listagem — só nome legível.
- ID técnico fica registrado em `meus-produtos/{ativo}/trafego/regras/INDEX.md` (rastreado automaticamente).
- Se a tradução PT do trigger falhar (campo desconhecido), exibir "trigger personalizado, ver no Gerenciador".

---

## Fluxo B — Ativar regra

**Quando rodar:** aluno escolhe B no menu interno OU escolhe "Ativar/Pausar" no sub-menu de uma regra específica.

### Passo 1: Listar PAUSADAS

Roda Fluxo A com filtro `status=DISABLED`. Se vazio, avisa: "Você não tem regras pausadas. Listar todas?"

### Passo 2: Aluno escolhe código (R1, R2...)

### Passo 3: Resumo em linguagem natural

```
📋 Antes de eu ativar essa regra, deixa eu te resumir o que ela vai fazer:

Regra: "{nome}"

A partir do momento que eu ativar, o Meta vai:
  - Avaliar {escopo em PT} a cada 30 minutos
  - Quando {trigger em PT}, vai {ação em PT}
  - Cooldown: depois de agir em uma entidade, espera {24h|1h} antes de agir nela de novo

Reset de aprendizado esperado: {sim — se ação é PAUSE ou CHANGE_BUDGET | não — se ação é NOTIFY}

Tá certo? (sim ativa, não cancela)
```

### Passo 4: Gate 🛡️

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: ativar regra automática
Endpoint: POST /<rule_id> (atualizar status)
Objeto: regra "{nome}"
O que vai mudar:
  - status: PAUSADA → ATIVA
  - regra começa a avaliar a cada 30 min
Reset de aprendizado esperado: {sim|não}
Reversível? sim, pausando de novo via opção C

Pode aplicar? Responda "sim" pra confirmar, "não" pra cancelar.
```

### Passo 5: Executar

`POST /<rule_id>` com payload `{ "status": "ENABLED" }`.

### Passo 6: Mensagem em linguagem natural

```
✅ Regra "{nome}" foi ATIVADA. Já começou a avaliar a cada 30 minutos.

📊 Pra ver o histórico de execução (quando ela disparar pela primeira vez):
   Rode /trafego-regras de novo e escolha [3] Gerir regras → F. Ver histórico.

🟠 Pra PAUSAR de novo se quiser:
   Mesma skill, opção C.
```

---

## Fluxo C — Pausar regra

Espelho do Fluxo B com 3 diferenças:

1. **Passo 1**: filtra `status=ENABLED`.
2. **Passo 5**: `POST /<rule_id>` com `{ "status": "DISABLED" }`.
3. **Resumo natural** muda pra "vou parar essa regra de avaliar" + "campanhas/adsets que ela tava monitorando ficam sem essa regra automática até você ativar de novo".

Mesmo gate 🛡️, mesma estrutura.

---

## Fluxo D — Editar regra

**Quando rodar:** aluno escolhe D no menu interno OU escolhe "Editar" no sub-menu de uma regra.

### Passo 1: Listar (qualquer status) + aluno escolhe código

### Passo 2: O que mudar?

```
O que você quer mudar em "{nome}"?

1. Trigger (métrica, operador, valor, janela de avaliação)
2. Ação (tipo de ação: pausar, mudar orçamento, notificar)
3. Percentual da mudança de orçamento (só se ação atual mexe em budget)
4. Escopo (campanha ou conjunto alvo)
5. Frequência de avaliação (Continuamente / Diariamente / Personalizado)
6. Frequência de ação (12h, 24h, semana)
7. Gasto mínimo / piso (min_daily_budget)
8. Subscribers (quem recebe email — só se ação é NOTIFICATION)
9. Nome da regra
10. Cancelar edição

Digite o número:
```

### Passo 3: Coletar o novo valor

Cada caminho **refaz só o sub-passo correspondente** do fluxo de criação da `regra-automatica.md`. Não rodar a coleta inteira de novo.

Exemplos:
- **1 (Trigger)**: roda o sub-fluxo de coleta de métrica/operador/valor/janela (passo 2 da criação).
- **2 (Ação)**: roda passo 4. Se nova ação é NOTIFICATION, coleta subscribers (passo 5).
- **4 (Escopo)**: roda passo 3 (fuzzy match de campanha/adset).
- **5 (Programação)**: roda Section B da "Funcionalidades adicionais".
- **9 (Nome)**: aceita texto livre.

### Passo 4: Mostrar antes/depois

```
Você vai mudar:

Trigger atual: CPA passar de R$ 40 (últimos 3 dias)
Trigger novo:  CPA passar de R$ 50 (últimos 7 dias)

(Os outros campos da regra continuam iguais.)

Confirma? (sim segue pro gate, não cancela)
```

### Passo 5: Gate 🛡️

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: editar regra automática
Endpoint: POST /<rule_id> (atualizar campo)
Objeto: regra "{nome}"
O que vai mudar:
  - {campo atual} → {campo novo}
Reset de aprendizado esperado: {depende do campo — editar trigger não reseta; editar action pode resetar}
Reversível? sim, editando de novo

Pode aplicar?
```

### Passo 6: POST só do campo alterado

```
POST /<rule_id>
{
  "evaluation_spec": { ... só se trigger mudou ... }
  OU
  "execution_spec": { ... só se ação mudou ... }
  OU
  "schedule_spec": { ... só se programação mudou ... }
  OU
  "name": "..."
}
```

Meta aceita PATCH parcial neste endpoint.

### Passo 7: Mensagem em linguagem natural

```
✅ Regra "{nome}" foi atualizada.

Mudança aplicada: {campo} agora é {novo valor}.

A próxima avaliação vai usar o novo trigger/ação.
```

---

## Fluxo E — Excluir regra

**Quando rodar:** aluno escolhe E no menu interno OU "Excluir" no sub-menu de uma regra.

### Passo 1: Listar (qualquer status) + aluno escolhe código

### Passo 2: Aviso reforçado (operação irreversível)

```
⚠️ ATENÇÃO: exclusão é IRREVERSÍVEL.

Vou excluir permanentemente a regra "{nome}".
O histórico de execução dela (toda vez que ela rodou e o que fez) também será apagado.

Se você só quer parar a regra temporariamente, vale mais usar a opção C (Pausar)
— assim você mantém o histórico e pode reativar quando quiser.

Tem certeza que quer EXCLUIR de vez?

Digite "EXCLUIR" (em maiúsculas, exatamente assim) pra confirmar.
Qualquer outra resposta cancela.
```

### Passo 3: Validar resposta

- Se aluno digita exatamente `EXCLUIR`: segue.
- Qualquer outra coisa (sim, ok, EXCLUIR., excluir, etc.): cancela e volta ao menu interno.

### Passo 4: Gate 🛡️ extra

```
🛡️ Confirmação FINAL antes de excluir

Operação: DELETAR regra automática
Endpoint: DELETE /<rule_id>
Objeto: regra "{nome}"
O que vai mudar:
  - regra removida permanentemente
  - histórico de execução apagado
Reversível? NÃO

Confirma a exclusão definitiva? Responda "sim" ou "não".
```

### Passo 5: DELETE

```
DELETE /<rule_id>
```

### Passo 6: Mensagem em linguagem natural

```
🗑️ Regra "{nome}" foi excluída.

Removida também do INDEX local: meus-produtos/{ativo}/trafego/regras/INDEX.md
```

---

## Fluxo F — Ver histórico de execução

**Quando rodar:** aluno escolhe F no menu interno OU "Ver histórico" no sub-menu.

### Passo 1: Listar + aluno escolhe código

### Passo 2: GET no histórico

```
GET /<rule_id>/history?fields=schedule,timestamp,results,evaluation_type&limit=50
```

Read-only, **sem gate 🛡️**.

### Passo 3: Apresentar em PT-BR

```
📊 Histórico da regra "{nome}" (últimas 50 execuções):

📅 23/05/2026 às 14:30 — Avaliou 12 adsets, agiu em 2:
   ✅ Pausou: "Adset HOT - Capacete - LAL1%" (CPA estava R$ 67)
   ✅ Pausou: "Adset COLD - Interesses - 25-55" (CPA estava R$ 52)

📅 23/05/2026 às 13:30 — Avaliou 12 adsets, nada disparou.

📅 23/05/2026 às 12:30 — Avaliou 12 adsets, nada disparou.

📅 22/05/2026 às 16:30 — Avaliou 12 adsets, agiu em 1:
   ✅ Pausou: "Adset WARM - Capacete - LAL2%" (CPA estava R$ 78)

...

(Mostrando últimas 50. Pra ver mais, peça "mais 50".)
```

### Passo 4 (opcional): Filtros

Se aluno pergunta:
- **"só as execuções que agiram"**: filtra `results` não vazio.
- **"últimos 7 dias"**: filtra `timestamp >= now - 7d`.
- **"qual adset foi mais pausado"**: agrupa por entidade.

---

## Estado final + handoff

Após qualquer fluxo (A-F), oferecer:

```
Quer fazer mais alguma coisa?

1. Voltar pra lista de regras (ver outras)
2. Voltar pro menu principal da /trafego-regras
3. Encerrar

Digite o número:
```

---

## Princípios desta sub-skill

1. **Listar é o ponto de entrada de todos os fluxos** (B, C, D, E, F sempre listam primeiro).
2. **Linguagem natural sempre.** Tradução automática de triggers e ações via tabela PT da `regra-automatica.md`.
3. **Nunca mostrar JSON técnico ou comandos curl ao aluno.** ID técnico fica em INDEX local.
4. **Gate 🛡️ obrigatório** em ativar, pausar, editar, excluir. NÃO usar em listar e histórico (read-only).
5. **Excluir exige confirmação dupla**: digitar "EXCLUIR" em maiúsculas + responder "sim" no gate.
6. **Sempre mencionar o Gerenciador como caminho alternativo** no final de cada operação. Aluno avançado prefere clique.
7. **Reusar coleta da `regra-automatica.md`** na edição. Não duplicar lógica.
8. **Cooldown da regra editada/ativada não reseta** automaticamente — Meta mantém o histórico de execução. Útil avisar isso na confirmação.

## Output esperado (após operação de escrita)

```yaml
operacao: gerir_regra
sub_fluxo: ativar | pausar | editar | excluir
rule_id: <id técnico, oculto do aluno>
nome: "{nome}"
acao_executada: status_change | field_update | delete
campos_afetados: [status]  # ou [evaluation_spec.filters[2].value], etc.
valores_antes: { ... }
valores_depois: { ... }
reversivel: true | false
comando_rollback: "POST /<id> {status: <anterior>}"  # só pra ativar/pausar
timestamp: 2026-05-23T14:30:00-03:00
```

Esse output fica no INDEX local. Aluno não vê.

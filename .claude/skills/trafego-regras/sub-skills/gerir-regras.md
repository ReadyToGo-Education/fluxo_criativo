# Sub-fluxo. Gerir Regras Automáticas Existentes

Cobre 6 operações sobre regras já criadas: listar, ativar, desativar, editar, excluir e ver histórico. Reaproveita a tabela de tradução e o resumo em linguagem natural da `regra-automatica.md`.

Tudo aqui também existe no Gerenciador de Anúncios ("Regras automatizadas"). A vantagem da skill é manter a conversa no chat, com tradução para o português e as validações de segurança.

Passo 0 e gate: ver `SKILL.md` desta skill.

> ⚠️ **Roteamento por modo.** As 6 operações usam o `adrules_library`, que **não tem tool no MCP**, nem de leitura (`GET /adrules_library`, `GET /<rule_id>/history`), nem de escrita.
> - **`APP`:** tudo por `curl`, como nos fluxos abaixo. **Exceção: excluir** nunca roda por `curl -X DELETE` direto (Fluxo E).
> - **`MCP_CONECTOR`:** cada fluxo vira um **passo a passo curto no Gerenciador** (seção "Versão MCP" de cada fluxo). A skill ajuda a decidir e traduz; quem clica é o aluno. Para listar, a skill também lê o registro local `meus-produtos/_global/trafego/regras/INDEX.md` (regras que o Severino desenhou). Nunca montar `curl` com token no modo MCP.

## Perguntas que cobre

- "Lista minhas regras automáticas"
- "Ativa a regra que eu criei ontem"
- "Desativa todas as regras de CPA"
- "Quero mudar o gatilho daquela regra de CPA 40 para 50"
- "Excluir a regra de teste"
- "Quando essa regra rodou pela última vez?"

## Menu interno (depois do [3] no menu principal)

```
O que você quer fazer com as suas regras?

A. Listar as minhas regras (status, gatilho, ação)
B. Ativar uma regra
C. Desativar uma regra
D. Editar uma regra (gatilho, valor, ação)
E. Excluir uma regra
F. Ver o histórico de execução de uma regra

Digite a letra:
```

"Voltar" retorna ao menu principal da `/trafego-regras`.

---

## Fluxo A. Listar regras

**Ponto de entrada** dos fluxos B a F (a skill sempre lista primeiro para o aluno escolher).

### Versão App

**Passo 1.** Leitura (sem gate):
```
GET /act_<id>/adrules_library?fields=id,name,status,evaluation_spec,execution_spec,schedule_spec,created_time,updated_time&limit=50
```

**Passo 2.** Agrupar por `status` (`ENABLED` → ATIVAS; `DISABLED` → DESATIVADAS; ignorar `DELETED` e `HAS_ISSUES`), ordenar por `created_time` (mais novas primeiro). Se o aluno disser "só as minhas", filtrar o prefixo `[WS] AutoRule-`.

**Passo 3.** Mostrar em português:

```
Suas regras automáticas ({N_ativas} ativas, {N_desativadas} desativadas):

🟢 ATIVAS

[R1] [WS] AutoRule-PauseCPAGT40-curso-tarot
     Gatilho: CPA passar de R$ 40 (últimos 3 dias, com gasto acima de R$ 200)
     Ação: pausar o conjunto
     Escopo: campanha "Curso Tarot - CBO"
     Criada em: 18/05/2026 às 14:32
     Última execução: 23/05/2026 às 09:15 (pausou 1 conjunto)

[R2] [WS] AutoRule-Brake10PctCTRLT0.5-curso-tarot
     Gatilho: CTR cair abaixo de 0,5% (últimos 7 dias)
     Ação: reduzir o orçamento da campanha em 10%
     Escopo: todas as campanhas ativas de vendas
     Criada em: 19/05/2026 às 16:48
     Última execução: ainda não rodou

🟠 DESATIVADAS

[R3] [WS] AutoRule-AlertSpendGT500-curso-tarot
     Gatilho: gasto diário passar de R$ 500
     Ação: te mandar e-mail
     Escopo: campanha "Campanha de Vendas Principal"
     Criada em: 17/05/2026 às 11:20
     (ainda não foi ativada)

Digite o código (ex: R1) para ver mais ou agir nela, ou "voltar".
```

**Passo 4.** Com o código: mostrar todos os campos em português e o submenu:
```
O que você quer fazer com [WS] AutoRule-PauseCPAGT40-curso-tarot?

1. Voltar para a lista
2. Ativar ou desativar
3. Editar
4. Excluir
5. Ver histórico de execução
```

**Regras de exibição:**
- **Nunca mostrar IDs** (regra, campanha, conjunto) na listagem: só nomes.
- O ID técnico fica em `meus-produtos/_global/trafego/regras/INDEX.md`.
- Campo desconhecido na tradução do gatilho: "gatilho personalizado, veja no Gerenciador".

### Versão MCP

Mostrar as regras do registro local (`INDEX.md`, regras que o Severino desenhou) e orientar:
```
O conector da Meta não lê regras automáticas. As regras que a gente desenhou estão
no seu registro: {lista do INDEX}.

Para ver TODAS as regras da conta (inclusive as criadas fora daqui):
📋 Gerenciador de Anúncios → "Regras automatizadas" → "Gerenciar regras"
   A lista mostra status, condições e ação de cada uma.

Se quiser, me mande um print da lista que eu traduzo e te ajudo a decidir.
```

---

## Fluxo B. Ativar regra

### Passo 1. Listar as DESATIVADAS (Fluxo A filtrado). Vazio: "Você não tem regras desativadas. Listar todas?"
### Passo 2. O aluno escolhe o código.
### Passo 3. Resumo em linguagem natural

```
📋 Antes de ativar essa regra, o que ela vai fazer:

Regra: "{nome}"

A partir da ativação, a Meta vai:
  - Avaliar {escopo em português} a cada 30 minutos
  - Quando {gatilho em português}, vai {ação em português}
  - Depois de agir numa entidade, esperar {24h | 1h} antes de agir nela de novo

Reset de aprendizado esperado: {sim, se a ação pausa ou mexe em orçamento | não, se só avisa}

Está certo? (sim ativa, não cancela)
```

### Passo 4 (App). Bloco 🛡️

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: ativar regra automática
Endpoint: POST /<rule_id> (status)
Objeto: regra "{nome}"
O que vai mudar:
  - status: DESATIVADA → ATIVA
  - a regra passa a avaliar a cada 30 min
Reset de aprendizado esperado: {sim | não}
Reversível? sim, desativando de novo (opção C)

Pode aplicar? Responda "sim" pra confirmar, "não" pra cancelar.
```

### Passo 5 (App). Executar: `POST /<rule_id>` com `{ "status": "ENABLED" }`.

### Versão MCP (passos 4 e 5)
```
📋 Gerenciador de Anúncios → "Regras automatizadas" → "Gerenciar regras"
📋 Ligue a chave da regra "{nome}"
Me avise com "feito".
```

### Passo 6. Mensagem

```
✅ Regra "{nome}" ATIVADA. A primeira avaliação acontece em até 30 minutos.

📊 Para ver o histórico (quando ela disparar): /trafego-regras → 3 → F
🟠 Para desativar de novo: /trafego-regras → 3 → C
```

Marcar como desatualizado o cache do `/trafego-insights` da conta.

---

## Fluxo C. Desativar regra

Espelho do Fluxo B, com 3 diferenças:
1. **Passo 1:** lista as ATIVAS.
2. **Passo 5 (App):** `POST /<rule_id>` com `{ "status": "DISABLED" }`. **MCP:** desligar a chave da regra no Gerenciador.
3. **Resumo:** "vou parar essa regra" e "as campanhas que ela monitorava ficam sem essa automação até você ativar de novo".

Mesmo bloco 🛡️ no App. **Desativar é a forma padrão de desfazer uma regra:** é reversível e mantém o histórico.

---

## Fluxo D. Editar regra

### Passo 1. Listar (qualquer status) e o aluno escolhe.

### Passo 2. O que mudar?

```
O que você quer mudar em "{nome}"?

1. Gatilho (métrica, operador, valor, janela)
2. Ação (pausar, mudar orçamento, avisar)
3. Percentual de mudança de orçamento (se a ação mexe em orçamento)
4. Escopo (campanha ou conjunto)
5. Programação (continuamente, diariamente, personalizado)
6. Frequência de ação (12h, 24h, semana)
7. Gasto mínimo ou piso do orçamento
8. Quem recebe o e-mail (se a ação é avisar)
9. Nome da regra
10. Cancelar a edição

Digite o número:
```

### Passo 3. Coletar o valor novo
Refazer **só** o passo correspondente da `regra-automatica.md` (nunca a coleta inteira):
- **1 (Gatilho):** passo 2 da criação.
- **2 (Ação):** passo 4; se virar aviso, passo 5.
- **4 (Escopo):** passo 3.
- **5 (Programação):** recurso extra B.
- **9 (Nome):** texto livre.

### Passo 4. Antes e depois

```
Você vai mudar:

Gatilho atual: CPA passar de R$ 40 (últimos 3 dias)
Gatilho novo:  CPA passar de R$ 50 (últimos 7 dias)

(O resto da regra continua igual.)

Confirma? (sim segue, não cancela)
```

### Passo 5 (App). Bloco 🛡️

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: editar regra automática
Endpoint: POST /<rule_id> (campo alterado)
Objeto: regra "{nome}"
O que vai mudar:
  - {campo atual} → {campo novo}
Reset de aprendizado esperado: {editar o gatilho não reseta; mudar a ação pode resetar quando ela disparar}
Reversível? sim, editando de novo

Pode aplicar? Responda "sim" pra confirmar, "não" pra cancelar.
```

### Passo 6 (App). `POST` só do campo alterado

```
POST /<rule_id>
{
  "evaluation_spec": { ...só se o gatilho mudou... }
  OU "execution_spec": { ...só se a ação mudou... }
  OU "schedule_spec": { ...só se a programação mudou... }
  OU "name": "..."
}
```

A Meta aceita atualização parcial nesse endpoint. Valem as pegadinhas da `regra-automatica.md` (`time_preset` como filtro próprio, `change_spec` com `limit`, `user_ids`).

### Versão MCP (passos 5 e 6)
```
📋 Gerenciador de Anúncios → "Regras automatizadas" → "Gerenciar regras"
📋 Na regra "{nome}", clique em editar (lápis ou três pontos → Editar)
📋 Troque {campo em português}: de "{valor atual}" para "{valor novo}"
📋 Clique em "Salvar"
Me avise com "feito".
```

### Passo 7. Mensagem

```
✅ Regra "{nome}" atualizada.

Mudança aplicada: {campo} agora é {valor novo}.

A próxima avaliação já usa o novo {gatilho | ação}.
```

Atualizar o registro local da regra.

---

## Fluxo E. Excluir regra (sempre à parte)

Excluir não tem volta e nunca entra num lote (regra 7 do gate no CLAUDE.md). **A skill nunca roda `curl -X DELETE` direto.**

### Passo 1. Listar (qualquer status) e o aluno escolhe.

### Passo 2. Aviso e alternativa não destrutiva

```
⚠️ Excluir uma regra NÃO tem volta.

A regra "{nome}" e todo o histórico de execução dela somem.

Se a ideia é só parar a regra, DESATIVAR resolve: ela para de agir, o histórico fica
e dá para ligar de novo quando quiser.

Como quer seguir?

1. Desativar (recomendado, reversível)
2. Excluir de vez

Digite o número:
```

- **1:** seguir o Fluxo C.
- **2:** passo 3.

### Passo 3. Bloco 🛡️ próprio

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: EXCLUIR regra automática
Endpoint: DELETE /<rule_id> (você mesmo executa, pelo Gerenciador ou por comando)
Objeto: regra "{nome}"
O que vai mudar:
  - a regra some da conta
  - o histórico de execução some junto
Reset de aprendizado esperado: não
Reversível? NÃO

Confirma a exclusão definitiva? Responda "sim" ou "não".
```

### Passo 4. Exclusão feita pelo aluno

Depois do "sim":

```
Eu não apago nada por conta própria. Escolha o caminho:

1. Pelo Gerenciador (recomendado):
   📋 Gerenciador de Anúncios → "Regras automatizadas" → "Gerenciar regras"
   📋 Na regra "{nome}", três pontos → "Excluir" → confirme

2. {Só no modo App} Por comando, que você mesmo roda no terminal Bash (Git Bash no
   Windows), na pasta do projeto. O token é lido do seu .env na hora e não aparece:

   curl -s -X DELETE "https://graph.facebook.com/v25.0/<rule_id>?access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"

Me avise quando terminar que eu confiro.
```

### Passo 5. Conferir e registrar

- **App:** conferir com `GET /act_<id>/adrules_library` que a regra sumiu (ou aparece como `DELETED`).
- **MCP:** confiar no "feito" do aluno (o conector não lê regras).
- Tirar a regra do `meus-produtos/_global/trafego/regras/INDEX.md` e marcar `excluida_em: {data}` no arquivo dela.

```
🗑️ Regra "{nome}" excluída e retirada do registro local.
```

---

## Fluxo F. Ver histórico de execução

### Passo 1. Listar e o aluno escolhe.

### Passo 2 (App). Leitura (sem gate)

```
GET /<rule_id>/history?fields=schedule,timestamp,results,evaluation_type&limit=50
```

### Passo 3. Mostrar em português

```
📊 Histórico da regra "{nome}" (últimas 50 execuções):

📅 23/05/2026 às 14:30. Avaliou 12 conjuntos, agiu em 2:
   ✅ Pausou "Conjunto Quente - LAL 1%" (CPA estava R$ 67)
   ✅ Pausou "Conjunto Frio - Interesses 25-55" (CPA estava R$ 52)

📅 23/05/2026 às 13:30. Avaliou 12 conjuntos, nada disparou.

📅 22/05/2026 às 16:30. Avaliou 12 conjuntos, agiu em 1:
   ✅ Pausou "Conjunto Morno - LAL 2%" (CPA estava R$ 78)

...

(Mostrando as últimas 50. Para ver mais, peça "mais 50".)
```

### Passo 4 (opcional). Filtros
- **"só as execuções que agiram":** `results` não vazio.
- **"últimos 7 dias":** `timestamp` dos últimos 7 dias.
- **"qual conjunto foi mais pausado":** agrupar por entidade.

### Versão MCP
```
📋 Gerenciador de Anúncios → "Regras automatizadas" → "Gerenciar regras"
📋 Clique na regra "{nome}" e abra o histórico de atividade (ou a coluna "Resultados")

Se quiser, me mande um print que eu traduzo o que aconteceu.
```

Para cruzar o histórico com as mudanças da conta toda, o MCP tem `ads_account_get_activity_logs` (histórico de alterações da conta), que mostra o que mudou e quando.

---

## Fim de qualquer fluxo

```
Quer fazer mais alguma coisa?

1. Voltar para a lista de regras
2. Voltar ao menu principal da /trafego-regras
3. Encerrar

Digite o número:
```

---

## Princípios desta sub-skill

1. **Listar é a porta de entrada** dos fluxos B a F.
2. **Linguagem natural sempre**, com a tabela de tradução da `regra-automatica.md`.
3. **Nunca mostrar JSON nem `curl` com token.** ID técnico só no registro local.
4. **Bloco 🛡️ no App** para ativar, desativar, editar e excluir. Listar e histórico não passam pelo gate.
5. **Excluir é sempre à parte**, com alternativa de desativar, bloco 🛡️ próprio e execução feita pelo aluno (Gerenciador ou comando sem token). Nunca `curl -X DELETE` direto.
6. **No MCP, o Gerenciador é o caminho**, com passo a passo curto.
7. **Reaproveitar a coleta da `regra-automatica.md`** na edição.
8. **O intervalo entre ações da regra editada ou ativada não zera**: a Meta mantém o histórico. Vale avisar na confirmação.

## Saída (depois de uma escrita, só no registro local)

```yaml
operacao: gerir_regra
sub_fluxo: ativar | desativar | editar | excluir
modo: MCP_CONECTOR (feito pelo aluno no Gerenciador) | APP
rule_id: <id técnico, fora da vista do aluno>
nome: "{nome}"
acao_executada: status_change | field_update | delete
campos_afetados: [status]
valores_antes: { ... }
valores_depois: { ... }
reversivel: true | false
como_desfazer: "voltar o status anterior pelo /trafego-regras → 3"
timestamp: 2026-05-23T14:30:00-03:00
```

O aluno não vê esse bloco.

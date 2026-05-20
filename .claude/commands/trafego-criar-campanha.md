---
name: workshop-marketing:trafego-criar-campanha
description: Subir campanha nova no Meta Ads (Facebook + Instagram) via Marketing API. Cobre apenas infoprodutos com objetivo OUTCOME_SALES (perpétuo de venda direta) ou OUTCOME_LEADS (lançamento de captação). Conduz coleta de insumos, exige pixel ativo, mostra preview YAML antes de criar e sobe a campanha PAUSED por padrão. Use quando o aluno pedir "subir campanha", "criar campanha", "lançar anúncio novo", "rodar tráfego", "anunciar produto X". Não cobre Awareness, Traffic, Engagement ou App Promotion.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Trafego Criar Campanha. Subir Campanha Meta Ads

Sobe campanha nova no Meta Ads diretamente via Marketing API, com preview YAML obrigatório e status PAUSED por padrão. Foca em infoprodutos: venda direta (`OUTCOME_SALES`) ou captação de leads (`OUTCOME_LEADS`). Não toca em outros objetivos.

A especificação técnica completa está em `.claude/skills/trafego-criar-campanha/SKILL.md`. Este command é o orquestrador.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo`. Leia `meus-produtos/{ativo}/perfil.md` para inferir ticket, Quadro, Furadeira e Identidades quando o aluno não declarar.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia `META_AUTH_MODO` no `.env`.

- **Se vazio ou ausente:** acione `/trafego-conexao` antes de prosseguir. Não tente adivinhar nem cair em fallback. Esta verificação é o passo zero de toda skill `/trafego-*`.
- **Se `MCP_CONECTOR`:** confirmar que pelo menos uma tool com prefixo `mcp__*__ads_*` está disponível. Se nenhuma estiver, pedir ao aluno para reabrir o Claude Code (MCP recém-adicionado às vezes precisa de reload). Se persistir, voltar a `/trafego-conexao` para diagnosticar.
- **Se `APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE`, `FB_AD_ACCOUNT_ID` e `FB_PAGE_ID` existem no `.env` (e opcionalmente `FB_INSTAGRAM_USER_ID`, necessário se for usar Reels/Stories no Instagram). Se faltar algum, acionar `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

### 0.3 Selecao de conta de anuncio (multi-conta)

Apos a validacao da conexao, decidir qual conta usar para subir a campanha:

1. Ler `FB_AD_ACCOUNT_IDS` no `.env`. Lista de IDs separados por virgula.
2. Se `FB_AD_ACCOUNT_IDS` nao existe ou esta vazio, usar `FB_AD_ACCOUNT_ID` direto.
3. Se `FB_AD_ACCOUNT_IDS` tem **1 conta**, usar `FB_AD_ACCOUNT_ID` direto sem perguntar.
4. Se `FB_AD_ACCOUNT_IDS` tem **2 ou mais contas**, perguntar:

   ```
   Em qual conta de anuncio voce quer subir essa campanha?

   1. {nome_conta_1} ({id_1})  ← padrao
   2. {nome_conta_2} ({id_2})
   3. {nome_conta_3} ({id_3})

   Digite o numero ou aperte Enter para usar a padrao:
   ```

   Para mostrar nomes amigaveis, fazer 1 chamada na Graph API:
   ```bash
   curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name&limit=100&access_token=TOKEN"
   ```
   Filtrar apenas as que estao em `FB_AD_ACCOUNT_IDS`. Marcar como "padrao" a que esta em `FB_AD_ACCOUNT_ID`.

5. Salvar a conta escolhida em variavel local da execucao (`AD_ACCOUNT_ID_ATUAL`). Nao sobrescrever o `.env`. A campanha sera criada na conta escolhida, nao necessariamente na padrao.

> **Atencao especifica deste command:** se a conta escolhida for diferente da padrao, validar que `FB_PAGE_ID` selecionado tem acesso na conta escolhida. Se a conta tem outra Pagina associada, perguntar qual usar. Sem `FB_PAGE_ID` valido para a conta escolhida, a Marketing API rejeita a criacao com erro 200.

### 0.4 Ler especificação da skill
Leia `.claude/skills/trafego-criar-campanha/SKILL.md` para carregar fluxo de coleta, validações de pixel, formato do preview YAML e ordem de criação.

---

## Passo 1. Detectar modo

Se a primeira mensagem do aluno já tem objetivo + produto + budget + público + criativo + tracking, ir para **modo expresso** (Passo 4 direto).

Caso contrário, **modo guia**: começar pela Fase 1 da skill.

---

## Passo 2. Conduzir as 9 fases (modo guia)

Aplicar as Fases 1 a 9 da skill, uma pergunta por mensagem:

1. **Objetivo**. Sales ou Leads.
2. **Produto e ticket**. Infere de `perfil.md` se possível, senão pergunta.
3. **Estrutura**. 1-X-1, 1-1-X ou X-1-1.
4. **Orçamento**. ABO ou CBO + valor diário.
5. **Tracking** (gate duro). Validar pixel ativo + evento recebendo dados.
6. **Público**. Advantage+ ou segmentação manual.
7. **Criativos**. Existentes na biblioteca ou subir novos. Para gerar copy, sugerir `/copy-anuncio`. Para imagem, sugerir `/criativo-estatico` ou `/img-anuncio`.
8. **Posicionamentos**. Advantage+ Placements (default) ou manual.
9. **Nome da campanha**. Padrão automático, aluno pode editar.

Manter o tom do projeto: pergunta numerada quando há opção, exemplo entre parênteses quando aberta.

---

## Passo 3. Validar pixel (gate duro)

🔍 Próximo passo: validar pixel e evento de conversão. Tempo estimado: cerca de 15 segundos.

Antes de seguir para o preview:

1. Listar pixels da conta (`GET /act_{id}/adspixels`). Confirmar que o ID informado existe.
2. Buscar stats do evento (`GET /pixel/{id}/stats`). Confirmar que o evento está recebendo dados nos últimos 7 dias.

Se pixel inexistente:
```
Não encontrei pixel com esse ID na conta. Para Sales/Leads, pixel
ativo é pré-requisito. Caminhos:

1. Configurar o pixel no Gerenciador de Anúncios
2. Para instalar Pixel em página HTML pronta, use /pagina-pixel
3. Cancelar essa campanha por enquanto

Digite o número:
```

Se pixel existe mas sem dados nos últimos 7 dias:
```
Pixel existe mas o evento [Purchase|Lead] não recebeu dados nos
últimos 7 dias. O algoritmo vai otimizar por proxy até o evento
começar a disparar. Quer prosseguir mesmo assim?

1. Sim, prosseguir
2. Não, vou configurar o evento primeiro
```

✅ Concluído: pixel e evento validados.

---

## Passo 4. Preview YAML

Montar o bloco `preview_campanha` completo conforme seção 3 da skill. Apresentar em código YAML legível, com todas as validações pré-criação marcadas (`pixel_ativo`, `evento_recebendo_dados_7d`, `budget_coerente_com_ticket`, `page_id_valido`, `instagram_user_id_valido`, `criativos_no_formato_correto`).

Pedir aprovação:

```
Esse é o preview da campanha. Confirma criar com status PAUSED?

1. Confirmo, pode subir
2. Quero ajustar algo
3. Cancela

Digite o número:
```

Se opção 2: perguntar o que ajustar e voltar ao Passo 4 com novo preview.
Se opção 3: encerrar sem criar nada.
Se opção 1: ir para Passo 5.

---

## Passo 5. Criação

🔍 Próximo passo: criar campanha, conjuntos e anúncios via Marketing API. Tempo estimado: 1 a 2 minutos.

Aplicar a ordem da seção 4 da skill:

1. `POST /act_{id}/campaigns` (status PAUSED)
2. Para cada conjunto: `POST /act_{id}/adsets`
3. Para cada anúncio:
   - `POST /act_{id}/adcreatives`
   - `POST /act_{id}/ads`

Em caso de falha:
- Falha em campanha: parar tudo, retornar erro detalhado.
- Falha em conjunto: deletar campanha já criada se ela ficou órfã.
- Falha em anúncio: preservar o que já subiu, listar quais falharam, perguntar se quer tentar manualmente.

Anunciar progresso por nível:
```
⏳ Passo 1/3: criando campanha "[nome]"...
⏳ Passo 2/3: criando [N] conjunto(s)...
⏳ Passo 3/3: criando [N] anúncio(s)...
```

✅ Concluído: campanha criada com status PAUSED.

---

## Passo 6. Apresentar resultado

Mostrar ao aluno:

```
✅ Campanha criada com sucesso (status PAUSED).

Campanha: [nome]
ID: [id]

Conjuntos criados:
- [nome]   ID [id]   PAUSED
- ...

Anúncios criados:
- [nome]   ID [id]   PAUSED
- ...

[Se houver falhas parciais, listar separadamente:]
Falhas:
- [nivel] [nome]   motivo: [...]
  Ação sugerida: [...]

Acessar no Gerenciador:
https://business.facebook.com/adsmanager/manage/campaigns?act=[id]&selected_campaign_ids=[campaign_id]

Próximos passos:

1. Abrir no Gerenciador (link acima) e revisar visualmente cada
   anúncio (preview, copy, criativo).
2. Quando estiver tudo certo, ativar manualmente OU me peça
   "ativa a campanha [nome]" que eu ativo via API.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-analise
Espere a campanha rodar 48 a 72 horas (maturação mínima do
algoritmo) e rode /trafego-analise pra primeira leitura narrada
em método VTSD.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Passo 7. Salvar resumo (opcional)

Salvar em:
```
meus-produtos/{ativo}/entregas/trafego/campanha-criada-{nome-slug}-{YYYY-MM-DD}.md
```

Conteúdo: o preview YAML aprovado + IDs gerados + link do Gerenciador + próximos passos.

Caminho absoluto a exibir: `{raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\campanha-criada-{...}.md`

---

## Ativação posterior

Se o aluno disser depois "ativa a campanha [nome|id]":

1. Confirmar com aluno: "Vou ativar a campanha agora. Uma vez ativa, começa a gastar imediatamente. Confirma?"
2. Se confirmado: chamar `POST /campaign/{id}` com `status: ACTIVE`.
3. Confirmar ativação e lembrar: "Lembre de monitorar nas primeiras 48h. Use `/trafego-insights` pra acompanhar."

---

## Princípios que este command nunca viola

1. **Sales/Leads sem pixel = não cria.** Gate duro.
2. **Sempre PAUSED por default.** Ativação só com pedido explícito posterior.
3. **Preview obrigatório, sempre.** Mesmo no modo expresso.
4. **Não cobre objetivos fora de Sales/Leads.** Recusa Awareness, Traffic, Engagement, App Promotion.
5. **Liberdade de estrutura.** Aluno pode pedir customizada (ex: 2 conjuntos × 4 anúncios).
6. **Nunca chama edição.** Edição mora em `/trafego-otimizar` e `/trafego-escalar`.
7. **Falha parcial preserva.** Não faz rollback completo automático.
8. **Geração de copy via `/copy-anuncio`.** Não gera copy aqui.

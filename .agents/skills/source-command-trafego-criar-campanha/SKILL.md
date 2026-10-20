---
name: "source-command-trafego-criar-campanha"
description: "Subir campanha nova no Meta Ads (Facebook + Instagram) pelo conector da Meta (MCP) ou pela Marketing API (modo App). Cobre apenas infoprodutos com objetivo OUTCOME_SALES (perpétuo de venda direta) ou OUTCOME_LEADS (lançamento de captação). Lê o resumo do produto ativo, exige pixel ativo, mostra preview antes de criar, pede uma única confirmação para o lote inteiro e sobe a campanha PAUSED por padrão. Use quando o aluno pedir \"subir campanha\", \"criar campanha\", \"lançar anúncio novo\", \"rodar tráfego\", \"anunciar produto X\". Não cobre Awareness, Traffic, Engagement ou App Promotion."
---

# source-command-trafego-criar-campanha

Use esta skill quando o usuário pedir o comando `/trafego-criar-campanha` do workshop (ou `trafego-criar-campanha`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/trafego-criar-campanha.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Tráfego Criar Campanha. Subir Campanha Meta Ads

Sobe campanha nova no Meta Ads com preview obrigatório e status PAUSED por padrão. Foca em infoprodutos: venda direta (`OUTCOME_SALES`) ou captação de leads (`OUTCOME_LEADS`). Não toca em outros objetivos.

A especificação técnica completa está em `.claude/skills/trafego-criar-campanha/SKILL.md`. Este command é o orquestrador.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (se o resumo não existir, gere conforme a seção "Contexto Persistente do Negócio" do CLAUDE.md). Do resumo saem nome, tipo, preço, nicho, Quadro, público, Decorados e Urgências Ocultas. Nada disso é perguntado ao aluno.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia só a linha `META_AUTH_MODO` do `.env` (`grep "^META_AUTH_MODO=" .env | cut -d= -f2-`).

- **Se vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive valor legado de versão antiga): acione `/trafego-conexao` antes de prosseguir. Não tente adivinhar nem cair em fallback. Esta verificação é o passo zero de toda skill `/trafego-*`.
- **Se `MCP_CONECTOR`:** confirmar que existe tool do conector da Meta, procurando pelo final do nome (`ads_create_campaign`, `ads_get_ad_accounts`), como manda a seção 5.1 da skill `trafego-conexao`. Se nenhuma estiver disponível, pedir ao aluno para reabrir o Claude (conector recém-adicionado às vezes precisa de reload). Se persistir, voltar a `/trafego-conexao` para diagnosticar. Conferir também `FB_AD_ACCOUNT_ID` com `grep -q "^FB_AD_ACCOUNT_ID=." .env` (com o ponto: linha vazia conta como ausente): as tools de escrita exigem a conta. Se faltar (conexão feita numa versão antiga, que não gravava a conta no modo MCP), acionar `/trafego-conexao` avisando que o motivo é a conta padrão, para ele ir direto à seção 5.1.1 (listar as contas com `ads_get_ad_accounts`, perguntar quando houver mais de uma e gravar `FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS`), e depois voltar a este Passo 0. Nunca seguir com a conta vazia. Conta não liberada no conector (`is_ads_mcp_enabled: false` ou "Ads MCP is gradually being rolled out"): avisar e oferecer o modo App pelo `/trafego-conexao`.
- **Se `APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` têm valor no `.env`, com `grep -q "^FB_ACCESS_TOKEN_PERMANENTE=." .env` e `grep -q "^FB_AD_ACCOUNT_ID=." .env` (linha vazia, como vem do `.env.example`, conta como ausente). Se faltar algum, acionar `/trafego-conexao`. `FB_PAGE_ID` (e `FB_INSTAGRAM_USER_ID`, necessário para Reels/Stories) também é conferido: se faltar só ele, a seção 7.1 da skill descobre e grava, sem refazer a conexão.

Nunca exibir o token nem o conteúdo do `.env` (seção "LEITURA SEGURA DO .env" do CLAUDE.md). A skill nunca prossegue sem essa validação passar.

### 0.3 Seleção de conta de anúncio (multi-conta)

Após a validação da conexão, decidir qual conta usar para subir a campanha:

1. Ler `FB_AD_ACCOUNT_IDS` no `.env`. Lista de IDs separados por vírgula.
2. Se `FB_AD_ACCOUNT_IDS` não existe ou está vazio, usar `FB_AD_ACCOUNT_ID` direto (o Passo 0.2 já garantiu que ele tem valor; sem ele, voltar ao Passo 0.2, nunca seguir com conta vazia).
3. Se `FB_AD_ACCOUNT_IDS` tem **1 conta**, usar `FB_AD_ACCOUNT_ID` direto sem perguntar.
4. Se `FB_AD_ACCOUNT_IDS` tem **2 ou mais contas**, perguntar:

   ```
   Em qual conta de anúncio você quer subir essa campanha?

   1. {nome_conta_1} ({id_1})  ← padrão
   2. {nome_conta_2} ({id_2})
   3. {nome_conta_3} ({id_3})

   Digite o número ou aperte Enter para usar a padrão:
   ```

   Para mostrar nomes amigáveis, fazer 1 leitura:
   - **MCP:** tool `ads_get_ad_accounts`.
   - **APP:**
     ```bash
     curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name&limit=100&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
     ```
   Filtrar apenas as que estão em `FB_AD_ACCOUNT_IDS`. Marcar como "padrão" a que está em `FB_AD_ACCOUNT_ID`.

5. Salvar a conta escolhida em variável local da execução (`AD_ACCOUNT_ID_ATUAL`). Não sobrescrever o `.env`. A campanha será criada na conta escolhida, não necessariamente na padrão.

> **Atenção específica deste command:** se a conta escolhida for diferente da padrão, validar que a Página (`FB_PAGE_ID`) tem acesso na conta escolhida. Se a conta tem outra Página associada, perguntar qual usar. Sem Página válida para a conta escolhida, a criação falha com erro 200.

### 0.4 Ler especificação da skill
Leia `.claude/skills/trafego-criar-campanha/SKILL.md` para carregar fluxo de coleta, validações de pixel, roteamento por modo, formato do preview e ordem de criação.

---

## Passo 1. Detectar modo

Se a primeira mensagem do aluno já tem objetivo + produto + budget + público + criativo + tracking, ir para **modo expresso** (Passo 4 direto).

Caso contrário, **modo guia**: começar pela Fase 1 da skill.

---

## Passo 2. Conduzir as 9 fases (modo guia)

Aplicar as Fases 1 a 9 da skill, uma pergunta por mensagem:

1. **Objetivo**. Sales ou Leads.
2. **Produto e ticket**. Lidos do `resumo-produto.md` e confirmados em uma linha. Só pergunta se a campanha vender outra oferta.
3. **Estrutura**. 1-X-1, 1-1-X ou X-1-1.
4. **Orçamento**. ABO ou CBO + valor diário.
5. **Tracking** (gate duro). Validar pixel ativo + evento recebendo dados.
6. **Público**. Advantage+ (recomendado), Advantage+ com interesses (termos tirados do resumo) ou personalizado. Lookalike novo é criado pelo `/trafego-publicos`. No modo MCP, interesse por nome é lacuna: a skill recomenda Advantage+ ou conduz o passo manual guiado.
7. **Criativos**. Arquivos em `meus-produtos/{ativo}/entregas/criativos/`, biblioteca da conta ou pendentes (pendentes: o lote cria só a campanha e os conjuntos, sem anúncios; os anúncios entram depois pela seção 7.8 da skill). Para gerar copy, sugerir `/copy-anuncio`. Para imagem, `/criativo-estatico` ou `/img-anuncio`. Para vídeo, `/video-heygen`, `/video-remotion` ou `/video-editar`. No modo MCP, vídeo novo é lacuna: o aluno sobe pelo Gerenciador antes do preview e a skill usa o vídeo da biblioteca.
8. **Posicionamentos**. Advantage+ Placements (default) ou manual.
9. **Nome da campanha**. Padrão automático, aluno pode editar.

Manter o tom do projeto: pergunta numerada quando há opção, exemplo entre parênteses quando aberta.

---

## Passo 3. Validar pixel (gate duro)

🔍 Próximo passo: validar o pixel e o evento de conversão. Tempo estimado: cerca de 15 segundos.

Antes de seguir para o preview (Fase 5 da skill):

1. Listar os pixels da conta (MCP `ads_get_datasets`, com o plano B da Fase 5.0 se a tool ainda não estiver liberada; APP `GET /act_<id>/adspixels`). Confirmar que o pixel escolhido existe.
2. Conferir os dados do evento (MCP `ads_get_dataset_stats`; APP `GET /<pixel_id>/stats`). Confirmar que o evento está recebendo dados nos últimos 7 dias.

Se pixel inexistente:
```
Não encontrei pixel com esse ID na conta. Para Sales/Leads, pixel
ativo é pré-requisito. Caminhos:

1. Configurar o pixel no Gerenciador de Eventos
2. Instalar o pixel numa página HTML feita aqui no projeto (/pagina-pixel)
3. Cancelar essa campanha por enquanto

Digite o número:
```

Se pixel existe mas sem dados nos últimos 7 dias:
```
O pixel existe, mas o evento [Purchase|Lead] não recebeu dados nos
últimos 7 dias. O algoritmo vai otimizar por proxy até o evento
começar a disparar. Quer prosseguir mesmo assim?

1. Sim, prosseguir
2. Não, vou investigar o evento primeiro (/trafego-pixel)

Digite o número:
```

✅ Concluído: pixel e evento validados.

---

## Passo 4. Preview e confirmação do lote

Montar o preview completo conforme a seção 3 da skill: o YAML fica salvo em `meus-produtos/{ativo}/entregas/trafego/criar-campanha/preview-campanha-{tipo_funil}-{slug}-{data}.yaml` e o aluno vê um resumo em texto corrido, com `Nome (ID)` em toda referência e as validações pré-criação marcadas (`pixel_ativo`, `evento_recebendo_dados_7d`, `budget_coerente_com_ticket`, `page_id_valido`, `instagram_user_id_valido`, `criativos_no_formato_correto`).

Pedir a aprovação com **um único bloco 🛡️ para o lote inteiro** (campanha + conjuntos + criativos + anúncios + uploads), no formato do CLAUDE.md:

```
🛡️ Confirmação necessária antes de tocar na conta Meta

Operação: criar campanha completa (lote)
Endpoint: {ads_create_* pelo conector | POST /act_<id>/campaigns, /adsets, /adcreatives, /ads}
Objeto: {nome da campanha}
O que vai mudar:
  - 1 campanha nova "{nome}", status PAUSED{, orçamento de R$ X/dia se CBO}
  - {N} conjunto(s), status PAUSED: {nomes e orçamento diário em reais}
  - {N} anúncio(s) com {N} criativo(s), status PAUSED {ou: 0 anúncios (criativos pendentes)}
  - {N} upload(s) de imagem/vídeo (se houver)
Reset de aprendizado esperado: não (campanha nova)
Reversível? sim (tudo nasce pausado; dá para arquivar depois)

Pode aplicar? Responda "sim" pra confirmar, "não" pra cancelar.
```

- **sim:** ir para o Passo 5 e executar o lote inteiro sem nova pergunta.
- **ajustar:** perguntar o que muda e voltar ao Passo 4 com novo preview.
- **não / cancela:** encerrar sem criar nada.

---

## Passo 5. Criação

🔍 Próximo passo: criar a campanha, os conjuntos e os anúncios na conta. Tempo estimado: 60 a 120 segundos.

Aplicar a ordem da seção 4 da skill, roteando por `META_AUTH_MODO` (tools `ads_create_*` no MCP, `curl` no APP). Orçamento na chamada: inteiro em centavos no APP (R$ × 100); no MCP, na unidade que o schema da tool pedir (seção 4 da skill).

0. Mídia, só se houver arquivo novo ou vídeo: subir imagens e vídeos (APP), esperar cada vídeo ficar pronto e pegar a miniatura; no MCP, confirmar o vídeo na biblioteca e pegar a miniatura dele. Tudo antes de criar a campanha.
1. Campanha (status PAUSED; em ABO no modo APP, com `is_adset_budget_sharing_enabled=false`, senão erro 4834011)
2. Conjuntos (sempre com `advantage_audience` 0 ou 1, senão erro 1870227)
3. Para cada anúncio que não está pendente: criativo e anúncio (vídeo sempre com miniatura, senão erro 1443226)

Anunciar progresso por nível (sem o passo 0, quando não há arquivo novo nem vídeo, são 3 passos):
```
⏳ Passo 1/4: preparando imagens e vídeos.
⏳ Passo 2/4: criando a campanha "[nome]".
⏳ Passo 3/4: criando [N] conjunto(s).
⏳ Passo 4/4: criando [N] anúncio(s).
```

Depois de criar, conferir o orçamento gravado contra o valor em reais do preview (seção 4 da skill). Se não bater, avisar antes de qualquer ativação.

Em caso de falha:
- **Falha no upload, vídeo que não fica pronto ou sem miniatura:** parar antes de criar a campanha (nada foi criado na conta). Oferecer tentar de novo, trocar o arquivo ou seguir sem aquele anúncio (com novo bloco 🛡️ do plano ajustado).
- **Falha na campanha:** parar tudo, retornar erro detalhado.
- **Falha num conjunto:** parar e não apagar nada automaticamente. A campanha fica PAUSED e sem conjunto não gasta. Oferecer corrigir e tentar de novo, arquivar a campanha (bloco 🛡️ próprio) ou excluir à mão pelo Gerenciador.
- **Falha num anúncio:** preservar o que já subiu, marcar no preview salvo como pendentes (`pendente: true`) o anúncio que falhou e os que não chegaram a ser criados, listar quais falharam, perguntar se quer tentar de novo depois (seção 7.8 da skill).

Depois, conduzir os passos manuais pendentes, se houver (interesses no modo MCP, anúncio com imagem a criar pelo Gerenciador), com os passos numerados da skill. O vídeo novo do modo MCP já foi para a biblioteca antes do preview.

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

[Se os criativos ficaram pendentes (opção 2 da Fase 7):]
Anúncios pendentes: [N]. A campanha não entrega enquanto os
conjuntos estiverem sem anúncio. Quando os criativos estiverem
prontos, me peça "adiciona os anúncios na campanha [nome]".

[Se houver falhas parciais, listar separadamente:]
Falhas:
- [nível] [nome]   motivo: [...]
  Ação sugerida: [...]

Acessar no Gerenciador:
https://business.facebook.com/adsmanager/manage/campaigns?act=[id]&selected_campaign_ids=[campaign_id]

Próximos passos:

1. Abrir no Gerenciador (link acima) e revisar visualmente cada
   anúncio (preview, copy, criativo). Se quiser, eu mostro a prévia
   de qualquer anúncio por aqui.
2. Quando estiver tudo certo, ativar no Gerenciador (a campanha,
   os conjuntos e os anúncios, porque todos nasceram pausados) OU
   me peça "ativa a campanha [nome]" que eu ativo tudo de uma vez.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-analise
Espere a campanha rodar 48 a 72 horas (maturação mínima do
algoritmo) e rode /trafego-analise para a primeira leitura narrada
pelo método VTSD. Para acompanhar os números no dia a dia, use
/trafego-dashboard.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Passo 7. Salvar resumo (opcional)

Salvar em:
```
meus-produtos/{ativo}/entregas/trafego/criar-campanha/campanha-criada-{nome-slug}-{YYYY-MM-DD}.md
```

Conteúdo: o resumo do preview aprovado + IDs gerados + link do Gerenciador + próximos passos.

Caminho absoluto a exibir: `{raiz-do-projeto}\meus-produtos\{ativo}\entregas\trafego\criar-campanha\campanha-criada-{...}.md`

---

## Ativação posterior

Se o aluno disser depois "ativa a campanha [nome|id]", seguir a seção 7.6 da skill. Ativar só a campanha não liga os conjuntos e anúncios, que também nasceram pausados, então a ativação cobre tudo:

1. Ler a campanha, os conjuntos e os anúncios, com o orçamento diário (MCP `ads_get_ad_entities` nos níveis campaign, adset e ad, cada consulta já filtrada pela campanha, com `daily_budget` em reais; APP `GET /<campaign_id>`, `/adsets` e `/ads`, com `daily_budget` em centavos, dividir por 100), como no passo 1 da seção 7.6 da skill.
2. Mostrar um único bloco 🛡️ listando a campanha, cada conjunto e cada anúncio, cada um com "status PAUSED → ACTIVE", o gasto diário em reais que começa e "reversível: sim, pausando de novo". Avisar: "Uma vez ativa, a campanha começa a gastar imediatamente." Se algum conjunto estiver sem anúncio, avisar que ele não vai entregar.
3. Com o `sim`, ativar anúncios, depois conjuntos, por último a campanha: MCP `ads_activate_entity` (ou `ads_update_entity` com `status=ACTIVE`); APP `POST /<id>` com `status: ACTIVE` para cada objeto.
4. Conferir com uma nova leitura o que ficou ativo e lembrar: "Monitore nas primeiras 48h. Use `/trafego-insights` para acompanhar."

## Anúncios adicionados depois

Se o aluno disser "adiciona os anúncios na campanha [nome]" (criativos pendentes ou anúncios que falharam), seguir a seção 7.8 da skill: criativos e copy, preview atualizado, bloco 🛡️ próprio e criação dos anúncios com `status: PAUSED`. A ativação continua sendo a de cima.

---

## Princípios que este command nunca viola

1. **Sales/Leads sem pixel = não cria.** Gate duro.
2. **Sempre PAUSED por default.** Ativação só com pedido explícito posterior, cobrindo campanha, conjuntos e anúncios.
3. **Preview obrigatório, sempre.** Mesmo no modo expresso.
4. **Um `sim` por lote.** A criação inteira é aprovada de uma vez. Ativação, anúncios adicionados depois e arquivamento têm confirmação própria. Exclusão nunca é automática nem entra em lote.
5. **Não cobre objetivos fora de Sales/Leads.** Recusa Awareness, Traffic, Engagement, App Promotion.
6. **Liberdade de estrutura.** Aluno pode pedir customizada (ex: 2 conjuntos × 4 anúncios).
7. **Nunca chama edição.** Edição mora em `/trafego-otimizar` e `/trafego-escalar`. Adicionar os anúncios pendentes numa campanha criada aqui é criação (seção 7.8 da skill).
8. **Falha parcial preserva.** Não faz rollback automático.
9. **Geração de copy via `/copy-anuncio`.** Não gera copy aqui.
10. **Nunca exibe o token.** Nem no chat, nem em comando mostrado ao aluno.

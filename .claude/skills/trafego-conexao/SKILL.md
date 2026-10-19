---
name: trafego-conexao
description: >
  Especificação técnica completa da conexão com o Meta Ads (Facebook + Instagram). A conexão
  sempre começa pelo conector oficial da Meta no Claude (MCP_CONECTOR) e é testada; o App via
  Facebook Developers (APP, token permanente no .env) só entra quando o teste mostra que a conta
  ainda não foi liberada no conector ou o conector não responde. Confere os pré-requisitos no Meta, valida a conexão, salva a conta padrão
  no .env nos dois modos e documenta as lacunas do conector (operações sem ferramenta no MCP) com o
  passo a passo manual guiado que todas as skills de tráfego seguem. Consultada pelo command
  /trafego-conexao.
user-invocable: false
---

# Tráfego Conexão. Especificação Técnica

O command `/trafego-conexao` é o orquestrador. Esta skill guarda a especificação de cada passo e a referência que as outras skills de tráfego consultam (lacunas do conector, descoberta de ferramentas, mapa de erros).

A preferência fica gravada em `META_AUTH_MODO` no `.env`. Todas as skills `/trafego-*` leem essa variável no Passo 0, e os commands `/ads-relatorio` e `/enviar-relatorio-ads` também consultam ela para decidir o caminho.

Existem só dois valores válidos:

- **`MCP_CONECTOR`** (padrão, recomendado). Conector oficial da Meta adicionado no Claude. Login via OAuth na própria conta do Claude. Sem token permanente, sem App no Facebook Developers, sem instalar nada na máquina.
- **`APP`** (reserva). App criado no Facebook Developers, com token permanente do Usuário do Sistema salvo no `.env`. Faz tudo o que a Marketing API permite, por `curl`.

**Ordem obrigatória:** a conexão sempre começa pelo conector. O aluno não escolhe o modo no início: a skill conduz a adição do conector (seção 3), testa (seção 5.1) e só oferece o App em dois casos, depois do teste: a conta de anúncios ainda não foi liberada pela Meta no conector (seção 5.1.2), ou o conector não responde mesmo depois das conferências da seção 5.1. Se o aluno pedir o App antes de testar, explicar em 2 linhas que o conector é mais simples (1 minuto, sem token) e propor o teste; só seguir direto para o App (seção 4) se ele insistir.

Qualquer outro valor é tratado no Passo 0 (seção 1). O valor `HIBRIDO`, que aparece em `.env` de quem usou uma versão antiga destas skills, é legado: a seção 1 explica como regravar.

---

## Lacunas do MCP (referência para todas as skills de tráfego)

No modo `MCP_CONECTOR` quase tudo tem ferramenta no conector. Pela lista oficial da Meta (outubro de 2026), quatro operações ainda não têm. Nelas, a skill **não troca de modo e não pede token**: conduz o aluno por um passo a passo manual curto no Gerenciador de Anúncios (passos numerados, em português) e depois segue o fluxo pelo conector.

No modo `APP` as quatro rodam por `curl` na Graph API, sem passo manual (a exclusão continua com as regras de segurança da L4).

### L1. Subir vídeo novo

O conector só usa vídeo que já está na biblioteca de mídia da conta de anúncios (tool `ads_get_ad_videos`). Passo a passo para o aluno:

```
O conector da Meta ainda não sobe vídeo novo. Faça assim, leva 2 minutos:

1. Abra o Gerenciador de Anúncios (adsmanager.facebook.com) na conta
   de anúncios certa.
2. No menu de ferramentas, entre em "Biblioteca de mídia".
3. Clique em "Carregar" e escolha o vídeo no seu computador.
4. Espere o processamento terminar (o vídeo aparece com miniatura).
5. Me avise aqui ("subi") e me diga o nome do arquivo.
```

Depois do "subi", a skill chama `ads_get_ad_videos`, localiza o vídeo pelo nome, confirma com o aluno (`Nome (ID)`) e segue usando o `video_id` da biblioteca. Se a tela do Gerenciador estiver diferente, pedir ao aluno que descreva o que vê e adaptar os passos.

Imagem não é lacuna: o criativo do conector aceita imagem por URL pública (`image_url`). Imagem que está só no computador segue o caminho da Fase 7.1 do `/trafego-criar-campanha`.

### L2. Buscar interesse por nome

Não existe ferramenta de busca de interesse no conector. Caminho padrão: **recomendar público aberto com Advantage+**, que é o padrão atual da Meta e dispensa interesses. Se o aluno quiser interesse específico mesmo assim:

```
O conector não pesquisa interesses. Dá para fazer assim:

1. Eu crio o conjunto com público aberto (Advantage+), tudo pausado.
2. Abra o conjunto no Gerenciador de Anúncios (te passo o link).
3. Em "Público", no campo de segmentação detalhada, digite cada
   termo da lista que eu te passei e escolha os interesses que
   aparecerem.
4. Salve. A campanha continua pausada.
5. Me avise aqui ("pronto") para eu conferir.
```

Se o aluno já tiver o ID do interesse (de uma exportação ou de outra ferramenta), usar direto no targeting.

### L3. Criar regra automática

A biblioteca de regras da Meta (`adrules_library`) não tem ferramenta no conector. A skill monta a regra (condição, ação, frequência, a quem notificar) e guia a criação manual:

```
1. No Gerenciador de Anúncios, abra o menu de ferramentas e entre
   em "Regras automatizadas".
2. Clique em "Criar regra".
3. Escolha onde a regra se aplica: {campanhas | conjuntos | anúncios}.
4. Ação: {ação}. Condição: {condição com valor}.
5. Frequência de verificação: {frequência}. Notificação: {sim | não}.
6. Salve e me avise aqui ("criei").
```

Agendamento de liga e pausa por horário (`adset_schedule`) não é regra automática: continua pelo conector via `ads_update_entity`.

### L4. Apagar campanha, conjunto ou anúncio

O conector só apaga público (`ads_delete_custom_audience`). Para campanha, conjunto ou anúncio:

1. **Preferir pausar ou arquivar** via `ads_update_entity` (`status` `PAUSED` ou `ARCHIVED`). Não destrói histórico e passa pelo bloco 🛡️ normal.
2. **Se o aluno quiser excluir de verdade**, guiar a exclusão manual: no Gerenciador, marcar a caixa da linha, clicar em "Excluir" e confirmar.

Toda exclusão (inclusive de público pelo conector) tem bloco 🛡️ e "sim" próprios: **nunca entra no "sim" de um lote**. No modo `APP` a regra é a mesma: não rodar `curl -X DELETE` inline. Oferecer pausar ou arquivar, ou mostrar o comando com `***TOKEN_MASCARADO***` para o aluno rodar manualmente.

### Deixou de ser lacuna

Pelo conector, com `ads_create_custom_audience` (subtipos `LOOKALIKE`, `ENGAGEMENT` e os demais):

- público semelhante (lookalike);
- público de engajamento no Instagram ou na Página do Facebook;
- público de visualização de vídeo.

Quem cria públicos é o `/trafego-publicos`. Se a Meta recusar algum subtipo na prática, cair no passo manual guiado (Gerenciador de Anúncios > Públicos > Criar público).

### Conta não liberada no conector

A Meta libera o conector conta por conta. Sinais de conta ainda não liberada: `is_ads_mcp_enabled: false` (ou `is_queryable: false`) no retorno de `ads_get_ad_accounts`, ou erro com a mensagem "Ads MCP is gradually being rolled out". Nesse caso, avisar o aluno em linguagem simples e oferecer trocar para o modo App pelo `/trafego-conexao` (mensagem na seção 5.1.2).

Diferente disso é **uma ferramenta específica em liberação gradual** (erro do tipo "This tool is new and is being gradually rolled out across ad accounts"). A conta funciona, só aquela tool ainda não. Não travar: seguir o plano B da skill que chamou (exemplo: Fase 5.0 do `/trafego-criar-campanha` para a listagem de pixels).

### Ferramentas do conector que as skills podem citar

Quando encaixar naturalmente, as skills podem oferecer estas ferramentas. Os parâmetros vêm do schema da tool na hora da chamada, nunca de memória.

| Tool (sufixo) | Para que serve |
|---|---|
| `ads_experiment_abtest_create_test`, `ads_experiment_abtest_get_test`, `ads_experiment_abtest_update_test`, `ads_experiment_check_eligibility`, `ads_experiment_list_tests` | Teste A/B oficial da Meta |
| `ads_pixel_event_*`, `ads_pixel_parameter_*` | Eventos e parâmetros do pixel |
| `ads_account_get_activity_logs` | Histórico de alterações da conta |
| `ads_get_opportunity_score` | Pontuação de oportunidade da conta |
| `ads_insights_anomaly_signal` | Sinal de anomalia nas métricas |
| `ads_insights_industry_benchmark`, `ads_insights_auction_ranking_benchmarks` | Comparação com o mercado e com o leilão |
| `ads_get_ad_preview` | Prévia visual de um anúncio |
| `ads_get_creatives` | Criativos da conta |
| `ads_get_custom_audience_adsets` | Conjuntos que usam um público |
| `ads_boost_ig_post` | Impulsionar post do Instagram |

As de escrita (`ads_experiment_abtest_create_test`, `ads_experiment_abtest_update_test`, as `ads_pixel_event_*` e `ads_pixel_parameter_*` de criação, edição ou exclusão e `ads_boost_ig_post`, que gasta verba) passam pelo bloco 🛡️ do CLAUDE.md antes da chamada.

---

## 0. Pré-requisitos no Meta (antes de tudo)

Sem estes 5 itens nenhum dos dois modos funciona:

1. **Business Manager** (Portfólio Empresarial) criado em business.facebook.com.
2. **Página do Facebook** vinculada ao Business Manager.
3. **Conta de Anúncios** ativa dentro do Business Manager, com moeda e fuso configurados.
4. **Forma de pagamento** cadastrada na Conta de Anúncios.
5. **Pixel** (Conjunto de Dados) criado no Gerenciador de Eventos.

Se o aluno não tiver certeza, perguntar:

```
Antes de conectar com o Meta, você precisa ter 5 coisas prontas:

1. Business Manager criado
2. Página do Facebook vinculada a ele
3. Conta de Anúncios ativa
4. Forma de pagamento cadastrada
5. Pixel criado

Você já tem tudo isso?

1. Sim, pode continuar
2. Não sei / falta algo

Digite o número:
```

- **Opção 1:** seguir para a seção 1.
- **Opção 2:** parar e orientar com o mapa abaixo. Não conduzir a configuração do Business Manager pelo chat além disso: o aluno cria os itens no Meta e volta.

```
Sem problema. Crie o que falta no Meta e depois volte aqui:

1. Business Manager: business.facebook.com > Criar conta.
2. Página: Configurações do negócio > Contas > Páginas
   (adicionar uma Página que você já tem ou criar uma nova).
3. Conta de Anúncios: Configurações do negócio > Contas > Contas
   de anúncios > Adicionar. Escolha moeda Real e fuso de São Paulo:
   os dois não podem ser trocados depois.
4. Forma de pagamento: Configurações de pagamento da conta de
   anúncios.
5. Pixel: Gerenciador de Eventos > Conectar fontes de dados > Web.
   Para instalar o pixel numa página feita aqui no projeto, use
   /pagina-pixel depois.

Quando estiver tudo pronto, rode /trafego-conexao de novo.
```

---

## 1. Passo 0. Verificar estado atual

Ler o modo sem exibir o resto do `.env` (`META_AUTH_MODO` não é sensível, pode aparecer):

```bash
grep "^META_AUTH_MODO=" .env | cut -d= -f2-
```

Se o `.env` não existir, tratar como Caso 4.

**Caso 1. Valor `MCP_CONECTOR` ou `APP`.** Antes do menu, conferir o que a conexão precisa (linha vazia conta como ausente). No modo `APP`, primeiro o token:

```bash
grep -q "^FB_ACCESS_TOKEN_PERMANENTE=." .env && echo "presente" || echo "ausente"
```

Se vier `ausente`, avisar em 1 linha ("O modo App está ativo, mas o token não está salvo. Vou gerar um token novo no seu App.") e acionar direto o `/gerar-token-permanente-facebook-ads`, sem mostrar o menu e sem passar pelo `/criar-aplicativo-analise-ads`. O modo `APP` só é gravado depois que um token do App passa nos testes, então esse aluno já tem o App e o Usuário do Sistema: ele vai direto ao passo de gerar o token, como na opção 2 da 4.1. Esse command também lista as contas e grava a conta padrão. Ao terminar, seguir como no fim da 4.2 (passo 3, só se a conta continuar faltando, e depois a seção 5.2). Só se o aluno disser que não tem mais o App (apagou o App ou perdeu o acesso a ele), seguir a 4.2 desde o passo 1.

Nos dois modos, a conta padrão:

```bash
grep -q "^FB_AD_ACCOUNT_ID=." .env && echo "presente" || echo "ausente"
```

Se vier `ausente` (conexão feita por uma versão antiga, que no MCP não gravava a conta, ou `.env` copiado do `.env.example`), avisar em 1 linha ("A conexão está ativa, mas falta escolher a conta de anúncios padrão.") e aplicar direto a opção "Validar a conexão atual" abaixo, sem mostrar o menu. Vale também quando o `/trafego-conexao` foi acionado por outra skill por falta do token ou da conta: ao terminar, voltar para ela.

Com o token (no `APP`) e a conta presentes, traduzir o modo para o aluno (`MCP_CONECTOR` = "conector da Meta", `APP` = "App do Facebook Developers") e perguntar. No modo `MCP_CONECTOR` não existe a opção de trocar para o App: o App só entra quando o conector falha no teste (seção 5.1.2). No modo `APP`, a opção de passar para o conector aparece sempre, porque é o caminho recomendado.

Modo `MCP_CONECTOR`:

```
Já existe uma conexão configurada com o Meta Ads.

Modo ativo: conector da Meta

O que você quer fazer?

1. Manter como está
2. Validar a conexão atual
3. Trocar a conta de anúncios padrão

Digite o número:
```

Modo `APP`:

```
Já existe uma conexão configurada com o Meta Ads.

Modo ativo: App do Facebook Developers

O que você quer fazer?

1. Manter como está
2. Passar para o conector da Meta (recomendado, sem token)
3. Validar a conexão atual
4. Trocar a conta de anúncios padrão

Digite o número:
```

As opções abaixo usam os nomes, não os números, porque o menu do conector tem uma opção a menos.

- **Manter como está:** encerrar com "Conexão atual mantida. Modo ativo: {valor traduzido}."
- **Passar para o conector (só no `APP`):** seguir para a seção 3 e validar pela 5.1. Se passar, gravar `META_AUTH_MODO=MCP_CONECTOR` (6.1). Se a conta não estiver liberada (5.1.2), avisar e manter o modo `APP` como está. O token continua no `.env`, caso precise voltar.
- **Validar a conexão atual:** ir direto para a validação (seção 5) do modo registrado. No MCP, a seção 5.1 segue para a 5.1.1, que lista as contas e grava `FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS`. No APP, se faltar `FB_AD_ACCOUNT_ID`, rodar antes a listagem da seção 4.3 (o teste 3 da 5.2 usa a conta). Se a validação passar e faltar `FB_PAGE_ID` ou `FB_INSTAGRAM_USER_ID`, completar pela seção 6 sem refazer o resto.
- **Trocar a conta de anúncios padrão:** listar as contas do modo registrado (MCP: seção 5.1.1, com a coluna do conector; APP: seção 4.3), deixar o aluno escolher a nova padrão e regravar só `FB_AD_ACCOUNT_ID` (e completar `FB_PAGE_ID` e `FB_INSTAGRAM_USER_ID` da nova conta pela seção 6.3). No MCP, não aceitar como padrão uma conta marcada como não liberada no conector (seção 5.1.2). O resto da conexão fica como está.

**Caso 2. Valor `HIBRIDO` (legado).** Esse valor vem de uma versão antiga das skills de tráfego. Aqui só existem os dois modos acima, e o conector vem sempre primeiro. Avisar e seguir pelo conector:

```
Encontrei no seu .env o modo HIBRIDO, de uma versão antiga das skills
de tráfego. Aqui no projeto a conexão é pelo conector da Meta, e o App
fica só de reserva. As operações que o conector ainda não faz agora
têm um passo a passo guiado no Gerenciador, então o modo híbrido
deixou de ser necessário.

Seu token do App continua salvo no .env. Não apago nada. Vou testar o
conector agora.
```

Validar pela seção 5.1. Se passar, gravar `META_AUTH_MODO=MCP_CONECTOR` (seção 6.1). Se a conta não estiver liberada no conector (5.1.2) ou o conector não responder depois das conferências da 5.1, validar o token que já existe pela seção 5.2 e gravar `META_AUTH_MODO=APP` (seção 6.2), avisando o aluno em 1 linha. Enquanto a validação não passar, não mexer na linha do `.env`.

**Caso 3. Valor não reconhecido** (qualquer outro):

```
Encontrei a variável META_AUTH_MODO no .env, mas o valor "{valor}"
não é reconhecido (esperado MCP_CONECTOR ou APP). Vou tratar como se
a conexão não estivesse configurada.
```

Seguir para a seção 2.

**Caso 4. Linha ausente ou vazia:** seguir para a seção 2 sem aviso.

---

## 2. Passo 1. Conectar pelo conector da Meta (sempre o primeiro caminho)

Não perguntar o modo. Apresentar o caminho em poucas linhas e seguir direto para a seção 3:

```
Vamos conectar pelo conector oficial da Meta no Claude. É o caminho
mais simples: leva cerca de 1 minuto, autoriza pelo login do Facebook
e não precisa de token nem de App no Facebook Developers. A conexão
fica na sua conta do Claude e vale em qualquer máquina onde você
estiver logado.

Depois de conectar, eu testo se a Meta já liberou a sua conta de
anúncios para o conector. Se ainda não tiver liberado, eu te mostro o
outro caminho.
```

O App (seção 4) só é oferecido depois do teste da seção 5.1: conta não liberada no conector (5.1.2) ou conector sem resposta depois das conferências da 5.1. Se o aluno pedir o App antes, aplicar a "Ordem obrigatória" do topo desta skill.

---

## 3. Caminho A. Conector da Meta (MCP)

> O conector da Meta ainda não está na lista oficial de conectores do Claude, então entra como **conector personalizado**. Leva 1 minuto.

### 3.1 Adicionar o conector personalizado

Instruir o aluno e esperar a confirmação:

```
Para adicionar o conector da Meta na sua conta do Claude:

1. Abra o aplicativo Claude Desktop (o site claude.com não tem mais
   a opção de adicionar conector personalizado).

2. Clique em "Customize" (Personalizar) e depois em "Connectors"
   (Conectores).

3. Clique no "+" e escolha "Adicionar conector personalizado"
   (Add custom connector).

4. Preencha:
   - URL do servidor: https://mcp.facebook.com/ads
   - Nome: Meta Ads
     (pode ser outro nome, mas "Meta Ads" fica fácil de achar)

5. Clique em "Adicionar" ou "Salvar".

6. Vai abrir uma aba do Facebook pedindo autorização:
   - Entre com a conta de admin do Business Manager que tem a
     conta de anúncios que você quer usar
   - Selecione a Página do Facebook e o perfil do Instagram
   - Confirme as permissões

7. Quando o conector "Meta Ads" aparecer como "Conectado", me avise
   aqui ("conectei", "feito") que eu continuo.
```

> **O conector é da conta do Claude, não da máquina.** Em outra máquina logada na mesma conta, o conector já aparece ativo. Não precisa adicionar de novo.

Com a confirmação, seguir para a seção 5.1.

---

## 4. Caminho B. App via Facebook Developers

Só se chega aqui depois do teste do conector (seção 5.1.2 ou conector sem resposta na 5.1), pelo Caso 1 com o modo `APP` já ativo, ou quando o aluno insiste no App depois da explicação da "Ordem obrigatória".

O caminho do App usa as skills de configuração do projeto, nesta ordem: `/criar-aplicativo-analise-ads` → `/gerar-token-permanente-facebook-ads` (que já lista as contas e grava a conta padrão) → `/obter-id-conta-anuncios` (só se a conta padrão continuar faltando). Esta seção só acrescenta o que vem antes e o que vem depois delas.

### 4.1 Checar token existente antes de qualquer passo de criação (regra dura)

O aluno pode já ter um App configurado de uma execução anterior. Mostrar o passo a passo de criação do zero nesse caso gera retrabalho. Checar se o token tem valor, sem expor o valor:

```bash
grep -q "^FB_ACCESS_TOKEN_PERMANENTE=." .env && echo "presente" || echo "ausente"
```

A linha vazia (`FB_ACCESS_TOKEN_PERMANENTE=`, como vem do `.env.example`) conta como ausente e vai para a 4.2.

**Token presente:** pular a criação e perguntar:

```
Encontrei um token de App já salvo no seu projeto. O que você quer
fazer?

1. Usar o token que já tenho (recomendado, valido agora)
2. Gerar um token novo

Digite o número:
```

- **Opção 1:** se faltar `FB_AD_ACCOUNT_ID`, listar as contas pela 4.3 antes (o teste 3 da 5.2 usa a conta). Depois validar pela seção 5.2 e, se passar, salvar (6.2). Não recriar nada.
- **Opção 2:** acionar `/gerar-token-permanente-facebook-ads`. O App e o Usuário do Sistema já existem, então o aluno vai direto ao passo de gerar o token.

**Token ausente:** seguir para 4.2.

### 4.2 Encadeamento das skills do App

1. **`/criar-aplicativo-analise-ads`.** Cria o App no developers.facebook.com com os 7 casos de uso, cadastra a política de privacidade e publica o App.
2. **`/gerar-token-permanente-facebook-ads`** (encadeada pela primeira). Cria o Usuário do Sistema, atribui os ativos (Conta de Anúncios, App, Página, Instagram e Conjunto de Dados), gera o token com expiração "Nunca", grava `FB_ACCESS_TOKEN_PERMANENTE` (sem abrir o `.env`, guardando o token anterior como `FB_ACCESS_TOKEN_ANTERIOR` até os testes passarem), roda os 3 testes com o token por substituição, grava `META_AUTH_MODO=APP`, lista as contas que o token enxerga e grava `FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS`.
3. **`/obter-id-conta-anuncios`.** Só quando `FB_AD_ACCOUNT_ID` continuar ausente depois do passo 2. Antes de acionar, rodar a listagem automática da seção 4.3: se ela devolver contas, a conta sai dali; se vier vazia, a correção é atribuir a conta ao Usuário do Sistema (Passo 2 do `/gerar-token-permanente-facebook-ads`), não digitar o ID.

Ao fim do encadeamento, voltar aqui e seguir para a seção 5.2.

### 4.3 Listar as contas que o token enxerga

Usada quando o token já existia (4.1, opção 1) ou quando a conta padrão não foi gravada no encadeamento. O ID da conta nunca é pedido ao aluno quando a listagem automática está disponível.

🔍 Próximo passo: listar as contas de anúncios que o seu token enxerga. Tempo estimado: cerca de 10 segundos.

```bash
curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name,account_status,currency,timezone_name&limit=100&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

**Mapa de `account_status`:**

| Valor | Significado |
|---|---|
| 1 | Ativa |
| 2 | Desabilitada |
| 3 | Sem conformidade |
| 7 | Pendente de risco |
| 9 | Em revisão |
| 100 | Pendente de fechamento |
| 101 | Fechada |
| 201 | Outro motivo de inatividade |

- **1 conta:** salvar como `FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS` sem perguntar. Avisar em 1 linha: `✅ Conta identificada: {name} (act_{account_id}), em {currency}, fuso {timezone_name}. Salva como conta padrão.`
- **2 ou mais contas:** mostrar a tabela e perguntar quais salvar e qual é a padrão:

  ```
  Contas de anúncios que seu token enxerga:

  | # | Nome             | ID                   | Moeda | Fuso              | Status |
  |---|------------------|----------------------|-------|-------------------|--------|
  | 1 | Conta Principal  | act_1234567890123456 | BRL   | America/Sao_Paulo | Ativa  |
  | 2 | Conta Secundária | act_9876543210987654 | BRL   | America/Sao_Paulo | Ativa  |

  Quais contas quer salvar no projeto? Digite os números separados
  por vírgula (ex: 1,2) ou "todas".
  ```

  Depois: `Qual delas é a padrão? Digite o número:`. Avisar antes de salvar uma conta que não esteja Ativa.
- **Lista vazia:** o Usuário do Sistema não recebeu nenhuma conta. Orientar a refazer a atribuição de ativos (Passo 2 do `/gerar-token-permanente-facebook-ads`).
- **Erro 190 ou 200:** consultar o mapa de erros (5.3).

---

## 5. Validação final

### 5.1 Modo `MCP_CONECTOR`

🔍 Próximo passo: validar o conector da Meta. Tempo estimado: cerca de 20 segundos.

**Descoberta da tool pelo final do nome (regra para todas as skills de tráfego).** O prefixo das tools muda conforme o ambiente: pode ser `mcp__Meta_Ads__...` ou um identificador longo, como `mcp__9dc3edbb-e8b6-44ae-a6f0-4917300912c1__ads_get_ad_accounts`. O que é estável é o final do nome (`ads_get_ad_accounts`, `ads_create_campaign` etc.). Estratégia, em ordem:

1. Procurar a tool cujo nome termine em `ads_get_ad_accounts` (ou qualquer tool com `__ads_` no nome). Em alguns ambientes as tools do conector ficam adormecidas e só aparecem depois de uma busca pelo nome: nesse caso, buscar pelo final `ads_get_ad_accounts` antes de chamar.
2. Se a busca não for conclusiva, perguntar: "Qual nome você deu ao conector da Meta? Vou usar para localizar a ferramenta certa."
3. Chamar `ads_get_ad_accounts` (sem parâmetro obrigatório; devolve as contas que o conector enxerga).

Resultados:

- **Lista de contas:** conexão validada. Seguir para 5.1.1 usando esse mesmo retorno (não fazer segunda chamada).
- **Lista vazia:** nenhuma conta foi autorizada no login do Facebook. Tratar como erro de permissão (abaixo). Nunca seguir com a conta padrão vazia.
- **Nenhuma tool do conector disponível:**

  ```
  Não consegui acessar o conector da Meta. Confira:

  - Você está logado no Claude com a mesma conta onde adicionou o
    conector?
  - No Claude Desktop, em Customize > Connectors, o "Meta Ads"
    aparece como "Conectado"?
  - Reiniciou o Claude depois de adicionar? (feche e abra de novo o
    Claude Desktop ou o Claude Code)

  Quando estiver tudo certo, me avise que eu tento de novo.
  ```

  Tentar de novo quando o aluno avisar. Se, depois dessas conferências, o conector continuar sem responder na segunda tentativa (ou o aluno não conseguir adicionar o conector no Claude dele), aí sim oferecer o App como caminho alternativo (seção 4), explicando em 1 linha que ele faz o mesmo pela API, com um token salvo no computador.
- **Erro de permissão:** o conector está ativo, mas nenhuma conta foi autorizada no login do Facebook. Pedir para refazer o passo 6 da seção 3.1.
- **Conta não liberada no conector:** seção 5.1.2.

### 5.1.1 Selecionar e salvar a conta padrão (modo MCP)

As tools de escrita do conector (`ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`, `ads_create_custom_audience` etc.) exigem `ad_account_id`. Por isso o modo MCP também salva a conta padrão no `.env`. O retorno de `ads_get_ad_accounts` vem numa lista `ad_accounts`. De cada conta, ler (quando vierem) `ad_account_id` (pode vir com `act_`; salvar só os dígitos), `ad_account_name`, `currency`, `timezone_name`, `is_ads_mcp_enabled` e `is_queryable`, os nomes que o modelo do `/trafego-dashboard` usa na conta real. Se vierem com outro nome (`name`, `account_id`), usar o equivalente. `account_status` pode não vir no conector: sem ele, a coluna Status fica de fora.

Uma conta está **liberada** no conector quando nem `is_ads_mcp_enabled` nem `is_queryable` vêm `false`. Nos outros casos, ela é "ainda não": não entra em `FB_AD_ACCOUNT_IDS` e não vira padrão.

**Caso A. 1 conta.** Se ela estiver liberada, salvar como `FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS` sem perguntar:

```
✅ Conta identificada: {ad_account_name} (act_{dígitos do ad_account_id}), em {currency}. Salva no .env como conta padrão.
```

Se a única conta vier "ainda não", ir direto para a seção 5.1.2.

**Caso B. 2 ou mais contas.** Mostrar a tabela com a coluna "Conector" (liberada ou ainda não, pela regra acima) e a coluna "Status" (`account_status`, quando vier; mapa da seção 4.3):

```
Contas que o conector enxerga:

| # | Nome             | ID                   | Moeda | Status | Conector   |
|---|------------------|----------------------|-------|--------|------------|
| 1 | Conta Principal  | act_1234567890123456 | BRL   | Ativa  | liberada   |
| 2 | Conta Secundária | act_8765432109876543 | BRL   | Ativa  | ainda não  |

Qual conta você quer usar como padrão? Digite o número.
(Contas marcadas "ainda não" não funcionam no conector por enquanto.)
```

Se o aluno escolher uma conta "ainda não" (`is_ads_mcp_enabled` ou `is_queryable` igual a `false`), aplicar a seção 5.1.2 para essa conta.

Salvar o `ad_account_id` escolhido (só dígitos) como `FB_AD_ACCOUNT_ID` e a lista das contas liberadas como `FB_AD_ACCOUNT_IDS`. Seguir para a seção 6.

### 5.1.2 Conta não liberada no conector

Quando todas as contas vierem "ainda não" (`is_ads_mcp_enabled` ou `is_queryable` igual a `false`), quando o aluno precisar de uma conta ainda não liberada, ou quando a chamada devolver "Ads MCP is gradually being rolled out":

```
A Meta ainda não liberou essa conta de anúncios para o conector do
Claude. A liberação está sendo feita aos poucos, conta por conta, e
não depende de nenhuma configuração sua.

Enquanto isso, dá para usar o App do Facebook Developers, que faz
tudo pela API e não depende dessa liberação. Leva de 8 a 12 minutos
para configurar.

1. Configurar o App agora
2. Esperar a liberação e tentar de novo depois

Digite o número:
```

- **Opção 1:** seção 4.
- **Opção 2:** encerrar sem gravar `META_AUTH_MODO=MCP_CONECTOR`. O conector continua adicionado no Claude.

### 5.2 Modo `APP`

🔍 Próximo passo: validar o token permanente com 3 testes na Graph API. Tempo estimado: cerca de 20 segundos.

Conferir a presença com `grep -q` (seção "LEITURA SEGURA DO .env" do CLAUDE.md) e rodar os 3 testes. **Cada teste é uma chamada `Bash` independente**, com o token entrando por substituição dentro do próprio `curl`. Nunca empacotar os testes num script com `TOKEN="..."` no início: esse formato dispara o pop-up de permissão com o token visível.

```bash
curl -s "https://graph.facebook.com/v25.0/me?access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

```bash
curl -s "https://graph.facebook.com/v25.0/me/adaccounts?access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

```bash
curl -s "https://graph.facebook.com/v25.0/act_<FB_AD_ACCOUNT_ID>/campaigns?limit=1&access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)"
```

| Teste | Esperado | Se falhar |
|---|---|---|
| 1. Token válido (`/me`) | `{"id":"...","name":"relatorio-ads"}` ou o nome dado ao Usuário do Sistema | Token copiado errado ou revogado |
| 2. Contas visíveis (`/me/adaccounts`) | Lista com `act_<id>` da conta padrão | Conta não atribuída ao Usuário do Sistema |
| 3. Leitura na conta (`/campaigns`) | `data` com 1 campanha ou `data: []` em conta nova, sem erro | Falta permissão na conta |

Depois de cada teste, descrever o resultado em linguagem natural ("Teste 1 passou: o token responde como relatorio-ads"). Nunca ecoar a URL com o token. Os três passaram: seguir para a seção 6. Algum falhou: mapa de erros (5.3), sem gravar `META_AUTH_MODO`.

### 5.3 Mapa de erros

**Modo APP (Graph API):**

| Código | Causa provável | Solução |
|---|---|---|
| `190` Invalid OAuth access token | Token errado, copiado pela metade ou revogado | Gerar de novo (Passo 3 do `/gerar-token-permanente-facebook-ads`). O token tem mais de 200 caracteres: conferir se foi copiado inteiro |
| `200` Permissions error | Token válido, mas o Usuário do Sistema não tem o ativo atribuído | Refazer a atribuição de ativos (Passo 2 do `/gerar-token-permanente-facebook-ads`) |
| `100` Invalid parameter | Prefixo `act_` no lugar errado | No `.env`, só os dígitos. Na URL, prefixar com `act_` |
| `10` Application does not have permission | App sem o caso de uso da Marketing API ou App não atribuído ao Usuário do Sistema | Conferir os casos de uso (`/criar-aplicativo-analise-ads`) e o App com controle total (Passo 2 do `/gerar-token-permanente-facebook-ads`) |
| `4` Application request limit reached | Limite de chamadas do App | Aguardar 1 hora. Se persistir, confirmar que o App está publicado |
| `17` User request limit reached | Muitas chamadas em pouco tempo | Aguardar e espaçar as chamadas. Regerar o token não resolve |
| `appsecret_proof` exigido | App Secret Proof ligado nas configurações avançadas do App | Para o teste manual, desligar temporariamente, testar e religar |

**Modo MCP (conector):**

| Sinal | Causa provável | Solução |
|---|---|---|
| Nenhuma tool `ads_*` encontrada | Conector não adicionado, desconectado ou Claude não reiniciado | Mensagem da seção 5.1 |
| Erro de permissão em `ads_get_ad_accounts` | Nenhuma conta autorizada no login do Facebook | Refazer o passo 6 da seção 3.1 |
| `is_ads_mcp_enabled: false`, `is_queryable: false` ou "Ads MCP is gradually being rolled out" | Conta ainda não liberada pela Meta | Seção 5.1.2 |
| "This tool is new and is being gradually rolled out" | Uma tool específica ainda não liberada para a conta | Plano B da skill que chamou (ver "Conta não liberada no conector") |

Se a tela do Business Manager ou do Facebook Developers não bater com o roteiro, pedir ao aluno que descreva o que está vendo. A Meta muda a interface sem aviso.

---

## 6. Salvamento no `.env`

Gravar `META_AUTH_MODO` só depois que a validação passar (seção 9, princípio 1). A conta padrão listada na 4.3 e o token gravado pelo `/gerar-token-permanente-facebook-ads` podem ir antes, porque os testes da 5.2 usam os dois. Gravar cada variável com o comando de uma linha do item 4 da seção "LEITURA SEGURA DO .env" do CLAUDE.md, que apaga a linha antiga (inclusive a vazia, vinda do `.env.example`) e acrescenta a nova, sem abrir o arquivo, sem duplicar a linha e sem mexer nas outras variáveis. Nunca usar Read, Edit ou Write no `.env`: o Edit exige ler o arquivo inteiro antes, com o token e as outras chaves. Para conferir se uma variável já tem valor, usar o padrão da mesma seção (`grep -q "^FB_AD_ACCOUNT_ID=." .env`): linha vazia conta como ausente.

**Nunca tocar em `RELATORIO_AUTH_MODO`.** É dos commands legados `/ads-relatorio` e `/enviar-relatorio-ads`, que serão migrados em outra rodada.

### 6.1 Modo `MCP_CONECTOR`

```
META_AUTH_MODO=MCP_CONECTOR
FB_AD_ACCOUNT_ID={id_da_conta_padrao}
FB_AD_ACCOUNT_IDS={id_1},{id_2}
```

- `FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS` vêm da seção 5.1.1. São obrigatórios porque as tools de escrita exigem `ad_account_id`.
- O modo MCP não salva token: a autenticação fica na conta do Claude. Se já existir `FB_ACCESS_TOKEN_PERMANENTE` de antes, deixar como está e não usar.

### 6.2 Modo `APP`

```
META_AUTH_MODO=APP
FB_ACCESS_TOKEN_PERMANENTE={token}
FB_AD_ACCOUNT_ID={id_da_conta_padrao}
FB_AD_ACCOUNT_IDS={id_1},{id_2}
```

Quase tudo já foi gravado pelo `/gerar-token-permanente-facebook-ads`. Aqui a skill só confere com `grep -q` e completa o que faltar (o token nunca é digitado ou exibido por esta skill).

Depois que a validação da 5.2 passar, apagar a sobra de uma geração de token interrompida, se houver: `sed -i '/^FB_ACCESS_TOKEN_ANTERIOR=/d' .env` (no Mac, `sed -i ''`). O token validado é o que vale; a cópia antiga deixaria a próxima geração confusa.

### 6.3 Página e Instagram (os dois modos)

O `/trafego-criar-campanha` precisa da Página (e do Instagram, para Reels e Stories). Depois de gravar a conta padrão, tentar descobrir e gravar:

```
FB_PAGE_ID={id_da_pagina}
FB_INSTAGRAM_USER_ID={id_do_instagram}
```

- **MCP:** tool `ads_get_ad_account_pages` com `ad_account_id = FB_AD_ACCOUNT_ID`.
- **APP:** `curl -s "https://graph.facebook.com/v25.0/act_<FB_AD_ACCOUNT_ID>/promote_pages?fields=id,name&access_token=..."` e, para a Página escolhida, `curl -gs "https://graph.facebook.com/v25.0/<FB_PAGE_ID>?fields=name,instagram_business_account{id,username}&access_token=..."` (`-g` por causa do campo aninhado), com o token por substituição como na seção 5.2.

1 Página: gravar sem perguntar. Várias: mostrar `Nome (ID)` numerado e perguntar qual. Instagram vinculado: gravar o `id`. Se a descoberta falhar ou não houver Instagram, seguir sem gravar: não é motivo para travar a conexão, e o `/trafego-criar-campanha` pergunta na hora.

### 6.4 Regras de formato

- Só dígitos, sem o prefixo `act_`.
- `FB_AD_ACCOUNT_IDS` separado por vírgula, sem espaço.
- O `FB_AD_ACCOUNT_ID` precisa aparecer também dentro de `FB_AD_ACCOUNT_IDS`.
- Nunca gravar `META_AUTH_MODO` com valor diferente de `MCP_CONECTOR` ou `APP`.

---

## 7. Saída final

```
✅ Conexão com o Meta Ads configurada.

Modo ativo: {Conector da Meta (MCP) | App do Facebook Developers}
Conta padrão: {nome} (act_{id})
Salvo no .env: META_AUTH_MODO={MCP_CONECTOR | APP}, FB_AD_ACCOUNT_ID,
FB_AD_ACCOUNT_IDS{, FB_PAGE_ID, FB_INSTAGRAM_USER_ID}

As skills de tráfego vão ler essa preferência e usar o caminho certo
sozinhas. Você não precisa configurar de novo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Antes da primeira campanha, confirme que o pixel está instalado
    na sua página e disparando eventos. O /trafego-criar-campanha
    exige pixel ativo para venda direta e captação.

    Página feita aqui no projeto: instale com /pagina-pixel.
    Para conferir se os eventos estão chegando: /trafego-pixel.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔭 Próximo passo recomendado: /trafego-criar-campanha
Suba sua primeira campanha (venda direta ou captação de leads).

Já tem campanhas rodando? Comece por /trafego-analise (leitura
narrada) ou /trafego-dashboard (painel da conta).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para trocar o modo no futuro, rode /trafego-conexao de novo.
```

---

## 8. Como as outras skills usam a conexão

Toda skill que fala com o Meta Ads, no Passo 0 (depois de ler o produto ativo e o `resumo-produto.md`):

1. Ler `META_AUTH_MODO` com `grep "^META_AUTH_MODO=" .env | cut -d= -f2-`.
2. **Vazio, ausente ou valor não reconhecido** (inclusive o legado `HIBRIDO`): acionar `/trafego-conexao` e aguardar. Não adivinhar, não cair em fallback, não pedir credencial avulsa.
3. **`MCP_CONECTOR`:** usar as tools do conector, descobertas pelo final do nome (seção 5.1). O `ad_account_id` vem de `FB_AD_ACCOUNT_ID`: conferir antes se ele tem valor (`grep -q "^FB_AD_ACCOUNT_ID=." .env`). Se faltar (conexão feita por uma versão antiga, que no MCP não gravava a conta), acionar `/trafego-conexao`, que vai direto à opção "Validar a conexão atual" do Caso 1 (seção 1) e completa a conta pela 5.1.1: lista com `ads_get_ad_accounts`, grava sem perguntar quando há 1 conta liberada e pergunta quando há mais. Depois, voltar à skill. Nunca chamar o conector com a conta vazia. Nunca montar `curl` com token nesse modo, mesmo que exista um token antigo no `.env`. Nas 4 lacunas, seguir o passo manual guiado (seção "Lacunas do MCP").
4. **`APP`:** conferir se `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` têm valor, com o padrão da seção "LEITURA SEGURA DO .env" do CLAUDE.md (linha vazia conta como ausente). Se faltar algum, acionar `/trafego-conexao`. Chamadas por `curl`, uma por `Bash`, com o token por substituição dentro do próprio comando e `curl -g` quando o `fields=` tiver campos aninhados (regras do CLAUDE.md).
5. **Escrita na conta, nos dois modos:** bloco 🛡️ do CLAUDE.md antes de executar, um "sim" por lote dentro do mesmo fluxo, e exclusão sempre com bloco e "sim" próprios (L4).

Esta skill é idempotente: pode ser chamada várias vezes sem efeito colateral.

---

## 9. Princípios que esta skill nunca viola

1. **Nunca salvar `META_AUTH_MODO` antes da validação passar.** Evita o estado em que a conexão parece pronta e as outras skills falham.
2. **Conector sempre primeiro, sem perguntar o modo.** Mesmo com `FB_ACCESS_TOKEN_PERMANENTE` antigo no `.env`, a primeira conexão vai pelo conector e é testada.
3. **App só depois do teste.** Ele é oferecido quando a conta não foi liberada no conector (5.1.2) ou o conector não responde depois das conferências da 5.1. Nunca como opção inicial.
4. **Nunca pedir token no caminho MCP.** A autenticação fica na conta do Claude.
5. **Sempre validar antes de declarar pronto.** MCP: uma chamada de leitura. APP: os 3 testes.
6. **Nunca exibir o token nem o conteúdo do `.env`.** Usar `grep -q` para presença, substituição dentro do `curl` para uso e `***TOKEN_MASCARADO***` ou "salvo" na exibição.
7. **Nunca usar `python3 << 'EOF'` nem `curl | python3 -c` com o token.** Cada `curl` é uma chamada `Bash` independente.
8. **Nunca tocar em `RELATORIO_AUTH_MODO`.**
9. **Nunca gravar `HIBRIDO`.** Só existem `MCP_CONECTOR` e `APP`. Lacuna do conector se resolve com passo manual guiado, não com troca de modo.
10. **Nunca pedir o ID da conta ao aluno** quando a listagem automática está disponível.

# Regras da Meta API no projeto

> Leitura obrigatória antes de qualquer leitura ou escrita na conta de anúncios da Meta, pelo conector (MCP) ou pela Graph API (`graph.facebook.com`). Vale para todos os comandos `/trafego-*`, para os agentes e para qualquer outra skill que toque a conta. Estas regras saíram do CLAUDE.md para ele ficar mais leve; as regras de segurança (token só no `.env`, mascaramento, leitura segura do `.env` e confirmação antes de qualquer escrita na conta) continuam no CLAUDE.md e valem sempre.

## 1. CONEXÃO META OBRIGATÓRIA NO PASSO 0

> Esta regra tem prioridade sobre qualquer outra instrução de execução das skills de tráfego. Aplica-se a todo command que comece com `/trafego-*` ou que precise tocar a Marketing API do Meta (Facebook Ads, Instagram Ads).

**Toda skill que faz operação no Meta Ads precisa de conexão configurada antes de qualquer outra ação.** A conexão é estabelecida pelo command `/trafego-conexao`, que valida e salva o modo em `META_AUTH_MODO` no `.env`. O aluno não escolhe o modo no início: a conexão sempre começa pelo conector da Meta e é testada; o App só é oferecido depois desse teste, quando a conta não foi liberada no conector ou o conector não responde. Existem só dois modos:

- **`MCP_CONECTOR` (padrão, recomendado).** Conector oficial Claude + Meta, login por OAuth, sem token e sem App no Facebook Developers.
- **`APP` (reserva).** App via Facebook Developers com token permanente no `.env`. Serve para quem tem a conta de anúncios ainda não liberada pela Meta no MCP (a Meta libera conta por conta; a conta não liberada devolve `is_ads_mcp_enabled: false` ou o erro "Ads MCP is gradually being rolled out"). Configurado pela sequência `/criar-aplicativo-analise-ads` e `/gerar-token-permanente-facebook-ads` (que já lista as contas e grava a conta padrão). O `/obter-id-conta-anuncios` só entra se a conta padrão continuar faltando depois dessa listagem.

Não existe modo híbrido no Severino. Se o `.env` trouxer `META_AUTH_MODO=HIBRIDO` (de outro material), o `/trafego-conexao` explica e regrava como `MCP_CONECTOR` (ou `APP`, se a conta não estiver liberada no MCP) depois de validar e confirmar com o aluno.

### O que o MCP da Meta ainda não faz

No modo `MCP_CONECTOR`, estas operações não têm ferramenta no conector. A skill não troca de modo sozinha: conduz o aluno por um passo a passo curto no Gerenciador de Anúncios e depois segue o fluxo.

1. **Subir vídeo novo.** O MCP só usa vídeo que já está na biblioteca da conta. O aluno sobe o vídeo pelo Gerenciador e a skill segue usando esse vídeo.
2. **Buscar interesse por nome.** Recomendar público aberto com Advantage+. Se o aluno quiser interesse específico, ele pesquisa no Gerenciador.
3. **Criar ou gerenciar regra automática.** A skill ajuda a desenhar a regra e o aluno cria no Gerenciador (Regras automatizadas). Liga e pausa por horário continua pelo MCP.
4. **Apagar campanha, conjunto ou anúncio.** O MCP só apaga público. Para o resto: pausar ou arquivar pelo MCP, ou apagar no Gerenciador.
5. **Subir imagem que está só no computador.** O MCP aceita imagem por URL pública, mas não recebe arquivo. Padrão: o aluno sobe todas as imagens de uma vez na Biblioteca de mídia do Gerenciador e a skill pega pelo conector. Reserva: token usado só para subir a mídia (`FB_TOKEN_MIDIA`, temporário, apagado no fim do lote, ou o `FB_ACCESS_TOKEN_PERMANENTE` se existir), sem trocar o modo. Detalhes na lacuna L5 da skill `trafego-conexao`.

Público semelhante (lookalike), público de engajamento e de visualização de vídeo já são criados pelo MCP.

### Passo 0 obrigatório de toda skill de tráfego

Antes de executar qualquer ação, a skill deve:

1. **Ler `META_AUTH_MODO`** no `.env`.
2. **Se vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive o legado `HIBRIDO`): acionar `/trafego-conexao` e aguardar conclusão. Não tentar adivinhar, não cair em fallback, não pedir credenciais ad-hoc.
3. **Se `MCP_CONECTOR`:** confirmar que pelo menos uma tool cujo nome termina em `ads_get_ad_accounts` (ou outra `ads_*` do conector da Meta) está disponível. O começo do nome da tool varia de instalação para instalação. Se nenhuma estiver, instruir o aluno a reabrir o Claude Code (MCP recém-adicionado pode precisar de reload). Se persistir, voltar ao `/trafego-conexao` para diagnosticar. Se a conta escolhida vier como não liberada, oferecer o modo App pelo `/trafego-conexao`. Conferir também se `FB_AD_ACCOUNT_ID` tem valor (padrão da seção "LEITURA SEGURA DO .env" do CLAUDE.md). Se faltar (conexão feita por uma versão antiga, que no MCP não gravava a conta), acionar `/trafego-conexao`: ele completa a conta pela opção Validar (seção 5.1.1 da SKILL: lista com `ads_get_ad_accounts`, grava sem perguntar quando há 1 conta liberada e pergunta quando há mais) e volta para a skill. Nunca chamar o conector com a conta vazia.
4. **Se `APP`:** confirmar que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` têm valor no `.env`, sempre com o padrão da seção "LEITURA SEGURA DO .env" do CLAUDE.md (linha vazia conta como ausente). Se faltar algum, acionar `/trafego-conexao`. O `FB_PAGE_ID`, usado pelo `/trafego-criar-campanha`, é descoberto e gravado pela própria skill ou pelo `/trafego-conexao` quando falta.

A skill **nunca prossegue** sem essa validação passar.

### Skills que herdam essa regra

Todos os commands `/trafego-*` invocáveis pelo usuário:
- `/trafego-insights`. Leitura de métricas (com cache local em arquivo .md).
- `/trafego-criar-campanha`. Criação de campanha via Marketing API ou MCP.
- `/trafego-otimizar`. Diagnóstico e otimização, com camada de lucro. Inclui ações em lote por filtro e atalhos compostos.
- `/trafego-escalar`. Escala de campanha validada (também acionada pelo `/trafego-otimizar` quando `sinal_para_escala.pronta: true`).
- `/trafego-analise`. Análise narrada VTSD em 10 outputs.
- `/trafego-diagnostico`. Investigação antes de agir: hipóteses, auditoria estrutural, falso vencedor e score de confiança (apenas leitura).
- `/trafego-criativos`. Leitura de atenção, intenção e conversão dos criativos, DNA e briefing do próximo teste (apenas leitura).
- `/trafego-oferta-funil`. Funil depois do clique, congruência anúncio x página, oferta e checkout (apenas leitura).
- `/trafego-pixel`. Diagnóstico de pixels e eventos (apenas leitura).
- `/trafego-publicos`. Cria e gerencia públicos (personalizado, semelhante, engajamento, lista de clientes, bases por nível).
- `/trafego-regras`. Regras automáticas e liga e pausa por horário.
- `/trafego-testes`. Testes A/B disciplinados, duplicação variando uma coisa só e campanha de remarketing.
- `/trafego-dashboard`. Dashboard da conta de anúncios (artefato do Claude com o conector MCP da Meta, montado a partir de um modelo pronto), com vendas da Hotmart ou da Kiwify quando há credenciais no `.env`. Para conta que a Meta ainda não liberou no conector, o mesmo painel com dados gravados: o Claude busca os números com o token do App no computador do aluno e grava no banco do artefato, e o token nunca vai para a página. Sem artefato, dashboard estático (legado).
- `/trafego-dashboard-analisador`. Só para mandar o dashboard ao analisador da mentoria: fotografia fixa dos números da última atualização do dashboard, publicada como página que o analisador consegue abrir, com o link para colar no card do Fluxer.

**Base de conhecimento (não invocável diretamente):**
- `trafego-pago`. Conceitos e métricas de tráfego consultados pelas outras skills.

### Onde as skills de tráfego salvam

- Relatórios e entregas: `meus-produtos/{ativo}/entregas/trafego/` (com subpastas por skill, ex: `diagnostico/`, `criativos/`, `oferta-funil/`, `testes/`, `otimizar/`).
- Dados de trabalho do produto: `meus-produtos/{ativo}/trafego/` (cache de insights, HTML da análise, histórico de escala).
- O que pertence à conta de anúncios e não a um produto: `meus-produtos/_global/trafego/` (`insights/` da conta, `publicos/`, `regras/`, `pixel/`).

Os commands legados (`/ads-relatorio`, `/enviar-relatorio-ads`, `/lt-otimizar`) usam variáveis próprias (`RELATORIO_AUTH_MODO=CLI`, `ACCESS_TOKEN`, `AD_ACCOUNT_ID`) e não dependem de `META_AUTH_MODO`. Migração desses commands é tarefa separada.

### Quando outras skills de tráfego forem criadas no futuro

Toda skill nova que precise se conectar ao Meta Ads deve seguir o mesmo padrão de Passo 0: ler `META_AUTH_MODO` antes de qualquer outra ação, e acionar `/trafego-conexao` se a variável não estiver configurada. A skill `/trafego-conexao` é idempotente, pode ser chamada várias vezes sem efeito colateral.


## 2. EXECUÇÃO TÉCNICA DE CHAMADAS GRAPH API (REGRA GLOBAL)

> Esta regra tem prioridade absoluta. Aplica-se a toda skill ou agente que faça chamada para `https://graph.facebook.com/*`.

### Padrão obrigatório

1. **Cada chamada Graph API = 1 chamada `Bash(curl ...)` separada.** Token vai inline na URL.
2. **Cada cálculo de data = 1 `Bash(date ...)` separado.** Já autorizado em `.claude/settings.local.json`.
3. **Processamento dos JSONs retornados = feito pelo Claude lendo a saída do curl como texto.** Sem rodar Python adicional.

### Proibições absolutas

- **PROIBIDO `python3 << 'EOF' ... EOF`** (heredoc bash com Python). O detector "expansion obfuscation" do Claude Code dispara em qualquer heredoc que carregue token e ignora o allow list, forçando pop-up nativo com token visível.
- **PROIBIDO `curl ... | python3 -c "..."`** (pipe com Python que lê stdin). Mesma classe de detector dispara.
- **PROIBIDO `python3 -c "<código longo com token>"`.** Apenas `python3 -c` com expressões curtas e sem token (ex: `python3 -c "import json; print(json.load(open('/tmp/x.json')))"`).
- **PROIBIDO scripts bash multi-linha começando com `TOKEN="..."`** + múltiplos `curl`. Mesmo problema.

### Padrão correto para análises complexas (ex: comparativo CPM/ROAS, ranking, lifecycle, períodos múltiplos)

Quando uma skill precisa de várias chamadas Graph API + cálculos:

1. Calcular timestamps via `Bash(date +%s)` separados (cada um = 1 Bash call).
2. Para cada chamada Graph API, disparar `Bash(curl -s "https://graph.facebook.com/...?access_token=$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)")` **individual**, com o token entrando por substituição dentro do próprio `curl`, como no padrão da seção "LEITURA SEGURA DO .env" do CLAUDE.md. Nunca ler o valor para depois colar no comando.
3. Receber o JSON de retorno como texto.
4. Processar mentalmente os JSONs (somar, comparar, calcular delta) — Claude faz o cálculo direto na resposta, sem código intermediário.
5. Apresentar resultado ao aluno em linguagem natural, mascarando qualquer token na exibição.

### Convenção `curl -g` quando o `fields` tem campos aninhados

Quando o parâmetro `fields=` usar campos aninhados (ex: `campaign{name}`, `creative{video_id,thumbnail_url}`), usar `curl -g`. Sem o `-g`, o curl trata `{` e `}` como padrão de expansão e corta a URL sem avisar: a Graph API responde 200, mas sem os campos aninhados.

```bash
curl -gs "https://graph.facebook.com/v25.0/act_<id>/ads?fields=id,creative{video_id,thumbnail_url}&access_token=..."
```

### Por que essa restrição existe

O Claude Code tem proteções anti-injection que ignoram allow list quando detectam padrões suspeitos:
- Heredoc bash + variável interpolada
- Pipe com Python que recebe stdin
- Script bash com aspas duplas dentro de aspas simples
- Brace expansion combinada com aspas (`${...}`, `$(...)`)

Em todas essas situações, o pop-up nativo dispara e exibe o comando completo. O perigo está no formato em que o token aparece escrito no próprio comando (heredoc, `TOKEN="..."`, pipe para Python): aí ele vai inteiro para a tela. A única exceção é a gravação do segredo que o aluno acabou de colar (item 4 da seção "LEITURA SEGURA DO .env" do CLAUDE.md), que não serve de modelo para nenhuma outra chamada. O formato padrão do projeto é cada chamada Graph API como um `curl` simples, com o token entrando por substituição (`$(grep ^FB_ACCESS_TOKEN_PERMANENTE= .env | cut -d= -f2-)`). Esse formato também pode pedir aprovação, mas o pop-up mostra só a expressão, nunca o valor do token.

### Exceção controlada

Se a análise realmente precisa de processamento que não dá pra fazer mentalmente (ex: agrupar 200+ ads por idade × posicionamento × hora):

1. Salvar JSONs em arquivos via `curl ... > /tmp/insights-{nome}.json` (cada um = 1 Bash call, casa com `Bash(curl ...)`).
2. Processar com `Bash(python3 /tmp/script.py)` onde `/tmp/script.py` foi escrito previamente via `Edit` ou `Write` no arquivo (sem token dentro do script — script lê os JSONs locais).
3. Limpar `/tmp/insights-*.json` ao final.

Esse caminho mantém cada chamada Bash simples e cobre o pattern matching.


## 3. Operações de escrita e skill que executa cada uma

Complemento da seção "GATE EM CAMADA DE CHAT ANTES DE OPERAÇÕES DE ESCRITA NA META GRAPH API" do CLAUDE.md (o bloco 🛡️ e as regras de confirmação ficam lá).


| Operação semântica | Método HTTP | Skill que executa |
|---|---|---|
| Criar campanha | POST `/campaigns` | `/trafego-criar-campanha` |
| Atualizar campanha (status, budget) | POST `/{campaign_id}` | `/trafego-otimizar`, `/trafego-escalar` |
| Pausar / ativar adset | POST `/{adset_id}` | `/trafego-otimizar`, `/trafego-regras` |
| Atualizar orçamento de adset/campanha | POST `/{id}` com `daily_budget` | `/trafego-otimizar`, `/trafego-escalar` |
| Pausar / ativar anúncio | POST `/{ad_id}` | `/trafego-otimizar` |
| Arquivar anúncio, conjunto ou campanha (apagar, não: não há ferramenta no MCP e não se roda `curl -X DELETE` direto, regra 7; a exclusão é feita à mão no Gerenciador) | POST `/{id}` com `status=ARCHIVED` ou `ads_update_entity` | `/trafego-otimizar` |
| Criar público (personalizado, semelhante, engajamento, lista de clientes) | POST `/customaudiences` ou `ads_create_custom_audience` | `/trafego-publicos` |
| Apagar público | `ads_delete_custom_audience` (sempre à parte, regra 7) | `/trafego-publicos` |
| Criar regra automática | POST `/adrules_library` (só no modo App; no MCP é feita à mão no Gerenciador) | `/trafego-regras` |
| Programar liga e pausa por horário | POST `/{adset_id}` com `adset_schedule` | `/trafego-regras` |
| Subir imagem ou vídeo de criativo | POST `/adimages`, POST `/advideos` | `/trafego-criar-campanha`, `/trafego-testes` |
| Duplicar adset / campanha (cria novo) | POST `/{id}/copies` ou `ads_create_*` com `source_*_id` | `/trafego-escalar`, `/trafego-testes` |
| Lote (em massa) | qualquer combinação acima | `acoes-lote.md` (sub-skill de `/trafego-otimizar`) |

### Princípio de fundo

A autorização no settings é confiança operacional (evita pop-up + vazamento visual de token). O gate em camada de chat é confiança semântica (aluno aprova o QUE vai ser feito, não o COMO). As duas camadas juntas dão segurança sem fricção tóxica.

---
name: workshop-marketing:trafego-conexao
description: Porta única de entrada para conectar o projeto com o Meta Ads (Facebook + Instagram). Confere os pré-requisitos no Meta, pergunta se o aluno quer usar o conector oficial da Meta no Claude (recomendado, MCP via OAuth) ou o App via Facebook Developers (reserva, token permanente no .env), valida a conexão e salva o modo em META_AUTH_MODO e a conta padrão em FB_AD_ACCOUNT_ID. Skill reutilizável, chamada por qualquer skill de Meta Ads quando META_AUTH_MODO ainda não está configurada ou tem valor antigo.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Tráfego Conexão. Conectar o Projeto com o Meta Ads

Orquestrador da conexão. Pergunta o modo, executa o caminho escolhido, valida e salva a preferência em `META_AUTH_MODO` no `.env`. As skills `/trafego-*` e os commands `/ads-relatorio`, `/enviar-relatorio-ads` e `/lt-otimizar` leem essa variável para saber qual caminho usar.

A especificação técnica completa está em `.claude/skills/trafego-conexao/SKILL.md`. Leia esse arquivo antes do Passo 0: ele é a fonte de verdade de cada passo abaixo.

Os dois modos:

- **`MCP_CONECTOR`** (recomendado). Conector oficial da Meta adicionado no Claude. Login pelo Facebook, sem token, sem App, sem instalar nada.
- **`APP`** (reserva). App no Facebook Developers com token permanente no `.env`. Para quem tem a conta de anúncios ainda não liberada pela Meta no conector.

---

## Pré-requisitos no Meta (antes do Passo 0)

Aplicar a seção **0. Pré-requisitos no Meta** da SKILL. Se o aluno não tiver certeza de que já tem Business Manager, Página, Conta de Anúncios, forma de pagamento e pixel, perguntar. Faltando algo, mostrar o mapa de onde criar cada item, encerrar e pedir para rodar `/trafego-conexao` de novo quando terminar.

---

## Passo 0. Verificar estado atual

Aplicar a seção **1. Passo 0** da SKILL, lendo só a linha `META_AUTH_MODO` do `.env`:

- **`MCP_CONECTOR` ou `APP`:** oferecer manter, trocar ou validar.
- **`HIBRIDO` (valor legado de versão antiga):** explicar que agora só existem dois modos, perguntar e, com a confirmação do aluno, validar e regravar como `MCP_CONECTOR` (recomendado) ou `APP`. O token salvo continua no `.env`.
- **Valor não reconhecido:** avisar e seguir para o Passo 1.
- **Ausente ou vazio:** seguir para o Passo 1 sem aviso.

---

## Passo 1. Escolher o modo

Aplicar a seção **2. Passo 1** da SKILL. O aluno escolhe:

1. Conector da Meta no Claude (recomendado). Vai para o Passo 2A.
2. App via Facebook Developers (reserva). Vai para o Passo 2B.

---

## Passo 2A. Caminho MCP (adicionar o conector)

🔍 Próximo passo: adicionar o conector da Meta no Claude Desktop. Tempo estimado: cerca de 60 segundos.

Aplicar a seção **3.1** da SKILL: o aluno adiciona o conector personalizado (URL `https://mcp.facebook.com/ads`, nome "Meta Ads"), autoriza no Facebook e avisa "conectei". Depois, Passo 3.

Este passo também é usado pelo `/trafego-dashboard` quando o aluno ainda não tem o conector: nesse caso, depois do "conectei", voltar para o `/trafego-dashboard`.

---

## Passo 2B. Caminho App

🔍 Próximo passo: criar o App no Facebook Developers e gerar o token permanente. Tempo estimado: 8 a 12 minutos.

Aplicar a seção **4** da SKILL:

1. **4.1. Checar se já existe token** com `grep -q`. Se existir, oferecer usar o token atual (só valida) ou gerar um novo. Nunca mostrar o passo a passo de criação para quem já tem o App.
2. **4.2. Encadeamento das skills do App**, quando não há token:
   - `/criar-aplicativo-analise-ads` (cria e publica o App)
   - `/gerar-token-permanente-facebook-ads` (Usuário do Sistema, ativos, token, 3 testes, `FB_ACCESS_TOKEN_PERMANENTE`, `META_AUTH_MODO=APP` e conta padrão pela listagem automática)
   - `/obter-id-conta-anuncios`, só se a conta padrão continuar faltando depois da listagem automática
3. **4.3. Listagem automática das contas** quando a conta padrão não estiver gravada. O ID da conta nunca é pedido ao aluno quando a listagem está disponível.

Depois, Passo 3.

---

## Passo 3. Validar a conexão

Aplicar a seção **5** da SKILL, conforme o modo:

- **MCP:** seção 5.1 (descobrir a tool pelo final do nome `ads_get_ad_accounts` e chamar) e 5.1.1 (conta padrão com a coluna do conector, `is_ads_mcp_enabled`). Conta não liberada no conector: seção 5.1.2, que oferece o modo App.
- **APP:** seção 5.2 (3 testes, cada um numa chamada `Bash` própria) e, em caso de erro, o mapa de erros da seção 5.3.

Nunca salvar `META_AUTH_MODO` antes da validação passar.

✅ Concluído: conexão validada.

---

## Passo 4. Salvar no `.env`

Aplicar a seção **6** da SKILL:

- **MCP:** `META_AUTH_MODO=MCP_CONECTOR`, `FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS` (as tools de escrita do conector exigem a conta). Nenhum token.
- **APP:** conferir com `grep -q` o que o `/gerar-token-permanente-facebook-ads` já gravou e completar o que faltar.
- **Os dois modos:** tentar descobrir e gravar `FB_PAGE_ID` e `FB_INSTAGRAM_USER_ID` (seção 6.3). Se não der, seguir sem travar.

Não sobrescrever outras variáveis. Não tocar em `RELATORIO_AUTH_MODO`.

---

## Passo 5. Saída final

Aplicar a seção **7** da SKILL: confirmar o modo e a conta padrão, lembrar do pixel (`/pagina-pixel` para instalar, `/trafego-pixel` para conferir) e recomendar `/trafego-criar-campanha` como próximo passo.

---

## Princípios que este command nunca viola

Respeitar os princípios da seção **9** da SKILL. Em especial:

1. Nunca salvar `META_AUTH_MODO` antes da validação passar, e nunca gravar valor diferente de `MCP_CONECTOR` ou `APP`.
2. Nunca exibir o token nem o conteúdo do `.env` no chat. Presença com `grep -q`, uso por substituição dentro do `curl`, exibição com `***TOKEN_MASCARADO***` ou só "salvo".
3. Cada `curl` à Graph API é uma chamada `Bash` independente. Nunca `python3 << 'EOF'` nem `curl | python3 -c` com o token.
4. Nunca tocar em `RELATORIO_AUTH_MODO`.
5. Idempotente: pode ser chamado várias vezes sem efeito colateral.

---
name: workshop-marketing:trafego-conexao
description: Porta única de entrada para conectar o projeto com o Meta Ads (Facebook + Instagram). Pergunta se o aluno quer usar o conector personalizado da Meta no Claude (recomendado, MCP via OAuth) ou criar um App via Facebook Developers (token permanente no .env). Descobre e grava no .env o modo de autenticação, as contas de anúncio, a conta padrão, a Página e o perfil do Instagram. Use quando o aluno pedir "conectar Meta Ads", "conectar Facebook", "configurar conta de anúncio", "trocar de conta", ou quando qualquer skill de tráfego encontrar META_AUTH_MODO vazio.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
---

# Tráfego Conexão. Estabelecer Conexão com o Meta Ads

Conecta o projeto ao Meta Ads e grava no `.env` tudo que a stack de tráfego precisa para operar: modo de autenticação, contas de anúncio, conta padrão, Página e perfil do Instagram. É o passo zero de `/trafego-insights`, `/trafego-criar-campanha`, `/trafego-otimizar`, `/trafego-escalar` e `/trafego-analise`.

A especificação técnica completa está em `.claude/skills/trafego-conexao/SKILL.md`. Este command é o orquestrador.

---

## Passo 0. Ler a especificação

Leia `.claude/skills/trafego-conexao/SKILL.md` para carregar o contrato de saída (seção 1), a máquina de estados (seção 3), o mapa de erros (seção 4) e os princípios (seção 6).

Em seguida leia o `.env` na raiz do projeto e localize a linha `META_AUTH_MODO`.

---

## Passo 1. Roteamento por estado

Aplique o Passo 0 da skill.

| Estado do `.env` | Rota |
|---|---|
| `META_AUTH_MODO` válido | Menu de 4 opções: manter, trocar, validar, redescobrir identificadores |
| `META_AUTH_MODO` inválido | Avisar e tratar como ausente. Seguir para o Passo 2 |
| `META_AUTH_MODO` ausente ou vazia | Seguir direto para o Passo 2 |

Quando o aluno escolher "redescobrir identificadores", pule a autenticação e vá direto aos Passos 3.5 e 3.6 da skill. Esse é o caminho para quem ganhou acesso a uma conta nova ou trocou a Página que assina os anúncios.

---

## Passo 2. Escolher o modo e autenticar

🔍 Próximo passo: conectar sua conta do Meta Ads (4 passos). Tempo estimado: 2 a 4 minutos.

Apresente as duas opções no formato exato do Passo 1 da skill, sempre com o conector em primeiro lugar.

- **Opção 1, `MCP_CONECTOR`.** Conduza o registro do conector personalizado (Passo 2A da skill) e aguarde a confirmação do aluno.
- **Opção 2, `APP`.** Acione `/criar-aplicativo-analise-ads`, que encadeia `/gerar-token-permanente-facebook-ads` e `/obter-id-conta-anuncios`. Ao voltar, confirme que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` existem no `.env`.

---

## Passo 3. Validar, descobrir e gravar

⏳ Passo 1/3: validar a conexão.

Rode o ramo de validação do modo escolhido (Passo 3 da skill). No modo `MCP_CONECTOR`, localize e chame a tool de listagem de contas. No modo `APP`, rode os 3 testes da Graph API, cada `curl` em uma chamada `Bash` separada.

Se a validação falhar, use o mapa de erros da seção 4 da skill. **Não grave nada e não avance.**

⏳ Passo 2/3: descobrir as contas de anúncio.

Aplique o Passo 3.5 da skill. Reaproveite o retorno da validação em vez de repetir a chamada. Grave `FB_AD_ACCOUNT_ID` e `FB_AD_ACCOUNT_IDS`, sem prefixo `act_` e sem espaço depois da vírgula.

⏳ Passo 3/3: descobrir Página e Instagram.

Aplique o Passo 3.6 da skill. Grave `FB_PAGE_ID` e, quando houver perfil vinculado, `FB_INSTAGRAM_USER_ID`. Instagram ausente é aviso, não bloqueio.

Só depois disso, grave `META_AUTH_MODO` (Passo 4 da skill). Essa é a última variável, e é ela que sela a conexão.

✅ Concluído: conexão validada e configuração gravada no `.env`.

---

## Passo 4. Saída final

Mostre o bloco de saída da skill com conta padrão, quantidade de contas disponíveis, Página e Instagram, sempre no formato `Nome (ID)`. Encerre com o handoff para `/trafego-criar-campanha`.

Nunca exiba token no chat, nem parcial. Ver a regra de mascaramento no `CLAUDE.md`.

---

## Regras deste command

1. **Nunca gravar `META_AUTH_MODO` antes da validação passar e dos identificadores serem descobertos.** Conexão pela metade quebra a skill seguinte, não esta.
2. **Nunca exibir o `curl` completo no chat.** Ele carrega o token.
3. **Cada chamada Graph API é um `Bash(curl ...)` separado.** Sem heredoc Python, sem pipe para `python3`.
4. **Este command é idempotente.** Pode rodar quantas vezes for preciso.
5. **Todo ID exibido vem com o nome humano junto.**

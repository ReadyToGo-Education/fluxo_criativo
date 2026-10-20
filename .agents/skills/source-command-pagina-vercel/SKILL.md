---
name: "source-command-pagina-vercel"
description: "Publicar uma página HTML do projeto direto na Vercel via API e devolver o link público. Inclui setup guiado do token da API. Skill de infraestrutura, última etapa do fluxo de página, depois de copy + performance + pixel + checkout."
---

# source-command-pagina-vercel

Use esta skill quando o usuário pedir o comando `/pagina-vercel` do workshop (ou `pagina-vercel`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/pagina-vercel.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Página Vercel. Publicação via API

Publica uma página HTML local diretamente na Vercel e devolve o link público pronto pra usar em anúncios, bio e emails. Sem upload manual, sem Git.

## Usage

```
/pagina-vercel
```

## O Que Fazer

Acione a skill `pagina-vercel` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo`. Se não houver produto, oriente a usar `/produto-novo`.
2. Verificar `VERCEL_API_TOKEN` no `.env`. Se não existir, mostrar setup guiado (cadastro em vercel.com > Settings > Tokens, colar o token no chat). O assistente salva no `.env` automaticamente, nunca pede pro usuário abrir o arquivo.
3. Coletar (uma pergunta por vez): qual página, nome do projeto na Vercel, conta pessoal ou time, modo (novo projeto ou nova versão de projeto existente).
4. Se já existe `meus-produtos/{ativo}/entregas/.vercel` com `project_id`, oferecer publicar nova versão do projeto anterior.
5. Mostrar resumo e pedir confirmação:
   ```
   1. Publicar
   2. Cancelar
   ```
6. Publicar via `curl` POST em `https://api.vercel.com/v13/deployments?skipAutoDetectionConfirmation=1` com payload no formato `{name, files: [{file, data}], target: "production", projectSettings: {framework: null}}`. A página vai como `index.html`. Usar arquivo de payload temporário pra evitar problema de tamanho. Apagar depois.
   - **Página com função no servidor.** Se o HTML chama `fetch('/api/...')` (pre-checkout do `/pagina-precheckout`, captura do `/pagina-active` no Modo B), incluir no mesmo `files` o arquivo da função que ela chama, saído de `meus-produtos/{ativo}/entregas/paginas/api/`, com o caminho `api/{nome}.js`. Só a função que a página chama, nunca a pasta inteira. Sem esse arquivo no mesmo deploy, o formulário não tem para onde enviar.
7. Se o deploy voltar como `QUEUED` ou `BUILDING`, fazer polling em `GET /v13/deployments/{id}` até virar `READY` (máximo 30 segundos).
8. Tratar erros de API (até 3 tentativas com ajuste). Se persistir, mostrar erro completo e perguntar como prosseguir.
9. **Se subiu função, cadastrar as variáveis de ambiente e publicar de novo.** A função lê chaves e destinos de `process.env`, e a Vercel só entrega uma variável à função depois de um novo deploy.
   - Liste as variáveis que a função lê (`process.env.NOME`) e mostre ao aluno só os nomes.
   - Ofereça cadastrar pelo próprio Severino: com a confirmação do aluno no chat, chamar `POST https://api.vercel.com/v10/projects/{projeto}/env?upsert=true` uma vez por variável, com `{key, value, type: "encrypted", target: ["production"]}`. O valor vem do `.env` lido no próprio comando (`source .env` e `$NOME_DA_VARIAVEL`), nunca escrito no comando, num arquivo ou no chat.
   - Variável que não está no `.env` (ex: URL do webhook do Zapier ou do Apps Script): peça ao aluno para colar no chat, salve no `.env` e siga o item anterior. Alternativa manual: no painel da Vercel, abrir o projeto, Settings > Environment Variables, preencher Name e Value, marcar Production e salvar.
   - Depois de cadastrar, publique de novo com o mesmo `files` (novo POST em `/v13/deployments`).
   - Por fim, oriente a regra de limite de envios no firewall, que vale na hora, sem novo deploy: no painel, abrir o projeto, Firewall, Configure, nova regra; em **If**, Request Path começa com `/api/`; em **Then**, Rate Limit, por IP, 5 envios por minuto; salvar e publicar a regra. O plano grátis da Vercel permite uma regra de limite por projeto, por isso a regra cobre todas as funções em `/api/`.
10. Salvar histórico em `meus-produtos/{ativo}/entregas/.vercel` e atualizar `meus-produtos/{ativo}/entregas/paginas/.vercel-link.md` com o link público.
11. Mostrar resumo final com URL pública (`https://{projeto}.vercel.app`) e sugerir próximos passos: se a página tem formulário, preencher com um e-mail próprio e conferir se o lead chegou ao destino; depois, usar o link no `/copy-anuncio` para tráfego pago.

## Regras Resumidas

- Nunca pedir login/senha da Vercel. Só o token da API, colado no chat.
- Nunca expor o token em mensagens, logs ou arquivos fora do `.env`. O mesmo vale para os valores das variáveis de ambiente da função: o aluno vê só os nomes.
- Cadastrar variável de ambiente na Vercel muda a configuração do projeto do aluno: sempre pedir confirmação no chat antes.
- `.env` deve estar no `.gitignore` (validar antes de salvar).
- Sempre confirmar antes de publicar.
- Nome do projeto precisa ser minúsculo, sem acentos, sem espaços. Normalizar silenciosamente se o usuário informar fora do padrão.
- A documentação oficial da Vercel (`vercel.com/docs/rest-api`) é fonte de verdade. Se a chamada falhar, ler o erro e adaptar. Não tentar adivinhar mais de 3 vezes.
- Não usar travessão em nenhum texto exibido.

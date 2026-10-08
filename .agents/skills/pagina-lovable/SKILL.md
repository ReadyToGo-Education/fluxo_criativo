---
name: pagina-lovable
description: >
  Publica uma página HTML do projeto direto no Lovable via API, sem o aluno
  precisar fazer upload manual nem mexer em servidor. Configura a chave da API,
  faz o deploy, devolve o link público da página e salva o histórico. Skill de
  infraestrutura. Roda depois da página estar pronta, idealmente após
  /pagina-performance, /pagina-pixel e /pagina-checkout.
---

# Página Lovable. Publicação via API

Pega uma página HTML local e publica diretamente no Lovable, devolvendo o link público pra usar em anúncio, biografia, email, onde quer que seja. Sem upload manual, sem WordPress, sem hospedagem própria.

## Quando Usar

- Última etapa do fluxo de página, depois que tudo já foi feito (copy + performance + pixel + checkout).
- Quando o usuário disser "publica essa página", "manda pro Lovable", "preciso do link", "hospeda essa página".

## O Que Fazer

### 0. Contexto e verificação de API

Leia `entregas/.ativo`. Se não houver produto, oriente a rodar `/produto-novo` antes.

**Verificar chave da API do Lovable:**

Leia `.env` e procure `LOVABLE_API_KEY`.

**Cenário A. Chave existe e não está vazia.** Siga em frente.

**Cenário B. Chave não existe ou está vazia.**

Mostre o setup guiado:
```
Pra publicar no Lovable preciso da API key dele. Cadastro rápido:

1. Acesse https://lovable.dev e faça login
2. Vá em Settings > API Keys
3. Clique em "Create API key"
4. Copie a chave gerada (começa com lov_ ou similar)
5. Cole aqui no chat

Não abra o .env, eu salvo a chave pra você.
```

Quando o usuário colar a chave:
- Valide que tem mais de 20 caracteres e é alfanumérica.
- Salve no `.env` na raiz do projeto, na linha `LOVABLE_API_KEY=...`. Se a linha já existir, substitua o valor. Se o `.env` não existir, crie.
- Verifique se `.env` está no `.gitignore`. Se não estiver, adicione.
- Confirme: "Chave salva. Pronto pra publicar."

(Padrão do projeto, ver memória `feedback_chaves_api_no_chat`. Nunca pedir pra abrir o .env.)

### 1. Coletar dados (uma pergunta por vez)

**Pergunta 1. Qual página vou publicar?**
1. Última página salva em `entregas/{ativo}/paginas/`
2. Outra (informar caminho)

**Pergunta 2. Qual nome vai aparecer no Lovable?**
(ex: `crenca-raiz-vendas`, `quiz-tarot`, `inscricao-retiro`)

Sugira como padrão: `{ativo}-{nome do arquivo sem extensão}`. Se o usuário aprovar, use isso.

**Pergunta 3. Subdomínio personalizado?**
1. Usar o subdomínio padrão que o Lovable atribuir
2. Quero escolher o subdomínio (ex: `crencaraiz`)

Se 2, peça o subdomínio. Avise que pode estar ocupado, e nesse caso o Lovable retorna erro e a gente tenta outro.

**Pergunta 4. Versionamento?**
1. Publicar como nova página (cria do zero no Lovable)
2. Atualizar uma página que já existe lá (preciso do project_id)

Se já existe registro em `entregas/{ativo}/.lovable` com `project_id` da página, ofereça direto "Atualizar `nome` (publicada em {data})".

### 2. Confirmação antes de subir

Mostre o resumo:
```
Vou publicar agora:

Arquivo:     entregas/{ativo}/paginas/{nome}.html
Tamanho:     {KB}
Nome:        {nome}
Subdomínio:  {auto / escolhido}
Modo:        {nova / atualizar}

1. Publicar
2. Cancelar
```

### 3. Publicação via API

Use `Bash` com `curl` pra fazer a requisição. Endpoint base e payload conforme documentação do Lovable.

**Cenário "nova página":**
```bash
curl -X POST "https://api.lovable.dev/v1/projects" \
  -H "Authorization: Bearer $LOVABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "{nome}",
    "subdomain": "{subdomínio ou null}",
    "html": "{conteúdo do arquivo escapado}"
  }'
```

**Cenário "atualizar página existente":**
```bash
curl -X PATCH "https://api.lovable.dev/v1/projects/{project_id}" \
  -H "Authorization: Bearer $LOVABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "html": "{conteúdo do arquivo escapado}"
  }'
```

Por causa do tamanho do HTML, em vez de embutir o conteúdo direto na linha de comando, salve o body num arquivo temporário JSON em `entregas/{ativo}/paginas/.lovable-payload.json` e use `--data @arquivo`. Apague depois.

**Importante.** A documentação oficial do Lovable é a fonte de verdade. Se a chamada falhar com 404 ou 400, leia a mensagem de erro do response e adapte (ex: endpoint pode ser `/v1/sites`, header pode ser `X-API-Key`, payload pode usar `content` em vez de `html`). Não tente "adivinhar" mais de 3 vezes. Se passar de 3 tentativas, mostre o erro completo pro usuário e pergunte:
```
A API do Lovable retornou um erro que não consigo resolver sozinho.
Erro: {mensagem}

1. Tentar de novo (com ajuste)
2. Confere a documentação do Lovable e me passa o endpoint correto
3. Cancelar
```

### 4. Salvar histórico

Em sucesso, salve em `entregas/{ativo}/.lovable` (modo append):
```
{timestamp}|{nome}|{project_id}|{url_publica}|{arquivo}
```

E também atualize/crie `entregas/{ativo}/paginas/.lovable-link.md`:
```
# Páginas publicadas no Lovable

## {nome}
- URL: {url_publica}
- Project ID: {project_id}
- Arquivo local: {caminho}
- Última publicação: {data}
```

### 5. Resumo final

```
Pronto. Página publicada.

URL pública:  {url}
Project ID:   {id}
Arquivo:      {caminho local}
Histórico:    entregas/{ativo}/.lovable

Próximos passos sugeridos:
- Cole o link na bio do Instagram
- Use no /copy-anuncio como destino dos anúncios
```

## Regras

- Nunca peça login ou senha do Lovable. Só a API key, que o usuário cola no chat.
- Nunca exponha a chave em mensagens, logs ou arquivos fora do `.env`. Não imprima a chave no resumo.
- Sempre confirme antes de publicar. Publicação é ação irreversível em termos de URL pública.
- Se a API key ficar inválida (401), avise e peça uma nova, salvando por cima.
- Se a documentação real do Lovable divergir do template usado aqui, **prefira a documentação oficial**, esses payloads são exemplos.
- Não use travessão em nenhum texto exibido ao usuário.

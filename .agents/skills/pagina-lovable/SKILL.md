---
name: pagina-lovable
description: >
  Leva uma página HTML do projeto para o Lovable e devolve o link público
  .lovable.app. Com o conector do Lovable ligado no Claude, cria o projeto,
  confere e publica sozinho. Sem o conector, entrega um prompt pronto para
  colar no Lovable. Skill de infraestrutura. Roda depois da página estar
  pronta, idealmente após /pagina-performance, /pagina-pixel e /pagina-checkout.
---

# Página Lovable. Publicação pelo conector do Lovable

Pega uma página HTML local e leva para o Lovable, devolvendo o link público pra usar em anúncio, biografia, email, onde quer que seja.

## Como o Lovable recebe uma página (leia antes de tudo)

O Lovable não tem caminho para subir um HTML pronto e publicar como está. A API pública dele só republica projetos que já existem e exige plano Business ou Enterprise. Por isso esta skill não usa chave de API do Lovable.

Os dois caminhos reais:

1. **Conector do Lovable no Claude (padrão).** O Claude manda a página como anexo, o Lovable recria a página no projeto dele, o Claude confere e publica. Funciona em todos os planos do Lovable e gasta créditos da conta do aluno.
2. **Prompt pronto (sem conector).** O Severino monta um prompt com o conteúdo e o visual da página, e o aluno cola no chat do Lovable.

Nos dois caminhos o Lovable **recria** a página com a IA dele. Ela não é copiada byte a byte: texto, cores e links são pedidos de forma literal, mas o aluno confere antes de publicar. Quando a página precisa sair idêntica ao arquivo, o caminho é o `/pagina-vercel`, que publica o HTML exatamente como está.

## Quando Usar

- Última etapa do fluxo de página, depois que tudo já foi feito (copy + performance + pixel + checkout).
- Quando o usuário disser "manda pro Lovable", "publica no Lovable", "quero editar essa página no Lovable".
- Se o usuário só quer o link público e não faz questão do Lovable, ofereça também o `/pagina-vercel`.

## O Que Fazer

### 0. Contexto e verificações

Leia `meus-produtos/.ativo`. Se não houver produto, oriente a rodar `/produto-novo` antes.

**Página com função no servidor não vai para o Lovable.** Se o HTML chama `fetch('/api/...')` (pre-checkout do `/pagina-precheckout` no modo com função, captura do `/pagina-active` no Modo B), pare e explique: "Essa página depende de uma função que só roda na Vercel. Publique pelo /pagina-vercel, que sobe a página e a função juntas." Ofereça rodar o `/pagina-vercel`.

**Verificar o conector do Lovable:** procure ferramentas cujo nome termina em `__create_project`, `__deploy_project` e `__get_file_upload_url` (o conector do Lovable no Claude).

**Cenário A. O conector está disponível.** Siga para o passo 1.

**Cenário B. O conector não está disponível.** Mostre:
```
Pra publicar direto no Lovable, preciso que o Lovable esteja conectado ao Claude. É uma vez só:

1. No Claude, clique no + da caixa de mensagem
2. Conectores > Procurar conectores
3. Busque Lovable e clique em Conectar (ele pede o login do Lovable)
4. Feche o Claude por completo e abra de novo

Quem usa o Claude Code pelo terminal pode rodar: claude mcp add --transport http lovable "https://mcp.lovable.dev"

O que prefere?
1. Vou conectar agora e já volto
2. Seguir sem conector: você me dá o prompt pronto e eu colo no Lovable
3. Publicar pelo /pagina-vercel (a página sai idêntica ao arquivo)
```
Se 1, aguarde o aluno voltar e confira de novo. Se o conector continuar sem aparecer depois de reabrir o Claude, siga com a opção 2. Se 2, vá para o passo 6. Se 3, acione o `/pagina-vercel`.

### 1. Coletar dados (uma pergunta por vez)

**Pergunta 1. Qual página vou publicar?**
1. Última página salva em `meus-produtos/{ativo}/entregas/paginas/`
2. Outra (informar caminho)

**Pergunta 2. Qual nome vai aparecer no Lovable?**
(ex: `crenca-raiz-vendas`, `quiz-tarot`, `inscricao-retiro`)

Sugira como padrão: `{ativo}-{nome do arquivo sem extensão}`. Se o usuário aprovar, use isso.

**Pergunta 3. Nova página ou atualização?**
1. Publicar como nova página (cria um projeto novo no Lovable)
2. Atualizar uma página que já existe lá

Se já existe registro em `meus-produtos/{ativo}/entregas/.lovable` com o `project_id` dessa página, ofereça direto "Atualizar `nome` (publicada em {data})".

### 2. Confirmação antes de criar

Antes, chame a ferramenta `get_workspace` do conector (ou `list_workspaces`, se houver mais de uma área de trabalho) para saber em qual conta o projeto vai nascer e o saldo de créditos.

Mostre o resumo:
```
Vou levar a página para o Lovable:

Arquivo:     meus-produtos/{ativo}/entregas/paginas/{nome}.html
Tamanho:     {KB}
Nome:        {nome}
Conta:       {área de trabalho do Lovable}
Créditos:    {saldo}
Modo:        {nova / atualizar}

O Lovable recria a página com a IA dele e isso gasta créditos da sua conta. No plano grátis, uma página longa pode não terminar no mesmo dia.

1. Criar no Lovable
2. Cancelar
```

### 3. Criar no Lovable pelo conector

1. Chame `get_file_upload_url` com `file_name` = nome do arquivo HTML e `content_type` = `text/html`. Envie o arquivo para o `upload_url` devolvido com `curl -X PUT -T "{caminho do arquivo}" -H "Content-Type: text/html" "{upload_url}"` e guarde o `file_id`.
2. **Nova página:** chame `create_project` com `files` = [`file_id`], `wait` = verdadeiro e `initial_message` com o pedido abaixo. **Atualização:** chame `send_message` com o `project_id` salvo, o mesmo `file_id` em `files` e o pedido abaixo, trocando a primeira frase por "Substitua a página atual pela do arquivo HTML anexado."

Pedido (preencha os dados entre colchetes a partir do HTML):
```
Recrie como página única o arquivo HTML anexado, o mais fiel possível ao original.

Regras:
1. Copie todos os textos exatamente como estão no arquivo, com a mesma acentuação. Não reescreva, não resuma e não traduza nada.
2. Mantenha a ordem das seções, as cores, as fontes, os espaçamentos e o comportamento no celular do arquivo.
3. Mantenha todos os links e botões com os mesmos endereços, inclusive os de checkout: [lista dos links de checkout e de WhatsApp encontrados no HTML].
4. Mantenha as imagens com os mesmos endereços. Onde o arquivo tem um espaço reservado para imagem, mantenha o espaço reservado.
5. Se o arquivo tem Meta Pixel ou outro código de rastreamento no head, coloque o mesmo código no index.html do projeto, sem alterar o ID: [ID do Pixel, se houver].
6. Não crie login, banco de dados nem páginas extras. É só esta página.
7. Página em português do Brasil.
```

3. Se a resposta vier com status `awaiting_input`, o Lovable parou para pedir uma aprovação. Avise o aluno para abrir o projeto no Lovable e aprovar, ou responda pelo `send_message` se for uma pergunta simples sobre a página.
4. Se a chamada passar do tempo, acompanhe com `get_message`. Não repita o `create_project`: chamada repetida cria projeto duplicado ou devolve a mesma resposta.

### 4. Conferir antes de publicar

Chame `get_project` com o `project_id`. Ele devolve uma imagem da tela atual. Compare com o HTML local: seções na ordem, headline e textos principais iguais, botões de compra presentes. Se algo faltou, peça a correção com `send_message`, uma vez, citando exatamente o que mudar.

Mostre ao aluno o resultado da conferência e o link do projeto no Lovable para ele olhar, e pergunte:
```
A página ficou pronta no Lovable. Confira pelo link do projeto antes de publicar.

1. Publicar
2. Quero ajustar algo
3. Cancelar
```

### 5. Publicar

Chame `deploy_project` com o `project_id` e `name` = nome escolhido. Ele devolve o endereço público `.lovable.app`. Siga para o passo 7.

### 6. Caminho sem conector: prompt pronto

1. Monte o mesmo pedido do passo 3, colocando, logo depois das regras, o conteúdo da página em texto: a ordem das seções e, em cada seção, os textos literais, os botões com os links, as cores (variáveis do CSS) e as fontes. Não cole o HTML inteiro: o prompt precisa caber em 50.000 caracteres.
2. Se a página já está publicada num endereço público (ex: pelo `/pagina-vercel`), acrescente no prompt "Use como referência visual a página {url}" e gere também o link `https://lovable.dev/#prompt={prompt codificado para URL}&html={url codificada}`, que abre o Lovable com tudo preenchido. Use o link só se ele tiver menos de 50.000 caracteres; se passar, entregue só o prompt.
3. Salve em `meus-produtos/{ativo}/entregas/paginas/{nome}-prompt-lovable.md`.
4. Instrua:
```
Pronto. Prompt salvo em meus-produtos/{ativo}/entregas/paginas/{nome}-prompt-lovable.md

1. Abra https://lovable.dev e comece um projeto novo
2. Cole o prompt inteiro no chat (se aparecer "Paste attached", clique em "Paste inline")
3. Confira se a página ficou igual à original
4. Clique em Publish, no canto superior direito, e copie o endereço .lovable.app
5. Volte aqui e me mande o link
```
Quando o aluno mandar o link, siga para o passo 7 sem `project_id`.

### 7. Salvar histórico

Salve em `meus-produtos/{ativo}/entregas/.lovable` (modo append):
```
{timestamp}|{nome}|{project_id ou "manual"}|{url_publica}|{arquivo}
```

E também atualize/crie `meus-produtos/{ativo}/entregas/paginas/.lovable-link.md`:
```
# Páginas publicadas no Lovable

## {nome}
- URL: {url_publica}
- Project ID: {project_id ou "criado manualmente"}
- Arquivo local: {caminho}
- Última publicação: {data}
```

### 8. Resumo final

```
Pronto. Página publicada no Lovable.

URL pública:  {url}
Arquivo:      {caminho local}
Histórico:    meus-produtos/{ativo}/entregas/.lovable

Próximos passos sugeridos:
- Abra o link no celular e confira os botões de compra
- Cole o link na bio do Instagram
- Use no /copy-anuncio como destino dos anúncios
```

## Regras

- Nunca peça login ou senha do Lovable no chat. O login acontece na tela do próprio Lovable, quando o aluno conecta.
- Não use chave de API do Lovable: ela só serve para republicar projeto existente e exige plano Business ou Enterprise.
- Sempre confirme antes de criar o projeto (gasta créditos) e antes de publicar (o endereço fica público).
- Sempre avise que o Lovable recria a página com IA e que o aluno confere antes de publicar. Para cópia idêntica, ofereça o `/pagina-vercel`.
- Página que chama `/api/` nunca vai para o Lovable: ela depende da função na Vercel.
- Não repita `create_project` em caso de demora: acompanhe com `get_message`.
- Não use travessão em nenhum texto exibido ao usuário.

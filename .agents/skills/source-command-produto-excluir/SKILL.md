---
name: "source-command-produto-excluir"
description: "Excluir um produto cadastrado e todas as suas entregas e pastas. Use esta skill SEMPRE que o usuário quiser deletar, remover ou apagar um produto do sistema."
---

# source-command-produto-excluir

Use this skill when the user asks to run the migrated source command `produto-excluir`.

## Command Template

# Excluir Produto. Remover Produto e Todas as Entregas

Exclui permanentemente um produto e toda a sua pasta, incluindo perfil, identidade do consumidor e todas as entregas geradas.

## Usage

```
/produto-excluir
```

## O Que Fazer

### 1. Ler produto ativo atual

Leia `meus-produtos/.ativo` para saber qual produto está ativo agora.

### 2. Listar produtos disponíveis

Liste todas as subpastas dentro de `meus-produtos/` (ignorar arquivos como `.ativo`, `index.js` e pastas que começam com `_` como `_legado`).

Para cada pasta, verifique se existe `meus-produtos/{slug}/perfil.md` e mostre:
- Nome do produto (leia a linha do Quadro do `perfil.md` se existir, senão mostre só o slug)
- Indicador se é o produto ativo atual

Exemplo de listagem:
```
Qual produto você quer excluir?

1. curso-tarot. "Fazer leituras de tarô seguras para si e outros" ← ATIVO
2. mentoria-fitness. "Emagrecer 10kg sem academia em 60 dias"
3. taro-para-iniciantes. (sem perfil cadastrado ainda)

0. Cancelar

Digite o número:
```

### 3. Se não houver produtos

Se `meus-produtos/` estiver sem subpastas de produto (só tem `.ativo`, `index.js` ou `_legado/`), informe:
```
Você ainda não tem produtos cadastrados.
Use /produto-novo para criar seu primeiro produto.
```
E encerre o comando.

### 4. Confirmar exclusão

Após o usuário escolher um produto, mostre um aviso claro antes de prosseguir.

**Se o produto escolhido for o produto ativo:**
```
⚠ Atenção: você está prestes a excluir o produto ATIVO.

Produto: {nome/slug}
O que será apagado:
- Perfil do produto (perfil.md)
- Identidade do consumidor (idconsumidor.md)
- Todas as entregas (páginas, anúncios, emails, conteúdo, etc.)

Esta ação não pode ser desfeita.

1. Confirmar exclusão
2. Cancelar
```

**Se o produto NÃO for o ativo:**
```
Você está prestes a excluir:

Produto: {nome/slug}
O que será apagado:
- Perfil do produto (perfil.md)
- Identidade do consumidor (idconsumidor.md)
- Todas as entregas (páginas, anúncios, emails, conteúdo, etc.)

Esta ação não pode ser desfeita.

1. Confirmar exclusão
2. Cancelar
```

Se o usuário cancelar (opção 2 ou digitar 0), encerre sem fazer nada.

### 5. Executar a exclusão

Após confirmação:

1. Apague toda a pasta do produto (contexto + entregas) recursivamente usando o Bash:
   ```bash
   rm -rf "meus-produtos/{slug}"
   ```

2. **Se o produto excluído era o produto ativo** (slug igual ao conteúdo de `meus-produtos/.ativo`):

   - Liste os produtos restantes em `entregas/`
   - **Se ainda houver outros produtos:** pergunte qual ativar:
     ```
     O produto ativo foi excluído. Qual produto quer ativar agora?

     1. {produto-restante-1}. "{quadro}"
     2. {produto-restante-2}. "{quadro}"

     Digite o número:
     ```
     Após a escolha, salve o slug em `meus-produtos/.ativo`.

   - **Se não houver mais produtos:** apague o conteúdo de `meus-produtos/.ativo` (deixe o arquivo vazio).

### 6. Atualizar o manifest do painel

Rode no terminal para regenerar `meus-produtos/index.js` (remove o produto excluído da lista do painel global):

```
py -3 scripts/painel-atualizar.py
```

### 7. Confirmar e sugerir próximo passo

**Se havia outros produtos e um foi ativado:**
```
Produto "{nome excluído}" excluído com sucesso.
Produto ativo agora: {novo produto ativo}

Use /produto-editar para editar o perfil ou /produto-trocar para alternar entre produtos.
```

**Se não há mais produtos:**
```
Produto "{nome excluído}" excluído com sucesso.
Você não tem mais produtos cadastrados.

Use /produto-novo para criar um novo produto.
```

**Se o produto excluído não era o ativo:**
```
Produto "{nome excluído}" excluído com sucesso.
Produto ativo continua sendo: {produto ativo}
```

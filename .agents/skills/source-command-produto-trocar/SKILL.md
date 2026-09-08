---
name: "source-command-produto-trocar"
description: "Listar os produtos cadastrados e trocar o produto ativo."
---

# source-command-produto-trocar

Use this skill when the user asks to run the migrated source command `produto-trocar`.

## Command Template

# Trocar Produto. Selecionar Produto Ativo

Lista todos os produtos cadastrados em `meus-produtos/` e permite trocar o produto ativo.

## Usage

```
/produto-trocar
```

## O Que Fazer

### 1. Ler produto ativo atual

Leia `meus-produtos/.ativo` para saber qual produto está ativo agora. Use este valor **somente** para marcar o produto ativo na listagem. não use para descobrir os outros produtos.

### 2. Descobrir todos os produtos cadastrados

Use **Glob** com o padrão `meus-produtos/*/perfil.md` para encontrar todos os produtos que têm perfil cadastrado.

Em seguida, use **Glob** com o padrão `meus-produtos/*/` para detectar pastas que existem mas ainda não têm `perfil.md`. Ignore pastas que começam com `_` (ex: `_legado`) e o arquivo `index.js`.

**Nunca** assuma que só existe o produto que está em `.ativo`. Sempre varre toda a pasta `meus-produtos/` para descobrir os produtos disponíveis.

Para cada pasta encontrada, mostre:
- Nome do produto (leia a linha do Quadro do `perfil.md` se existir, senão mostre só o slug)
- Indicador se é o produto ativo atual

Exemplo de listagem:
```
Seus produtos cadastrados:

1. curso-tarot. "Fazer leituras de tarô seguras para si e outros" ← ATIVO
2. mentoria-fitness. "Emagrecer 10kg sem academia em 60 dias"
3. curso-ingles. (sem perfil cadastrado ainda)

Digite o número do produto que quer ativar, ou 0 para cancelar:
```

### 3. Se não houver produtos

Se `meus-produtos/` não tiver subpastas de produto (só tem `.ativo`, `index.js` ou `_legado/`), informe:
```
Você ainda não tem produtos cadastrados.
Use /produto-novo para criar seu primeiro produto.
```

### 4. Ativar o produto escolhido

Após o aluno digitar o número:
- Salve o slug correspondente em `meus-produtos/.ativo` (sobrescreva)

### 5. Atualizar o manifest do painel

Rode no terminal para atualizar `meus-produtos/index.js` (o painel global usa esse arquivo para saber o produto ativo):

```
py -3 scripts/painel-atualizar.py
```

### 6. Confirmar e sugerir próximo passo

```
Produto ativado: {nome/slug}
Todos os próximos comandos usarão este produto.

Quer continuar com /produto-concepcao para editar o perfil, ou já ir para /copy-pagina?
```

### 5. Se o produto escolhido não tiver perfil

Se `meus-produtos/{slug}/perfil.md` não existir:
```
Este produto ainda não tem perfil cadastrado.
Use /produto-editar para cadastrar o Quadro, Furadeira e as 3 Identidades.
```

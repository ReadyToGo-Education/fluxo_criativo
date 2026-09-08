---
name: "source-command-produto-zerar"
description: "Apaga todas as informações de contexto pessoal de negócio. produto ativo, perfil, identidade do consumidor e entregas. permitindo recomeçar do zero."
---

# source-command-produto-zerar

Use this skill when the user asks to run the migrated source command `produto-zerar`.

## Command Template

# Zerar Contexto. Limpeza Completa do Contexto

Remove todo o contexto de negócio salvo no projeto: produto ativo, perfil, identidade do consumidor e, opcionalmente, todas as entregas geradas.

## Usage

```
/produto-zerar
```

## O Que Fazer

### 1. Mapear tudo que existe

Verifique os seguintes caminhos e registre o que encontrar com conteúdo:

- `meus-produtos/.ativo`. slug do produto ativo
- `meus-produtos/{ativo}/perfil.md`. perfil do produto (se existir pasta)
- `meus-produtos/{ativo}/idconsumidor.md`. identidade do consumidor (se existir pasta)
- `meus-produtos/{ativo}/entregas/`. pasta com todas as entregas do produto (se existir)
- `meu-negocio/perfil.md`. perfil legado (se existir e tiver conteúdo)
- `meu-negocio/idconsumidor.md`. identidade legada (se existir e tiver conteúdo)
- `entregas/`. pasta de entregas legada (se existir e tiver arquivos)

Se nenhum dos caminhos acima tiver conteúdo, informe:
```
Não há nenhum contexto de negócio salvo no momento.
Use /produto-novo para criar um produto primeiro.
```
E encerre o comando.

### 2. Perguntar o escopo da limpeza

Mostre um resumo do que foi encontrado e pergunte:

```
Encontrei o seguinte contexto de negócio salvo:

{lista do que existe, ex:}
- Produto ativo: curso-tarot
- Perfil do produto: entregas/curso-tarot/perfil.md
- Identidade do consumidor: entregas/curso-tarot/idconsumidor.md
- Entregas: X arquivos em entregas/curso-tarot/

O que você quer apagar?

1. Só o perfil e identidade do consumidor (manter o produto e entregas)
2. Tudo. produto, perfil, identidade e entregas
3. Apenas as entregas (manter perfil e identidade)

0. Cancelar

Digite o número:
```

Adapte a lista conforme o que realmente existir.

### 3. Confirmar antes de executar

Após a escolha, mostre um aviso claro com o que será apagado:

```
Você está prestes a apagar permanentemente:

{lista detalhada do que será removido}

Essa ação não pode ser desfeita.

1. Confirmar e apagar tudo
2. Cancelar
```

Se o usuário cancelar, encerre sem fazer nada.

### 4. Executar a limpeza

Execute conforme a opção escolhida:

**Opção 1. Perfil e identidade apenas:**
- Sobrescreva `meus-produtos/{ativo}/perfil.md` com `# Perfil do Negócio`
- Sobrescreva `meus-produtos/{ativo}/idconsumidor.md` com `# Identidade do Consumidor`
- Se existir `meu-negocio/perfil.md`, sobrescreva com `# Perfil do Negócio`
- Se existir `meu-negocio/idconsumidor.md`, sobrescreva com `# Identidade do Consumidor`
- Mantenha o produto ativo e as entregas intactas

**Opção 2. Tudo:**
- Delete todos os arquivos dentro de `meus-produtos/{ativo}/entregas/` usando a ferramenta Delete (arquivo por arquivo)
- Esvazie `meus-produtos/.ativo` (grave conteúdo vazio)
- Se existir `meu-negocio/perfil.md` com conteúdo, sobrescreva com `# Perfil do Negócio`
- Se existir `meu-negocio/idconsumidor.md` com conteúdo, sobrescreva com `# Identidade do Consumidor`
- Se existir pasta `entregas/` legada com arquivos, delete os arquivos dentro dela

**Opção 3. Só as entregas:**
- Delete todos os arquivos dentro de `meus-produtos/{ativo}/entregas/` usando a ferramenta Delete
- Se existir pasta `entregas/` legada com arquivos, delete os arquivos dentro dela
- Mantenha perfil, identidade do consumidor e `.ativo` intactos

> **Importante:** Use a ferramenta Delete para cada arquivo individualmente. Não tente apagar pastas vazias. isso pode causar erros.

### 5. Confirmar e sugerir próximo passo

**Se apagou tudo (Opção 2):**
```
Pronto. Todo o contexto de negócio foi apagado.

Para começar um novo produto, use /produto-novo.
```

**Se apagou só perfil/identidade (Opção 1):**
```
Pronto. Perfil e identidade do consumidor foram zerados.
As suas entregas continuam salvas.

Use /produto-editar para preencher o perfil novamente.
```

**Se apagou só entregas (Opção 3):**
```
Pronto. Todas as entregas foram apagadas.
O perfil do produto e a identidade do consumidor continuam salvos.

Use /copy-pagina ou /copy-anuncio para gerar novos materiais.
```

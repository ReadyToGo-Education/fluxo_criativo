---
name: "source-command-toolkit-anotar"
description: "Registrar uma pendência, ideia ou lembrete no projeto ativo sem interromper o fluxo. Útil quando surge uma ideia no meio de outra etapa."
---

# source-command-toolkit-anotar

Use this skill when the user asks to run the migrated source command `toolkit-anotar`.

## Command Template

# Toolkit. Anotar

Captura rápida de ideias, pendências e lembretes no arquivo de pendências do projeto ativo. Serve para registrar algo que apareceu no meio do trabalho e não deve ser esquecido, sem precisar parar o que está fazendo.

## Usage

```
/toolkit-anotar
```

Ou direto com o conteúdo:

```
/toolkit-anotar revisar o depoimento da Ana na página de vendas
```

## O Que Fazer

### 1. Verificar projeto ativo

Leia `meus-produtos/.ativo` e `meus-produtos/{ativo}/projeto/.ativo`.

Se não houver projeto ativo, pergunte:

```
Não tem projeto ativo. Quer anotar no perfil do produto mesmo assim, ou criar um projeto primeiro?

1. Anotar em meus-produtos/{ativo}/pendencias.md (nota solta do produto)
2. Criar projeto com /toolkit-novo
3. Cancelar
```

Se escolher 1, crie (ou anexe) em `meus-produtos/{ativo}/pendencias.md`. Se escolher 2, oriente o comando e pare.

### 2. Capturar o conteúdo

Se o usuário passou o texto junto com o comando, use-o direto.

Se não passou, pergunte:
```
O que quer anotar?
(ex: "revisar CTA da página 3", "testar ângulo de anúncio curiosidade", "seguir Fulana como referência visual")
```

### 3. Classificar (opcional, rápido)

Pergunte:
```
Como classificar?

1. Pendência (algo que precisa ser feito)
2. Ideia (conceito pra explorar depois)
3. Referência (link, inspiração, exemplo)
4. Lembrete geral

Digite o número (ou enter para "Lembrete geral"):
```

### 4. Adicionar ao arquivo

Abra `meus-produtos/{ativo}/projeto/{projeto}/pendencias.md` (ou `meus-produtos/{ativo}/pendencias.md` se for nota solta do produto).

Acrescente no final:

```markdown
- [{tipo}] {conteúdo} — anotado em {data}
```

Se o arquivo tiver apenas o cabeçalho "(Nenhuma por enquanto...)", substitua essa linha pela anotação.

### 5. Confirmar

```
Anotado em {caminho}.

Pendências atuais: {X} itens.
Use /toolkit-progresso para ver o quadro geral.
```

## Regra

Este comando é rápido por design. Não faça entrevista longa, não peça confirmação de salvamento. O objetivo é não tirar o usuário do foco da etapa principal em que ele estava.

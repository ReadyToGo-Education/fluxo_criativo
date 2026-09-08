---
name: "source-command-toolkit-executar"
description: "Executar a próxima etapa pendente do plano do projeto ativo. Aciona a skill correta, registra o entregável e atualiza o estado automaticamente."
---

# source-command-toolkit-executar

Use this skill when the user asks to run the migrated source command `toolkit-executar`.

## Command Template

# Toolkit. Executar Próxima Etapa

Pega a próxima etapa pendente do plano e conduz a execução. O comando faz a ponte entre o plano e as skills do toolkit, mantendo o estado atualizado.

## Usage

```
/toolkit-executar
```

Ou para uma etapa específica:

```
/toolkit-executar 3
```

## O Que Fazer

### 1. Verificar contexto

Leia:
- `meus-produtos/.ativo` (produto ativo, aborte se vazio)
- `meus-produtos/{ativo}/projeto/.ativo` (projeto ativo, aborte se vazio)
- `meus-produtos/{ativo}/projeto/{projeto}/plano.md` (plano, aborte se não existir)
- `meus-produtos/{ativo}/projeto/{projeto}/estado.md` (estado atual)

### 2. Selecionar etapa

Se o usuário passou um número (`/toolkit-executar 3`), use a etapa 3.

Caso contrário, pegue a **primeira etapa com status `pendente`** cuja dependência já esteja `concluido` (ou não tenha dependência).

Se todas estiverem concluídas:
```
Todas as etapas do plano já estão concluídas.
Use /toolkit-verificar para validar a entrega completa.
```

Se a próxima etapa tem dependência não concluída, avise:
```
A etapa {N} depende de {M}, que ainda está {status}.
Complete a etapa {M} primeiro, ou use /toolkit-executar {M}.
```

### 3. Apresentar a etapa ao usuário

Mostre o que vai fazer:

```
Etapa {N}: {título}
Skill/comando: {skill}
Entregável esperado: {caminho do arquivo}

1. Executar agora
2. Pular esta etapa (vou fazer depois)
3. Marcar como concluída manualmente (já fiz fora do fluxo)
```

### 4. Executar

Se escolheu opção 1:
- Atualize o status da etapa no `plano.md` para `em-execucao`
- Atualize `estado.md` com "Etapa atual: {N}"
- **Acione a skill ou comando da etapa.** Siga o fluxo completo da skill (entrevista, aprovação, geração, salvamento).
- Quando a skill terminar e salvar o entregável, volte para este fluxo.
- Atualize o status da etapa para `concluido`.
- Adicione linha no histórico do `estado.md`: `{data}: etapa {N} ({título}) concluída. Entregável: {caminho}`

Se escolheu opção 2 (pular):
- Atualize o status para `pulado`.
- Peça: "Por que está pulando? (para registrar no histórico)"
- Registre a razão no histórico do `estado.md`.

Se escolheu opção 3 (já fiz):
- Peça o caminho do entregável.
- Atualize o status para `concluido` com nota "(feito manualmente)".
- Registre no histórico.

### 5. Sugerir próxima

Após concluir, verifique se há mais etapas pendentes e sugira:

```
Etapa {N} concluída. Entregável: {caminho}

Progresso: {X} de {total} etapas ({porcentagem}%).

Próxima etapa pendente: {N+1} — {título}.
Use /toolkit-executar para rodar ou /toolkit-progresso para ver o quadro completo.
```

Se concluiu a última:

```
Última etapa concluída. Projeto "{nome}" pronto.

Use /toolkit-verificar para fazer a conferência final contra o objetivo do roteiro.
```

## Regras importantes

- **Nunca execute sem o usuário aprovar** (opção 1). A escolha entre executar, pular ou marcar manual é obrigatória.
- **Uma etapa por vez.** Mesmo que o usuário peça "faz tudo", respeite o fluxo: execute uma, atualize estado, pergunte se continua.
- **Se a skill da etapa não existir**, avise e pergunte se quer trocar pela skill mais próxima ou marcar como manual.
- **Nunca pule dependências.** Se a etapa 5 depende da 3 e a 3 não está pronta, force o usuário a resolver a 3 antes.

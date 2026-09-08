---
name: "source-command-toolkit-verificar"
description: "Conferir se o projeto entregou o que foi prometido no roteiro. Checa cada entregável, sinaliza pendências e faz auditoria contra o objetivo."
---

# source-command-toolkit-verificar

Use this skill when the user asks to run the migrated source command `toolkit-verificar`.

## Command Template

# Toolkit. Verificar Entrega

Validação final do projeto contra o objetivo do roteiro. Checa se todos os entregáveis existem, se a qualidade bateu com o padrão do toolkit e se ainda falta alguma peça pro objetivo ser atingido.

## Usage

```
/toolkit-verificar
```

## O Que Fazer

### 1. Carregar contexto

Leia:
- `meus-produtos/.ativo`
- `meus-produtos/{ativo}/projeto/.ativo`
- `meus-produtos/{ativo}/projeto/{projeto}/roteiro.md`
- `meus-produtos/{ativo}/projeto/{projeto}/plano.md`
- `meus-produtos/{ativo}/projeto/{projeto}/estado.md`
- `meus-produtos/{ativo}/projeto/{projeto}/pendencias.md`

### 2. Checklist de verificação

Monte um relatório em 4 blocos:

**Bloco 1. Objetivo do roteiro atingido?**

Compare o "Resultado esperado" do `roteiro.md` com o que foi produzido. Responda objetivo por objetivo:
- [x] {item do resultado esperado} → atingido por {etapa N / entregável}
- [ ] {item não atingido} → ainda falta

**Bloco 2. Entregáveis existem fisicamente?**

Para cada etapa com status `concluido`, verifique se o arquivo no campo "Entregável esperado" realmente existe. Liste:
- OK: {etapa N} → {caminho} (existe)
- FALTA: {etapa N} marcada como concluída, mas {caminho} não foi encontrado

Se encontrar FALTA, é sinal de que o estado está desatualizado. Peça ao usuário para esclarecer.

**Bloco 3. Etapas pendentes, em execução ou puladas**

Liste cada uma:
- Pendente: {etapa N} — {título}
- Em execução: {etapa N} — {título}
- Pulada: {etapa N} — {título} (razão: {texto do histórico})

**Bloco 4. Pendências e ideias soltas**

Releia `pendencias.md`. Se tiver itens, liste todos e classifique em 3 grupos:
- Crítico para o objetivo (não pode ficar de fora)
- Útil mas opcional
- Pode virar outro projeto depois

### 3. Aplicar padrão de qualidade

Para cada entregável de copy, abra o arquivo e rode o Checklist 1 do AGENTS.md (Light Copy) nos primeiros parágrafos. Se encontrar violação (travessão, exclamação, pergunta no gancho, "não é X é Y", "mesmo que", "sem precisar", produto no lead), sinalize.

Para cada página HTML, verifique só: arquivo existe, tem `<!DOCTYPE html>`, abre sem erro óbvio. Auditoria completa de design é trabalho do `/feedback-pagina`, não aqui.

### 4. Apresentar resultado

Estrutura do relatório final:

```
Verificação do projeto "{nome}"

BLOCO 1. Objetivo
[lista com checkmarks]
Veredito: {atingido / parcial / não atingido}

BLOCO 2. Entregáveis
[lista OK / FALTA]

BLOCO 3. Etapas
[lista por status]

BLOCO 4. Pendências
[lista classificada]

AUDITORIA DE QUALIDADE
[alertas de Light Copy e HTML encontrados, ou "sem alertas"]

RECOMENDAÇÃO
{o que fazer agora: dar como pronto, rodar mais etapas, revisar copy X, etc.}
```

### 5. Atualizar estado

Após mostrar o relatório:

- Atualize `estado.md`:
  - Se objetivo atingido e sem pendências críticas: status = `verificado`
  - Se parcial: status = `verificado-parcial`
  - Se não atingido: status = `em-andamento`
- Adicione linha no histórico com o veredito.

### 6. Sugerir próximo passo

Dependendo do veredito:

- **Atingido:** "Projeto pronto. Use `/toolkit-pausar` para arquivar o estado, ou inicie outro com `/toolkit-novo`."
- **Parcial:** "Resolva as pendências críticas listadas no Bloco 4. Use `/toolkit-executar` para rodar as etapas que faltam ou `/toolkit-anotar` para converter ideia solta em etapa nova."
- **Não atingido:** "O roteiro ainda está em aberto. Sugestão: rever o `plano.md` e voltar ao `/toolkit-planejar` pra reorganizar as etapas que faltam."

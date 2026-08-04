---
name: workshop-marketing:configurar-higgsfield
description: Guia para conectar o Higgsfield ao Claude via conector personalizado (MCP), permitindo animar criativos direto pelo chat. Skill reutilizável chamada pelo sub-fluxo Animar em loop do /criativo-estatico quando o conector não está ativo.
allowed-tools: Read, Bash
model: sonnet
---

# Configurar Higgsfield (conector do Claude)

Guia para conectar o Higgsfield ao Claude. Só precisa fazer uma vez. Depois de conectado, o Claude anima criativos pelo Higgsfield direto no chat, sem colar prompt em lugar nenhum.

**Pré-requisito:** assinatura ativa do Higgsfield. O conector usa a conta do aluno, então sem assinatura a geração não roda. Se o aluno não tiver, avise antes de começar e ofereça as alternativas (colar o prompt no Magnific ou animar via Replicate).

**Público não técnico:** conduza um passo por vez, sem jargão.

---

## Passo 1. Verificar se já está conectado

Antes de instruir qualquer coisa, verifique se já existe alguma ferramenta MCP com "higgsfield" no nome disponível na sessão.

- **Se existir:** avise "O Higgsfield já está conectado" e volte ao fluxo que chamou esta skill.
- **Se não existir:** siga para o Passo 2.

---

## Passo 2. Adicionar o conector personalizado

Instrua, um passo por vez:

```
Vamos conectar o Higgsfield ao Claude:

1. Abra as configurações do Claude e vá em "Conectores"
2. Clique em "Adicionar conector personalizado"
3. No nome, coloque: Higgsfield MCP
4. Na URL, cole exatamente este endereço:

   https://mcp.higgsfield.ai/mcp

5. Clique em "Vincular a conta" e autorize com o seu login do Higgsfield

Quando terminar, me avise.
```

---

## Passo 3. Recarregar e confirmar

Conector recém-adicionado pode precisar de recarga pra aparecer:

```
Agora feche e abra o Claude de novo (ou inicie uma nova conversa) pra ativar o conector.
```

Na sequência, verifique de novo se alguma ferramenta MCP com "higgsfield" no nome apareceu.

- **Se apareceu:** confirme:

```
✅ Higgsfield conectado. Daqui pra frente eu consigo animar seus criativos por ele direto no chat.
```

- **Se não apareceu:** peça para conferir se a URL foi colada exata e se o vínculo da conta foi concluído. Se persistir, o plano do Higgsfield pode não incluir acesso ao MCP; nesse caso ofereça as alternativas (Magnific manual ou Replicate via API com `configurar-replicate`).

---

## Após configurar

Retorne ao fluxo que chamou esta skill (ex: sub-fluxo "Animar em loop" do `/criativo-estatico`) e continue de onde parou.

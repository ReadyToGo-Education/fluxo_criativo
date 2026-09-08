---
name: "source-command-pagina-precheckout"
description: "Criar uma página de pre-checkout leve que captura nome, email e WhatsApp antes de enviar o lead pro checkout real. Salva o contato num CRM simples em JSON local, dispara evento InitiateCheckout no Pixel e redireciona pro Hotmart/Kiwify/Stripe. Skill de infraestrutura."
---

# source-command-pagina-precheckout

Use this skill when the user asks to run the migrated source command `pagina-precheckout`.

## Command Template

# Página Pre-checkout com CRM Simples

Cria uma página intermediária entre o botão "Comprar" e o checkout da plataforma (Hotmart, Kiwify, Stripe, etc). Captura nome, email e WhatsApp, salva num CRM leve e redireciona. Dobra a taxa de recuperação de carrinho abandonado porque o lead fica na sua base mesmo se não finalizar a compra.

## Usage

```
/pagina-precheckout
```

## O Que Fazer

Acione a skill `pagina-precheckout` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo`. Se não houver produto, oriente a usar `/produto-novo`.
2. Coletar (uma pergunta por vez): URL do checkout real, qual oferta (nome + preço), se quer capturar WhatsApp opcional ou obrigatório, cor principal da página (pega do `/copy-pagina` se já existir).
3. Gerar uma página HTML minimalista com logo, título da oferta, formulário (Nome, Email, WhatsApp) e botão "Ir para o pagamento seguro".
4. No submit do formulário: salvar o contato em `meus-produtos/{ativo}/entregas/crm/leads.json` (array local), disparar `fbq('track', 'InitiateCheckout')` se houver Pixel configurado, redirecionar pro checkout real com UTMs preservadas.
5. Criar um endpoint simples via `fetch` pra um arquivo PHP opcional ou usar localStorage como fallback (explicar que se a página for pública sem backend, o CRM vira apenas localStorage do navegador). Para uso real, instruir a hospedar no Vercel com uma Serverless Function básica (incluir código pronto).
6. Salvar a página em `meus-produtos/{ativo}/entregas/paginas/precheckout-{nome}.html` e a serverless function em `meus-produtos/{ativo}/entregas/paginas/api/lead.js`.
7. Oferecer publicar com `/pagina-vercel`.

## Regras Resumidas

- A página precisa ser rápida (menos de 50kb sem imagens).
- Validar email e WhatsApp no front (regex simples).
- WhatsApp deve virar link clicável depois, formato `55DDDNÚMERO`.
- Sempre pedir confirmação antes de gerar.
- O CRM é um JSON local simples, não substitui ferramenta paga. Deixar claro pro aluno.
- Não usar travessão em nenhum texto exibido.

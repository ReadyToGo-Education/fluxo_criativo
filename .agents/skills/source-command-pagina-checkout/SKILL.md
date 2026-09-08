---
name: "source-command-pagina-checkout"
description: "Conectar uma página HTML pronta ao checkout (Hotmart, Kiwify, Eduzz, Cakto, Pepper, Stripe ou link próprio). Configura UTMs, order bump opcional e dispara InitiateCheckout no Pixel. Skill de infraestrutura, roda depois da página estar pronta."
---

# source-command-pagina-checkout

Use this skill when the user asks to run the migrated source command `pagina-checkout`.

## Command Template

# Página Checkout. Conexão com Plataforma de Pagamento

Pega uma página existente e conecta os botões de CTA ao link real do checkout, sem mexer na copy. Configura UTMs, order bump e evento de pixel.

## Usage

```
/pagina-checkout
```

## O Que Fazer

Acione a skill `pagina-checkout` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo` e checar `meus-produtos/{ativo}/entregas/.checkout` (se já existe configuração).
2. Coletar (uma pergunta por vez): qual página, plataforma (Hotmart/Kiwify/Eduzz/Cakto/Pepper/Stripe/outro), link do checkout, UTMs, order bump, evento Pixel.
3. Localizar botões de CTA no HTML (procurar por `cta`, `btn-cta`, `btn-comprar`, palavras-chave de compra). Se não estiver óbvio, mostrar candidatos e perguntar.
4. Substituir `href` dos CTAs pelo link de checkout (com UTMs apensas se aplicável). Adicionar `target="_blank"` e `rel="noopener"`.
5. Order bump opcional: checkbox simples no HTML ou troca de link via script.
6. Disparar evento `InitiateCheckout` no Pixel se o usuário quiser.
7. Salvar configuração em `meus-produtos/{ativo}/entregas/.checkout`.
8. Backup em `meus-produtos/{ativo}/entregas/paginas/.backup-checkout-{timestamp}.html` antes de sobrescrever.
9. Mostrar resumo final e sugerir próximos passos: `/pagina-performance`, `/pagina-pixel`, `/pagina-lovable`.

## Regras Resumidas

- Nunca pedir login da plataforma de checkout. Só o link de pagamento, que é público.
- Nunca aplicar link em CTA sem confirmação se houver dúvida.
- Sempre criar backup antes de sobrescrever.
- Não usar travessão em nenhum texto exibido.

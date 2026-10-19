---
name: "source-command-pagina-precheckout"
description: "Criar uma página de pre-checkout leve que captura nome, email e WhatsApp antes de enviar o lead pro checkout real. Salva o contato num CRM simples em JSON local, dispara evento InitiateCheckout no Pixel e redireciona pro Hotmart/Kiwify/Stripe. Skill de infraestrutura."
---

# source-command-pagina-precheckout

Use esta skill quando o usuário pedir o comando `/pagina-precheckout` do workshop (ou `pagina-precheckout`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/pagina-precheckout.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

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
3. Gerar uma página HTML minimalista com logo, título da oferta, formulário (Nome, Email, WhatsApp, mais o campo escondido `website` que pega robô) e botão "Ir para o pagamento seguro".
4. No submit do formulário: salvar o contato no modo escolhido pelo aluno (localStorage só para teste, ou função na Vercel para uso real), disparar `fbq('track', 'InitiateCheckout')` se houver Pixel configurado, redirecionar pro checkout real com UTMs preservadas.
5. Para uso real, gerar a Serverless Function `api/lead.js` seguindo o checklist de segurança (`.claude/rules/seguranca/checklist-seguranca.md`): valida de novo no servidor, ignora envio com o campo `website` preenchido, lê o destino do lead de variável de ambiente e devolve erro genérico. Se a função falhar, a página segue para o checkout mesmo assim. Explicar que, sem a função, o CRM vira apenas o localStorage do navegador de cada visitante, e que a função só roda se a página for publicada pelo `/pagina-vercel`.
6. Salvar a página em `meus-produtos/{ativo}/entregas/paginas/precheckout-{nome}.html` e a serverless function em `meus-produtos/{ativo}/entregas/paginas/api/lead.js`.
7. Oferecer publicar com `/pagina-vercel` e orientar a regra de limite de envios no firewall do projeto na Vercel.

## Regras Resumidas

- A página precisa ser rápida (menos de 50kb sem imagens).
- Validar email e WhatsApp no navegador (regex simples) e de novo na função do servidor.
- Nenhuma chave, URL de webhook ou URL de Apps Script no HTML.
- WhatsApp deve virar link clicável depois, formato `55DDDNÚMERO`.
- Sempre pedir confirmação antes de gerar.
- O CRM é simples, não substitui ferramenta paga. Deixar claro pro aluno.
- Não usar travessão em nenhum texto exibido.

---
name: pagina-precheckout
description: >
  Cria uma página intermediária de pre-checkout que captura nome, email e
  WhatsApp antes de mandar o lead para o checkout real (Hotmart, Kiwify,
  Stripe). Salva o contato num CRM simples em JSON, dispara InitiateCheckout
  no Pixel e redireciona preservando UTMs. Skill de infraestrutura.
---

# Página Pre-checkout com CRM Simples

Cria uma página intermediária entre o botão "Comprar" e o checkout da plataforma. O visitante preenche nome, email e WhatsApp, o contato é salvo localmente ou via serverless function, e o lead é redirecionado pro checkout real com as UTMs preservadas. O resultado é que mesmo quem abandonar o carrinho fica na sua base pra remarketing e recuperação via WhatsApp.

## Quando Usar

- Depois de ter a página de vendas principal pronta.
- Quando o usuário disser "quero capturar o lead antes do checkout", "preciso de pre-checkout", "quero um CRM simples antes do pagamento".
- Idealmente antes de rodar `/pagina-pixel` e `/pagina-checkout`.

## O Que Fazer

### 0. Contexto

Leia `meus-produtos/.ativo`. Se não houver produto, oriente a usar `/produto-novo`.
Leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md) pra pegar o nome do produto e pegar a cor principal se já existir em alguma página. Use também o tom e as frases do público do resumo na copy da página.

### 1. Coletar dados (uma pergunta por vez)

**Pergunta 1. Qual o nome da oferta?**
(ex: "Curso de Inglês Fluente", "Mentoria de 3 meses")

**Pergunta 2. Qual o preço?**
(ex: R$ 297, R$ 1.997)

**Pergunta 3. Qual a URL do checkout real?**
(ex: https://pay.hotmart.com/ABC123, https://kiwify.com.br/xyz)

**Pergunta 4. WhatsApp é obrigatório ou opcional?**
1. Obrigatório (recomendado pra recuperação)
2. Opcional

**Pergunta 5. Como salvar os leads?**
1. LocalStorage do navegador (só pra teste, cada visitante só vê o próprio)
2. Serverless Function na Vercel (recomendado, a função confere o lead e manda para sua planilha, CRM ou automação)

### 2. Gerar a página HTML

Estrutura mínima:
- `<header>`: logo ou nome do produto (pegar do resumo).
- Seção principal: H1 com nome da oferta, subtítulo com preço, 3 bullets curtos de benefício (puxar dos Decorados principais do resumo ou, se existir `meus-produtos/{ativo}/entregas/copy-pagina/bullets-{produto}.md`, dos 10 bullets quentes salvos pelo `/copy-bullets`), formulário (Nome, Email, WhatsApp), botão "Ir para o pagamento seguro".
- Rodapé: selo "Compra 100% segura" + link de contato.
- CSS inline: mobile first, fonte do Google Fonts (Inter), paleta baseada na cor do produto ou azul escuro padrão.
- Campo escondido `website` no formulário (honeypot: fora da tela por CSS, `tabindex="-1"`, `autocomplete="off"`, `aria-hidden="true"`). Pessoas não veem; robô preenche.
- JS inline:
  - Preservar UTMs da URL atual e anexar no redirect final.
  - Validar email (regex) e WhatsApp (apenas números, 10 ou 11 dígitos com DDD). Essa validação é para a experiência do visitante; no Modo 2 a função do servidor valida de novo.
  - No submit: salvar lead, disparar `fbq('track', 'InitiateCheckout')` se existir `fbq` global, redirecionar pro checkout com UTMs.
  - Se o envio falhar, mostrar só "Não foi possível enviar agora. Tente de novo em instantes.", nunca o texto do erro.

### 3. Modo de persistência

**Modo 1 (localStorage):**
```js
const leads = JSON.parse(localStorage.getItem('precheckout_leads') || '[]');
leads.push({nome, email, whatsapp, data: new Date().toISOString(), utms});
localStorage.setItem('precheckout_leads', JSON.stringify(leads));
```
Deixar claro pro aluno que isso só funciona pra teste. Cada visitante vê só o próprio localStorage.

**Modo 2 (Serverless Function):**
Antes de gerar, carregue `.claude/rules/seguranca/checklist-seguranca.md` e siga a seção "Função no servidor (Vercel, `api/*.js`)".

Gerar `meus-produtos/{ativo}/entregas/paginas/api/lead.js` com handler Node.js que:
- Aceita só POST com `{nome, email, whatsapp, utms, website}`
- Valida de novo cada campo no servidor (nome até 100 caracteres, e-mail válido até 254, WhatsApp só números com 10 ou 11 dígitos)
- Se `website` vier preenchido, responde sucesso e não grava (é robô)
- Adiciona timestamp
- Repassa o lead para o destino escolhido, com o endereço do destino lido de variável de ambiente (`LEAD_DESTINO_URL`), nunca escrito no HTML
- Em erro, registra o detalhe no log e devolve só a mensagem genérica
- Pergunta ao aluno qual destino: webhook do Zapier/Make, ActiveCampaign/Brevo ou Google Sheets

Pra simplificar, padrão sugerido: webhook do Zapier/Make, se o aluno tiver.

Se o aluno não souber nenhuma dessas opções, use a opção "Google Sheets via Apps Script" com tutorial de 4 passos (criar planilha, adicionar Apps Script com `doPost`, publicar como web app, colar a URL nas variáveis de ambiente da Vercel como `LEAD_DESTINO_URL`). O `doPost` também confere os campos e ignora envio com `website` preenchido.

Depois de publicar com `/pagina-vercel`, oriente o aluno a criar no firewall do projeto na Vercel uma regra de limite de envios por IP para a rota `/api/lead` (ex: 5 por minuto). Se a conta dele não tiver essa opção, o honeypot segura o robô comum.

### 4. Salvar arquivos

- `meus-produtos/{ativo}/entregas/paginas/precheckout-{nome-oferta}.html`
- `meus-produtos/{ativo}/entregas/paginas/api/lead.js` (se modo 2)
- `meus-produtos/{ativo}/entregas/crm/leads.json` (arquivo inicial vazio, só pra lembrar o caminho)

### 5. Resumo final

```
Pronto. Página de pre-checkout criada.

Arquivo:     meus-produtos/{ativo}/entregas/paginas/precheckout-{nome}.html
Modo CRM:    {localStorage / serverless}
Oferta:      {nome} ({preço})
Destino:     {url do checkout}

Próximos passos:
- Rode /pagina-performance pra auditar
- Rode /pagina-pixel pra instalar o Pixel
- Rode /pagina-vercel pra publicar
- Cadastre o endereço do destino como LEAD_DESTINO_URL nas variáveis de ambiente do projeto na Vercel (modo serverless)
- Crie a regra de limite de envios para /api/lead no firewall do projeto na Vercel (modo serverless)
- Teste o fluxo completo em modo anônimo
```

## Regras

- A página precisa ser leve. Meta de 50kb sem imagens.
- WhatsApp deve virar link clicável no CRM depois, formato `https://wa.me/55{numero}`.
- UTMs sempre preservadas. Nunca perder `utm_source`, `utm_campaign`, `utm_content`, `utm_medium`, `utm_term`.
- Sempre pedir confirmação antes de gerar.
- Modo localStorage precisa vir com aviso claro de "só pra teste, não serve pra produção".
- Modo serverless sempre passa pelo checklist de segurança (`.claude/rules/seguranca/checklist-seguranca.md`) antes de salvar. Nenhuma chave, URL de webhook ou URL de Apps Script no HTML.
- Não usar travessão em nenhum texto exibido.

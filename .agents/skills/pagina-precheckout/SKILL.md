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

Leia `entregas/.ativo`. Se não houver produto, oriente a usar `/produto-novo`.
Leia `entregas/{ativo}/perfil.md` pra pegar o nome do produto e pegar a cor principal se já existir em alguma página.
Leia `entregas/{ativo}/idconsumidor.md` (se existir) para usar o tom e as frases do público na copy da página.

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
2. Serverless Function na Vercel (recomendado, leads ficam centralizados num JSON no servidor)

### 2. Gerar a página HTML

Estrutura mínima:
- `<header>`: logo ou nome do produto (pegar do perfil).
- Seção principal: H1 com nome da oferta, subtítulo com preço, 3 bullets curtos de benefício (puxar do Decorado do perfil), formulário (Nome, Email, WhatsApp), botão "Ir para o pagamento seguro".
- Rodapé: selo "Compra 100% segura" + link de contato.
- CSS inline: mobile first, fonte do Google Fonts (Inter), paleta baseada na cor do produto ou azul escuro padrão.
- JS inline:
  - Preservar UTMs da URL atual e anexar no redirect final.
  - Validar email (regex) e WhatsApp (apenas números, 10 ou 11 dígitos com DDD).
  - No submit: salvar lead, disparar `fbq('track', 'InitiateCheckout')` se existir `fbq` global, redirecionar pro checkout com UTMs.

### 3. Modo de persistência

**Modo 1 (localStorage):**
```js
const leads = JSON.parse(localStorage.getItem('precheckout_leads') || '[]');
leads.push({nome, email, whatsapp, data: new Date().toISOString(), utms});
localStorage.setItem('precheckout_leads', JSON.stringify(leads));
```
Deixar claro pro aluno que isso só funciona pra teste. Cada visitante vê só o próprio localStorage.

**Modo 2 (Serverless Function):**
Gerar `entregas/{ativo}/paginas/api/lead.js` com handler Node.js que:
- Recebe POST com `{nome, email, whatsapp, utms}`
- Adiciona timestamp
- Faz append num arquivo JSON hospedado no próprio projeto da Vercel via KV (Vercel KV ou Upstash) ou grava num Google Sheets via Sheets API, ou simplesmente envia um webhook pro ActiveCampaign/Brevo/etc.
- Pergunta ao aluno qual destino: Vercel KV, Google Sheets, webhook simples

Pra simplificar, padrão sugerido: gravar num arquivo `leads.json` dentro do projeto Vercel via API do próprio Vercel Blob storage, ou mandar pro webhook do Zapier/Make se o aluno tiver.

Se o aluno não souber nenhuma dessas opções, use a opção "webhook do Google Sheets via AppScript" com tutorial de 4 passos (criar planilha, adicionar AppScript com `doPost`, publicar como web app, colar a URL no código).

### 4. Salvar arquivos

- `entregas/{ativo}/paginas/precheckout-{nome-oferta}.html`
- `entregas/{ativo}/paginas/api/lead.js` (se modo 2)
- `entregas/{ativo}/crm/leads.json` (arquivo inicial vazio, só pra lembrar o caminho)

### 5. Resumo final

```
Pronto. Página de pre-checkout criada.

Arquivo:     entregas/{ativo}/paginas/precheckout-{nome}.html
Modo CRM:    {localStorage / serverless}
Oferta:      {nome} ({preço})
Destino:     {url do checkout}

Próximos passos:
- Rode /pagina-performance pra auditar
- Rode /pagina-pixel pra instalar o Pixel
- Rode /pagina-vercel pra publicar
- Teste o fluxo completo em modo anônimo
```

## Regras

- A página precisa ser leve. Meta de 50kb sem imagens.
- WhatsApp deve virar link clicável no CRM depois, formato `https://wa.me/55{numero}`.
- UTMs sempre preservadas. Nunca perder `utm_source`, `utm_campaign`, `utm_content`, `utm_medium`, `utm_term`.
- Sempre pedir confirmação antes de gerar.
- Modo localStorage precisa vir com aviso claro de "só pra teste, não serve pra produção".
- Não usar travessão em nenhum texto exibido.

# Ferramentas do Workshop. Guia de Integracoes

Base de conhecimento sobre as ferramentas externas usadas no Workshop Marketing IA e como o toolkit se conecta com cada uma.

## Principio

O toolkit funciona 100% sem nenhuma ferramenta externa (nivel basico). As integracoes sao opcionais e progressivas. Cada ferramenta adiciona automacao a um tipo de entregavel.

## Ferramentas e Como Usar

### Vercel. Publicacao de Paginas

**O que faz:** Publica paginas HTML na internet com URL propria.
**Usada por:** `/copy-pagina`, agent `construtor-de-paginas`
**Chave necessaria:** `VERCEL_TOKEN`, `VERCEL_PROJECT_ID`

**Como configurar:**
1. Acesse vercel.com e crie uma conta gratuita
2. Crie um novo projeto vazio
3. Va em Account Settings > Tokens > Create Token
4. Copie o token e o Project ID para o arquivo `.env`

**Como o toolkit usa:**
Apos gerar o HTML, o Claude Code executa `vercel deploy` e retorna a URL publica da pagina.

**Sem a chave:** A pagina e salva localmente em `entregas/paginas/`. O aluno abre no navegador manualmente ou publica por conta propria.

---

### Freepik (Magnific). Geracao de Imagens com IA

**O que faz:** Gera imagens a partir de prompts de texto (text-to-image).
**Usada por:** `/criativo-estatico`
**Chave necessaria:** `FREEPIK_API_KEY`

**Como configurar:**
1. Acesse freepik.com e crie uma conta (plano com API)
2. Va em API > Manage API Keys > Create Key
3. Copie a chave para o arquivo `.env`

**Como o toolkit usa:**
Apos gerar os prompts de imagem, o Claude Code envia cada prompt para a API do Freepik (Magnific) e salva as imagens geradas em `entregas/criativos/`.

**Sem a chave:** Os prompts sao salvos em arquivo. O aluno copia e cola no site do Freepik (Magnific), Midjourney ou DALL-E manualmente.

**Formatos suportados:**
- Square (1:1). Feed do Instagram, anuncios
- Portrait (9:16). Stories, Reels
- Landscape (16:9). YouTube, banners

---

### HeyGen. Videos com Avatar IA

**O que faz:** Cria videos com avatares virtuais a partir de scripts de texto.
**Usada por:** `/video-heygen` (formato avatar)
**Chave necessaria:** `HEYGEN_API_KEY`

**Como configurar:**
1. Acesse app.heygen.com e crie uma conta
2. Va em Settings > API > Generate API Key
3. Copie a chave para o arquivo `.env`

**Como o toolkit usa:**
Quando o aluno escolhe o formato "Avatar" no `/video-heygen`, o Claude Code envia o script para a API do HeyGen. O video e gerado em segundo plano e o link e informado quando pronto.

**Sem a chave:** O roteiro e salvo em arquivo. O aluno copia o script e cola no app.heygen.com para gravar manualmente.

**Dicas para bons roteiros de avatar:**
- Frases curtas (max 15 palavras)
- Linguagem natural e pausada
- Indicar expressoes entre colchetes: [sorriso], [pausa], [enfase]
- Duracao ideal: 60-90 segundos

---

### Meta Ads. Gerenciamento de Campanhas

**O que faz:** Cria e gerencia campanhas de anuncios no Facebook e Instagram.
**Usada por:** `/copy-anuncio`, agent `criador-de-campanhas`
**Chaves necessarias:** `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`

**Como configurar:**
1. Acesse developers.facebook.com
2. Crie um App do tipo "Business"
3. Adicione a permissao "Marketing API"
4. Gere um token de acesso de longa duracao
5. Copie o token e o Ad Account ID para o arquivo `.env`

**Como o toolkit usa:**
OPCIONAL e AVANCADO. O toolkit gera a copy e a estrutura de campanha em arquivo. Com as chaves, pode criar rascunhos de campanhas diretamente no Gerenciador.

**Sem as chaves:** Os anuncios sao salvos em `entregas/criativos/`. O aluno copia a copy e cria a campanha manualmente no Gerenciador de Anuncios.

---

### Facebook Pixel. Rastreamento de Conversoes

**O que faz:** Rastreia acoes dos visitantes nas paginas (cadastros, compras, visualizacoes).
**Usada por:** `/copy-pagina`, agent `construtor-de-paginas`
**Chave necessaria:** `META_PIXEL_ID`

**Como configurar:**
1. Acesse Gerenciador de Eventos do Facebook (eventsmanager.facebook.com)
2. Crie um novo Pixel (se nao tiver)
3. Copie o Pixel ID (numero de 15-16 digitos)
4. Cole no arquivo `.env`

**Como o toolkit usa:**
Ao gerar qualquer pagina HTML, o Claude Code insere automaticamente o snippet do Pixel no `<head>` com os eventos adequados:
- Pagina de captura: evento `Lead`
- Pagina de vendas: evento `ViewContent`
- Pagina de obrigado: evento `Purchase` ou `CompleteRegistration`

**Sem a chave:** As paginas sao geradas sem codigo de rastreamento. O aluno instala o Pixel manualmente depois.

---

### Google Ads. Campanhas de Pesquisa

**O que faz:** Cria campanhas de anuncios na rede de pesquisa do Google.
**Usada por:** `/copy-anuncio`, agent `criador-de-campanhas`
**Chaves necessarias:** `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`

**Como configurar:**
1. Acesse ads.google.com e crie uma conta
2. Solicite um Developer Token (conta de nivel basico)
3. Copie o token e o Customer ID para o arquivo `.env`

**Sem as chaves:** Os anuncios de Google Ads sao salvos em arquivo com titulos, descricoes e palavras-chave para o aluno criar manualmente.

---

### Hotmart. Checkout e Vendas

**O que faz:** Gera links de checkout para produtos digitais.
**Usada por:** `/copy-pagina`, `/lt-funil`
**Chaves necessarias:** `HOTMART_TOKEN`, `HOTMART_PRODUCT_ID`

**Como configurar:**
1. Acesse app.hotmart.com
2. Va em Ferramentas > API Hotmart (Hottok)
3. Gere um token de acesso
4. Copie o token e o ID do produto para o arquivo `.env`

**Como o toolkit usa:**
Ao gerar paginas de vendas, o Claude Code pode inserir automaticamente o link correto de checkout nos botoes de compra.

**Sem as chaves:** Os botoes de compra na pagina ficam com placeholder `[INSERIR LINK DE CHECKOUT]`. O aluno substitui manualmente.

---

### WhatsApp Business. Automacoes

**O que faz:** Envia mensagens automaticas (lembretes, confirmacoes, abertura de carrinho).
**Usada por:** `/estrategia-lancamento`
**Chaves necessarias:** `WHATSAPP_PHONE_ID`, `WHATSAPP_ACCESS_TOKEN`

**Como configurar:**
1. Acesse developers.facebook.com
2. Crie um App com produto "WhatsApp"
3. Configure um numero de teste ou o numero comercial
4. Gere um token de acesso permanente
5. Copie o Phone ID e o token para o arquivo `.env`

**Sem as chaves:** As mensagens de WhatsApp sao salvas em arquivo como templates. O aluno envia manualmente ou configura em ferramentas como ManyChat, Z-API, etc.

---

### OpenRouter. Geracao de Imagens para Anuncios

**O que faz:** Acessa dezenas de modelos de IA para gerar imagens reais de anuncios (feed, stories, banners).
**Usada por:** `/criativo-estatico`
**Chaves necessarias:** `OPENROUTER_API_KEY`, `OPENROUTER_IMAGE_MODEL` (opcional)

**Como configurar:**
1. Acesse openrouter.ai e crie uma conta
2. Va em Settings > API Keys > Create Key
3. Copie a chave para o arquivo `.env`
4. Opcionalmente, defina o modelo preferido em `OPENROUTER_IMAGE_MODEL`

**Como o toolkit usa:**
Quando o aluno usa `/criativo-estatico` em modo "api" e aprova o prompt gerado, o Claude Code envia o prompt para a API do OpenRouter e salva a imagem em `entregas/criativos/`. A imagem fica pronta para usar diretamente no Meta Ads ou Google Ads.

**Fluxo de chamada (curl):**
```
POST https://openrouter.ai/api/v1/images/generations
Authorization: Bearer $OPENROUTER_API_KEY
{
  "model": "$OPENROUTER_IMAGE_MODEL",
  "prompt": "[prompt gerado]",
  "size": "1024x1024"
}
```

**Formatos e tamanhos suportados:**
- `1024x1024`. Feed quadrado (Instagram, Facebook)
- `1024x1792`. Stories e Reels (vertical 9:16)
- `1792x1024`. Banner horizontal (YouTube, Google Display)

**Modelos disponiveis no OpenRouter (por uso):**

| Modelo | Uso Ideal | Velocidade | Custo |
|---|---|---|---|
| `black-forest-labs/flux-schnell` | Testes rapidos, variações | Muito rapido | Baixo |
| `black-forest-labs/flux-1.1-pro` | Anuncios finais, alta qualidade | Rapido | Medio |
| `openai/dall-e-3` | Conceitos criativos, texto na imagem | Medio | Medio |
| `stability-ai/stable-diffusion-3.5-large` | Fotos realistas, pessoas | Medio | Medio |

**Para anuncios de video:**
O OpenRouter nao gera video diretamente. Para videos, use o fluxo:
1. O aluno escreve o roteiro completo do video (ou usa um modelo pronto)
2. O aluno grava o video com o roteiro, ou usa HeyGen (se configurado) para avatar IA
3. OpenRouter pode ser usado para gerar a **miniatura do video** (thumbnail) como imagem

**Sem a chave:** Os prompts de imagem sao salvos em arquivo `.md`. O aluno copia e cola manualmente no Midjourney, Leonardo.ai, Freepik (Magnific) ou qualquer gerador de imagem.

---

### OpenRouter. Mesma chave para imagens da landing (HTML)

**O que faz:** Grava PNG em `entregas/{slug}/paginas/assets/` para ilustrar secoes da pagina (hero, dor, autoridade, OG, etc.), usando modelo de imagem via API (ver script).
**Quando usar:** No fluxo **`/pagina-ajuste`**, quando o aluno escolher **gerar imagens com IA** em vez de enviar arquivos.
**Chave:** a mesma `OPENROUTER_API_KEY` no `.env` na raiz do repositorio (ver `.env.example`).

**Script:** `scripts/generate-openrouter-nano-banana-images.py` na raiz do projeto. O arquivo lista `JOBS` com nome do PNG, proporcao e `prompt` (em ingles costuma funcionar melhor). Saida direta em `entregas/{slug}/paginas/assets/`.

**Comando tipico (na raiz):** `py -3 scripts/generate-openrouter-nano-banana-images.py --slug nome-do-produto`  
Opcoes uteis: `--skip N` e `--max M` para gerar so parte da lista (ver cabecalho do script).

**Referencias para o assistente e o aluno:**  
`skills/paginas/references/playbook-evolucao-visual-html-landing.md` (estilo corporativo, prompts, o que evitar).  
Depois de gerar, o assistente atualiza `src` e `alt` no HTML como no fluxo de upload.

**Sem a chave:** Indicar prompts e proporcoes para o aluno gerar fora (Canva, outro gerador) e subir manualmente para `paginas/assets/`.

---

### Lovable. Criacao de Quiz

**O que faz:** Cria paginas interativas de quiz com logica condicional.
**Usada por:** `/lt-funil` (funil low ticket)
**Integracao:** Manual (sem API no toolkit)

**Como usar:**
1. Acesse lovable.dev
2. Descreva o quiz desejado em linguagem natural
3. O Lovable gera a pagina interativa
4. Publique e conecte a pagina final do quiz (gerada pelo toolkit)

**Fluxo recomendado:**
```
Anuncio -> Quiz (Lovable) -> Pagina Final do Quiz (toolkit) -> Checkout (Hotmart)
```

---

## Tabela Resumo

| Ferramenta | Chave .env | Nivel | Automacao |
| --- | --- | --- | --- |
| Vercel | VERCEL_TOKEN | Intermediario | Deploy de paginas |
| OpenRouter | OPENROUTER_API_KEY | Intermediario | Criativos de anuncio (`/criativo-estatico`) e assets de landing (`generate-openrouter-nano-banana-images.py`, ver playbook) |
| Freepik (Magnific) | FREEPIK_API_KEY | Intermediario | Geracao de imagens (alternativa) |
| HeyGen | HEYGEN_API_KEY | Intermediario | Criacao de videos com avatar IA |
| Meta Pixel | META_PIXEL_ID | Intermediario | Tracking nas paginas |
| Hotmart | HOTMART_TOKEN | Intermediario | Links de checkout |
| Meta Ads | META_ACCESS_TOKEN | Avancado | Criacao de campanhas |
| Google Ads | GOOGLE_ADS_DEVELOPER_TOKEN | Avancado | Criacao de campanhas |
| WhatsApp | WHATSAPP_ACCESS_TOKEN | Avancado | Envio de mensagens |
| Lovable | (manual) | Manual | Quiz interativo |

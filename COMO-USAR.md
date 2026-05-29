# Como Usar o Workshop Marketing IA — Guia Completo

## Antes de comecar

### Opcao A. Claude Code (VS Code)

1. VSCode instalado
2. Extensao Claude Code instalada
3. Pasta do projeto aberta no VSCode

### Opcao B. Cursor

1. Cursor instalado ([cursor.com](https://cursor.com))
2. **File → Open Folder** e escolha a pasta `workshop_inteligente`
3. Pronto. As regras em `.cursor/rules/` e o `CLAUDE.md` orientam o chat. Veja tambem `AGENTS.md` para um mapa rapido de pastas.

**Comandos `/alguma-coisa` no Cursor:** a barra `/` nao e a mesma do Claude Code. Para seguir um fluxo (ex.: copy-pagina), diga no chat **"segue o comando copy-pagina"** ou anexe o arquivo **`.claude/commands/copy-pagina.md`** com `@`. O assistente executa o mesmo roteiro do `.md`.

---

## Seu primeiro uso

### 1. Abra o chat do assistente

**No VSCode:** procure o icone do Claude Code na barra lateral.

**No Cursor:** use o chat do agente (Composer ou Chat) com o projeto aberto.

### 2. Cadastre seu produto

Na primeira mensagem o assistente ja inicia o fluxo automaticamente. Ou digite:

```text
/produto-concepcao
```

O assistente vai te guiar com perguntas sobre:

- Quadro (a transformacao principal do seu produto)
- Furadeira (seu metodo estruturado)
- Decorados (beneficios do produto)
- Urgencias Ocultas (dores, desejos, duvidas do publico)
- Identidade do consumidor (quem e seu publico)

Responda uma pergunta por vez. Ao final, o painel de entregas e gerado automaticamente em `meus-produtos/{ativo}/painel-entregas.html`.

### 3. Crie seus materiais

Use os comandos na ordem que fizer sentido para voce.

---

## Fluxos recomendados

### Para quem quer comecar a vender

1. `/produto-concepcao` — Cadastrar produto e gerar identidade do consumidor
2. `/copy-pagina` — Criar copy e pagina de vendas profissional
3. `/copy-anuncio` — Criar anuncios para trafego pago

### Para quem vai lancar

1. `/produto-concepcao` — Cadastrar produto e gerar identidade do consumidor
2. `/estrategia-lancamento` — Planejar o evento completo
3. `/copy-pagina` — Criar pagina do evento e pagina de vendas
4. `/copy-anuncio` — Criar anuncios de captacao
5. `/carrossel` — Criar conteudo pre-lancamento

### Para quem quer vender no perpetuo

1. `/produto-concepcao` — Cadastrar produto e gerar identidade do consumidor
2. `/estrategia-funil` — Mapear funil perpetuo
3. `/copy-pagina` — Criar paginas (captura + vendas + obrigado)
4. `/copy-anuncio` — Criar anuncios para cada fase do funil

### Para quem quer vender low ticket

1. `/produto-concepcao` — Cadastrar produto e gerar identidade do consumidor
2. `/lt-funil` — Criar produto de entrada (quiz, desafio, agente GPT)
3. `/lt-criar-produto` — Criar o conteudo real do produto digital
4. `/lt-pagina` ou `/lt-quiz` — Gerar a pagina ou quiz de venda
5. `/copy-anuncio` — Criar anuncios low ticket
6. `/lt-otimizar` — Otimizar campanhas com planilha do Gerenciador

### Para quem quer vender high ticket

1. `/produto-concepcao` — Cadastrar produto e gerar identidade do consumidor
2. `/estrategia-lancamento` — Planejar retiro ou evento online
3. `/comercial-playbook` — Criar scripts SPIN para venda 1:1
4. `/copy-pagina` — Criar pagina de inscricao do evento

---

## O que cada comando faz

### /produto-concepcao

Cadastra o produto usando a metodologia VTSD: Quadro, Furadeira, Decorados, 3 Identidades, Urgencias Ocultas, Identidade do Consumidor e Painel de Entregas. Tudo em fluxo unico.

Resultado: `meus-produtos/{ativo}/perfil.md`, `meus-produtos/{ativo}/idconsumidor.md` e `meus-produtos/{ativo}/painel-entregas.html`

### /copy-pagina

Cria a copy completa da pagina de vendas (estrutura 8D, 11 secoes) e gera o HTML profissional pronto para uso. Tres tipos: vendas, captura e obrigado.

Resultado: `meus-produtos/{ativo}/entregas/copy-pagina/copy-[produto].md` e `meus-produtos/{ativo}/entregas/paginas/[tipo]-[produto].html`

Como ver: abra o arquivo `.html` no navegador.

### /copy-anuncio

Cria pacotes de anuncios usando a Mandala de 18 Tipos. Inclui copy, direcao criativa e estrategia de campanha para Meta Ads.

Resultado: `meus-produtos/{ativo}/entregas/anuncios/anuncios-[plataforma]-[produto].md`

### /carrossel

Cria carrosseis com 7 a 10 slides baseados nas urgencias ocultas do produto.

Resultado: `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-[tema]-[produto].md`

### /copy-social

Cria posts para redes sociais (Instagram, LinkedIn, Twitter) a partir das urgencias ocultas e decorados do produto.

Resultado: `meus-produtos/{ativo}/entregas/conteudo-social/`

### /estrategia-lancamento

Planeja lancamento ou evento completo: Big Idea, cronograma, materiais necessarios, estrutura de campanha.

Resultado: `meus-produtos/{ativo}/entregas/`

### /estrategia-funil

Mapeia funil completo: perpetuo, lancamento ou low ticket com quiz. Inclui todas as etapas e metricas.

Resultado: `meus-produtos/{ativo}/entregas/`

### /comercial-playbook

Cria scripts de venda 1:1 usando SPIN Selling: roteiro de call, pitch, quebra de objecoes, script de WhatsApp.

Resultado: `meus-produtos/{ativo}/entregas/comercial/playbook-[produto].html` (abrir no navegador; Imprimir → Salvar como PDF)

### /criativo-estatico

Gera criativos estaticos para anuncios. Pergunta se voce quer apenas o prompt para colar em ferramenta externa (Midjourney, DALL-E, Freepik AI) ou geracao automatica via API (OpenRouter ou Freepik).

Resultado: `meus-produtos/{ativo}/entregas/criativos/`

### /lt-funil

Cria produto de entrada usando a metodologia low ticket (R$37-97): define o formato (quiz, desafio ou agente GPT), estrategia e estrutura do funil.

Resultado: definicao do funil e direcionamento para `/lt-criar-produto`, `/lt-quiz` ou `/lt-pagina`.

### /lt-criar-produto

Cria o conteudo real do produto digital: e-book, checklist ou mini-curso pronto para entrega.

Resultado: `meus-produtos/{ativo}/entregas/produto/`

### /lt-pagina

Gera as 4 leads do produto low ticket (pagina de vendas direta, sem quiz).

Resultado: `meus-produtos/{ativo}/entregas/paginas/`

### /lt-otimizar

Analisa planilha exportada do Gerenciador de Anuncios e recomenda ajustes de campanha low ticket.

### /video-heygen

Cria roteiro e aciona o HeyGen via API para gerar video com avatar IA.

Resultado: `meus-produtos/{ativo}/entregas/videos/`

### /video-remotion

Cria video animado para Meta Ads usando Remotion (requer Node.js).

### /video-editar

Edita videos existentes com FFmpeg (corte, legenda, compressao).

### /pagina-ajuste

Faz ajustes pontuais em uma pagina HTML ja gerada: headline, cores, CTA, FAQ, SEO, etc.

### /pagina-lovable

Publica a pagina HTML diretamente no Lovable.

### /pagina-vercel

Publica a pagina HTML diretamente na Vercel.

### /pagina-pixel

Instala o Meta Pixel na pagina de vendas.

### /pagina-checkout

Conecta a pagina ao checkout (Hotmart, Kiwify, Eduzz, Cakto, Pepper, Stripe).

### /feedback-pagina

Corrige e otimiza uma pagina de vendas existente (auditoria de copy + design + conversao).

### /feedback-low-ticket

Corrige pagina de produto low ticket (copy, estrutura, design) e gera HTML novo.

### /elementos-literarios

Aplica 1 a 3 dos 26 elementos literarios do Light Copy em um texto existente.

### /gerar-furadeira

Gera a Furadeira (metodo) do produto ativo no perfil.md. Decide automaticamente qual das 6 mecanicas (Fases, Logica Condicional, Enquadramento, Listas, Empecilhos, Dinamica de Entrega) faz mais sentido para o nicho, sugere o nome do metodo e aplica o teste de eficiencia.

### /furadeira-visual

Le a Furadeira ja escrita no perfil.md, decide o layout visual conforme a mecanica + nicho, monta um prompt em ingles para o aluno colar no ChatGPT e salva a imagem PNG retornada em entregas/furadeira/furadeira.png.

### /instagram-dashboard, /tiktok-dashboard, /youtube-dashboard

Gera dashboard HTML de metricas da plataforma via Apify. O aluno roda o script manualmente para atualizar os dados.

### /ads-relatorio

Cria rotina diaria automatica que busca metricas do Facebook Ads e envia relatorio pelo WhatsApp via Z-API. Agente agendado na nuvem, roda todo dia sem precisar do computador ligado.

### /toolkit-novo, /toolkit-planejar, /toolkit-executar...

Fluxo proprietario para projetos grandes (lancamentos, funis completos, reestruturacoes). Quebra o objetivo em etapas, aciona as skills certas e mantém estado entre sessoes. Use `/toolkit-progresso` para retomar de onde parou.

---

## Dicas para melhores resultados

1. Quanto mais detalhes voce der, melhor o resultado.
2. Peca alteracoes: "mude o titulo", "adicione depoimentos", "troque a cor".
3. Use os comandos na ordem sugerida — cada um usa informacoes dos anteriores.
4. Revise antes de publicar.
5. Atualize seu produto com `/produto-concepcao` quando mudar algo.

---

## Perguntas frequentes

**Preciso saber programar?**
Nao. Tudo funciona por conversa.

**Posso usar as paginas geradas?**
Sim. Os arquivos HTML podem ser hospedados em qualquer servico ou publicados na Vercel com `/pagina-vercel`. Voce tambem pode copiar os textos para WordPress, Elementor, Carrd, etc.

**Posso pedir alteracoes?**
Sim. Basta pedir no chat: "mude a cor para azul", "adicione FAQ", etc. Ou use `/pagina-ajuste` para um fluxo guiado de edicao.

**Onde ficam meus arquivos?**
Na pasta `meus-produtos/{ativo}/entregas/`, organizada por tipo. O painel de entregas em `meus-produtos/{ativo}/painel-entregas.html` mostra tudo centralizado.

**O que e a metodologia VTSD?**
Venda Todo Santo Dia — metodologia de Leandro Ladeira para infoprodutores venderem no perpetuo com copy argumentativa e logica. Inclui conceitos como Quadro, Furadeira, Decorados, Light Copy, Mandala de Anuncios e Estrutura 8D.

**Tenho varios produtos. Como alterno entre eles?**
Use `/produto-trocar` para listar os produtos cadastrados e ativar outro. O seletor no painel de entregas tambem permite navegar entre produtos.
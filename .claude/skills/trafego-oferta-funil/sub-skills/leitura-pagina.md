# Sub-skill. Leitura da Página

Lê a página de vendas que está no ar (a URL do anúncio) e extrai os elementos principais da oferta, para cruzar com os números do funil. Não é a auditoria de copy da página: essa é do `/feedback-pagina` (ou do `/feedback-low-ticket`, em página low ticket).

## Quando é acionado

- Opção [3] do menu principal.
- Automaticamente no Diagnóstico Completo (segundo módulo).
- Quando o aluno pergunta "o que tem na minha página?" ou "a página está boa?".

## Fluxo técnico (3 etapas + alternativa)

### Etapa 1. Obter a URL

Ordem de prioridade:
1. URL informada pelo aluno no Passo 0.95 do SKILL.md.
2. Extrair do criativo pela API (só leitura): `object_story_spec.link_data.link` ou `asset_feed_spec.link_urls[0].website_url` (MCP: `ads_get_creatives`; App: `curl -g` no campo `creative{...}` do anúncio).
3. Se nenhuma estiver disponível: perguntar diretamente.

Se vários anúncios apontam para URLs diferentes: listar com números e perguntar qual analisar (ou todas).

### Etapa 2. Ler a página (regra 10 do CLAUDE.md)

1. **Claude in Chrome** (`read_page`): primeira opção, porque renderiza a página completa, inclusive o que carrega por JavaScript.
2. **WebFetch** da URL, se o Claude in Chrome não estiver disponível (ferramenta ausente ou erro de conexão).
3. Nunca travar a conversa pedindo para conectar o Chrome ou instalar algo: usar a alternativa e seguir.

**Nada de mexer em configuração.** A skill não lê nem edita o `settings.local.json` e não adiciona domínio a nenhuma lista de permissões. Se o Claude Code pedir autorização para acessar o domínio, é a janela de permissão do próprio Claude Code, e a decisão é do aluno.

### Etapa 3. Processar o conteúdo

Extrair os elementos da tabela abaixo do conteúdo lido.

### Alternativa (quando as duas leituras falham)

Situações de falha: página só em JavaScript sem o Chrome disponível (HTML vazio), página com senha, erro, tempo esgotado.

```
Não consegui ler a página automaticamente. Pode ser uma
página que carrega por JavaScript ou que exige login.

Duas opções:

1. Abrir a página no navegador, selecionar todo o texto
   (Ctrl+A), copiar e colar aqui
2. Descrever os principais elementos: headline, promessa,
   garantia, preço, CTA, se tem vídeo

Digite o número:
```

Se o aluno colar: processar como texto puro. Declarar: "Análise baseada no conteúdo colado. Estrutura visual e posição dos elementos não analisadas."

## O que extrair do conteúdo

| Elemento | O que buscar | Onde geralmente está |
|----------|-------------|---------------------|
| **Headline** | H1 ou o primeiro texto grande em destaque | Primeira dobra |
| **Subheadline** | H2 ou texto logo abaixo do H1 | Primeira dobra |
| **Promessa principal** | Frase que diz o resultado ou a transformação. Comparar com o **Quadro do resumo do produto** | Headline ou primeiro parágrafo |
| **Mecanismo** | Nome do método, sistema ou processo. Comparar com a **Furadeira do resumo** | Depois da promessa |
| **Público-alvo implícito** | Para quem a página fala. Comparar com o público do resumo | Linguagem, exemplos, dores citadas |
| **Dor atacada** | Qual problema a oferta resolve. Comparar com as Urgências Ocultas do resumo | Primeiros blocos |
| **Desejo explorado** | O que a pessoa quer alcançar | Blocos de resultado e transformação |
| **Prova social** | Depoimentos, logos, números | Antes ou depois do CTA |
| **Garantia** | Tipo (dias, incondicional), posição | Perto do preço |
| **Bônus** | Quantidade, relevância, valor | Antes do preço |
| **Preço** | Visível? Ancorado? Parcelado? Bate com o preço do resumo? | Bloco da oferta |
| **CTA** | Texto do botão, cor, posição, quantidade | Várias posições |
| **Urgência/escassez** | Contador, vagas, prazo | Perto do CTA |
| **FAQ** | Perguntas respondidas. Comparar com as objeções principais do resumo | Final da página |
| **Vídeo (VSL)** | Presença de tag `<video>` ou vídeo incorporado | Topo ou bloco dedicado |
| **Estrutura** | Ordem dos blocos, tamanho da página | Fluxo geral |

## Limitações declaradas

Sempre incluir no output:

- **Leitura pelo WebFetch:** "Análise baseada no HTML público. Elementos carregados por JavaScript podem não estar visíveis." (Na leitura pelo Claude in Chrome, a página foi renderizada e essa ressalva não se aplica.)
- **VSL:** "A página contém vídeo. A análise cobre os elementos de texto e a estrutura, não o conteúdo do vídeo."
- **Velocidade:** "Sem dados de velocidade de carregamento. Connect rate baixo pode sugerir lentidão, mas não confirma." (Medição de verdade: `/pagina-performance`.)
- **Versão de celular:** "A leitura pega a versão padrão da página. A experiência no celular pode ser diferente."
- **Páginas protegidas:** "Páginas com login, área de membros ou página de obrigado não podem ser lidas automaticamente."

## Explicação obrigatória

Cada elemento extraído DEVE ter avaliação:

```
LEITURA DA PÁGINA: https://seusite.com.br/oferta

HEADLINE: "Aprenda a vender todos os dias usando IA"
Avaliação: promessa clara, mas genérica. Não traz o resultado
mensurável do Quadro do produto nem o mecanismo. Comparada com o
anúncio (que promete "método que gerou R$ 47k em 30 dias"), há
desalinhamento de especificidade.

PROVA SOCIAL: 3 depoimentos em texto, sem foto ou vídeo
Avaliação: quantidade baixa. Sem prova visual (foto, vídeo), a
credibilidade cai. Posicionados DEPOIS do preço (deviam estar
ANTES para construir confiança).

GARANTIA: 7 dias, condicional
Avaliação: existe, mas 7 dias é curto para um produto de R$ 2.500.
Uma garantia mais longa e incondicional costuma reduzir o risco
percebido.

CTA: "Quero começar agora" (1 botão, acima do preço)
Avaliação: só 1 CTA na página inteira é pouco para uma página
longa. Faltam CTAs intermediários.
```

A correção de cada ponto não sai daqui: vai para `/pagina-ajuste` (ajuste pontual numa página do Severino), `/feedback-pagina` ou `/feedback-low-ticket` (auditoria completa), conforme o plano de correção.

## Output YAML

```yaml
leitura_pagina:
  url: "https://seusite.com.br/oferta"
  metodo: claude_in_chrome | webfetch | conteudo_colado | descricao_manual
  confianca: alta | media | baixa

  elementos:
    headline: { texto: "...", avaliacao: "..." }
    subheadline: { texto: "...", avaliacao: "..." }
    promessa: { texto: "...", especificidade: alta | media | baixa, bate_com_quadro: true | false }
    mecanismo: { presente: true | false, descricao: "...", bate_com_furadeira: true | false }
    prova_social: { quantidade: 3, tipo: "texto_sem_foto", posicao: "apos_preco" }
    garantia: { presente: true, tipo: "7_dias_condicional", posicao: "apos_preco" }
    bonus: { quantidade: 2, relevancia: alta | media | baixa }
    preco: { visivel: true, ancorado: true, parcelado: true, valor: "...", bate_com_resumo: true | false }
    cta: { texto: "...", quantidade: 1, posicao: "acima_preco" }
    urgencia: { presente: false }
    faq: { presente: true, quantidade: 8, objecoes_do_resumo_cobertas: 3 }
    vsl: { presente: true }
    estrutura: { blocos: ["headline", "vsl", "beneficios", "depoimentos", "preco", "garantia", "faq"] }

  limitacoes:
    - "VSL presente, conteúdo do vídeo não analisado"
    - "Leitura pelo WebFetch: JavaScript não executado"
```

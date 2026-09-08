---
name: pagina-performance
description: >
  Audita a performance de uma página HTML gerada (peso, requisições, imagens,
  fontes, CSS/JS bloqueante, Core Web Vitals estimados) e corrige automaticamente
  os problemas encontrados, devolvendo a página otimizada. Pensada para páginas
  estáticas single-file produzidas pelas skills `copy-pagina`, `lt-pagina` e
  `ht-pagina-inscricao`.
---

# Página Performance. Auditoria e Correção Automática

Roda uma auditoria de performance em uma página HTML que já existe no projeto e devolve uma versão otimizada, sem precisar abrir o PageSpeed manualmente.

## Quando Usar

- Logo após gerar uma página com `/copy-pagina`, `/lt-pagina` ou `/ht-pagina-inscricao`.
- Quando o usuário disser "audita essa página", "tá lenta", "melhora o PageSpeed", "otimiza essa página", "deixa essa página leve".
- Antes de instalar Pixel ou publicar via Lovable. Página rápida primeiro, tracking depois.

## O Que Fazer

### 1. Localizar a página

Pergunte qual página auditar. Por padrão, ofereça:

1. Última página salva em `entregas/{ativo}/paginas/`
2. Outra página (informar caminho)

Se houver só uma, use direto.

### 2. Auditoria (sem chamar API externa)

Leia o HTML completo e analise os pontos abaixo. Para cada item gere um pequeno score (OK / ATENÇÃO / RUIM).

**Peso e estrutura**
- Tamanho total do arquivo em KB.
- Quantidade de imagens, fontes externas, scripts e folhas de estilo externas.
- CSS e JS inline vs externo (single-file é o padrão do projeto).
- Comentários grandes ou código morto.

**Imagens**
- Imagens sem `loading="lazy"` (exceto a primeira dobra).
- Imagens sem `width` e `height` (causa CLS).
- Formatos pesados (PNG/JPG grande sem motivo). Sugerir WebP.
- Background-image em `<div>` que poderia ser `<img>` lazy.
- Picsum, placehold.it, imagens aleatórias da internet (proibido pelo padrão do projeto, ver memória `feedback_imagens_paginas_html`).

**Fontes**
- Mais de 2 famílias do Google Fonts.
- Mais de 4 pesos por família.
- Falta de `&display=swap`.
- Falta de `preconnect` para `fonts.gstatic.com`.

**CSS**
- Seletores muito profundos.
- `!important` em excesso.
- Animações pesadas em elementos grandes.
- Falta de `prefers-reduced-motion`.

**JS**
- `<script>` sem `defer` no `<head>`.
- Bibliotecas externas (jQuery, Bootstrap CDN, etc.) que não são usadas pelo projeto. O padrão é zero dependências externas além do Google Fonts.
- Listeners pesados em scroll/resize sem throttle.

**HTML / SEO básico**
- Falta de `<meta name="viewport">`.
- Falta de `<title>` e `<meta description>`.
- Falta de `lang="pt-BR"` no `<html>`.
- Falta de favicon.
- Headings fora de ordem (h1 único, h2/h3 hierárquicos).

**Acessibilidade rápida**
- Imagens sem `alt`.
- Botões sem texto descritivo.
- Contraste pobre em textos pequenos (avaliar visualmente pelas cores hex declaradas).

**Core Web Vitals estimados**
Com base nos pontos acima, estime em palavras (não em número):
- LCP: provavelmente bom / médio / ruim, e por quê.
- CLS: provavelmente bom / médio / ruim, e por quê.
- INP/TBT: provavelmente bom / médio / ruim, e por quê.

### 3. Relatório

Apresente o relatório no chat com este formato:

```
Auditoria. {nome do arquivo}

Peso:        {KB}  ({score})
Imagens:     {n}   ({score})
Fontes:      {n}   ({score})
CSS/JS:      {score}
SEO básico:  {score}
Acessib.:    {score}

Core Web Vitals estimados:
- LCP: {bom/médio/ruim}. {motivo curto}
- CLS: {bom/médio/ruim}. {motivo curto}
- INP: {bom/médio/ruim}. {motivo curto}

Problemas encontrados:
1. {problema concreto}
2. {problema concreto}
3. ...

Correções que vou aplicar:
1. {correção}
2. {correção}
3. ...
```

Pergunte:
```
1. Aplicar todas as correções
2. Aplicar só algumas (eu escolho)
3. Só o relatório, não corrigir agora
```

### 4. Correção automática

Se o usuário aprovar, edite o HTML aplicando as correções listadas. Não regenere a página do zero, **mantenha a copy intacta**, mexa apenas em estrutura, atributos, ordem de tags e otimizações técnicas.

Salve a versão otimizada **substituindo o arquivo original**. Antes disso, salve uma cópia de segurança em `entregas/{ativo}/paginas/.backup-perf-{timestamp}.html`.

### 5. Resumo final

Mostre:
```
Pronto. Página otimizada.

Antes:  {KB antes}, {n imagens sem lazy}, {problemas críticos}
Depois: {KB depois}, {n imagens sem lazy}, {problemas críticos}

Backup: entregas/{ativo}/paginas/.backup-perf-{timestamp}.html
Arquivo: entregas/{ativo}/paginas/{nome}.html

Próximo passo sugerido:
- /pagina-pixel  (instalar Meta Pixel)
- /pagina-lovable (publicar online)
```

## Regras

- Nunca chame API externa real do PageSpeed/Lighthouse. A skill faz auditoria estática lendo o HTML, é offline.
- Nunca apague ou substitua a copy. Se uma correção for impossível sem alterar texto, só sinalize no relatório, não aplique.
- Sempre crie o backup antes de sobrescrever.
- Não introduza dependências externas novas. O padrão do projeto é single-file, máximo Google Fonts.
- Não use travessão em nenhum texto exibido ao usuário.

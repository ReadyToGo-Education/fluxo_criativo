# Etapa de ajustes da página (pós-merge)

Documento de referência da **etapa obrigatória** que vem **depois** do `workshop-merge-pagina.py` e **antes** de tratar a página como pronta para tráfego, anúncio ou deploy.

## Quando acionar

Sempre que existir arquivo mergeado em `entregas/{ativo}/paginas/vendas-{slug}.html` (ou equivalente), o assistente deve considerar que o merge entrega um **esqueleto completo**, não a versão final de produção. A etapa de ajustes fecha o gap entre template genérico e página do produto real.

## O que esta etapa é e o que não é

| É | Não é |
|---|---|
| Checklist operacional no HTML gerado | Substituição do `/feedback-pagina` (auditoria estilo Nav, copy profunda) |
| Correções pontuais no arquivo em `entregas/` ou retorno aos blocos atômicos se precisar | Refazer a página inteira sem pedido |
| Alinhar links, SEO básico, placeholders e duplicatas conhecidas do merge | O mesmo que `/pagina-performance` (Lighthouse, peso de assets) |

## Ordem sugerida (do bloqueante ao opcional)

1. **Crítico para conversão**
   - Link real de checkout no CTA principal e na oferta final (substituir placeholders tipo `COLOCAR_LINK` ou `#checkout`).
   - Preço e parcelamento conferidos com a copy aprovada e com a plataforma.
   - Vídeo na primeira dobra: URL de embed ou placeholder explícito se ainda não houver gravação.

2. **Crítico para credibilidade**
   - Seção de autoridade: nome do criador, bio, foto e marcos (tirar placeholders `[Seu nome]`, "A definir", textos de exemplo).
   - Depoimentos: trocar modelos por textos reais quando houver autorização; revisar fotos genéricas se o aluno enviar substitutos.

3. **SEO e descoberta**
   - `<title>` e `<meta name="description">` no arquivo final (o `build_merge.py` do tema pode deixar placeholders; reaplicar após cada novo merge ou editar o shell em `pagina_completa_{estilo}` antes do merge).
   - Opcional: Open Graph (`og:title`, `og:description`, `og:image`) se o aluno for compartilhar o link em redes.

4. **Consistência do merge**
   - **Segundo bloco de provas sociais:** em temas como `flat_claro`, o mesmo template pode aparecer duas vezes. Se a copy tiver depoimentos diferentes no Bloco 11, ajustar o HTML mergeado na segunda ocorrência **ou** duplicar lógica em template dedicado, conforme o tema.
   - Rodapé: marca, ano, links de termos e privacidade reais (não deixar "SuaMarca" ou `#` se for publicar).

5. **Polish**
   - **Cores e layout:** no fluxo guiado `/pagina-ajuste`, o assistente deve **perguntar** a cor ou as cores predominantes da marca antes de alterar estilos visuais (botões, fundos, detalhes). Com a resposta (hex, nomes ou "manter atual"), aplicar de forma consistente.
   - Revisar um CTA órfão ou âncora quebrada.
   - Confirmar que não restaram strings óbvias de template em português confuso.

## Checklist rápido (copiar mentalmente ao fechar uma página)

- [ ] Checkout e CTAs com URL válida
- [ ] Preço e parcelas batendo com copy e plataforma
- [ ] Vídeo ou aviso claro de placeholder
- [ ] Autoridade sem placeholder
- [ ] Depoimentos alinhados à política (real ou modelo explícito)
- [ ] Title e meta description únicos do produto
- [ ] Segunda prova social revisada se o tema duplicar bloco
- [ ] Rodapé com marca e links corretos
- [ ] Cores predominantes alinhadas com o aluno quando houver ajuste de layout ou identidade visual
- [ ] Imagens: arquivos em `paginas/assets/`, `src` e `alt` corretos; `og:image` se for usar compartilhamento
- [ ] Após novo merge: title/meta e ajustes em `entregas/` reaplicados se necessário

## Relação com outros comandos

- **`/feedback-pagina`:** use quando o aluno quiser revisão profunda (copy + design + depoimentos). A etapa de ajustes pode **preceder** o feedback para não enviar página com placeholder de checkout.
- **`/pagina-performance`:** depois que a página está conteudisticamente fechada.
- **`/pagina-pixel`:** após links e publicação definidos, se usar Meta Ads.

## Onde ficam as imagens no repositório

| O quê | Caminho |
| --- | --- |
| Arquivos de imagem (upload ou gerados por script) | `entregas/{ativo}/paginas/assets/` |
| Página HTML que usa essas imagens | `entregas/{ativo}/paginas/vendas-{slug}.html` (ou nome equivalente) |
| Como o HTML referencia | Atributos `src="assets/nome.png"` (caminho relativo à pasta do HTML) |

Sempre que o assistente mencionar imagens ao aluno, **verbalizar essa pasta** para não haver dúvida de onde abrir ou onde colar arquivos no explorador de pastas.

## Nota para o assistente

No comando **`/pagina-ajuste`**, o fluxo padrão é **guiado**: primeiro diagnóstico, **pergunta sobre cor ou cores predominantes para o layout**, menu de escolhas (incrementar copy, headline, placeholders de imagem, análise de imagens para enriquecer, conversão, SEO, imagens), depois executar só o que o aluno pediu. Este arquivo continua sendo a **lista técnica** de tudo que pode ser ajustado.

Se o aluno escolher **varredura completa** ou pedir explicitamente aplicar tudo, aí sim percorrer a checklist de forma ativa, sem repetir o menu inteiro, e ainda assim **não inventar** dados pessoais ou links sem confirmação.

Para **imagens**, o fluxo guiado pelo comando `/pagina-ajuste` deve cobrir três caminhos:

1. **Upload:** pasta `entregas/{ativo}/paginas/assets/`, nomes claros, atualizar `src` e `alt` no HTML; opcional `og:image` no `<head>`.
2. **Ainda sem arquivo:** registrar slots recomendados no resumo; oferecer orientação de tamanho e nomenclatura.
3. **Geração com IA (OpenRouter):** quando o aluno quiser gerar em vez de enviar, o assistente deve:
   - Apontar **referências de estilo e processo** em `references/playbook-evolucao-visual-html-landing.md` (prompts, estética corporativa, o que evitar).
   - Apontar o **script** `scripts/generate-openrouter-nano-banana-images.py`, saída em `entregas/{slug}/paginas/assets/`, necessidade de `OPENROUTER_API_KEY` no `.env` na raiz (ver `.env.example`).
   - Depois de existirem os arquivos, tratar como upload: encaixar no HTML e OG se aplicável.

A skill **`ferramentas`** documenta OpenRouter no contexto de anúncios; para **assets de página**, o playbook acima e o cabeçalho do script são a referência principal.

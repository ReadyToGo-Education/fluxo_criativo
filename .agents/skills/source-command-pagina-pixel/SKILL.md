---
name: "source-command-pagina-pixel"
description: "Instalar Meta Pixel (Facebook Pixel) numa página HTML pronta. Configura os eventos certos pro tipo de página (vendas, captura, obrigado, inscrição C10X) e suporta Conversions API opcional. Skill de infraestrutura, roda depois da página estar pronta."
---

# source-command-pagina-pixel

Use this skill when the user asks to run the migrated source command `pagina-pixel`.

## Command Template

# Página Pixel. Instalação de Meta Pixel

Instala Meta Pixel num arquivo HTML existente, sem mexer na copy. Configura PageView + eventos específicos do tipo de página.

## Usage

```
/pagina-pixel
```

## O Que Fazer

Acione a skill `pagina-pixel` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo` e checar se existe `meus-produtos/{ativo}/entregas/.pixel-id` salvo.
2. Coletar (uma pergunta por vez): qual página, Pixel ID, tipo de página, se quer Conversions API.
3. Tipos de página suportados:
   - Vendas: PageView + ViewContent + InitiateCheckout no clique do CTA.
   - Captura: PageView + Lead no submit.
   - Obrigado de venda: PageView + Purchase.
   - Obrigado de captura: PageView + CompleteRegistration.
   - Inscrição C10X: PageView + Lead no submit.
4. Verificar se já existe pixel instalado. Se existir, perguntar antes de substituir.
5. Editar o HTML: bloco principal logo após `<head>`, eventos extras antes de `</body>`.
6. Salvar Pixel ID em `meus-produtos/{ativo}/entregas/.pixel-id` para próximas páginas.
7. Backup em `meus-produtos/{ativo}/entregas/paginas/.backup-pixel-{timestamp}.html` antes de sobrescrever.
8. Mostrar resumo final + instruções de teste com Meta Pixel Helper.
9. Sugerir próximos passos: `/pagina-checkout`, `/pagina-lovable`, `/copy-anuncio`.

## Regras Resumidas

- Nunca pedir login do Facebook Business. Só Pixel ID e Access Token (se CAPI), colados no chat.
- Nunca duplicar pixel sem perguntar.
- Sempre criar backup antes de sobrescrever.
- Access Token vai para `.pixel-capi` (sensível). Pixel ID vai para `.pixel-id` (público).
- Não usar travessão em nenhum texto exibido.

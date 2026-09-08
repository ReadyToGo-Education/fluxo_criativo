---
name: "source-command-pagina-performance"
description: "Auditar performance de uma página HTML pronta (peso, imagens, fontes, CSS/JS, Core Web Vitals estimados) e corrigir os problemas automaticamente. Roda offline, sem chamar PageSpeed externo. Pensada pra rodar logo após gerar a página."
---

# source-command-pagina-performance

Use this skill when the user asks to run the migrated source command `pagina-performance`.

## Command Template

# Página Performance. Auditoria e Correção Automática

Roda uma auditoria de performance estática numa página HTML salva e corrige os problemas encontrados, mantendo a copy intacta.

## Usage

```
/pagina-performance
```

## O Que Fazer

Acione a skill `pagina-performance` do plugin `workshop-marketing` e siga o roteiro completo dela:

1. Localizar a página (oferecer última gerada por padrão).
2. Auditoria estática lendo o HTML: peso, imagens, fontes, CSS/JS, HTML/SEO básico, acessibilidade e Core Web Vitals estimados.
3. Apresentar relatório no chat com score por categoria, lista de problemas e lista de correções propostas.
4. Pedir aprovação:
   ```
   1. Aplicar todas as correções
   2. Aplicar só algumas (eu escolho)
   3. Só o relatório, não corrigir agora
   ```
5. Aplicar correções editando o arquivo, mantendo a copy. Salvar backup antes em `meus-produtos/{ativo}/entregas/paginas/.backup-perf-{timestamp}.html`.
6. Mostrar resumo "antes vs depois" e sugerir próximos passos: `/pagina-pixel` e `/pagina-lovable`.

## Regras Resumidas

- Imagens costumam estar em `meus-produtos/{ativo}/entregas/paginas/assets/` (referência no HTML: `assets/...`). Se o gargalo for peso ou formato, combinar com `/pagina-ajuste` para trocar arquivos ou gerar variantes antes de otimizar o HTML.
- Não chamar API externa, auditoria é offline lendo o HTML.
- Não alterar copy, só estrutura e atributos técnicos.
- Sempre criar backup antes de sobrescrever.
- Não introduzir dependências externas novas (single-file é o padrão).
- Não usar travessão em nenhum texto exibido.

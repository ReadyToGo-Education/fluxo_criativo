---
name: workshop-marketing:copy-hardcopy
description: Criar copy de alta conversão (VSL, página de vendas ou X1) pelo método Hard Copy do Leandro Ladeira. Kishotenketsu em 4 atos, Mecanismo Único, Nível de Consciência do Lead e oferta irresistível. Usa a transcrição completa do curso como base.
---

# Copy Hard Copy

Cria copy de venda aplicando o método Hard Copy ponta a ponta: subnicho, mecanismo único, nível de consciência do lead, escolha do formato pela matriz Consciência × Preço e estrutura narrativa Kishotenketsu (4 atos com plot twist).

## Usage

```
/copy-hardcopy
```

## O Que Fazer

Acione a skill `copy-hardcopy` (via Skill tool) e siga o fluxo completo dela:

1. **Passo 0. Contexto.** Ler `meus-produtos/.ativo` e, se houver, `perfil.md` e `idconsumidor.md` do produto ativo (Quadro, público, dores, preço, Furadeira). Sem produto ativo, perguntar direto.
2. **Passo 1. Os 3 pilares.** Confirmar ou levantar subnicho, mecanismo único e preço. Se faltar mecanismo único, ajudar a construí-lo.
3. **Passo 2. Consciência e formato.** Diagnosticar o nível de consciência do lead e recomendar o formato pela matriz Consciência × Preço (VSL, Página ou X1), explicando o porquê.
4. **Passo 3. Lead.** Gerar 3 opções de início impactante, cada uma marcada com a técnica usada (notícia ruim, elefante na sala, desafio inusitado, autoridade). Usuário escolhe 1. Se houver anúncio rodando, pelo menos uma opção continua o gancho do anúncio vencedor.
5. **Passo 4. Copy completa.** Escrever os 4 atos do Kishotenketsu: início impactante, desenvolvimento com dor semelhante, plot twist revelando o mecanismo único e oferta com prova inteligente.
6. **Passo 5. Ajustes e salvar.** Oferecer variações, pedir aprovação antes de salvar e informar o caminho absoluto.
7. **Passo 6. Diagnóstico (quando houver dados).** Se o usuário trouxer métricas de player ou funil, aplicar a tabela de diagnóstico por métricas e localizar o ato quebrado antes de reescrever qualquer coisa.

Toda a metodologia, o mapa do curso e as regras estão em `.claude/skills/copy-hardcopy/SKILL.md`.

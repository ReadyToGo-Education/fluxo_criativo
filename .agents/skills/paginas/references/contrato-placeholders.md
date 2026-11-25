# Contrato de Placeholders. Página de Vendas 8D

Este arquivo é a **fonte única da verdade** sobre os placeholders usados nos templates atômicos dos 5 temas visuais e no arquivo de copy `copy-{slug}.md`.

Usado por:
- `scripts/build-pagina-vendas.py` — lê copy, aplica placeholders nos `code.html`, roda merge
- Command `/copy-pagina` — gera copy no formato compatível
- Os 80 arquivos `code.html` dos blocos atômicos (5 temas × 16 blocos)

## Regras gerais

1. **Sintaxe do placeholder no HTML:** `{{ nome_campo }}` (Jinja-like, com espaços). Ex: `<h1>{{ hero_headline }}</h1>`.
2. **Nome do campo no copy:** `### nome_campo` (heading markdown nível 3) dentro do `## Bloco NN — Nome`. Conteúdo livre em texto após o heading. Pode ter múltiplos parágrafos.
3. **Scopo do nome:** prefixo pelo nome do bloco (`hero_`, `dor_`, etc.) para evitar colisão.
4. **Placeholders de mídia:** URLs (vídeo, imagens, avatar) usam placeholder dummy em produção até o aluno trocar. Caso a copy não defina, o template mantém o valor padrão do tema (picsum, pravatar, YouTube demo).
5. **Campos opcionais:** se não houver `### campo` correspondente na copy, o script mantém o texto de exemplo do template. Sem erro.

---

## Bloco 01 — Hero (padrão split grid)

Arquivo: `hero_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `hero_headline` | texto curto | "Existe uma forma de passar em concurso..." |
| `hero_subheadline` | texto longo | "Como contadores entre 28 e 42 anos..." |
| `hero_bullet_1` | texto curto | "Sentar para estudar às 22h e fixar..." |
| `hero_bullet_2` | texto curto | "Saber exatamente onde pôr as 10 horas..." |
| `hero_bullet_3` | texto curto | "Trocar o aperto no peito de domingo..." |
| `hero_cta_texto` | texto curto | "Quero ver como funciona" |
| `hero_video_url` | URL | "https://www.youtube.com/embed/VIDEO_ID" |
| `hero_video_duracao` | texto curto | "15 minutos" |
| `hero_disclaimer` | texto curto | "Acesso imediato • Garantia 7 dias" |

**Variações (opcionais, selecionadas via argumento `--variante-hero`):**
- `hero_{tema}_centralizado` — mesmos 9 slots, layout diferente
- `hero_{tema}_depoimentos` — bloco separado com slots próprios (não substitui, aparece no bloco 11 em alguns temas)

---

## Bloco 02 — Dor

Arquivo: `dor_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `dor_headline` | texto curto | "O negócio gira, mas o controle não acompanha" |
| `dor_subheadline` | texto longo | "Se alguma dessas cenas é familiar..." |
| `dor_card_1_titulo` | texto curto | "Fechamento do mês no susto" |
| `dor_card_1_descricao` | texto longo | "Passa de meia-noite e você está..." |
| `dor_card_2_titulo` | texto curto | |
| `dor_card_2_descricao` | texto longo | |
| `dor_card_3_titulo` | texto curto | |
| `dor_card_3_descricao` | texto longo | |
| `dor_card_4_titulo` | texto curto | |
| `dor_card_4_descricao` | texto longo | |
| `dor_bridge` | texto longo | "O que falta não é mais uma planilha..." |

---

## Bloco 03 — Paliativo

Arquivo: `paliativo_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `paliativo_headline_1` | texto curto | "Você provavelmente já tentou" |
| `paliativo_headline_2` | texto curto | "E ainda assim não virou padrão." |
| `paliativo_subheadline` | texto longo | |
| `paliativo_card_1_titulo` | texto curto | "Plataforma gigante (Estratégia, Gran)" |
| `paliativo_card_1_descricao` | texto longo | |
| `paliativo_card_1_imagem_url` | URL | |
| `paliativo_card_2_titulo` | texto curto | |
| `paliativo_card_2_descricao` | texto longo | |
| `paliativo_card_2_imagem_url` | URL | |
| `paliativo_card_3_titulo` | texto curto | |
| `paliativo_card_3_descricao` | texto longo | |
| `paliativo_card_3_imagem_url` | URL | |
| `paliativo_card_4_titulo` | texto curto | |
| `paliativo_card_4_descricao` | texto longo | |
| `paliativo_card_4_imagem_url` | URL | |
| `paliativo_bridge` | texto longo | "Nenhuma dessas saídas olha de perto..." |

---

## Bloco 04 — Provas Sociais (primeiro bloco)

Arquivo: `provas_sociais_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `provas_headline` | texto curto | "Resultados de quem aplicou o método" |
| `provas_subheadline` | texto longo | "Depoimentos de modelo. Substitua por reais." |
| `provas_1_avatar_url` | URL | "https://i.pravatar.cc/150?img=47" |
| `provas_1_nome` | texto curto | "Marina S." |
| `provas_1_cargo` | texto curto | "MEI de serviços" |
| `provas_1_depoimento` | texto longo | "Antes eu misturava conta pessoal..." |
| `provas_2_avatar_url` | URL | |
| `provas_2_nome` | texto curto | |
| `provas_2_cargo` | texto curto | |
| `provas_2_depoimento` | texto longo | |
| `provas_3_avatar_url` | URL | |
| `provas_3_nome` | texto curto | |
| `provas_3_cargo` | texto curto | |
| `provas_3_depoimento` | texto longo | |

---

## Bloco 05 — CTA intermediário

Arquivo: `cta_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `cta_headline` | texto curto | "Se você reconhece o caos, vale 7 dias de teste" |
| `cta_descricao` | texto longo | |
| `cta_preco_parcelado` | texto curto | "12x de R$ 16,42" |
| `cta_preco_avista` | texto curto | "R$ 197,00 à vista" |
| `cta_botao_texto` | texto curto | "Quero ver o método agora" |
| `cta_disclaimer` | texto curto | "Acesso imediato • Garantia 7 dias" |

---

## Bloco 06 — Método (Furadeira)

Arquivo: `metodo_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `metodo_headline` | texto curto | "Método Modelo Pronto em 3 Passos" |
| `metodo_filosofia` | texto longo | "Planilhas Pro é a biblioteca de templates..." |
| `metodo_etapa_1_titulo` | texto curto | "Passo 1. Escolher o modelo" |
| `metodo_etapa_1_imagem_url` | URL | |
| `metodo_etapa_1_bullet_1` | texto curto | |
| `metodo_etapa_1_bullet_2` | texto curto | |
| `metodo_etapa_1_bullet_3` | texto curto | |
| `metodo_etapa_2_titulo` | texto curto | |
| `metodo_etapa_2_imagem_url` | URL | |
| `metodo_etapa_2_bullet_1` | texto curto | |
| `metodo_etapa_2_bullet_2` | texto curto | |
| `metodo_etapa_2_bullet_3` | texto curto | |
| `metodo_etapa_3_titulo` | texto curto | |
| `metodo_etapa_3_imagem_url` | URL | |
| `metodo_etapa_3_bullet_1` | texto curto | |
| `metodo_etapa_3_bullet_2` | texto curto | |
| `metodo_etapa_3_bullet_3` | texto curto | |

---

## Bloco 07 — Para quem é / não é

Arquivo: `para_quem_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `para_quem_headline` | texto curto | "Para quem é e para quem não é" |
| `para_quem_subheadline` | texto longo | "Confira se o perfil bate com o seu..." |
| `para_quem_sim_1` | texto longo | "Contador CLT que estuda depois das 20h..." |
| `para_quem_sim_2` | texto longo | |
| `para_quem_sim_3` | texto longo | |
| `para_quem_sim_4` | texto longo | |
| `para_quem_nao_1` | texto longo | "Quem está começando agora..." |
| `para_quem_nao_2` | texto longo | |
| `para_quem_nao_3` | texto longo | |
| `para_quem_nao_4` | texto longo | |

---

## Bloco 08 — Entregáveis

Arquivo: `entregaveis_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `entregaveis_headline` | texto curto | "O que vem na compra" |
| `entregaveis_subheadline` | texto longo | "Valores de referência de mercado..." |
| `entregaveis_1_titulo` | texto curto | "24 semanas de cronograma individual" |
| `entregaveis_1_descricao` | texto longo | |
| `entregaveis_1_valor` | texto curto | "R$ 1.200,00" |
| `entregaveis_2_titulo` | texto curto | |
| `entregaveis_2_descricao` | texto longo | |
| `entregaveis_2_valor` | texto curto | |
| `entregaveis_3_titulo` | texto curto | |
| `entregaveis_3_descricao` | texto longo | |
| `entregaveis_3_valor` | texto curto | |
| `entregaveis_4_titulo` | texto curto | |
| `entregaveis_4_descricao` | texto longo | |
| `entregaveis_4_valor` | texto curto | |

---

## Bloco 09 — Bônus

Arquivo: `bonus_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `bonus_headline` | texto curto | "Três bônus na mesma compra" |
| `bonus_subheadline` | texto longo | |
| `bonus_1_titulo` | texto curto | "Kit 10 Simulados da Banca FGV" |
| `bonus_1_descricao` | texto longo | |
| `bonus_1_valor` | texto curto | "R$ 297,00" |
| `bonus_2_titulo` | texto curto | |
| `bonus_2_descricao` | texto longo | |
| `bonus_2_valor` | texto curto | |
| `bonus_3_titulo` | texto curto | |
| `bonus_3_descricao` | texto longo | |
| `bonus_3_valor` | texto curto | |

---

## Bloco 10 — Stack de valor

Arquivo: `stack_valor_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `stack_headline` | texto curto | "Stack de valor de referência" |
| `stack_subheadline` | texto longo | "Itens separados para ancorar o investimento" |
| `stack_item_1_nome` | texto curto | "Biblioteca de cronogramas por banca" |
| `stack_item_1_valor` | texto curto | "R$ 1.200,00" |
| `stack_item_2_nome` | texto curto | |
| `stack_item_2_valor` | texto curto | |
| `stack_item_3_nome` | texto curto | |
| `stack_item_3_valor` | texto curto | |
| `stack_item_4_nome` | texto curto | |
| `stack_item_4_valor` | texto curto | |
| `stack_item_5_nome` | texto curto | |
| `stack_item_5_valor` | texto curto | |
| `stack_total_label` | texto curto | "Total ancorado" |
| `stack_total_valor` | texto curto | "R$ 7.991,00" |
| `stack_investimento_texto` | texto longo | "O preço não é arbitrário. Foi calibrado..." |

---

## Bloco 11 — Prova social (segundo bloco) ou Depoimentos

**Flat claro, Minimal claro:** usa segundo `provas_sociais_{tema}` (mesmo template do bloco 04, outros depoimentos).
**Glass escuro, Teal claro, Purple escuro:** usa `hero_{tema}_depoimentos` (carrossel mais elaborado).

Placeholders quando for o carrossel (hero_*_depoimentos):

| Placeholder | Tipo |
|-------------|------|
| `depoimentos_headline` | texto curto |
| `depoimentos_subheadline` | texto longo |
| `depoimentos_1_titulo` | texto curto |
| `depoimentos_1_texto` | texto longo |
| `depoimentos_1_autor_nome` | texto curto |
| `depoimentos_1_autor_cargo` | texto curto |
| ... (até `depoimentos_6_*`) | |

Placeholders quando for provas_sociais_2 (flat/minimal): mesmos slots do bloco 04, com prefixo `provas2_` para não colidir. Ex: `provas2_1_nome`, `provas2_1_depoimento`, etc.

---

## Bloco 12 — Suporte

Arquivo: `suporte_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `suporte_headline` | texto curto | "Depois da compra" |
| `suporte_subheadline` | texto longo | |
| `suporte_1_titulo` | texto curto | "Plantão de dúvida 5x por semana" |
| `suporte_1_descricao` | texto longo | |
| `suporte_2_titulo` | texto curto | |
| `suporte_2_descricao` | texto longo | |
| `suporte_rodape` | texto longo | "Se a venda passar por marketplace..." |

---

## Bloco 13 — Garantia

Arquivo: `garantia_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `garantia_dias` | número | "7" |
| `garantia_headline` | texto curto | "Garantia incondicional de 7 dias" |
| `garantia_texto_1` | texto longo | "Garantia incondicional de 7 dias..." |
| `garantia_texto_2` | texto longo | "Você testa a organização..." |
| `garantia_check_1` | texto curto | "Devolução integral em até 48h" |
| `garantia_check_2` | texto curto | "Sem burocracia" |
| `garantia_check_3` | texto curto | "Sem explicação necessária" |

---

## Bloco 14 — Autoridade do criador

Arquivo: `autoridade_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `autoridade_headline` | texto curto | "Autoridade do criador" |
| `autoridade_foto_url` | URL | |
| `autoridade_cargo` | texto curto | "Auditor de Controle Externo" |
| `autoridade_nome` | texto curto | "Anderson Silva" |
| `autoridade_bio` | texto longo | "Me chamo Anderson. Hoje sou..." |
| `autoridade_marco_1_valor` | texto curto | "7" |
| `autoridade_marco_1_label` | texto curto | "anos no serviço público" |
| `autoridade_marco_2_valor` | texto curto | |
| `autoridade_marco_2_label` | texto curto | |
| `autoridade_marco_3_valor` | texto curto | |
| `autoridade_marco_3_label` | texto curto | |
| `autoridade_marco_4_valor` | texto curto | |
| `autoridade_marco_4_label` | texto curto | |

---

## Bloco 15 — FAQ

Arquivo: `faq_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `faq_headline` | texto curto | "Perguntas frequentes" |
| `faq_subheadline` | texto longo | |
| `faq_1_pergunta` | texto curto | "R$ 2.997 é alto para o meu momento?" |
| `faq_1_resposta` | texto longo | |
| `faq_2_pergunta` | texto curto | |
| `faq_2_resposta` | texto longo | |
| `faq_3_pergunta` | texto curto | |
| `faq_3_resposta` | texto longo | |
| `faq_4_pergunta` | texto curto | |
| `faq_4_resposta` | texto longo | |
| `faq_5_pergunta` | texto curto | |
| `faq_5_resposta` | texto longo | |
| `faq_6_pergunta` | texto curto | |
| `faq_6_resposta` | texto longo | |
| `faq_7_pergunta` | texto curto | |
| `faq_7_resposta` | texto longo | |
| `faq_8_pergunta` | texto curto | |
| `faq_8_resposta` | texto longo | |
| `faq_rodape` | texto curto | "Outra dúvida? Escreva para [email]" |

**Observação:** FAQs 6/7/8 são opcionais. Se a copy só definir até `faq_5_*`, o script remove os cards 6/7/8 do HTML final.

---

## Bloco 16 — Oferta Final

Arquivo: `oferta_final_{tema}/code.html`

| Placeholder | Tipo | Exemplo |
|-------------|------|---------|
| `oferta_headline` | texto curto | "Oferta final" |
| `oferta_subheadline` | texto longo | |
| `oferta_item_1_nome` | texto curto | "24 semanas de cronograma" |
| `oferta_item_1_valor` | texto curto | "R$ 1.200,00" |
| `oferta_item_2_nome` | texto curto | |
| `oferta_item_2_valor` | texto curto | |
| `oferta_item_3_nome` | texto curto | |
| `oferta_item_3_valor` | texto curto | |
| `oferta_item_4_nome` | texto curto | |
| `oferta_item_4_valor` | texto curto | |
| `oferta_item_5_nome` | texto curto | |
| `oferta_item_5_valor` | texto curto | |
| `oferta_total_label` | texto curto | "Valor total somado" |
| `oferta_total_valor` | texto curto | "R$ 7.991,00" |
| `oferta_investimento_label` | texto curto | "Investimento hoje" |
| `oferta_investimento_parcelado` | texto curto | "12x de R$ 297,00" |
| `oferta_investimento_avista` | texto curto | "R$ 2.997,00 à vista" |
| `oferta_investimento_nota` | texto longo | |
| `oferta_cta_url` | URL | "https://pay.hotmart.com/ABC123" |
| `oferta_cta_texto` | texto curto | "Quero minha vaga" |
| `oferta_privacidade` | texto longo | "Ao finalizar a compra você será..." |

---

## Resumo

| Bloco | Slots |
|-------|-------|
| 01 Hero | 9 |
| 02 Dor | 11 |
| 03 Paliativo | 16 |
| 04 Provas Sociais | 14 |
| 05 CTA | 6 |
| 06 Método | 17 |
| 07 Para quem | 10 |
| 08 Entregáveis | 14 |
| 09 Bônus | 11 |
| 10 Stack | 15 |
| 11 Prova 2 / Depoimentos | variável (14-26) |
| 12 Suporte | 7 |
| 13 Garantia | 7 |
| 14 Autoridade | 13 |
| 15 FAQ | 19 |
| 16 Oferta Final | 21 |
| **Total** | **~200 slots por página** |

## Versionamento

Este contrato é versionado com o projeto. Mudanças quebram compatibilidade com produtos já renderizados. Mudanças futuras devem:

1. Adicionar slot novo **opcional** (sem remover/renomear existentes) → sem quebra
2. Remover/renomear slot → exigir migração dos `code.html` dos 5 temas + produtos já renderizados

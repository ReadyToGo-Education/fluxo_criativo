---
name: concepcao-produto
description: >
  Base de conhecimento para concepção de produto usando metodologia VTSD.
  Inclui Quadro, Furadeira, Decorados, Urgências Ocultas e 3 Identidades.
  Acionada automaticamente pelo command /produto-concepcao (que cobre o fluxo unificado, incluindo Identidade do Consumidor e Painel de Entregas).
---

# Concepção de Produto. Base de Conhecimento VTSD

> **Regra obrigatória de comunicação:** siga o padrão "Pensar em Voz Alta" do CLAUDE.md. Esta skill envolve várias operações longas (pesquisa de mercado, geração de 50 Decorados, geração de 70 Urgências Ocultas, escrita do perfil.md, montagem das 3 Identidades). Antes de cada uma, anuncie em UMA linha com `🔍 Próximo passo: {ação}. Tempo estimado: cerca de X segundos.` Ao concluir, confirme com `✅ Concluído: {entrega}. Caminho: {caminho}.`
>
> Exemplos desta skill:
> - `🔍 Próximo passo: gerar 50 Decorados a partir do Quadro do produto. Tempo estimado: cerca de 30 segundos.`
> - `🔍 Próximo passo: gerar as 7 categorias de Urgências Ocultas com 10 itens cada. Tempo estimado: cerca de 60 segundos.`
> - `🔍 Próximo passo: montar as 3 Identidades (Comunicador, Consumidor, Produto). Tempo estimado: cerca de 45 segundos.`
> - `✅ Concluído: perfil completo do produto. Caminho: meus-produtos/{ativo}/perfil.md.`

## Quadro (Transformação Principal)

Até 10 palavras. Verbo no infinitivo. Único resultado. Atrativo, claro, específico.

É o **resultado final** que a pessoa CONQUISTA ou SE TORNA após usar o produto. É a chegada, não o caminho.

**Teste rápido:** a pessoa pode dizer "isso aconteceu na minha vida" ao final do produto? Se sim, é Quadro. Se não, é processo.

**O que NÃO é Quadro (processo / meio):**
- "Identificar a crença que te trava" ❌. isso é o processo, não o resultado
- "Descobrir por que você sabota os resultados" ❌. é a investigação, não a chegada
- "Aprender como funciona X" ❌. é o caminho, não a transformação
- Slogan, promessa vaga, frase com imperativo ❌

**O que É Quadro (resultado final concreto e verificável):**
- Falar inglês em 90 dias ✓
- Fechar R$10 mil por mês como social media ✓
- Vender bolo caseiro todos os dias ✓
- Zerar dívidas em até 90 dias sem renda extra ✓
- Ganhar dinheiro sem culpa e guardar sem medo de perder ✓
- Cobrar o que vale sem sentir que está exagerando ✓
- Agir em direção ao que quer sem travar no último momento ✓

## Furadeira (Método)

Caminho claro, replicável e exclusivo do método. A Furadeira pode usar uma das 6 mecânicas (ou combinação de até 2):

1. **Lógica Condicional.** Decisão crítica que muda o caminho conforme perfil/situação (ex: "se criança reativa, então X; se passiva, então Y")
2. **Enquadramento.** Sistema próprio de categorias que classifica o aluno (ex: DISC, Trilha Vermelha/Azul/Verde, 4 perfis do vendedor)
3. **Listas.** 3 a 7 pilares finitos que coexistem (ex: 4 C's, 3 Pilares, 6 Erros)
4. **Fases e Sequências.** 3 a 5 etapas ordenadas A → B → C (ex: Método 3F: Fonética → Fluência → Fixação)
5. **Identificando Empecilhos.** Mapa de obstáculos + como o método remove cada um (geralmente combinada com Fases)
6. **Dinâmica de Entrega.** Ritual/rotina fixa que vira marca registrada (ex: Aperta e Solta 3 min ao acordar)

A mecânica certa para cada produto varia conforme nicho, Quadro e perfil do consumidor. A skill `gerar-furadeira` (acionada via `/gerar-furadeira`) decide a mecânica automaticamente com base no contexto do produto e gera a estrutura correta.

**Cada componente da Furadeira precisa carregar pelo menos 1 das 14 formas de eficiência** (mais rápido, mais barato, menos esforço, menos dor, menos erro, menos desperdício, mais adesão, mais prazeroso, mais ético, mais bonito, mais sustentável, mais saudável, mais gostoso, menos apelativo). Essa é a Teoria da Eficiência: o método só vale se torna o resultado mais eficiente que o aluno tentaria sozinho.

**Exemplos por mecânica:**
- Fases: "Protocolo Anticoceira: Raiz do Problema → Pele Blindada → Nutrição Antialérgica"
- Lógica Condicional: "Régua RCC: criança reativa segue protocolo de regulação; criança passiva segue protocolo de estímulo"
- Listas: "Os 4 C's da Lapidação: Compreensão, Convicção, Compromisso, Conversão"

**Detalhamento completo das 6 mecânicas, 14 formas de eficiência e 7 técnicas de nome de método:** `.claude/skills/furadeira-visual/references/6-mecanicas.md`.

**Visualização da Furadeira (depois de gerada):** acione `/furadeira-visual` para gerar a imagem PNG do método. A skill decide automaticamente o layout visual conforme a mecânica registrada (roadmap, fluxograma, mandala, hub, etc.) e o nicho do produto, monta um prompt em inglês para o aluno colar no ChatGPT e salva a imagem em `entregas/furadeira/furadeira.png`. Útil para a seção Método da página de vendas (8D), carrosséis, slides de pitch e stories.

## Decorados (50 Benefícios)

Categorias: Financeiro, Tempo, Autoestima, Reputação, Crescimento.
Gere 50 benefícios diretos e indiretos do Quadro.

## Urgências Ocultas

Estrutura oficial: 7 categorias com exatamente 10 itens cada (totalizando 70 itens). Não gere mais nem menos do que 10 em cada categoria.

1. Dores (problemas que incomodam): 10 itens
2. Dúvidas (perguntas que o público faz): 10 itens
3. Desejos (estados desejados): 10 itens
4. Assuntos Relacionados (temas adjacentes ao nicho): 10 itens
5. Urgências Quentes (alta intenção, ligadas direto à compra): 10 itens
6. Urgências Frias (baixa intenção, alto volume, atração): 10 itens
7. Urgências Inusitadas (ângulo inesperado que chama atenção): 10 itens

Usar como base para conteúdos, ganchos, anúncios e copy.

## 3 Identidades

1. **Comunicador**. Tom, valores, estilo, posicionamento, história
2. **Consumidor**. Demografia, psicografia, dores, desejos, comportamento, objeções, nível de consciência
3. **Produto**. Quadro, diferenciação, analogias, argumentos incontestáveis

## Pesquisa de Mercado (OBRIGATÓRIA em toda concepção)

A pesquisa de mercado NÃO mora mais nesta skill. Toda pesquisa de mercado, concorrência, objeções (Reclame Aqui), SEBRAE, precificação, ângulos virais e biblioteca de anúncios é responsabilidade da skill dedicada **`pesquisa-mercado`**.

**Regra absoluta:** em qualquer fluxo de concepção de produto (novo, low ticket, middle, high ticket, consultoria), a skill `pesquisa-mercado` precisa ser acionada antes de o assistente sugerir preço, posicionamento, identidades completas, oferta, argumentos incontestáveis ou ângulos de comunicação.

Fluxo padrão:
1. Definir nicho, Quadro inicial e formato pretendido.
2. Acionar `pesquisa-mercado` e aguardar o relatório completo em `entregas/{ativo}/pesquisa-mercado.md`.
3. Voltar para esta skill (`concepcao-produto`) usando os dados da pesquisa como insumo para gerar Decorados, enriquecer Urgências Ocultas, definir as 3 Identidades, preço e Argumentos Incontestáveis.

Sem pesquisa, sem sugestão. Se o aluno tentar pular, explicar que a pesquisa é obrigatória porque é ela que transforma "achismo" em decisão fundamentada.

## Níveis de Consciência (Eugene Schwartz)

1. Inconsciente. Não sabe que tem problema
2. Consciente do problema. Sabe que algo está errado
3. Consciente da solução. Sabe que existem soluções
4. Consciente do produto. Conhece seu produto
5. Totalmente consciente. Só precisa da oferta

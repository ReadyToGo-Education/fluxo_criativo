---
name: "source-command-gerar-furadeira"
description: "Gerar a Furadeira (metodo) do produto ativo no perfil.md. Decide automaticamente qual das 6 mecanicas usar (Logica Condicional, Enquadramento, Listas, Fases, Empecilhos, Dinamica de Entrega), gera a estrutura, sugere nome do metodo e aplica teste de eficiencia. Sem entrevista."
---

# source-command-gerar-furadeira

Use this skill when the user asks to run the migrated source command `gerar-furadeira`.

## Command Template

# Gerar Furadeira (Método Escrito no perfil.md)

Gera a Furadeira do produto ativo seguindo as 6 mecânicas do VTSD. A skill decide a mecânica sozinha com base no contexto, gera a estrutura completa, sugere o nome do método e mapeia a eficiência. Sem entrevista guiada. O aluno só aprova ou ajusta no final.

Coexiste com `/furadeira-visual`, que lê a Furadeira gerada por aqui e produz o prompt para o ChatGPT desenhar a imagem PNG.

## Usage

```
/gerar-furadeira
```

## O Que Fazer

### 1. Carregar contexto do produto ativo

Leia `meus-produtos/.ativo`. Se vazio, pare e informe:

```
Nenhum produto ativo. Use /produto-novo ou /produto-trocar primeiro.
```

Leia, na ordem:
- `meus-produtos/{ativo}/perfil.md` (Quadro, Decorados, Urgências Ocultas, 3 Identidades, Argumentos Incontestáveis, nicho)
- `meus-produtos/{ativo}/idconsumidor.md` (perfil do comprador, paliativos, objeções, frases que o público diria)
- `meus-produtos/{ativo}/pesquisa-mercado.md` (concorrentes, ângulos, biblioteca de anúncios)

**Se faltar o Quadro no perfil.md**, pare e informe:
```
O perfil ainda não tem o Quadro definido. Use /produto-concepcao antes para preencher Quadro, Decorados, Urgências e Identidades. Sem isso, a Furadeira sai genérica.
```

**Se idconsumidor.md ou pesquisa-mercado.md não existirem**, gere mesmo assim mas avise no final que a qualidade da Furadeira aumenta com esses arquivos.

### 2. Carregar a base de conhecimento

Leia `.Codex/skills/furadeira-visual/references/6-mecanicas.md`. Esse arquivo contém as 6 mecânicas detalhadas, as 14 formas de eficiência, as 7 técnicas de nome de método e a tabela de combinação.

### 3. Anunciar próximo passo

```
🔍 Próximo passo: gerar a Furadeira do seu produto, decidindo a mecânica certa para o nicho. Tempo estimado: cerca de 1 minuto.
```

### 4. Decidir a mecânica automaticamente

Aplique a tabela de decisão da skill `gerar-furadeira` (em `.Codex/skills/gerar-furadeira/SKILL.md`). Cruze sinais do perfil + idconsumidor + pesquisa-mercado:

| Sinal detectado | Mecânica principal |
|---|---|
| Quadro tem prazo definido OU descreve progressão clara | Fases e Sequências |
| 2+ perfis de comprador com necessidades opostas no idconsumidor | Lógica Condicional |
| Aluno precisa se identificar com categoria antes de seguir | Enquadramento |
| 3 a 7 Argumentos Incontestáveis que coexistem | Listas |
| Público falha sozinho por causas específicas | Empecilhos (combina com Fases) |
| Resultado depende de hábito/repetição | Dinâmica de Entrega (combina) |
| Nenhum sinal forte | Fases e Sequências (default) |

Limite: máximo 2 mecânicas combinadas. Anote internamente qual é a principal e qual é a complementar (se houver).

### 5. Gerar a estrutura específica da mecânica

A estrutura no perfil.md varia conforme a mecânica. Use os Decorados, Urgências Ocultas, idconsumidor e pesquisa-mercado como insumo.

#### Se Fases e Sequências
- 3 a 5 fases ordenadas, cada uma com:
  - Nome da fase (curto, ação ou estado)
  - 1 frase descrevendo o que acontece nela
  - 2 a 4 microetapas (ações práticas concretas)
  - 1 forma de eficiência (das 14)

#### Se Lógica Condicional
- 1 decisão crítica (ex: "criança reativa, equilibrada ou passiva?")
- 2 ou 3 ramificações, cada uma com:
  - Nome próprio
  - Descrição curta de quem se enquadra
  - Protocolo específico (3 a 5 passos)
- 1 método de diagnóstico (questionário, autoavaliação, observação)

#### Se Enquadramento
- Nome do sistema de categorias (próprio)
- 3 ou 4 categorias, cada uma com:
  - Nome
  - Características observáveis
  - Protocolo específico
- 1 método de diagnóstico

#### Se Listas
- 3 a 7 pilares finitos
- Sugerir acrônimo se as iniciais formarem palavra memorável
- Cada pilar com:
  - Nome
  - 1 frase de explicação
  - 1 forma de eficiência

#### Se Empecilhos (combinada com Fases)
- 3 a 5 empecilhos comuns do nicho (extrair do idconsumidor e pesquisa-mercado)
- Para cada empecilho: nome, por que acontece, qual fase do método remove ele
- Junto, gerar as Fases (como na mecânica Fases e Sequências)

#### Se Dinâmica de Entrega (combinada)
- Nome do ritual (verbo + ação memorável)
- Frequência (diária, semanal)
- Duração (3 min, 10 min, 30 min)
- Em qual momento (ao acordar, antes de dormir, segunda e quinta)
- O que o aluno faz exatamente
- Por quanto tempo total (4 semanas, 5 semanas)

### 6. Sugerir nome do método (3 opções, 7 técnicas)

Sugira 1 nome principal + 2 alternativas, cada uma usando uma técnica diferente das 7:

- Acrônimo (CAVE, VTSD, 3F)
- Nome do Autor (Método {Nome do Aluno})
- Curioso (Furadeira, Aperta e Solta)
- Impactante (Escudo do Comportamento)
- Benefício (Fluência em 90 Dias)
- Mistério (Tecnologia de Alinhamento Postural Titanium)
- Número + Substantivo (3 Pilares, 4 C's)

Evite genéricos ("Método Online"), técnicos demais ("Protocolo de Regulação Neuroemocional") ou parecidos com o normal ("Curso de Emagrecimento").

### 7. Aplicar teste de eficiência

Para cada componente da Furadeira (cada fase, pilar, ramificação, ritual), mapeie qual das 14 formas de eficiência ele entrega:

Mais rápido | Mais barato | Menos esforço | Menos dor | Menos erro | Menos desperdício | Mais adesão | Mais prazeroso | Mais ético | Mais bonito | Mais sustentável | Mais saudável | Mais gostoso | Menos apelativo

Se um componente não conseguir carregar nenhuma forma, reescreva ou descarte. Cada componente carrega no mínimo 1, no máximo 2 formas.

### 8. Mostrar o resumo na tela

Formato exato:

```
✅ Furadeira gerada para "{nome do produto}":

Mecânica: {Principal}{ + Complementar se houver}
Nome principal: {nome do método sugerido com técnica entre parênteses}
Eficiência principal: {qual das 14 formas é o argumento mais forte}

{Estrutura específica da mecânica, formatada legível:

Para Fases:
  Fase 1. {Nome}
     Eficiência: {forma}
     Microetapas: {ação 1}, {ação 2}, {ação 3}
  
  Fase 2. {Nome}
     ...

Para Condicional:
  Decisão crítica: {qual é}
  
  Ramificação 1: {Nome}
     Quem se enquadra: {descrição}
     Protocolo: 1) ... 2) ... 3) ...
  
  Ramificação 2: ...
  
  Diagnóstico: {método}

Para Enquadramento, Listas, etc. — análogo, sempre legível.}

Nomes alternativos:
- {alternativa 1} ({técnica})
- {alternativa 2} ({técnica})

1. Aprovar e salvar no perfil.md
2. Quero trocar o nome
3. Quero ajustar algum bloco específico
4. Transformar em Trilha de Progressão (somente se mecânica for Fases e Sequências)
```

A opção 4 só aparece no resumo quando a mecânica principal for **Fases e Sequências**. Para outras mecânicas, omitir silenciosamente.

### 9. Tratar resposta do aluno

**Se 1 (aprovar):** seguir para passo 10.

**Se 2 (trocar nome):** mostrar os nomes alternativos numerados, pedir o número escolhido, atualizar nome principal e voltar a mostrar o resumo (passo 8) com o novo nome destacado.

**Se 3 (ajustar bloco):** perguntar qual bloco específico (ex: "Fase 2", "Ramificação Trilha Vermelha", "Pilar 3"), o aluno descreve o ajuste, regenerar só aquele bloco, voltar a mostrar o resumo.

**Se 4 (Trilha de Progressão):** converter as fases em níveis de progressão gamificados. Para cada fase, gerar:
- **Nome criativo do nível** (pode usar metáforas: faixas, rankings, elementos, estações, etc. — alinhado ao nicho do produto)
- **Quem está neste nível** (descrição do estado atual do aluno)
- **O que ele faz aqui** (as microetapas da fase, reescritas como conquistas)
- **Como avança** (critério concreto e mensurável para passar ao próximo nível)

Mostrar a Trilha formatada para aprovação antes de salvar:

```
Trilha de Progressão — {Nome do Método}

Nível 1 — {Nome criativo}
  Quem está aqui: {descrição}
  O que faz: {conquistas}
  Avança quando: {critério}

Nível 2 — {Nome criativo}
  ...

(repetir para cada fase)

1. Aprovar e salvar no perfil.md
2. Quero ajustar algum nível
```

Após aprovação, seguir para passo 10 salvando a estrutura de Trilha no lugar das Fases.

### 10. Salvar no perfil.md

Anuncie:

```
🔍 Próximo passo: salvar a Furadeira no perfil.md. Tempo estimado: cerca de 5 segundos.
```

Substitua a seção "## Furadeira (Método)" do `meus-produtos/{ativo}/perfil.md` por este schema:

```markdown
## Furadeira (Método)

**Nome do método:** {nome aprovado}
**Mecânica(s):** {Principal}{ + Complementar se houver}
**Eficiência principal:** {forma}

### Estrutura

{conteúdo específico da mecânica, no formato da seção 5}

### Eficiência por componente

- {Componente 1}: {forma}
- {Componente 2}: {forma}
- {...}
```

**Compatibilidade com painel:** se a mecânica for "Fases e Sequências", manter também os campos `### Macroetapas` (com `**Etapa N — Nome:** descrição` no formato antigo) para o `painel-incremental.py` parsear sem mudança. Para outras mecânicas, o painel renderiza a partir do bloco "Estrutura".

### 11. Atualizar o painel de entregas

Rode:

```
py -3 scripts/painel-incremental.py --slug {ativo}
```

Se o script não existir ou falhar, avise:
```
Não foi possível atualizar o painel automaticamente. Rode manualmente quando puder:
py -3 scripts/painel-incremental.py --slug {ativo}
```

### 12. Mensagem final

```
✅ Concluído: Furadeira salva no perfil.md.

Nome do método: {nome}
Mecânica: {mecânica}
Caminho: {raiz-do-projeto}/meus-produtos/{ativo}/perfil.md

Próximo:
- /furadeira-visual para gerar o prompt do ChatGPT e criar a imagem PNG do método
- /copy-pagina para usar a Furadeira na seção Método da página de vendas
```

## Regras

- Não fazer entrevista guiada. Decidir tudo a partir do contexto e mostrar o resultado.
- Não chamar a skill `revisora` (não é copy de venda, é estrutura de método).
- Não gerar imagem aqui. Imagem é responsabilidade do `/furadeira-visual`.
- Se o contexto for insuficiente (sem Quadro ou sem Decorados), redirecionar para `/produto-concepcao` em vez de adivinhar.
- Erros sempre em português claro, sem stack trace.
- Anunciar "próximo passo" antes de operações longas (regra global do AGENTS.md).
- Português brasileiro com acentuação correta. Aplicar as palavras críticas listadas no AGENTS.md.

---
name: "source-command-produto-consumidor"
description: "Comando obsoleto. A identidade do consumidor e o Painel de Entregas agora são gerados automaticamente pelo /produto-concepcao."
---

# source-command-produto-consumidor

Use esta skill quando o usuário pedir o comando `/produto-consumidor` do workshop (ou `produto-consumidor`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/produto-consumidor.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Identidade do Consumidor (fluxo unificado em /produto-concepcao)

Este comando foi desativado. O fluxo de identidade do consumidor (dados demográficos, paliativos, objeções pelo Framework dos 7 Argumentos, baldes e geração do `idconsumidor.md`) e a geração do `painel-entregas.html` agora rodam automaticamente dentro de `/produto-concepcao`, logo após o perfil ser salvo.

## Usage

```
/produto-consumidor
```

## O Que Fazer

Responda ao usuário, sem executar nada:

```
Este fluxo agora é automático dentro da Concepção do Produto.

Rode /produto-concepcao. A identidade do consumidor e o Painel de Entregas
são gerados automaticamente ao final da concepção, sem precisar de comando
separado.

Se o perfil já estiver salvo e só faltar regerar a identidade do consumidor
ou o painel, rode /produto-concepcao e escolha a opção de refazer aquela
parte quando ele perguntar.
```

**Bloco 2/3. Comportamento (Geração Proativa):**

Com base nos dados demográficos + Urgências Ocultas + Identidade do Consumidor do perfil + `pesquisa-mercado.md`, GERE automaticamente:

- **Paliativos** *(somente Middle Ticket)* — ferramentas, produtos e soluções concorrentes que existem no mercado e resolvem o problema parcialmente, sem entregar o resultado completo. Não é "o que o público já tentou e falhou". São os concorrentes diretos e indiretos: Pinterest, perfis de Instagram do nicho, cursos genéricos, apps, planilhas, templates gratuitos, etc. (baseado na pesquisa de mercado e nos concorrentes mapeados)
- **Sonho** — a frase que ela diria para uma amiga se alcançasse o resultado (baseado nos desejos)
- **Canais** — onde essa pessoa busca informação (baseado no perfil demográfico e no nicho)

Apresente tudo gerado de uma vez para o aluno validar e ajustar. Não peça item por item.

Mostre progresso ao concluir.

**Bloco 3/3. Objecoes (Framework dos 7 Argumentos, 5 sub-agentes em paralelo):**

Primeiro, defina as **5 principais objecoes** que um potencial comprador pode ter, com base no perfil do consumidor, preco, nicho, Quadro do produto e dados de `pesquisa-mercado.md` (especialmente Reclame Aqui). NÃO liste opcoes para o aluno escolher.

Depois, dispare **5 sub-agentes simultaneamente** usando a ferramenta Agent (todos na mesma mensagem, em paralelo). Avise o aluno:

```
Gerando as quebras de objecoes em paralelo. Cada objecao recebe 7 argumentos com 2 paragrafos cada.
Leva cerca de 2 minutos.
```

**Prompt de cada sub-agente** deve conter:
- O Quadro do produto
- O preco
- O nicho e publico-alvo
- O texto da objecao especifica que ele deve quebrar
- Os dados relevantes de `pesquisa-mercado.md` (reclamacoes Reclame Aqui, concorrentes, dados de mercado)
- Instrucao para gerar **7 formas de quebra**, cada uma com **2 paragrafos**, seguindo esta ordem fixa:
  1. Argumento Incontestavel (dado concreto, estatistica ou fato irrefutavel com fonte)
  2. Argumento Logico (causa e efeito, raciocinio frio com numeros)
  3. Argumento por Analogia (comparacao visual e acessivel, NUNCA citar celebridades, usar situacoes reais)
  4. Argumento por Exemplificacao (caso real com nome ficticio, situacao inicial, decisao tomada e resultado concreto)
  5. Argumento de Valor (custo vs. beneficio, comparacao do investimento com retorno tangivel e intangivel)
  6. Argumento de Consequencia (agir agora vs. adiar)
  7. Argumento de Contradicao (onde a objecao contradiz outras escolhas da propria pessoa)
- Cada paragrafo com sofisticacao de advogado + tecnica de comunicacao persuasiva
- Light Copy: sem travessao, sem ponto de exclamacao, sem pergunta retorica abrindo paragrafo, afirmacoes diretas
- Devolver o resultado formatado em markdown com os 7 argumentos numerados

Quando os 5 sub-agentes retornarem, monte o bloco completo de objecoes e apresente ao aluno para validacao. O aluno aprova, ajusta, adiciona ou remove.

**Confirmação antes de gerar:**
```
Resumo da identidade do consumidor:
- Perfil: [gênero], [idade], [profissão]
- Renda: [renda]
- Paliativos: [ferramentas e soluções concorrentes do mercado que resolvem o problema parcialmente — incluir apenas se Middle Ticket]
- Sonho: [resultado mágico]
- Canais: [onde busca info]
- Objeções: [principais objeções]

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 3. Gerar Documento

Salve em `meus-produtos/{ativo}/idconsumidor.md`:

```markdown
# Identidade do Consumidor: [Nome Fictício]

## Para Quem É
[Frase de posicionamento clara, 1-2 linhas]
"Este produto é para [perfil específico], que [problema/situação atual], e quer [transformação desejada]."

Não é para: [exclusões que ajudam a posicionar — quem NÃO é o público]

## Identidade do Consumidor
- **Idade:** / **Gênero:** / **Profissão:**
- **Renda:** / **Estado civil:** / **Localização:**
- **Nível de consciência:** [inconsciente → totalmente consciente]
- **Onde busca informação:** [canais]

## Paliativos (somente Middle Ticket — ferramentas e soluções concorrentes do mercado que resolvem o problema parcialmente)
- [ferramenta/solução concorrente] → [o que ela oferece e por que não entrega o resultado completo]

*Se Low Ticket: omitir esta seção inteiramente.*

## Objeções de Compra (Framework dos 7 Argumentos)

Para cada uma das 5 principais objeções, gerar 7 formas de quebra com 2 parágrafos cada. Ordem fixa dos argumentos.

### Objeção 1: [texto da objeção]

**1. Argumento Incontestável**
[Parágrafo 1: dado concreto, estatística, fato irrefutável com fonte.]

[Parágrafo 2: aprofundamento do dado aplicado à realidade do consumidor.]

**2. Argumento Lógico (causa e efeito)**
[Parágrafo 1: raciocínio frio com números e relação causa-consequência.]

[Parágrafo 2: virada lógica que reposiciona a pergunta.]

**3. Argumento por Analogia**
[Parágrafo 1: comparação visual, acessível, SEM celebridades, com situação real que o público vive.]

[Parágrafo 2: extensão da analogia conectando ao contexto de compra.]

**4. Argumento por Exemplificação**
[Parágrafo 1: caso real com nome fictício, situação inicial, decisão tomada.]

[Parágrafo 2: desfecho concreto e moral aplicável ao leitor.]

**5. Argumento de Valor (custo vs. benefício)**
[Parágrafo 1: comparação do investimento com retorno tangível.]

[Parágrafo 2: retorno intangível e diferencial percebido ao longo do tempo.]

**6. Argumento de Consequência (de agir ou não agir)**
[Parágrafo 1: cenário de adiar a decisão.]

[Parágrafo 2: cenário de decidir agora.]

**7. Argumento de Contradição**
[Parágrafo 1: onde a objeção contradiz outras escolhas ou prioridades da própria pessoa.]

[Parágrafo 2: conclusão que reposiciona a prioridade.]

### Objeção 2: [texto da objeção]
[mesma estrutura dos 7 argumentos, 2 parágrafos cada]

### Objeção 3: [texto da objeção]
[mesma estrutura dos 7 argumentos, 2 parágrafos cada]

### Objeção 4: [texto da objeção]
[mesma estrutura dos 7 argumentos, 2 parágrafos cada]

### Objeção 5: [texto da objeção]
[mesma estrutura dos 7 argumentos, 2 parágrafos cada]

## Frases que Essa Pessoa Diria
- "[dor]"
- "[desejo]"
- "[objeção]"

## Como se Comunicar
- Tom de voz recomendado
- Palavras que conectam
- Palavras que afastam

## Baldes de Para Quem É

O agente cria 5 perfis específicos de segmentação com base nas Urgências Ocultas, no público mapeado e nos dados de `pesquisa-mercado.md`. Cada perfil tem 5 afirmações diretas em linguagem de copy e tráfego pago.

Os 5 perfis devem representar recortes distintos (por profissão, momento de vida, dor dominante, nível de consciência ou objetivo imediato), não variações do mesmo perfil.

➤ Pra quem é - [Perfil específico 1]
1.
2.
3.
4.
5.

➤ Pra quem é - [Perfil específico 2]
1.
2.
3.
4.
5.

➤ Pra quem é - [Perfil específico 3]
1.
2.
3.
4.
5.

➤ Pra quem é - [Perfil específico 4]
1.
2.
3.
4.
5.

➤ Pra quem é - [Perfil específico 5]
1.
2.
3.
4.
5.
```

NOTA: As Urgências Ocultas ficam centralizadas em `meus-produtos/{ativo}/perfil.md`. Os baldes são derivados delas, nunca copiados.

### 4. Gerar Painel de Entregas HTML (via script)

Apos salvar o `idconsumidor.md`, gere o Painel de Entregas rodando o script Python:

```bash
py -3 scripts/painel-incremental.py --secao pesquisa
py -3 scripts/painel-incremental.py --secao quadro
py -3 scripts/painel-incremental.py --secao furadeira
py -3 scripts/painel-incremental.py --secao decorados
py -3 scripts/painel-incremental.py --secao urgencias
py -3 scripts/painel-incremental.py --secao identidade-produto
py -3 scripts/painel-incremental.py --secao identidade-comunicador
py -3 scripts/painel-incremental.py --secao identidade-consumidor
```

O script `painel-incremental.py` cria o shell do painel na primeira execução (com design escuro Fluxo Criativo definido em `scripts/painel_template.py`) e atualiza apenas a seção pedida em cada chamada subsequente, preservando o que já está preenchido. Ele lê `perfil.md`, `idconsumidor.md`, `pesquisa-mercado.md` e `tipo.md`, e gera `meus-produtos/{ativo}/painel-entregas.html` em menos de 1 segundo por seção.

**NAO gere o HTML manualmente.** O script cuida de tudo: sidebar, 9 telas, accordions, timelines, badges, graficos SVG e responsivo.

**NAO leia** `design-system-components.md` nem `design-referencia-vtsd.md` para este arquivo. O painel usa design proprio definido no template.

**Apos rodar o script, leia o output (relatorio de validacao).** O script imprime `[OK]` e `[!!]` para cada campo:
- Se tudo `[OK]`: informe o aluno que o painel esta pronto.
- Se houver `[!!]`: corrija os campos faltantes no `.md` correspondente e rode o script de novo. Repita ate nao ter mais avisos. So entao informe o aluno.

Mensagem final para o aluno:
```
Identidade do consumidor salva em meus-produtos/{ativo}/idconsumidor.md.

Painel de entregas gerado com todas as informacoes do produto.

Para visualizar, copie e cole no navegador:
file:///{raiz-do-projeto}/meus-produtos/{ativo}/painel-entregas.html
```

### 5. Próximo Passo

**Se Middle Ticket:**
```
Próximo passo: /copy-pagina para criar a página de vendas 8D do produto.
```

**Se Low Ticket:**

Aplique o framework de decisão Quiz vs. Página com base no produto:

| Critério | QUIZ | PÁGINA |
|---|---|---|
| Tipo de produto | Emocional, dor, identificação | Prático, ferramenta, direto ao ponto |
| Nível de consciência | Não sabe que tem o problema | Já sabe o que quer |
| Complexidade | Precisa diagnosticar ou explicar | Decisão simples e direta |
| Faixa de preço | Até R$47 | Acima de R$97 |
| Tipo de público | Emocional | Analítico ou pragmático |

Regra: 2 ou mais critérios para o mesmo lado definem a recomendação. Em caso de empate: QUIZ.

Apresente a análise aplicada ao produto específico com justificativa e recomende:

```
Com base no seu produto, a recomendação é: [QUIZ / PÁGINA]

[Justificativa com os critérios que definiram a escolha]

Próximo passo: /lt-quiz   (se QUIZ)
              /lt-pagina  (se PÁGINA)
```

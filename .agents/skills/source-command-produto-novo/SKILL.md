---
name: "source-command-produto-novo"
description: "Porta de entrada do projeto. Verifica produto ativo, cria um novo produto ou gera ideias de produto. Acionada automaticamente em QUALQUER nova conversa pela regra de abertura de sessão do CLAUDE.md."
---

# source-command-produto-novo

Use esta skill quando o usuário pedir o comando `/produto-novo` do workshop (ou `produto-novo`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/produto-novo.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

<!--
GOVERNANÇA (NÃO REMOVER):

Esta skill é a PORTA DE ENTRADA do projeto. Ela é acionada automaticamente em
toda nova conversa, por força da seção "REGRA DE ABERTURA DE SESSÃO" do
CLAUDE.md, independentemente do texto que o aluno digitou ("olá", "oi",
"começar", "quero um produto", "vamos lá", etc.).

Por isso, a skill precisa atender três cenários possíveis num mesmo ponto de
entrada:

  1) Aluno já tem produto ativo → mostrar qual é e perguntar se quer continuar
     com ele ou criar um novo. NÃO recadastrar sem o aluno pedir.
  2) Aluno quer criar um produto novo (tem ideia) → seguir o fluxo "Ramo 1".
  3) Aluno não tem ideia e quer sugestões → seguir o fluxo "Ramo 2" (pesquisa
     de mercado + 50 ideias).

Futuras edições: mantenham as três opções no Passo 1 e a detecção de produto
ativo no Passo 0. Não quebrem o comportamento determinístico de abertura.
-->

# Novo Produto. Criar e Ativar

Porta de entrada do projeto. Detecta se já existe produto ativo, cria um produto novo ou ajuda a descobrir qual produto criar.

## Usage

```
/produto-novo
```

## O Que Fazer

> **Regra obrigatória de comunicação:** siga o padrão "Pensar em Voz Alta" do CLAUDE.md. Antes de cada operação longa desta skill (pesquisa de mercado, geração de 50 ideias, criação de pasta e arquivos do produto, escrita do perfil.md), anuncie em UMA linha com `🔍 Próximo passo: {ação}. Tempo estimado: cerca de X segundos.` Ao concluir, confirme com `✅ Concluído: {entrega}. Caminho: {caminho}.`
>
> Exemplos desta skill:
> - `🔍 Próximo passo: pesquisar o nicho de {nicho} no Google e TikTok para coletar ângulos e concorrentes. Tempo estimado: cerca de 90 segundos.`
> - `🔍 Próximo passo: gerar 50 ideias de produto a partir da pesquisa de mercado. Tempo estimado: cerca de 30 segundos.`
> - `🔍 Próximo passo: criar a pasta do produto e salvar o tipo.md com o formato escolhido. Tempo estimado: cerca de 5 segundos.`
> - `✅ Concluído: produto {nome} criado e ativado. Caminho: meus-produtos/{slug}/.`

### Passo 1. Verificar produto ativo

Antes de qualquer pergunta, leia `meus-produtos/.ativo`.

**Se o arquivo existir e tiver um slug válido**, leia `meus-produtos/{slug}/perfil.md` (ou `meus-produtos/{slug}/tipo.md` se o perfil ainda não existir) para descobrir o nome do produto e apresente:

```
Você já tem um produto ativo: **{nome do produto}** ({tipo}).

1. Continuar com este produto
2. Criar um produto novo (Já tenho nome, formato e preço)
3. Quero ideias de novo produto

Digite o número:
```

- Se escolher **1**: encerre a skill com a mensagem "Seguindo com **{nome}**. Me diga o que quer criar (copy, página, anúncio, funil) ou digite o comando da skill que quer usar." e pare.
- Se escolher **2**: siga direto para o **Ramo 1** abaixo (pule o Passo 2).
- Se escolher **3**: siga direto para o **Ramo 2** abaixo (pule o Passo 2).

**Se não houver produto ativo** (arquivo `.ativo` inexistente ou vazio), siga para o Passo 2.

### Passo 2. Verificar se já tem produto ou ideia

Primeira pergunta obrigatória (só quando NÃO há produto ativo):

```
Você já tem um produto cadastrado, quer criar um novo, ou quer ideias de produto?

1. Já tenho um produto e quero cadastrar agora
2. Quero criar um produto novo (tenho uma ideia)
3. Quero ideias de produto (ainda não sei o que criar)

Digite o número:
```

- Opção **1** ou **2**: siga para o **Ramo 1**.
- Opção **3**: siga para o **Ramo 2**.

---

### Ramo 1 — "Sim, já tenho"

#### Passo 1. Perguntar o nome do produto

```
Qual o nome deste produto?
(ex: "Curso de Inglês Fluente", "Mentoria Fitness Online", "Tarô para Iniciantes")
```

#### Passo 2. Perguntar o tipo do produto

> **CRÍTICO:** reproduza o texto abaixo exatamente como está. Não altere faixas de preço, não substitua R$37 por outro valor.

```
Que tipo de produto é este?

1. Low Ticket (R$ 37 a R$ 97. quiz, desafio, mini-curso, agente GPT)
2. Middle Ticket (R$ 97 a R$ 997. curso online, workshop, grupo)

Digite o número:
```

Guarde o tipo escolhido. Ele será salvo no arquivo `meus-produtos/{slug}/tipo.md`.

#### Passo 2b. Perguntar o preço do produto

Se Low Ticket:

```
Qual será o preço de venda?
(ex: "R$47", "R$67", "R$97")
```

Se Middle Ticket:

```
Qual será o preço de venda?
(ex: "R$197", "R$497", "R$997")
```

Guarde o valor informado. Ele será salvo em `meus-produtos/{slug}/preco.md`.

#### Passo 3. Gerar slug automaticamente

Com o nome fornecido, gere um slug em kebab-case (letras minúsculas, sem acentos, palavras separadas por hífen). Salve e siga direto, sem pedir confirmação do slug ao usuário (é um detalhe técnico irrelevante para ele).

Exemplos:
- "Curso de Inglês Fluente" → `curso-ingles-fluente`
- "Mentoria Fitness Online" → `mentoria-fitness-online`
- "Tarô para Iniciantes" → `taro-para-iniciantes`

#### Passo 4. Verificar se já existe

Verifique se já existe uma pasta `meus-produtos/{slug}/`. Se existir, informe:
```
Já existe um produto com esse identificador. Quer usar /produto-trocar para acessá-lo?
```

#### Passo 5. Criar estrutura de pastas

Crie as seguintes pastas:
```
meus-produtos/{slug}/
meus-produtos/{slug}/entregas/
meus-produtos/{slug}/entregas/paginas/
meus-produtos/{slug}/entregas/emails/
meus-produtos/{slug}/entregas/copy-pagina/
meus-produtos/{slug}/entregas/criativos/
meus-produtos/{slug}/entregas/comercial/
meus-produtos/{slug}/entregas/textos-de-venda/
```

#### Passo 6. Definir como produto ativo

Salve o slug em `meus-produtos/.ativo` (sobrescreva o conteúdo anterior).

#### Passo 7. Salvar o tipo e o preço do produto

Salve o tipo escolhido em `meus-produtos/{slug}/tipo.md`.

Salve o preço informado em `meus-produtos/{slug}/preco.md`. O arquivo deve conter apenas o valor (ex: `R$47`), sem texto adicional.

**Formato OBRIGATÓRIO do `tipo.md`:** o arquivo deve conter APENAS uma única linha com o texto literal `Low Ticket` OU `Middle Ticket`. Nada mais. Sem `#` de header, sem `**` de negrito, sem justificativa, sem faixa de preço, sem "formato escolhido", sem comentário, sem linha em branco no final.

Exemplos do conteúdo correto do arquivo:

```
Low Ticket
```

ou

```
Middle Ticket
```

**Por quê:** o `tipo.md` é lido por scripts (painel de entregas, validadores, detecção condicional de Furadeira/Paliativos) que esperam apenas o rótulo do tipo. Qualquer conteúdo extra vai aparecer cru no card "Tipo" da página de Visão Geral do painel e quebrar a detecção condicional. Justificativa, faixa de preço, preço definido e formato escolhido pertencem ao `perfil.md`, nunca ao `tipo.md`.

#### Passo 8. Atualizar o manifest do painel

Rode no terminal para regenerar `meus-produtos/index.js` (o painel global em `painel.html` lê esse arquivo):

```
py -3 scripts/painel-atualizar.py
```

#### Passo 9. Inicializar Painel de Entregas

Antes de mostrar a mensagem final, execute obrigatoriamente a seção **"Inicialização do Painel de Entregas"** no fim deste arquivo. Ela gera o `painel-entregas.html` do produto com placeholders "Em breve" e atualiza o manifest. O painel será aberto no navegador automaticamente quando o aluno rodar `/produto-concepcao`.

#### Passo 10. Confirmar e sugerir próximo passo

```
Produto "{nome}" criado e ativado.
Identificador: {slug}
Tipo: {tipo}
Preço: {preco}

Próximo passo: partir para a concepção do produto (/produto-concepcao).
```

---

### Ramo 2 — "Não, quero descobrir o que criar"

#### Passo 1. Perguntar especialidade

```
Qual é a sua especialidade? O que você ensina ou entrega para as pessoas?
(ex: "Tarô", "Emagrecimento feminino", "Marketing digital para pequenos negócios")
```

#### Passo 2. Pesquisa de mercado completa (UMA vez, agora)

Antes de pesquisar, gere um **slug provisório** derivado da especialidade informada (kebab-case, sem acentos, ex: `taro`, `emagrecimento`, `ingles-fluente`). Crie a pasta `meus-produtos/{slug-provisorio}/` e salve o slug em `meus-produtos/.ativo`. Isso garante que a pesquisa seja salva diretamente no caminho definitivo `meus-produtos/{slug-provisorio}/pesquisa-mercado.md`, sem arquivo temporário.

Em seguida, execute a SKILL `pesquisa-mercado` completa (9 eixos: tamanho de mercado, concorrentes, faixa de preço, público-alvo, objeções reais, assuntos quentes, YouTube Top 10, biblioteca de anúncios e riscos regulatórios). Esta é a pesquisa definitiva, que alimentará as 50 ideias, a sugestão de preço e todo o fluxo do `/produto-concepcao`. Não refaça em nenhuma etapa posterior.

Anuncie ao aluno (Nível 1, pois é o entry point que o aluno invocou):
```
🔍 Próximo passo: pesquisar o mercado de {nicho} (9 passos). Tempo estimado: 8 a 12 minutos.
```

Use como inputs para a SKILL:
- **Nicho:** a especialidade informada pelo aluno
- **Quadro:** ainda não definido (use a especialidade como promessa inicial)
- **Formato pretendido:** ainda não definido
- **Slug:** {slug-provisorio}
- **Caminho de destino:** `meus-produtos/{slug-provisorio}/pesquisa-mercado.md`

#### Passo 3. Gerar 50 ideias de infoprodutos

Com base na pesquisa de mercado e no conceito de **urgências ocultas**, gere **50 ideias DIVERSAS** de infoprodutos para o nicho informado. Não são variações da mesma ideia, são 50 conceitos distintos entre si (ângulo, método, público ou promessa diferentes).

**Conceito de urgências ocultas aplicado às ideias:**
- **Dores:** problemas que o público sofre e que o produto resolve
- **Dúvidas:** perguntas reais que o público faz e que abrem porta para o produto
- **Desejos:** estados que o público quer alcançar
- **Assuntos relacionados:** temas adjacentes que atraem o mesmo público
- **Urgências quentes:** pessoas com alta intenção de compra no nicho
- **Urgências frias:** volume alto de busca, baixa intenção direta, mas público certo
- **Urgências inusitadas:** conexões inesperadas e criativas que chamam atenção

**Distribuição obrigatória por formato (15 categorias, mínimo 3 ideias cada, total 50):**
1. Mentoria em grupo
2. Mentoria individual
3. Curso gravado
4. Curso ao vivo (turma fechada)
5. Ebook
6. Template ou kit pronto
7. Consultoria
8. Comunidade paga (assinatura)
9. Workshop (evento curto e intensivo)
10. Serviço (feito para o cliente)
11. Agente GPT (assistente personalizado treinado para resolver uma dor específica do nicho)
12. Mini-SaaS ou ferramenta web (microaplicativo simples, página única, que entrega um resultado em segundos)
13. Planilha pronta (Excel ou Google Sheets com cálculo, automação ou diagnóstico)
14. Checklist (PDF ou Notion com lista validada passo a passo, baixo ticket, alta percepção de valor)
15. Desafio (jornada cronometrada de 3, 7, 21 ou 30 dias com entrega diária)

Distribua as 50 ideias entre as 15 categorias garantindo **pelo menos 3 em cada**. Em particular, as 5 categorias finais (Agente GPT, Mini-SaaS, Planilha, Checklist, Desafio) **NUNCA podem ficar de fora**, mesmo que o nicho pareça pouco tecnológico. Sempre encaixe pelo menos 3 ideias em cada uma, traduzindo a metodologia do mestre/criador para o formato. As 5 ideias restantes (50 - 15×3 = 5) vão para as categorias com maior aderência ao nicho pesquisado.

**Organização do output:**
Apresente a lista **agrupada por formato**, com um subtítulo para cada categoria e as ideias daquela categoria numeradas logo abaixo. Dentro de cada grupo, use tabela:

```
### Mentoria em grupo

| # | Nome | Público-alvo resumido | Faixa de preço |
|---|------|----------------------|----------------|
| 1 | ... | ... | R$ ... |
```

**Colunas da tabela:**
| # | Nome | Público-alvo resumido | Faixa de preço |

Numeração **contínua de 1 a 50** (não reinicia a cada grupo), para o aluno escolher pelo número depois.

**Regras para as ideias:**
- 50 conceitos distintos, nunca variações da mesma ideia
- Evite ideias genéricas. Use criatividade e ângulos inusitados
- Gere ofertas com alto desejo e urgência natural
- Pense em métodos pouco conhecidos, tecnologias emergentes, estratégias exclusivas
- Os produtos precisam ser simples, fáceis de consumir e permitir picos de vendas
- Faixa de preço coerente com o formato e com os concorrentes mapeados na pesquisa
- Use Light Copy nas descrições: sem exageros, sem promessas vazias, sem ponto de exclamação

#### Passo 4. Usuário escolhe a ideia

```
Qual número da tabela mais te interessa?
(Pode adaptar o título ou combinar elementos de mais de uma ideia)
```

Após a escolha, confirme:
```
Ótima escolha. Vamos criar: "{título escolhido}"

Tipo sugerido com base na ideia e na pesquisa: {Low Ticket / Middle Ticket}
Preço sugerido: R${valor} ({justificativa baseada nos concorrentes mapeados})

1. Confirmar tipo e preço
2. Quero ajustar
```

#### Passo 5. Registrar o produto

Com a ideia aprovada, gere o slug definitivo. Se o slug definitivo for diferente do slug provisório criado no Passo 2, renomeie a pasta `meus-produtos/{slug-provisorio}/` para `meus-produtos/{slug}/` e atualize `meus-produtos/.ativo` com o slug definitivo. A pesquisa já estará no caminho correto dentro da pasta renomeada.

Crie as subpastas de entregas dentro de `meus-produtos/{slug}/` (mesmos passos 5 a 6 do Ramo 1). Salve `tipo.md` e `preco.md` com os valores confirmados.

#### Passo 6. Atualizar o manifest do painel

Rode no terminal para regenerar `meus-produtos/index.js`:

```
py -3 scripts/painel-atualizar.py
```

#### Passo 7. Inicializar Painel de Entregas

Antes de mostrar a mensagem final, execute obrigatoriamente a seção **"Inicialização do Painel de Entregas"** no fim deste arquivo. Ela gera o `painel-entregas.html` do produto com placeholders "Em breve" (incluindo a seção de pesquisa, que já está pronta) e atualiza o manifest. O painel será aberto no navegador automaticamente quando o aluno rodar `/produto-concepcao`.

#### Passo 8. Confirmar e sugerir próximo passo

```
Produto "{nome}" criado e ativado.
Identificador: {slug}
Tipo: {tipo}
Preço: {preco}

A pesquisa de mercado do nicho já foi feita e está salva.
Ela será usada em todas as etapas seguintes sem nova busca.

Próximo passo: partir para a concepção do produto (/produto-concepcao).
```

---

## Inicialização do Painel de Entregas

> Bloco compartilhado pelos dois ramos. Roda **uma vez**, logo após o produto estar criado e ativado, antes da mensagem final ao aluno. Gera o `painel-entregas.html` do produto com placeholders "Em breve", atualiza o manifest e abre o painel no navegador automaticamente.

### A. Anunciar a operação

```
🔍 Próximo passo: gerar o painel de entregas do produto. Tempo estimado: cerca de 5 segundos.
```

### B. Gerar o painel de entregas com placeholders

Rode no terminal (use `python3` no Mac/Linux, `py -3` no Windows):

```
python3 scripts/painel-incremental.py --secao quadro
```

Isso cria `meus-produtos/{slug}/painel-entregas.html` com o shell completo e todas as seções marcadas como "Em breve". Os blocos vão sendo preenchidos automaticamente conforme o aluno roda `/produto-concepcao`, `/copy-pagina`, `/copy-anuncio` etc.

Se for Ramo 2 (pesquisa de mercado já feita), rode também:

```
python3 scripts/painel-incremental.py --secao pesquisa
```

para que o card de pesquisa já apareça preenchido no painel.

### C. Atualizar o manifest

Garanta que o manifest está atualizado pra que o painel global encontre o produto novo:

```
python3 scripts/painel-atualizar.py
```

### D. Abrir o painel no navegador e mostrar caminho ao aluno

Detecte o caminho absoluto da raiz do projeto a partir do diretório de trabalho atual (execute `pwd` no Bash para obter o valor).

Monte o caminho absoluto completo: `{raiz}\meus-produtos\{slug}\painel-entregas.html`

Em seguida, abra o arquivo no navegador rodando no terminal:

- **Windows:** `start "" "{caminho-absoluto}"`
- **Mac/Linux:** `open "{caminho-absoluto}"`

Depois mostre ao aluno:

```
✅ Concluído: painel de entregas criado e aberto no navegador.

Se não abrir automaticamente, copie e cole este caminho no navegador:
{raiz}\meus-produtos\{slug}\painel-entregas.html
```

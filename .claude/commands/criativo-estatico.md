---
name: workshop-marketing:criativo-estatico
description: Gera criativo estático de anúncio (imagem) para Instagram. Orquestrador que pergunta o formato e direciona para a sub-skill correspondente. Cobre 24 formatos. Promessa Simples, Caixinha de Perguntas, Criativo Surreal, AIDA Completo, UGC Rotina Real, POV, Problema-Solução, Jeito Certo x Jeito Errado, Checklist, ASMR/Sensação, Meme, Jogo dos 7 Erros, Criativo Notícia, Associação Criativa, Criativo História com Quebra de Objeção, O Desespero de Quem, Fofinho, Nunca, Sempre, Timelapse, UGC Coisas Estranhas, Você Merece, Objetos Estranhos e Reflexão Editorial. Em todos, no fim o aluno escolhe gerar a imagem colando o prompt no ChatGPT ou direto pela API. Use sempre que o usuário pedir criativo estático, anúncio em imagem, arte de anúncio, promessa simples, caixinha de perguntas, criativo surreal, anúncio surreal, anúncio AIDA, UGC, POV, problema e solução, jeito certo e errado, checklist, ASMR, meme, jogo dos 7 erros, criativo notícia, associação criativa, criativo história, desespero de quem, fofinho, criativo nunca, criativo sempre, timelapse, UGC coisas estranhas, você merece, objetos estranhos, reflexão editorial ou variantes desses formatos.
allowed-tools: Read, Write, Bash, WebSearch
---

# Criativo Estático. Orquestrador de Formatos de Anúncio

Gera criativo estático de anúncio. Antes de tudo, pergunta o formato e direciona pra sub-skill correspondente. Cada formato tem fluxo próprio (número de perguntas, geração e saída).

## Usage

```
/criativo-estatico
```

## O Que Fazer

### 0. Contexto

Leia o máximo de contexto disponível sobre o produto ativo. Em ordem:

1. **`meus-produtos/.ativo`** (obrigatório). O slug do produto ativo (ex: `automacoes-inteligentes`).
2. **`meus-produtos/{ativo}/perfil.md`** (se existir). Quadro, Furadeira, Decorados, Identidades, Urgências Ocultas, nicho, público.
3. **`meus-produtos/{ativo}/idconsumidor.md`** (se existir). Identidade do Consumidor com objeções, paliativos, baldes.
4. **`meus-produtos/{ativo}/tipo.md`** (se existir). Tipo do produto (low ticket, mid ticket, high ticket).
5. **`meus-produtos/{ativo}/preco.md`** (se existir). Preço do produto.
6. **`meus-produtos/{ativo}/pesquisa-mercado.md`** (se existir). Pesquisa de mercado do nicho.

Da combinação desses arquivos, extrair pra passar pras sub-skills:

- **Nome do produto**: do `perfil.md` (cabeçalho ou seção "Nome do produto"); se não existir, **inferir do slug** capitalizando e expandindo (ex: `automacoes-inteligentes` vira "Automações Inteligentes", `curso-tarot` vira "Curso de Tarot").
- **Nicho**: do `perfil.md` (seção "Nicho"); se não existir, **inferir do nome inferido + tipo.md + preco.md** (ex: "Automações Inteligentes" + "low ticket" + "R$ 47" sugere nicho "automação com IA pra pequenos negócios").
- **O que o produto ensina ou resolve (Quadro)**: do `perfil.md` (seção "Quadro"); se não existir, **inferir do nome + tipo**.
- **Público**: do `idconsumidor.md` (resumo); se não existir, do `perfil.md` (seção "Para Quem É"); se não existir nenhum dos dois, **inferir do nicho** (ex: nicho "automação com IA pra pequenos negócios" sugere público "donos de pequenos negócios que querem economizar tempo com IA").
- **Tipo**: do `tipo.md` se existir.
- **Preço**: do `preco.md` se existir.

Esse contexto enriquecido (real + inferido) é compartilhado entre as 13 sub-skills. As sub-skills SEMPRE mostram o resumo do contexto ao aluno antes de prosseguir, marcando claramente o que veio do perfil e o que foi inferido, pedindo confirmação ou correção.

**Importante**: o objetivo é NUNCA fazer entrevista do zero quando há contexto disponível. Mesmo com perfil ausente, o slug + tipo + preço já dão pistas suficientes pra montar um chute inicial que o aluno confirma ou ajusta.

### 1. Atalho de roteamento direto (antes de mostrar o menu)

Se a mensagem inicial do aluno mencionar EXPLICITAMENTE o nome do formato, pular o menu e ir direto pra sub-skill correspondente. Termos que disparam o atalho:

| Mensagem do aluno contém | Sub-skill | Arquivo a ler |
|---|---|---|
| "promessa simples", "criativo simples", "anúncio simples", "formato simples" | Promessa Simples | `.claude/commands/criativo-estatico/promessa-simples.md` |
| "caixinha de perguntas", "caixinha", "pergunta e resposta", "anúncio nativo" | Caixinha de Perguntas | `.claude/commands/criativo-estatico/caixinha-de-perguntas.md` |
| "criativo surreal", "anúncio surreal", "surreal", "fora do mundo normal", "metáfora visual", "impacto visual", "editorial", "Cannes Lions" | Criativo Surreal | `.claude/commands/criativo-estatico/criativo-surreal.md` |
| "AIDA", "fluxo completo", "criativo avançado" | AIDA Completo | `.claude/commands/criativo-estatico/aida.md` |
| "UGC", "rotina real", "estilo TikTok", "anúncio orgânico", "creator amador" | UGC Rotina Real | `.claude/commands/criativo-estatico/ugc-rotina-real.md` |
| "POV", "ponto de vista", "situação reconhecível", "vivência" | POV | `.claude/commands/criativo-estatico/pov.md` |
| "problema solução", "problema e solução", "antes e depois", "UGC brasileiro" | Problema-Solução | `.claude/commands/criativo-estatico/problema-solucao.md` |
| "jeito certo", "jeito errado", "erro vs acerto", "o que não fazer", "comparação UGC" | Jeito Certo × Jeito Errado | `.claude/commands/criativo-estatico/jeito-certo-jeito-errado.md` |
| "checklist", "passo a passo", "5 passos", "protocolo", "lista de ações" | Checklist | `.claude/commands/criativo-estatico/checklist.md` |
| "ASMR", "sensação", "super zoom", "macro", "textura sensorial" | ASMR / Sensação | `.claude/commands/criativo-estatico/asmr-sensacao.md` |
| "meme", "criativo engraçado", "humor", "viral", "anúncio engraçado" | Meme | `.claude/commands/criativo-estatico/meme.md` |
| "jogo dos 7 erros", "jogo dos erros", "encontre os erros", "7 erros", "gamificado" | Jogo dos 7 Erros | `.claude/commands/criativo-estatico/jogo-7-erros.md` |
| "notícia", "manchete", "estilo portal", "matéria de jornal", "estilo Metrópoles" | Criativo Notícia | `.claude/commands/criativo-estatico/criativo-noticia.md` |
| "associação criativa", "associação", "objeto + pergunta", "ponte criativa", "metáfora com objeto" | Associação Criativa | `.claude/commands/criativo-estatico/associacao-criativa.md` |
| "criativo história", "história com quebra", "quebra de objeção", "diálogo 4 quadros", "criativo em diálogo" | Criativo História + Quebra de Objeção | `.claude/commands/criativo-estatico/criativo-historia.md` |
| "desespero de quem", "desespero", "dor visceral", "olhar de desespero" | O Desespero de Quem | `.claude/commands/criativo-estatico/desespero-de-quem.md` |
| "fofinho", "criativo fofo", "tom amoroso", "cena fofa", "anúncio fofo" | Fofinho | `.claude/commands/criativo-estatico/fofinho.md` |
| "nunca", "criativo nunca", "erro a não cometer", "o que não fazer no nicho" | Nunca | `.claude/commands/criativo-estatico/nunca.md` |
| "sempre", "criativo sempre", "hack a sempre fazer", "o que sempre fazer no nicho" | Sempre | `.claude/commands/criativo-estatico/sempre.md` |
| "timelapse", "ângulo aéreo", "comece hoje", "primeiros passos", "evolução em time-lapse" | Timelapse | `.claude/commands/criativo-estatico/timelapse.md` |
| "ugc coisas estranhas", "coisas estranhas", "absurdo viral", "humor com objeto", "ugc bizarro" | UGC Coisas Estranhas | `.claude/commands/criativo-estatico/ugc-coisas-estranhas.md` |
| "você merece", "voce merece", "aspiracional", "resultado visível", "3 desejos" | Você Merece | `.claude/commands/criativo-estatico/voce-merece.md` |
| "objetos estranhos", "objeto perto da câmera", "objeto curioso", "objeto metáfora", "frame de TikTok com objeto" | Objetos Estranhos | `.claude/commands/criativo-estatico/objetos-estranhos.md` |
| "reflexão editorial", "reflexao editorial", "criativo editorial", "post jornalístico", "estilo tweet expandido", "criativo com dados", "conta maluca", "polêmica do nicho" | Reflexão Editorial | `.claude/commands/criativo-estatico/reflexao-editorial.md` |

Se não tiver atalho claro, seguir pro Passo 2 (menu).

### 2. Pergunta de roteamento (menu padrão)

Apresente as 24 opções:

```
Qual formato de criativo você quer criar?

1. Promessa Simples
   O tipo mais direto. Gera título, legenda e o prompt da arte.
   Ideal quando você quer rapidez e simplicidade.

2. Caixinha de Perguntas
   Simula a caixinha nativa do Instagram. 15 ideias de pergunta + resposta,
   você escolhe a melhor. Ideal pra anúncio que pareça conteúdo orgânico.

3. Criativo Surreal
   Forte impacto visual fora do mundo normal (escalas impossíveis, metáforas
   visuais), estética editorial nível Cannes Lions. 10 ideias, escolhe uma.

4. AIDA Completo
   Fluxo avançado em 3 passos (cena, layout, texto). Controle visual total.

5. UGC Rotina Real
   Foto que parece post orgânico de pessoa comum brasileira em momento de
   rotina. 10 ideias, escolhe uma. Ideal pra anúncio que não parece anúncio.

6. POV
   Coloca o público vivendo uma situação reconhecível do nicho (dor ou
   desejo), texto em faixas estilo TikTok. 10 ideias, escolhe uma.

7. Problema-Solução
   Arte dividida ao meio. Problema de um lado, solução prática do outro.
   Estética UGC brasileira. 10 ideias, escolhe uma.

8. Jeito Certo × Jeito Errado
   Split com a mesma pessoa nas duas cenas, comparando o erro comum e o
   hack que muda o jogo. 10 ideias, escolhe uma.

9. Checklist
   Pessoa real segurando um caderno com checklist de 5 passos práticos.
   10 temas, escolhe um.

10. ASMR / Sensação
    Foto super zoom macro de um detalhe sensorial do nicho, textura ASMR.
    10 ideias, escolhe uma.

11. Meme
    Criativo humorístico com estrutura de meme. 20 ideias (10 estruturas
    criadas + 10 memes brasileiros reais), escolhe uma.

12. Jogo dos 7 Erros
    Cena com 7 erros visuais embutidos pro espectador encontrar. Gatilho de
    engajamento. 10 cenas, escolhe uma.

13. Criativo Notícia
    Arte com cara de matéria real de portal de notícias. 10 manchetes
    variando o tom, escolhe uma.

14. Associação Criativa
    Objeto inusitado + pergunta + ponte criativa com o nicho. 10 ideias,
    escolhe uma. Ideal pra parar o scroll com curiosidade visual.

15. Criativo História + Quebra de Objeção
    Diálogo em 4 quadros que apresenta uma objeção real do público e a
    quebra dela. 10 objeções, depois 10 ideias de roteiro, escolhe.

16. O Desespero de Quem
    Cena com olhar de dor visceral de alguém vivendo o problema do nicho.
    10 ideias, escolhe uma. Ativa identificação imediata.

17. Fofinho
    Cena com tom amoroso e leve, com o resultado positivo do nicho. 10
    ideias, escolhe uma. Para nichos onde dor pesada não converte.

18. Nunca
    Frame TikTok pausado mostrando um erro específico do nicho que o público
    NUNCA deve cometer. 10 ideias, escolhe uma. Par com a opção 19.

19. Sempre
    Frame TikTok pausado mostrando um hack/atitude que o público SEMPRE
    deveria fazer no nicho. 10 ideias, escolhe uma. Par com a opção 18.

20. Timelapse
    Ângulo aéreo com 3 primeiros passos do nicho em estética aesthetic.
    Promessa "Comece hoje". 10 ideias, escolhe uma.

21. UGC Coisas Estranhas
    Pessoa fazendo algo absurdo com 1 objeto, ponte genial com o nicho.
    10 ideias, escolhe uma. Humor viral.

22. Você Merece
    Cena aspiracional com resultado visível e 3 desejos reais do público.
    10 ideias, escolhe uma. Estilo TikTok com tom de conquista.

23. Objetos Estranhos
    Pessoa segurando um objeto curioso MUITO perto da câmera como metáfora
    visual do nicho. 10 ideias, escolhe uma. Frame ultra-realista.

24. Reflexão Editorial
    Texto estático estilo post jornalístico com dado, notícia ou conta
    maluca do nicho. Venda sutil no final. 10 reflexões, escolhe uma.

Em qualquer formato, no fim você escolhe gerar a imagem colando o prompt no
ChatGPT (grátis) ou direto pela API (tem custo, salva o arquivo automático).

Digite o número:
```

### 3. Roteamento

Conforme a resposta:

- **1** ou termos relacionados a Promessa Simples: leia `.claude/commands/criativo-estatico/promessa-simples.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **2** ou termos relacionados a Caixinha de Perguntas: leia `.claude/commands/criativo-estatico/caixinha-de-perguntas.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **3** ou termos relacionados a Criativo Surreal: leia `.claude/commands/criativo-estatico/criativo-surreal.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **4** ou termos relacionados a AIDA: leia `.claude/commands/criativo-estatico/aida.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **5** ou termos relacionados a UGC Rotina Real: leia `.claude/commands/criativo-estatico/ugc-rotina-real.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **6** ou termos relacionados a POV: leia `.claude/commands/criativo-estatico/pov.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **7** ou termos relacionados a Problema-Solução: leia `.claude/commands/criativo-estatico/problema-solucao.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **8** ou termos relacionados a Jeito Certo × Jeito Errado: leia `.claude/commands/criativo-estatico/jeito-certo-jeito-errado.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **9** ou termos relacionados a Checklist: leia `.claude/commands/criativo-estatico/checklist.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **10** ou termos relacionados a ASMR / Sensação: leia `.claude/commands/criativo-estatico/asmr-sensacao.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **11** ou termos relacionados a Meme: leia `.claude/commands/criativo-estatico/meme.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **12** ou termos relacionados a Jogo dos 7 Erros: leia `.claude/commands/criativo-estatico/jogo-7-erros.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **13** ou termos relacionados a Criativo Notícia: leia `.claude/commands/criativo-estatico/criativo-noticia.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **14** ou termos relacionados a Associação Criativa: leia `.claude/commands/criativo-estatico/associacao-criativa.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **15** ou termos relacionados a Criativo História + Quebra de Objeção: leia `.claude/commands/criativo-estatico/criativo-historia.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **16** ou termos relacionados a O Desespero de Quem: leia `.claude/commands/criativo-estatico/desespero-de-quem.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **17** ou termos relacionados a Fofinho: leia `.claude/commands/criativo-estatico/fofinho.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **18** ou termos relacionados a Nunca: leia `.claude/commands/criativo-estatico/nunca.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **19** ou termos relacionados a Sempre: leia `.claude/commands/criativo-estatico/sempre.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **20** ou termos relacionados a Timelapse: leia `.claude/commands/criativo-estatico/timelapse.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **21** ou termos relacionados a UGC Coisas Estranhas: leia `.claude/commands/criativo-estatico/ugc-coisas-estranhas.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **22** ou termos relacionados a Você Merece: leia `.claude/commands/criativo-estatico/voce-merece.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **23** ou termos relacionados a Objetos Estranhos: leia `.claude/commands/criativo-estatico/objetos-estranhos.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.
- **24** ou termos relacionados a Reflexão Editorial: leia `.claude/commands/criativo-estatico/reflexao-editorial.md` com a ferramenta Read e siga o fluxo descrito nesse arquivo.

O contexto do produto ativo (Passo 0) já está carregado. As sub-skills NÃO precisam ler `perfil.md` e `idconsumidor.md` de novo, podem usar o que já foi extraído.

## Regras

- Nunca pular a pergunta de roteamento, exceto quando o aluno mencionou explicitamente o nome do formato na primeira mensagem (atalho do Passo 1).
- As sub-skills herdam todas as regras globais do CLAUDE.md. Light Copy, auto-revisão obrigatória de copy, anúncio de próximo passo, aprovação antes de salvar, acentuação correta em pt_BR.
- O orquestrador NÃO gera copy nem texto de anúncio. Apenas roteia.
- Cada sub-skill tem fluxo próprio. O orquestrador não define perguntas, opções de saída ou regras de geração. Quem define isso é o arquivo da sub-skill.
- Se o aluno escolher um número inválido (fora de 1 a 24), repetir o menu de forma curta sem mostrar a descrição das opções de novo.
- Se a sub-skill terminar e o aluno quiser criar outro criativo de outro formato, retornar a esta skill (`/criativo-estatico`) em vez de chamar a outra sub-skill direto. O Passo 0 garante contexto fresco.

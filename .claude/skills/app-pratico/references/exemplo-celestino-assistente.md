# Segundo Arquétipo. Assistente que Indexa as Aulas (tipo "Celestino")

O caso em `references/exemplo-caso-anterior.md` é uma calculadora: o curso
ensina fórmulas, o app calcula. Mas nem todo curso pratico e assim. Alguns
cursos tem dezenas ou centenas de aulas, e o problema real do aluno nao e
"calcular um numero", e "eu nao sei qual aula resolve a minha situacao"
ou "eu tenho uma duvida especifica e nao sei onde no curso isso e
respondido". Pra esse caso, o arquetipo certo e um assistente
conversacional que conhece o indice do curso inteiro e indica o caminho,
sem substituir a aula.

Este e um caso real (identidade do curso omitida, o que importa aqui e a
mecanica), um curso com mais de cem aulas em video, onde os alunos ficavam
perdidos sobre por onde comecar ou qual aula resolvia o problema especifico
que estavam vivendo naquele momento.

## Diferenca de arquitetura em relacao ao arquetipo padrao

O arquetipo padrao desta skill (calculadora, checklist, conversor) e
sempre um HTML unico, sem nenhuma chamada de rede, sem custo recorrente.
O arquetipo assistente e diferente em 3 pontos, e isso precisa ficar claro
pro aluno antes de escolher esse caminho na Etapa 5:

1. **Tem backend, mas nao tem login nem banco de dados de usuario.** Um
   backend leve (`api/chat.js`, Vercel Edge Function) so faz proxy seguro
   pra uma API de LLM. Isso ainda esta dentro do escopo desta skill,
   diferente da `/app-saas` (que tem Supabase, login, 2 perfis, dados
   persistidos por usuario). O assistente e uma ferramenta compartilhada,
   sem conta de ninguem.
2. **Tem custo recorrente pequeno.** Cada conversa custa uma fracao de
   centavo (modelo de LLM barato via OpenRouter, tipo Gemini Flash). Avise
   o aluno disso antes de construir: para 1.000 conversas por mes, o custo
   fica na casa de poucos reais.
3. **A chave de API do LLM fica em variavel de ambiente no painel da
   Vercel**, nunca no codigo do frontend nem no `.env` local (o `.env`
   local so importa se voce testar em maquina, o que vale mesmo e a
   variavel configurada no projeto Vercel).

## Arquitetura

```
app-assistente/
├── public/
│   ├── index.html       chat UI, cores do curso
│   ├── app.js            busca local (client-side) + chamada pro backend
│   └── data/
│       └── aulas-index.json   uma entrada por aula, com tags
├── api/
│   └── chat.js            Vercel Edge Function, proxy seguro pro LLM
└── vercel.json             config de deploy
```

### Passo 1. Indexar as aulas

Diferente do arquetipo calculadora (que le so as aulas relevantes pro
calculo escolhido), o arquetipo assistente precisa de um indice de TODAS
as aulas do curso. Para cada aula, monte uma entrada com: id, titulo,
tipo (aula ou estudo de caso), resumo em 1 linha, resumo completo (com
numeros, prazos e situacoes cobertas, que e o que permite o assistente
justificar a recomendacao com evidencia concreta), tags/frameworks do
curso, palavras-chave, e link do video quando houver.

### Passo 2. Busca local antes de chamar o LLM

O frontend faz uma busca simples (BM25 + sobreposicao de tags, com lista
de sinonimos do nicho) inteiramente no navegador, sem gastar chamada de
API, e manda so as 10 a 15 aulas mais candidatas pro backend. Isso reduz
custo e melhora a precisao (o LLM so escolhe entre poucas opcoes ja
filtradas, nunca inventa aula fora da lista).

### Passo 3. System prompt com regra dura de nao inventar

O assistente so pode recomendar aulas que vieram na lista de candidatas.
Se a duvida do aluno nao bate com nenhuma candidata com confianca, ele
precisa dizer isso com honestidade em vez de forcar uma recomendacao
fraca. Cada recomendacao cita uma evidencia concreta do resumo completo da
aula (um numero, um prazo, uma situacao), nunca uma justificativa generica
tipo "essa aula cobre esse tema".

### Passo 4. Protocolo de entrevista curto

Se o aluno chega com uma pergunta vaga, o assistente pergunta 1 ou 2
coisas por vez (nunca uma lista de perguntas de uma vez), prioriza os
dados que mais diferenciam qual aula recomendar, e assim que tiver
contexto suficiente ja entrega a recomendacao, sem entrevistar a toa.

## Quando escolher este arquetipo em vez do padrao

- O curso tem muitas aulas (tipicamente 20 ou mais) e cobre situacoes
  variadas, nao um unico calculo linear.
- O problema real do aluno e navegacional ("por onde eu comeco", "qual
  aula resolve isso") mais do que computacional ("quanto isso da").
- O aluno topa o custo recorrente pequeno e a etapa extra de configurar a
  chave de API no painel da Vercel.

Se o curso ensina um metodo com formulas e numeros claros (como no caso da
calculadora), o arquetipo padrao continua sendo o caminho mais simples,
mais barato e mais rapido de construir e validar.

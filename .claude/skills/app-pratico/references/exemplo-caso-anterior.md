# Estudo de Caso. Um App Construido com Este Processo

Este e um caso real, ja publicado, que segue exatamente o processo desta
skill (identidade do curso omitida de proposito, o que importa aqui e a
mecanica, nao o negocio especifico).

## Ponto de partida

Um curso tecnico com 25 aulas em video, cada uma ensinando um calculo ou
conceito especifico do metodo do curso (indicadores de desempenho, custo e
resultado, no caso original). As aulas estavam no YouTube, nao listadas.

## Passo 1. Transcricao

Cada aula foi processada com o mesmo script que esta skill usa
(`scripts/cortes_transcrever.py`), gerando um `.txt` por aula em
`referencia-aulas/aula-{NN}-{tema}.txt` mais um `INDICE.md` com a lista
completa. Nenhum video foi baixado, so a legenda automatica.

## Passo 2. Mapeamento

Ao ler as 25 aulas, ficou claro que os calculos se agrupavam naturalmente
em 3 blocos logicos (desempenho, custo e resultado final), e que varios
calculos dependiam do resultado de outro calculo anterior (ex: o custo por
unidade produzida dependia do resultado de 3 outros calculos).

## Passo 3. Ideia escolhida

Uma unica calculadora com 3 paineis (um por bloco), em vez de 3 apps
separados. Cada painel reunia os calculos daquele bloco, com um botao
"puxar resultado" nos campos que dependiam de um calculo anterior, evitando
o aluno ter que redigitar o mesmo numero varias vezes.

## Passo 4 e 5. Construcao

- Arquivo HTML unico, mobile-first, calculo ao vivo (sem botao "calcular").
- Cada resultado aparecia em destaque, com a interpretacao do numero (por
  exemplo "otimo", "investigar" ou "prejuizo", conforme os parametros de
  referencia ensinados nas proprias aulas), nao so o valor cru.
- Onde a aula ensinava um metodo "estimado" e um "real" para o mesmo
  indicador (ex: consumo estimado antes de comprar vs. consumo real depois
  de medir), o app trouxe os dois modos lado a lado.
- Trava de senha simples: hash SHA-256 gravado no codigo, checagem contra
  `localStorage`, senha unica distribuida aos alunos compradores. Documentado
  como uma medida contra compartilhamento casual, nao seguranca forte (para
  isso, o caminho seria codigo individual por aluno com validacao no
  servidor, fora do escopo de um app estatico).

## Passo 6. Validacao

Antes de publicar, cada formula foi conferida contra os exemplos numericos
que o proprio curso usava para ensinar (ex: "peso foi de 330 para 430 kg em
150 dias" deveria dar exatamente o resultado que o professor calculou na
aula). Todas bateram. Essa etapa pegou, durante o processo, um pequeno erro
de arredondamento numa das formulas antes de publicar.

## Passo 9. Publicacao

Publicado na Vercel via API (mesmo mecanismo do `/pagina-vercel`), com
dominio proprio apontado depois via CNAME. O link do app nunca foi exposto
na pagina de vendas publica, so repassado a quem comprou.

## Licao principal para aplicar em outro curso

O trabalho pesado nao e a construcao do HTML, e a leitura completa e fiel
das aulas: toda formula, todo limite de referencia e toda interpretacao de
resultado tem que vir literalmente do que o curso ensina. Um app bonito com
formula errada ou inventada destroi a confianca do aluno no curso inteiro.

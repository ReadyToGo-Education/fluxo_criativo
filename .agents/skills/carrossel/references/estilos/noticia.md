# Estilo. Carrossel "Notícia"

> Carrossel que pega uma NOTÍCIA TEMPORAL (acontecimentos dos últimos 7 dias) do nicho e transforma em narrativa de revista de 7 a 9 slides com prompts visuais em 3 modos.
> Este estilo **delega o prompt-base** para `references/prompt-noticia.md`. O prompt é executado EXATAMENTE como está, sem reescrita. A única adaptação permitida é pré-preencher a Etapa 1 com dados do produto ativo.
> A âncora é o calendário (frescor obrigatório). Para curiosidades atemporais, use a opção 8 (Curiosidade) do menu.

---

## Coleta do Passo 1

O fluxo de coleta da Notícia **ignora** o `passo-coleta-base.md` padrão. A coleta é a Etapa 1 do `prompt-noticia.md` (3 perguntas):

### 1.1. @ do Instagram
Se `.env` tiver `IG_USER` ou `perfil.md` tiver handle, pré-preencha como sugestão.

### 1.2. Nicho
Se `perfil.md` tiver nicho, pré-preencha como sugestão.

### 1.3. Produto
Se `perfil.md` tiver Quadro/formato/público, pré-preencha como sugestão.

> Tema e tom NÃO são coletados aqui. Tema é escolhido na Etapa 3 do prompt (depois da busca na web); tom na Etapa 4. No modo "Gerar todos", veja a regra abaixo.

---

## Passo 2. Execução

A skill `/carrossel` no estilo Notícia faz o seguinte:

1. **Carrega** `references/prompt-noticia.md` inteiro.
2. **Executa a Etapa 1** (coleta de @, nicho, produto), uma pergunta por turno, com pré-preenchimento de sugestão a partir do `perfil.md`/`.env`.
3. Passa pela **confirmação consolidada** (Passo 2.5 da SKILL.md).
4. **Executa o prompt da Etapa 2 à Etapa 7 exatamente como está**, na sessão atual:
   - Etapa 2: busca de 5 notícias trend dos últimos 7 dias via `WebSearch`.
   - Etapa 3: aluno escolhe 1 das 5.
   - Etapa 4: aluno escolhe o tom (7 opções).
   - Etapa 5: escreve os 7 a 9 slides.
   - Etapa 6: gate de aprovação do texto.
   - Etapa 7: prompts visuais nos 3 modos + arquivo consolidado.
5. A data para o nome do arquivo consolidado é calculada via `Bash` com `Get-Date -Format "yyyy-MM-dd"` (PowerShell).
6. O texto dos slides passa pelo **Manual da Copy + revisora** de forma silenciosa antes de ser exibido na Etapa 6. As regras de copy do prompt (sem travessão, sem exclamação, sem pergunta na capa) já estão alinhadas com o Manual.

> **Diferença para o `/programar-carrossel-noticia`:** aquela skill (agendamento) usa um arquivo separado (`programar-carrossel-noticia/references/prompt-carrossel-noticia.md`) com placeholders e configurações de categoria/modo/tom para o modo Routine. O `/carrossel` opção 7 (geração imediata) usa o `prompt-noticia.md` interativo que está aqui.

---

## Diferenças importantes em relação aos 6 estilos clássicos

| Aspecto | 6 estilos clássicos | Notícia |
|---|---|---|
| Número de slides | 6 fixos | 7 a 9 (variável) |
| Estrutura do slide 1 | Frase começando com "Nunca/Sempre/..." | Capa com o FATO em até 8 palavras + subtítulo curto opcional |
| Slide N (último) | CTA criativa | CTA fixo: "Todos os dias, conteúdo sobre [nicho] aqui no @[handle]. Me segue para receber a próxima." |
| Prompts visuais | Template único 4:5 dois blocos | 3 modos (foto real composta, DALL-E ilustrativo, composição limpa) |
| Coleta extra | 5 dados (@, nicho, paleta, tom, estilo de design) | @, nicho, produto (Etapa 1) + tema (Etapa 3) + tom (Etapa 4) |
| Dependência externa | Não | `WebSearch` (busca real de notícias trend) |
| Frescor | Atemporal | Obrigatório: últimos 7 dias |
| Arquivo consolidado | Não | `carrossel-noticia-[slug]-[data].txt` com delimitadores `=== SLIDE N ===` |

---

## Modo "Gerar todos"

No fluxo "Gerar todos" (Passo 2 da SKILL.md, ramo `todos`), Notícia roda com **escolha automática de tema**, igual à Curiosidade e ao Editorial:

- A skill executa a Etapa 2 (busca das 5 notícias) e, em vez de perguntar, **seleciona automaticamente a notícia mais quente** das 5 (mais recente + maior potencial de gancho).
- O tom usado é o coletado no Passo 2.B da SKILL.md (`noticia_tom`).
- O restante do prompt (Etapas 5 a 7) roda normalmente.
- **Se nenhuma notícia dos últimos 7 dias existir**, a Notícia desse lote é PULADA com aviso no log do batch (o lote continua sem ela).

---

## Saída no projeto

Pasta de saída:

```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-noticia/
```

Arquivos gerados:
- `texto.md` (slides 1 a N, já aprovados)
- `carrossel-noticia-[slug]-[data].txt` (arquivo consolidado da Etapa 7, Parte B, com os prompts visuais delimitados)

> A legenda do Instagram para a Notícia já vem embutida no slide N (CTA fixo). Não há `legenda.txt` separado.

---

## Paleta

Sem paleta default rígida. A paleta vem das regras do prompt (3 cores hex consistentes entre todos os slides, tipografia serif editorial, sem ícones nem emoji).

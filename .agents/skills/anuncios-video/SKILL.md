---
name: anuncios-video
description: >
  Base de conhecimento para criacao de anuncios em video (Reels, Stories, YouTube Ads).
  Inclui estrutura de roteiro, formatos, timings, direcao criativa e especificacoes
  tecnicas para video ads. Focado em criativos que usam movimento e audio.
---

# Anuncios em Video. Base de Conhecimento

Criativos em video: Reels, Stories, YouTube Ads, UGC. Para anuncios estaticos (imagem + copy), consulte a skill `anuncios-texto`.

## Quando Usar Esta Skill

- Anuncios em formato Reels (Instagram/TikTok)
- Anuncios de Stories em video
- YouTube Ads (pre-roll, bumper)
- Videos UGC (User Generated Content)
- Anuncios com avatar IA (HeyGen)
- Videos com cenas reais (stock footage ou filmagem propria)
- Videos de motion/animacao (Remotion, CapCut, Canva)
- Videos hibridos (avatar + b-roll intercalado)
- Qualquer anuncio que envolva MOVIMENTO e/ou AUDIO

## Tres Caminhos de Execucao

Todo video ad pode ser executado de tres formas distintas:

**Caminho 1 — Geracao via API (HeyGen)**
Requer `HEYGEN_API_KEY`, `HEYGEN_AVATAR_ID` e `HEYGEN_VOICE_ID` no `.env`.
O sistema gera o roteiro e, apos aprovacao, envia automaticamente para o HeyGen.
Ideal para: Avatar IA simples e Hibrido (avatar + b-roll).

**Caminho 2 — Roteiro para gravacao propria**
O sistema gera o roteiro completo com timecodes e notas de edicao.
O usuario grava com o celular ou edita com stock footage.
Ideal para: Reels, YouTube, Cenas Reais, UGC.

**Caminho 3 — Direcao criativa para editor**
O sistema entrega: roteiro + shot list + paleta HEX + sugestao de musica + referencias visuais por cena + instrucoes de montagem.
Ideal para: producoes mais elaboradas, producoes terceirizadas, Motion/Remotion.

## Os 18 Tipos de Anuncios VTSD (Aplicados a Video)

Lista canonica (mesma da Mandala da Criatividade):
1. Comparacao, 2. Problema/Solucao, 3. Explicacao, 4. Curiosidade, 5. Reflexao,
6. Certo/Errado, 7. Demonstracao, 8. Procedimento, 9. Impacto Visual, 10. Oportunidade,
11. Historia, 12. Prova Social, 13. Clickbait, 14. Sensacao, 15. Contraste,
16. Ensino, 17. Revelacao, 18. Dilema

**Os que mais performam em video (ordem de eficacia):**
1. **Demonstracao**. Mostre o produto/metodo funcionando ao vivo
2. **Historia**. Narrativa pessoal com arco emocional
3. **Prova Social**. Depoimento em video, resultado filmado
4. **Problema/Solucao**. Comece pelo problema, mostre a virada
5. **Certo/Errado**. Demonstre os dois caminhos
6. **Curiosidade**. Comece com gancho e revele ao longo do video
7. **Explicacao**. Tutorial rapido, passo a passo visual
8. **Revelacao**. Comece com a crenca errada, quebre com prova
9. **Comparacao**. Antes e depois com transicao visual

## Aplicação interna de Elementos Literários (OBRIGATÓRIO. não exibir ao usuário)

Depois que o tipo da Mandala estiver definido e ANTES de gerar o roteiro, acionar internamente a skill `elementos-literarios` e escolher de **1 a 3 elementos** que mais combinarem com o tipo de video, com o perfil do consumidor e com o tom do produto.

Regras:
- Esse processo é silencioso. **Não mencionar ao usuário** quais elementos foram escolhidos, nem que a skill foi consultada.
- Os 1 a 3 elementos selecionados devem ser efetivamente aplicados no roteiro gerado (gancho, desenvolvimento, regancho ou CTA), não apenas listados.
- A escolha precisa fazer sentido com o tipo da Mandala (ex.: Historia combina com setup/punchline; Demonstracao combina com triade comica; Revelacao combina com antitese; Curiosidade combina com neologismo).
- Continuar respeitando todas as proibicoes de Light Copy.
- Nao exibir rotulos como "elemento usado: X" no entregavel final.

## Estrutura de Roteiro para Video Ad

### Formato Reels/Stories (15-60 segundos)

**Estrutura padrao (3 blocos):**

**Bloco 1. Gancho (0-3 segundos)**
- Premissa forte que para o scroll. afirmacao NAO OBVIA para quem ja esta no nicho
- ❌ NUNCA usar pergunta no gancho (regra VTSD)
- ❌ NUNCA usar premissa obvia ("aprender X e dificil")
- Texto na tela reforçando o gancho
- Movimento ou mudanca visual imediata

**Exemplos de gancho ERRADO:**
- "Voce ja sentiu dificuldade de..." ❌ (pergunta)
- "Aprender [nicho] e dificil." ❌ (obvio)

**Exemplos de gancho CERTO:**
- "A pessoa que mais trava raramente e a que sabe menos." ✓
- "O caminho mais rapido para travar e estudar da forma que todo mundo ensina." ✓

**Bloco 2 — Desenvolvimento (3-45 segundos)**
- Minimo 2 blocos de conteudo distinto: o primeiro aprofunda o argumento do gancho, o segundo traz a virada, o insight ou a solucao concreta
- Conte a historia, mostre o problema, apresente a solucao
- Cada bloco deve entregar valor real — ensinar algo especifico, revelar um dado ou detalhar um mecanismo. Nao apenas prometer
- Mantenha ritmo rapido (cortes a cada 3-5 segundos)
- Use texto na tela para reforcar pontos-chave
- Mantenha o suspense ate o final

**Bloco 3. CTA (ultimos 5-10 segundos)**
- CTA direto e claro
- Texto na tela com a acao
- Urgencia se aplicavel

### Formato Descoberta + Video (estrutura obrigatoria)

Videos de Descoberta devem **entregar conteudo real** dentro do proprio video. ensinar uma tecnica, dar um insight, entregar valor concreto. ERRADO: video que so promete ("me segue que eu te mostro"). CERTO: video que ensina algo e o CTA vem como convite natural.

```
[0-2s]   GANCHO      → Afirmacao contra-intuitiva. Texto na tela + fala simultaneos.
[3-5s]   TEASE       → Uma frase que expande o gancho e retem.
[6-25s]  ENTREGA     → Ensina a tecnica ou da o insight real. Especifico, concreto.
[26-30s] REGANCHO    → Texto na tela sintetizando a ideia central.
[31-35s] CTA         → Convite leve para seguir. Sem urgencia forcada.
```

Tamanho alvo: ~130 palavras por roteiro (~35-45 segundos de fala natural). Calibrar a partir dos virais encontrados na pesquisa.

### Formato YouTube Pre-Roll (15-30 segundos)

**Estrutura (nao pulavel em 5s):**
- 0-5s: Gancho FORTE (o espectador decide se pula aqui)
- 5-20s: Proposta de valor + prova rapida
- 20-30s: CTA com link/acao

### Formato UGC (User Generated Content)

**Estrutura natural (30-60 segundos):**
- Parece conteudo organico, nao anuncio
- Pessoa real falando para camera
- Iluminacao natural, cenario do dia a dia
- Linguagem informal e espontanea
- Depoimento genuino sobre experiencia

### Formato Avatar IA (HeyGen)

**Estrutura (60-90 segundos):**
- Frases curtas (max 15 palavras)
- Linguagem natural e pausada
- Indicacoes entre colchetes: [sorriso], [pausa], [enfase]
- Formato vertical (1080x1920) para Reels/Stories
- Fundo limpo e profissional

## Especificacoes Tecnicas

### Meta Ads (Reels/Stories)

| Especificacao | Valor |
| --- | --- |
| Dimensao | 1080x1920 (vertical 9:16) |
| Duracao Reels | 15-60 segundos |
| Duracao Stories | 15 segundos por card |
| Formato arquivo | MP4, MOV |
| Tamanho maximo | 4GB |
| Resolucao minima | 720p |
| Taxa de quadros | 30fps minimo |

### YouTube Ads

| Especificacao | Valor |
| --- | --- |
| Dimensao | 1920x1080 (horizontal 16:9) |
| Bumper Ad | 6 segundos (nao pulavel) |
| Pre-Roll pulavel | 15-30 segundos |
| Pre-Roll nao pulavel | 15 segundos |
| Formato | MP4 |

### TikTok Ads

| Especificacao | Valor |
| --- | --- |
| Dimensao | 1080x1920 (vertical 9:16) |
| Duracao | 15-60 segundos (ideal: 21-34s) |
| Formato | MP4, MOV |
| Com legenda | Obrigatorio (muitos assistem sem som) |

## Direcao Criativa para Video

### Gancho Visual (primeiros 3 segundos)
Tecnicas que param o scroll:
- Movimento inesperado (zoom rapido, transicao brusca)
- Texto grande e bold na tela
- Rosto proximo da camera com expressao forte
- Objeto caindo, quebrando, aparecendo
- Antes/depois com transicao instantanea

### Ritmo de Edicao
- Corte a cada 3-5 segundos (manter atencao)
- Texto na tela acompanhando a fala
- Musica de fundo energetica (sem abafar a voz)
- Zoom ins nos momentos de enfase
- B-roll intercalado com talking head

### Legendas e Texto
- SEMPRE incluir legendas (85% dos videos sao assistidos sem som)
- Fonte grande e legivel (minimo 40pt)
- Contraste forte (texto branco com sombra preta)
- Posicao: centro ou terco inferior

### Audio
- Voz clara e com energia
- Musica de fundo: 20-30% do volume da voz
- Efeitos sonoros nos cortes e transicoes
- Silencio estrategico antes de ponto importante

## Checklist de Video Ad

Antes de publicar, verifique:
- [ ] Gancho nos primeiros 3 segundos?
- [ ] Texto na tela reforça a mensagem?
- [ ] Legendas incluidas?
- [ ] CTA claro no final?
- [ ] Formato vertical (9:16) para Reels/Stories?
- [ ] Duracao adequada ao formato?
- [ ] Copy segue regras Light Copy (sem pontos de exclamacao, sem perguntas no gancho)?
- [ ] Audio limpo e audivel?

## Regras de Estilo de Copy para Video

**Vícios proibidos (Light Copy):**
- Ponto de exclamação: nunca usar.
- Perguntas no gancho: nunca usar.
- "Mesmo que" / "sem precisar" como muletas: nunca usar.
- Promessas vagas: nunca usar.
- Travessão longo (. ): nunca usar no roteiro. Substituir por vírgula, ponto ou pausa [pausa].
- Estrutura "Não é X. É Y.": nunca usar. Reformular de forma mais elaborada.
- Emojis: nunca usar.
- Frases genéricas: "Transforme sua vida", "Descubra o segredo", "Método revolucionário."
- Especificidade: usar números concretos, situações reais. "10 alunos em 30 dias" > "crescimento rápido".

**Checklist obrigatório. revisar antes de entregar qualquer roteiro:**

Antes de entregar, revise e substitua:
- Travessão (. ) → reescreva a frase sem ele
- Estrutura "Não é X. É Y." → desenvolva o argumento de outra forma
- Frases genéricas de vendedor → substitua por dado ou situação concreta
- Menção ao produto nos primeiros blocos → remova ou reescreva focando no leitor
- Emojis → remova sem substituição
- Desenvolvimento com menos de 2 blocos de conteúdo distinto → expanda com insight ou mecanismo concreto

- [ ] Nenhum travessão no texto
- [ ] Nenhuma estrutura "Não é X. É Y."
- [ ] Nenhuma frase genérica de vendedor
- [ ] Desenvolvimento tem mínimo 2 blocos de conteúdo com valor real entregado

**Princípio central:**
O roteiro não vende. Ele ensina, avisa ou revela. O produto não aparece nos primeiros blocos.
Quem assiste até o fim aprende algo concreto. não apenas fica curioso sobre um produto.

**Nomear cria realidade:**
Quando possível, dar nome próprio ao conceito ensinado no vídeo ("Método da Inversão", "Gatilho da Especificidade"). Nomes próprios criam autoridade sem exagero.

## CTAs por Objetivo (Mandala da Criatividade)

| Objetivo | Definicao | CTA em Video |
| --- | --- | --- |
| Descoberta | Atrair novas pessoas que ainda nao conhecem | "Me segue para mais" / "Salva esse video" |
| Relacionamento | Criar conexao com quem ja segue | "Comenta aqui" / "Marca alguem" / "Compartilha" |
| Conversao | Vender | "Link na bio" / "Clica no botao" / "Garante sua vaga" |
| RMKT | Converter quem ja viu a pagina | "Ultimas vagas" / "So ate amanha" / "Garanta agora" |

## Pesquisa de Tendencias (OBRIGATORIA antes de gerar)

Antes de escrever qualquer video ad, fazer 2 buscas na web:

**Busca 1. formato video:**
- `reels instagram virais [mes e ano atual]`
- `tiktok trends [mes e ano atual]`

Extrair: estrutura dos 3 primeiros segundos, duracao ideal, estilo de edicao, tom predominante, padrao de CTA.

**Busca 2. objetivo especifico:**
- Descoberta: `conteudo que vira seguidor instagram [mes e ano atual]`
- Relacionamento: `conteudo que gera comentarios instagram [mes e ano atual]`
- Conversao: `anuncio que converte instagram infoproduto [mes e ano atual]`
- RMKT: `remarketing anuncio instagram copy [mes e ano atual]`

Calibrar com o encontrado: gancho, estilo de edicao, tom, CTA.
**Fazer essa pesquisa a cada geracao. nao reutilizar pesquisa anterior.**

## Geracao Automatica de Video (HeyGen Avatar IA)

O comando `/copy-anuncio` gera o roteiro e, se configurado, cria o video automaticamente via HeyGen.

### Configuracao necessaria no `.env`

```
HEYGEN_API_KEY=sua_chave_aqui
HEYGEN_AVATAR_ID=id_do_avatar_aqui
HEYGEN_VOICE_ID=id_da_voz_aqui
```

Para obter esses valores:
- **HEYGEN_API_KEY**: painel HeyGen > Account > API
- **HEYGEN_AVATAR_ID**: painel HeyGen > Avatars > selecionar avatar > copiar ID
- **HEYGEN_VOICE_ID**: painel HeyGen > Voices > selecionar voz em português > copiar ID

### Fluxo de geracao

1. Roteiro aprovado → formatar como texto corrido (sem marcacoes de cena)
2. POST `/v2/video/generate` com avatar + voz + roteiro
3. Polling no `/v1/video_status.get?video_id=ID` a cada 30s ate status `completed`
4. Download do `video_url` → salvar como `.mp4` na pasta de entregas

### Formatacao do roteiro para HeyGen

O campo `input_text` deve conter apenas o texto que o avatar vai falar. sem colchetes de cena, sem indicacoes de edicao, sem marcacoes de tempo. Exemplo:

```
O aluno que mais trava raramente e o que sabe menos. Isso acontece porque ele aprendeu a decorar conteudo antes de aprender a aplicar. O metodo nao e um manual. E uma pratica. E praticas nao se decoram, se executam. Se voce quer parar de travar, comeca pela execucao. nao pelo estudo. Me segue para o proximo passo.
```

### Especificacoes de saida

- Dimensao: 1080x1920 (vertical 9:16). formato Reels/Stories
- Formato: MP4
- Avatar: falando para camera, fundo limpo
- Legendas: ativar no proprio HeyGen ou adicionar no editor de video

## Formatos de Video Suportados

| Formato | Descricao | Caminho Ideal |
|---|---|---|
| **Avatar IA simples** | Avatar falando direto para camera, fundo limpo | Caminho 1 (API HeyGen) |
| **Avatar + voz customizada** | Avatar com voz clonada ou ajustada no HeyGen | Caminho 1 (API HeyGen) |
| **Reels gravado** | Pessoa real ou roteiro para camera propria | Caminho 2 |
| **UGC** | Estilo organico, pessoa real, iluminacao natural | Caminho 2 |
| **Cenas reais + stock** | Narrativa com imagens/clips de stock footage | Caminho 2 ou 3 |
| **Motion / Animacao** | Remotion, CapCut, Canva animado | Caminho 3 |
| **Hibrido** | Avatar + b-roll intercalado | Caminho 1 ou 3 |
| **YouTube Pre-Roll** | 15-30s, gancho forte nos 5 primeiros segundos | Caminho 2 ou 3 |

## Estruturas de Roteiro Baseadas em Virais 2026

| Estrutura | Quando Usar | Logica de Retencao |
|---|---|---|
| **Loop Perfeito** | Revelacao, insights | Final conecta ao gancho, incentiva replay |
| **Tutorial de 3 Passos** | Procedimento, ensino | Cada passo avanca a narrativa ate o fim |
| **Quebra-Padrao** | Contraste, paradoxo | Abertura inesperada, forca pausa no scroll |

Usar estruturas diferentes nas 3 variacoes sempre que possivel.

## Boas Praticas Atuais

- **UGC** (conteudo gerado por usuario) tem maior CTR que producoes profissionais
- **Depoimentos em video** convertem mais que texto
- **Formato vertical** e obrigatorio (80%+ do consumo e mobile)
- **Primeiros 3 segundos** definem se o anuncio funciona
- **Legendas** sao obrigatorias (nao opcionais)
- **Avatar IA** funciona bem para escala rapida de criativos
- **Conteudo entregado dentro do video** performa mais que teaser que promete sem entregar
- **Hibrido avatar + b-roll** aumenta retencao em relacao ao avatar estatico simples

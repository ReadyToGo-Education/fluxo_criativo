# Estilo. Carrossel "Notícia"

> Carrossel que pega uma notícia (da semana, Trend) ou uma curiosidade (Atemporal) do nicho e transforma em narrativa de 7 a 9 slides.
> Este estilo **delega o prompt-base** para a skill `programar-carrossel-noticia` (que já existe no projeto). A diferença é: lá o prompt vai pra Routine na nuvem. Aqui, executa no chat do Claude Code agora.

---

## Coleta extra do Passo 1

O fluxo de coleta da Notícia é **mais simples** que os outros 6 estilos. Ignore o `passo-coleta-base.md` padrão. Use este:

### 1.1. @ do Instagram
Igual ao passo-coleta-base.md.

### 1.2. Nicho e produto em uma frase
Igual ao passo-coleta-base.md.

### 1.3. Categoria de notícia

```
Qual categoria de notícia você quer?

1. Trend (notícia da semana, últimos 7 dias)
2. Atemporal (curiosidade ou fato chocante sem prazo)
3. Mista (3 Trend + 3 Atemporais, você escolhe depois)

Digite o número.
```

Salve como `categoria_noticia` (`TREND`, `ATEMPORAL` ou `MISTA`).

### 1.4. Modo de escolha

```
Como você quer escolher a notícia que vai virar carrossel?

1. Eu escolho entre as 6 ideias que você me apresentar
2. Aleatório (você escolhe a mais quente entre as 6)

Digite o número.
```

Salve como `modo` (`MANUAL` ou `ALEATORIO`).

### 1.5. Tom do carrossel

```
Qual tom você quer no carrossel?

1. Enérgico (motivação, ritmo rápido)
2. Polêmico (provocador, defende tese forte)
3. Engraçado (ironia, leve)
4. Reflexivo (pausado, filosófico)
5. Didático (explicador, professor)
6. Jornalístico (apurado, sóbrio, foco no fato)
7. Confessional (primeira pessoa, vulnerável)
8. Aleatório (você escolhe o mais adequado à notícia escolhida)

Digite o número.
```

Salve como `tom_noticia`.

---

## Passo 2. Execução

A skill `/carrossel` no estilo Notícia faz o seguinte:

1. **Lê o prompt-base** em `.claude/skills/programar-carrossel-noticia/references/prompt-carrossel-noticia.md` e monta o prompt final concatenando:
   - **Bloco A** (cabeçalho fixo com handle, nicho, produto, data de hoje)
   - **Bloco B** (busca de 6 notícias, sempre executa)
   - Se `modo == MANUAL`: para aqui, mostra as 6 ideias, espera o aluno escolher uma + tom (se `tom_noticia == 8`).
   - Se `modo == ALEATORIO`: continua para **Bloco C-CARROSSEL.1** (seleção automática) + **C-CARROSSEL.2** (escrita do carrossel) + **C-CARROSSEL.3** (prompts visuais) + **C-CARROSSEL.4** (arquivo consolidado).

2. **Substitui os placeholders** do prompt-base com os valores coletados:
   - `{{HANDLE}}` → `handle`
   - `{{NICHO}}` → `nicho_produto` (parte do nicho)
   - `{{PRODUTO}}` → `nicho_produto` (parte do produto)
   - `{{DATA_HOJE_REF}}` → data atual (a skill calcula via `Get-Date` em PowerShell antes de injetar)
   - `{{ESCOPO}}` → `CARROSSEL_INTEIRO` (sempre, porque é geração imediata)
   - `{{MODO}}` → `ALEATORIO` ou `FIXO`
   - `{{CATEGORIA_FIXA}}` → `TREND`, `ATEMPORAL` ou `LIVRE` (se MISTA)
   - `{{TOM_FIXO}}` → nome do tom (Enérgico, Polêmico, etc.) ou `LIVRE`

3. **Executa o prompt** dentro da sessão atual (não dispara pra Routine). Usa `WebSearch` para buscar as 6 notícias e gera o carrossel.

---

## Diferenças importantes em relação aos 6 estilos atemporais

O carrossel Notícia tem **estrutura interna diferente** dos outros 6:

| Aspecto | 6 estilos atemporais | Notícia |
|---|---|---|
| Número de slides | 6 fixos | 7 a 9 (variável) |
| Estrutura do slide 1 | Frase começando com "Nunca/Sempre/..." | Capa com o FATO em até 8 palavras |
| Slide N (último) | CTA criativa | CTA fixo: "Todos os dias, conteudo sobre {{NICHO}} aqui no {{HANDLE}}. Me segue para receber a proxima." |
| Prompts visuais | Template único 4:5 dois blocos | 3 modos (foto real composta, DALL-E, composição limpa) |
| Saída no projeto | `meus-produtos/{ativo}/entregas/conteudo-social/carrossel-noticia/` + texto + prompts + legenda | Mesma pasta, mas com formato consolidado do prompt-carrossel-noticia |
| Coleta extra | Sem Desejo, sem Objetivo | Categoria + Modo + Tom |
| Dependência externa | Não | WebSearch (busca real de notícias) |

---

## Passo 3 e Passo 4

A skill **NÃO usa** o `passo-output-triplo.md` nem o `passo-legenda.md` padrão para o estilo Notícia, porque o prompt-carrossel-noticia já tem `ETAPA 4` (prompts visuais) e `ETAPA 5` (arquivo consolidado) próprios.

A legenda do Instagram para o carrossel Notícia já vem embutida no slide N (CTA fixo). Se o aluno quiser uma legenda mais elaborada, ele pode rodar a skill `revisora` separadamente em cima do texto do slide N.

Pasta de saída:

```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-noticia/
```

Arquivos gerados:
- `texto.md` (slides 1 a N)
- `prompts.txt` (prompts visuais por slide, formato do `ETAPA 5` do prompt-carrossel-noticia)
- `legenda.txt` (opcional, se o aluno quiser uma legenda separada do slide CTA final)

---

## Paleta

Sem paleta default rígida. A paleta é determinada pelo aluno ou pelo modo MISTA. Use:
- 3 cores em hex consistentes entre os 7 a 9 slides
- Tipografia serif editorial
- Sem ícones, formas geométricas decorativas ou emoji na arte

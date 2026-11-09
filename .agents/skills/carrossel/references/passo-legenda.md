# Passo de Geração de Legenda (compartilhado)

> Passo 5 do fluxo. Roda depois da entrega dos prompts de imagem (Passo 4).
> Fluxo único: a legenda é gerada localmente pela skill aplicando o Manual da Copy e a revisora, independente do caminho escolhido para gerar as imagens (manual, Chrome ou API). Isso garante alinhamento com o tom do produto e elimina round-trip desnecessário.

---

## 4.1. Regras obrigatórias (Manual da Copy)

Carregue `.claude/skills/revisora/references/manual-copy.md` na cabeça antes de escrever a legenda. Em particular:

**Bloco A. Vícios absolutos (zero tolerância):**
- Zero travessões (—).
- Zero pontos de exclamação.
- Zero "Não é X. É Y.".
- Zero perguntas no gancho ou primeira linha.
- Zero "mesmo que" ou "sem precisar" como muleta.
- Zero emojis.
- Nome do produto, curso, método ou sigla ausente das primeiras linhas.

**Princípios:**
- **1. Ensinar em vez de prometer.** A legenda entrega aprendizado, não promessa vaga.
- **5. Especificidade.** Número, prazo, cenário ou detalhe concreto. Zero generalização.
- **8. Argumentar.** Toda afirmação tem mecanismo, comparação antes/depois ou explicação do porquê.
- **11. Dor real.** Mira a dor real do público, não a superficial.

**Tese obrigatória:** a legenda explica POR QUE o que está no carrossel é verdade. Não repete os slides.

---

## 4.2. Estrutura da legenda

1. **Gancho (1 a 2 linhas).** Afirmação concreta que abre o tema sem repetir o slide 1 do carrossel. Sem pergunta. Sem nome de produto.
2. **Desenvolvimento (3 a 6 linhas).** Argumenta o ponto central com mecanismo, comparação antes/depois ou exemplo concreto. Traz informação que NÃO está nos slides.
3. **Pico de tensão (1 a 2 linhas).** Nomeia o problema real e a causa que ninguém mais diz.
4. **Virada (1 a 2 linhas).** Apresenta o caminho de saída de forma direta, sem rodeio.
5. **Ponte para o carrossel (1 linha).** Indica que o conteúdo prático está nos slides.
6. **CTA final (1 linha).** Chamada para seguir o @ + ação (salvar, comentar ou compartilhar) conectada com o tema. Sem exclamação.
7. **Hashtags (opcional, até 5).** Relevantes ao nicho, no final, separadas por espaço, em uma linha única.

---

## 4.3. Tom da legenda

Mesmo tom definido no Passo 1 da coleta (`tom_texto`). A legenda é continuação natural do carrossel, não resumo.

Exemplos de adaptação:
- Tom clássico/profissional. Direto, elegante, frase curta.
- Bem-humorado. Trocadilho, ironia, observação do absurdo.
- Técnico. Dados, mecanismos, comparações numéricas.
- Inspiracional. Aspiracional, mas com fato concreto.
- Casual. Conversa de amigo, vocabulário do dia a dia.
- Polêmico. Provocação direta, take forte.

---

## 4.4. Tamanho

Entre **600 e 1200 caracteres** (sem contar hashtags). Garantir que o CTA caia ANTES do "...mais" do Instagram cortar (geralmente cerca de 125 caracteres no preview, então o gancho precisa ser potente nas primeiras linhas).

---

## 4.5. Aplicar a revisora

**Antes de exibir ao aluno**, acione a skill `revisora` passando o texto da legenda. A revisora:
1. Aplica Bloco A (correção automática silenciosa).
2. Aplica Bloco B (correção + alertas).
3. Aplica Bloco C (alerta se faltar tese, lero-lero, etc.).

Aplique todas as correções da revisora DIRETO no texto. Não entregue lista de problemas. Se a revisora apontar alerta que depende de dado que só o aluno tem, peça o dado específico SEM mencionar a revisora.

---

## 4.6. Output

1. **Mostrar a legenda completa no chat**, em bloco pronto para copiar.
2. **Salvar em `legenda.txt`** na mesma pasta do `prompts.txt` (`meus-produtos/{ativo}/entregas/conteudo-social/carrossel-{estilo}/legenda.txt`).
3. **Informar o caminho absoluto** do arquivo no chat, em formato copiável.

---

## 4.7. Aprovação

Após mostrar a legenda, pergunte. **As 4 opções abaixo são obrigatórias. Não simplifique para 2 opções, mesmo que a legenda pareça ótima de primeira:**

```
1. Aprovar e salvar
2. Quero ajustar algo (diga o que)
3. Regenerar do zero
4. Cancelar

Digite o número.
```

- **Opção 1**: encerre o Passo 5 e siga para a entrega final do carrossel.
- **Opção 2**: pergunte o que ajustar, refaça a legenda (passando de novo pela revisora) e mostre. Loop até aprovação.
- **Opção 3**: regenere a legenda do zero (mesmo input, prompt diferente, nova passagem pela revisora). Volta a perguntar.
- **Opção 4**: encerre o fluxo sem salvar a legenda.

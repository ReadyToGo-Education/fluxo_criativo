# Estilo. Carrossel "Sempre"

> Carrossel viral de 6 slides que entrega 5 ações contraintuitivas, práticas e funcionais (coisas que a pessoa do nicho deveria SEMPRE fazer) + CTA criativa.
> Este estilo **delega o prompt-base** para `references/prompt-sempre.md`. O prompt é executado EXATAMENTE como está, sem reescrita. A única adaptação permitida é pré-preencher o Passo 1 (Coleta) com dados do produto ativo quando existirem.

---

## Coleta do Passo 1

O fluxo de coleta do Sempre **ignora** o `passo-coleta-base.md` padrão. A coleta é a do `prompt-sempre.md` (5 perguntas):

### 1.1. Nicho e produto em UMA frase
Se `perfil.md` tiver Quadro/categoria do produto, pré-preencha como sugestão.

### 1.2. @ do Instagram
Se `.env` tiver `IG_USER` ou `perfil.md` tiver handle, pré-preencha como sugestão.

### 1.3. Cores padrão da marca
Default sem paleta: creme bege `#F2EAD9` (slides 1-5) + verde-sálvia escuro `#3D4A3F` (slide 6).

### 1.4. Tipo de comunicação (texto)
6 opções: clássica/profissional, bem-humorada, técnica, inspiracional, descontraída/casual, polêmica/provocativa. Default: "clássica direta".

### 1.5. Estilo de design visual
7 opções (Sofisticado e elegante, Editorial e cinematográfico, Despojado e bem-humorado, Energético e vibrante, Sério e técnico, Aconchegante e humano, Provocativo e ousado) ou descrição livre.

---

## Passo 2. Execução

A skill `/carrossel` no estilo Sempre faz o seguinte:

1. **Carrega** `references/prompt-sempre.md` inteiro.
2. **Executa o Passo 1 do prompt** (coleta de 5 dados), uma pergunta por turno, com pré-preenchimento de sugestão a partir do `perfil.md`/`.env`.
3. Passa pela **confirmação consolidada** (Passo 2.5 da SKILL.md).
4. **Executa o prompt do Passo 2 ao Passo 4 exatamente como está**, na sessão atual:
   - Passo 2: gera os 6 slides com aprovação interna.
   - Passo 3: 3 outputs (chat slide por slide, arquivo `prompts.txt`, comando Cowork).
   - Passo 4: gera a legenda do Instagram com Manual da Copy e salva `legenda.txt`.
5. O texto dos 6 slides passa pelo **Manual da Copy + revisora** silenciosamente antes do gate de aprovação do Passo 2 do prompt.

---

## Diferenças importantes em relação aos outros estilos clássicos ainda não migrados

| Aspecto | Sempre (verbatim) | Estilos clássicos no modelo leve (Odeio, Erros, Amo, Ninguém Conta) |
|---|---|---|
| Fonte de regras | `references/prompt-sempre.md` (prompt completo, verbatim) | `references/estilos/{estilo}.md` (rules leves) + `passo-coleta-base.md` |
| Execução | A skill executa o prompt do estilo do início ao fim | A skill conduz Passo 3 padrão usando guidance leve |
| Output de prompts visuais | Output Triplo do próprio prompt (chat + `prompts.txt` + comando Cowork) | `passo-output-triplo.md` compartilhado |
| Output de legenda | Passo 4 do próprio prompt (com Manual da Copy citado explicitamente) | `passo-legenda.md` compartilhado |

---

## Modo "Gerar todos"

No fluxo "Gerar todos" (Passo 2 da SKILL.md, ramo `todos`), Sempre roda com **valores pré-coletados** no Passo 2.B da SKILL.md (handle, nicho_produto, cores_marca, tom_texto, estilo_design):

- A skill pula o Passo 1 do `prompt-sempre.md` (Coleta interativa) e injeta os valores diretamente.
- Em seguida executa o Passo 2 do prompt sem o gate de aprovação interativa (aprovação acontece depois, em lote, no Passo 2.D da SKILL.md).
- Passo 3 e Passo 4 do prompt rodam normalmente (visuais e legenda).

---

## Saída no projeto

Pasta de saída:

```
meus-produtos/{ativo}/entregas/conteudo-social/carrossel-sempre/
```

Arquivos gerados (definidos pelo próprio `prompt-sempre.md`):
- `texto.md` (6 slides aprovados — convenção da skill, ver Passo 3 da SKILL.md)
- `prompts.txt` (6 prompts visuais em inglês, separados por linha em branco — Passo 3.2 do prompt)
- `legenda.txt` (legenda do Instagram, revisada pelo Manual da Copy — Passo 4.5 do prompt)

Adicionalmente, durante a execução o prompt entrega no chat o **comando Cowork** pronto para automatizar a geração das imagens no ChatGPT via Claude in Chrome.

---

## Paleta default

- **Slides 1-5.** Fundo creme bege `#F2EAD9` + texto verde-sálvia escuro `#3D4A3F`.
- **Slide 6 (CTA).** Fundo verde-sálvia escuro `#3D4A3F` + texto creme bege `#F2EAD9`.

Inverte o jogo de contraste no slide 6 para fechar com peso. Se o aluno responder com outra paleta no Passo 1.3, use a dele.

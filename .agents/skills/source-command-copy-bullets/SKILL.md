---
name: "source-command-copy-bullets"
description: "Gerar 110 bullets de copy do produto ativo (frases curtas de curiosidade sobre uma entrega concreta do produto) nas 11 técnicas de bullet, mais os 10 bullets quentes para headline, assunto de e-mail e abertura de anúncio. Lê o resumo do produto no lugar de perguntar e salva os bullets aprovados em meus-produtos/{ativo}/entregas/copy-pagina/bullets-{produto}.md, de onde /lt-pagina, /copy-pagina e outras skills de página os reaproveitam. Use quando o aluno pedir \"gera bullets\", \"bullets pra minha página\", \"fascinations\", \"frases de curiosidade\", \"110 bullets do meu produto\" ou bullets para VSL, e-mail ou anúncio."
---

# source-command-copy-bullets

Use esta skill quando o usuário pedir o comando `/copy-bullets` do workshop (ou `copy-bullets`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/copy-bullets.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Bullets do Produto. 110 Bullets em 11 Técnicas

Gera 110 bullets do produto ativo, 10 por técnica, e separa os 10 mais fortes. Os bullets aprovados ficam salvos na pasta do produto para as páginas reaproveitarem.

**A skill completa está em `.claude/skills/gerador-de-bullets/SKILL.md`.** Leia o arquivo inteiro, com os dois apêndices, antes do Passo 1 e siga cada seção dele à risca. Este command é o roteiro com o aluno: diz a ordem, o que perguntar, onde salvar e o que mostrar.

## Usage

```
/copy-bullets
```

---

## Passo 0. Contexto

1. Leia `meus-produtos/.ativo` e `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme "Contexto Persistente do Negócio" no CLAUDE.md).
2. Com o resumo em mãos, não faça as duas perguntas da skill. Anuncie em uma linha o que vai usar:

```
Vi que o {nome do produto} é para {público} e entrega {o que o produto entrega, pela Furadeira}. Vou usar isso. Se quiser ajustar, me avisa.
```

3. Sem produto ativo, ou com o perfil ainda sem Quadro, siga o Passo 0 da skill: as duas perguntas, uma por vez.
   - **Sem produto ativo:** os bullets não são salvos, só ficam no chat. Avise isso antes de gerar.
   - **Produto ativo com o perfil sem Quadro:** salve normalmente na pasta do produto e, no fim, recomende `/produto-concepcao`, porque com a concepção completa os bullets saem mais fortes.
4. Se `meus-produtos/{ativo}/entregas/copy-pagina/bullets-{produto}.md` já existir, pergunte antes de gerar:

```
Você já tem bullets salvos deste produto. O que prefere?

1. Gerar 110 novos e substituir os atuais
2. Gerar mais bullets e somar aos atuais (a numeração continua)
3. Só abrir os bullets atuais

Digite o número:
```

   - **1:** siga para o Passo 1.
   - **2:** pergunte quantos e de quais técnicas, gere com a numeração contínua (a partir do último número salvo) e acrescente ao arquivo depois da aprovação.
   - **3:** mostre o caminho absoluto do arquivo e encerre.

---

## Passo 1. Gerar os bullets

```
🔍 Próximo passo: montar os 110 bullets do seu produto nas 11 técnicas e separar os 10 mais fortes (4 passos). Tempo estimado: 3 a 5 minutos.
```

Siga os Passos 1 a 4 da skill: inventário de entregas a partir do resumo (tabela do item 2 da seção "Como esta skill funciona no projeto"), os 110 bullets, os 10 quentes e a revisão interna com o Manual da Copy e a revisora. Nada aparece para o aluno antes da revisão.

---

## Passo 2. Aprovação

Mostre os 110 bullets e os 10 quentes no formato da skill e pergunte:

```
Quer ajustar alguma coisa? Dá pra pedir mais de uma técnica ("mais erro e consequência"), focar numa entrega, deixar mais agressivo ou mais sóbrio, ou trocar os 10 quentes.

1. Aprovar e salvar
2. Quero ajustar algo

Digite o número:
```

Com 2, regere só a parte pedida, na mesma numeração, e pergunte de novo.

---

## Passo 3. Salvar

Com a aprovação, salve em `meus-produtos/{ativo}/entregas/copy-pagina/bullets-{produto}.md`:

```markdown
# Bullets: {nome do produto}

> Gerados em {AAAA-MM-DD} pelo /copy-bullets. Matéria-prima para páginas, VSL, e-mails e anúncios.

## 110 bullets. {nicho}
...
## 10 bullets quentes (os que eu levaria pra headline, e-mail e anúncio)
...
```

Informe o caminho absoluto e feche:

```
✅ Concluído: 110 bullets salvos. Caminho: {caminho absoluto}
```

---

## Passo 4. Próximo passo

Recomende pelo `Tipo` em `## Produto` do resumo:

- **Low Ticket:** `/lt-pagina`. A seção de bullets de curiosidade da página parte destes bullets.
- **Middle ou High Ticket:** `/copy-pagina`. As etapas do método e os entregáveis da página 8D partem destes bullets.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: {/lt-pagina ou /copy-pagina}
Os bullets salvos entram direto na página. Os 10 quentes também servem
de assunto de e-mail e de primeira linha de anúncio (/copy-anuncio).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Regras

1. Uma pergunta por vez, sempre com opções numeradas quando houver escolha.
2. Nenhum bullet com número, passo ou prova que o produto não tem. Nome novo de mecanismo só para algo que o produto realmente faz. Dado de mercado não vira prova do produto.
3. Bullet é afirmação: sem pergunta, sem nome do produto, sem "neste curso" ou "no módulo 2" dentro do bullet.
4. Todo bullet passa pelo Manual da Copy e pela revisora antes de o aluno ver, sem avisar.
5. Só salva depois da aprovação.

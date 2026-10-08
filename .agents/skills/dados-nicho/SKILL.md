---
name: dados-nicho
description: >
  Descobre 10 a 20 perfis de referência do nicho do aluno, no Brasil e no
  mundo, via WebSearch. Identifica padrões de conteúdo que se repetem no
  ecossistema e entrega relatório com links, posicionamento de cada perfil,
  tipo de conteúdo e sugestões práticas pro aluno postar.
---

# Dados Nicho. Perfis e Conteúdos do Ecossistema

Mapeia o ecossistema do nicho do aluno. Faz 4 a 6 buscas combinadas de WebSearch pra trazer perfis de referência no Brasil e no mundo, separa por porte, identifica padrões de conteúdo e entrega um relatório com links clicáveis + sugestões de post baseadas no que já funciona.

## Quando Usar

- Quando o aluno disser "quem devo seguir no meu nicho", "quais os perfis referência em X", "não sei o que postar, me mostra o que os outros fazem", "quero estudar a concorrência".
- Como primeiro passo antes de começar a produzir conteúdo novo.
- Como input pra `/copy-carrossel` e `/dados-instagram`.

## O Que Fazer

### 0. Contexto

Leia `entregas/.ativo`, `entregas/{ativo}/perfil.md` e `entregas/{ativo}/idconsumidor.md` (se existir). Identifique:
- Nicho principal (ex: emagrecimento, finanças, tarô, marketing digital)
- Sub-nicho ou angle específico (ex: emagrecimento feminino 40+, finanças pra autônomos)
- Urgências Ocultas do perfil (vão virar ideia de conteúdo no fim)

### 1. Entrevista curta (uma pergunta por vez)

**Pergunta 1. Confirmar o nicho.**
Mostre o que está no perfil e pergunte se é isso mesmo:
```
Seu nicho é: {nicho} ({sub-nicho})
É isso mesmo, ou quer ajustar antes de buscar?

1. Sim, pode buscar
2. Vou ajustar
```

**Pergunta 2. Foco geográfico.**
1. Só Brasil
2. Só exterior
3. Ambos (padrão recomendado)

**Pergunta 3. Porte alvo.**
1. Grandes perfis de autoridade (500k+)
2. Perfis médios em crescimento (50k a 500k)
3. Perfis pequenos mas engajados (10k a 50k)
4. Todos os portes (padrão)

### 2. Rodar as buscas

Faça 4 a 6 buscas combinadas via WebSearch:
- `"melhores perfis instagram {nicho} brasil"`
- `"{nicho} creators brasileiros 2026"`
- `"top instagram accounts {nicho em inglês}"`
- `"{sub-nicho} influencer" site:instagram.com`
- `"{sub-nicho}" viral reels`
- `"{nicho}" "dicas" instagram`

Se o nicho for muito específico e as buscas retornarem pouco, peça pro aluno citar 2 ou 3 perfis que ele já segue e use como semente: `"similar to @perfil" {nicho}` ou `"parecidos com" @perfil`.

### 3. Compilar a lista

Extraia 10 a 20 perfis. Pra cada perfil, documente:
- `@` do perfil com link (`https://instagram.com/perfil`)
- País de origem
- Porte estimado em faixa (10k-50k, 50k-200k, 200k-1M, 1M+)
- Posicionamento em uma frase
- Tipo de conteúdo predominante (Reels educacional, carrossel prático, bastidores, humor, listas, etc)
- O que dá pra copiar eticamente: formato, tema, estrutura (nunca texto)

### 4. Identificar padrões

Leia os perfis coletados e responda em 5 a 8 bullets:
- Quais ganchos se repetem
- Quais formatos dominam (Reels curto, carrossel longo, quick tips, reação a comentário, etc)
- Quais temas aparecem em quase todo mundo
- Qual tom predomina (casual, educativo, provocativo, aspiracional)
- Quais erros parecem comuns (sempre tem)

### 5. Gerar sugestões pro aluno

Crie 5 ideias de post ou Reels pro aluno baseadas em:
- Padrões que funcionam no nicho
- Urgências Ocultas do perfil ativo (DORES, DESEJOS, etc)
- Formato específico (Reel, carrossel, etc)

Cada sugestão deve ter: título/gancho, formato, tema e por que provavelmente vai funcionar.

### 6. Montar o relatório final

Arquivo: `entregas/{ativo}/dados/nicho-{data}.md`

Estrutura:
```markdown
# Panorama do nicho {nicho}

Data: {data}
Foco: {Brasil / Exterior / Ambos}
Porte: {filtro}

## Padrões que se repetem no nicho
- {padrão 1}
- ...

## Perfis encontrados

### Autoridades (200k+)
1. [@perfil1]({link}) - {país} - {porte} - {posicionamento}
   Conteúdo: {tipo}
   O que copiar: {formato/tema/estrutura}
2. ...

### Em crescimento (50k-200k)
1. ...

### Pequenos e engajados (10k-50k)
1. ...

## Sugestões pro seu conteúdo
1. **{título}** ({formato})
   Tema: {tema}
   Por que funciona: {razão}
2. ...
```

### 7. Aprovação e entrega

Mostre o relatório resumido (padrões + sugestões) e pergunte:
```
1. Aprovar e salvar
2. Quero buscar mais perfis
3. Quero ajustar as sugestões
```

Após aprovação, salve e mostre:
```
Pronto. Relatório do nicho salvo.

Arquivo: entregas/{ativo}/dados/nicho-{data}.md

Próximos passos:
- Leve as sugestões pro /copy-carrossel pra virar posts e carrosséis
- Rode /dados-instagram no seu próprio perfil pra comparar com o que os outros fazem
```

## Regras

- Sempre combinar o que foi encontrado com as Urgências Ocultas do perfil ativo nas sugestões finais.
- Se não encontrar perfis suficientes no Brasil, puxar do exterior e traduzir o posicionamento pra português.
- Nunca copiar texto ou legenda de outro perfil. A skill entrega formato, tema e estrutura.
- Verificar que os links de `instagram.com` estão válidos (perfil público, não privado).
- Se um perfil citado nos resultados não existir mais, descartar.
- Não usar travessão em nenhum texto exibido.

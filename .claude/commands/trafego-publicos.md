---
name: workshop-marketing:trafego-publicos
description: Cria, lista e gerencia públicos (audiences) do Meta Ads via Marketing API. Cobre Custom Audiences por evento padrão do pixel, evento personalizado (cria evento + audience), engajamento de vídeo (25/50/75/100%), bases por nível (iniciante/intermediário/avançado), Lookalike e listagem. Toda criação passa por preview YAML e confirmação SIM. Use quando o aluno pedir "criar público", "audience custom", "lookalike", "remarketing", "público de quem viu vídeo", "público dos compradores", "público de quem clicou no botão".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
model: sonnet
user-invocable: false
---

# Trafego Publicos. Audiences Meta Ads

Cria, lista e gerencia audiences via Marketing API. Esta skill é a única que tem permissão para criar audience — outras skills que precisam de público (`/trafego-criar-campanha`, `/trafego-testes`, `/trafego-escalar`) chamam esta.

Especificação completa em `.claude/skills/trafego-publicos/SKILL.md`. Este command é o orquestrador.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo`. Leia `perfil.md` e `idconsumidor.md` (necessários para o sub-fluxo "Bases por nível").

### 0.2 Conexão Meta (gate duro)
Mesma validação dos outros `/trafego-*`. Se `META_AUTH_MODO` vazio, aciona `/trafego-conexao`.

### 0.3 Selecao de conta multi-conta
Idem aos outros commands.

### 0.4 Ler especificações
- `.claude/skills/trafego-publicos/SKILL.md`
- Sub-skill conforme escolha do aluno

---

## Passo 1. Menu

```
🎯 TRÁFEGO PÚBLICOS. Audiences Meta Ads

[1] Público por evento padrão do pixel
    PageView, ViewContent, AddToCart, IC, Purchase, Lead, etc.

[2] Público por evento personalizado
    Cria o evento custom no pixel + a audience baseada nele

[3] Público por engajamento de vídeo
    Quem viu 25%, 50%, 75% ou 100% do vídeo

[4] Bases por nível (iniciante / intermediário / avançado)
    Saved audiences combinando interesses do produto ativo

[5] Lookalike (LAL 1%, 2%, 5%, 10%)
    Audience semelhante a uma source existente

[6] Listar audiences existentes
    Visão geral + alertas (vazias, encolhendo, candidatas a LAL)

Digite o número:
```

## Passo 2. Sub-fluxo

| Escolha | Sub-skill | Endpoint principal |
|---|---|---|
| [1] | `publico-evento-padrao.md` | `POST /act_<id>/customaudiences` (subtype WEBSITE) |
| [2] | `publico-evento-personalizado.md` | `POST /<pixel>/customconversions` + `POST /act_<id>/customaudiences` |
| [3] | `publico-video-view.md` | `POST /act_<id>/customaudiences` (subtype ENGAGEMENT) |
| [4] | `bases-niveis.md` | `POST /act_<id>/saved_audiences` (x3) |
| [5] | `lookalike.md` | `POST /act_<id>/customaudiences` (subtype LOOKALIKE) |
| [6] | `listar.md` | `GET /act_<id>/customaudiences` + `GET /act_<id>/saved_audiences` |

---

## Passo 3. Coletar inputs (varia por sub-fluxo)

Cada sub-skill define os inputs específicos. Padrão geral:
- Nome / descrição (gerado pela skill com convenção `[FC] tipo-descricao-janela-produto`)
- Janela (default 30d, aceita 1-180d para WEBSITE, 1-365d para vídeo)
- Tamanho mínimo da source (apenas Lookalike)

🔍 Próximo passo: validar dados e calcular tamanho estimado da audience. Tempo estimado: cerca de 30 segundos.

---

## Passo 4. Preview YAML

Mostrar bloco YAML completo: nome final, subtype, regra (rule JSON), janela, tamanho estimado, alertas (se audience micro < 1.000, etc.).

```
confirma criar? (digite SIM)
```

---

## Passo 5. Criação

Se confirmado:
- Executa `POST` na Marketing API.
- Devolve `id` da audience.
- Cria `meus-produtos/{ativo}/trafego/publicos/{id}.md` com payload completo + comando de rollback.
- Atualiza `meus-produtos/{ativo}/trafego/publicos/INDEX.md`.
- Invalida cache do `/trafego-insights`.

✅ Concluído: audience criada.

---

## Passo 6. Próximos passos

```
Próximos passos:

- Para usar essa audience numa campanha: /trafego-criar-campanha
- Para criar lookalike a partir dela: /trafego-publicos opção 5
- Para ver tamanho real (Meta calcula em ~24h): /trafego-publicos opção 6
- Para criar campanha de remarketing usando essa audience:
  /trafego-testes opção 9 (campanha de remarketing)
```

---

## Princípios

1. **Preview antes de write. Sempre.**
2. **Confirmação SIM** explícita antes de criar.
3. **Convenção de nome `[FC]`** padrão.
4. **Audience nasce disponível** (não há PAUSED para audience).
5. **Não conecta a adset automaticamente.** Só cria.
6. **Não deleta.** Operação manual no Audiences Manager.
7. **Não cria evento padrão fora do contexto.** Só `[2]` cria evento, e apenas para alimentar audience da mesma sessão.

# PRD. Stack de Tráfego Enxuta

> Documento de decisão e procedimento de remoção das skills de tráfego que NÃO fazem parte da minha stack pessoal.
> Última aplicação. 2026-05-29.
> Autor da decisão. gabrieljose-hue.

---

## 1. Contexto

O repositório oficial do Fluxo Criativo entrega 10 skills `trafego-*`. Não uso 4 delas (são handoffs opcionais de skills de leitura e diagnóstico). Sempre que rodo `/atualizar-projeto` (git pull), o repositório oficial pode reintroduzir as pastas e arquivos removidos. Este PRD documenta a decisão e ensina como re-aplicá-la sem precisar pensar de novo.

---

## 2. Decisão

### 2.1 Stack que MANTENHO (9 skills)

| Skill | Função | Por que mantenho |
|---|---|---|
| `trafego-conexao` | Conecta com Meta Ads (MCP ou App) | Porta de entrada |
| `trafego-criar-campanha` | Cria campanha via Marketing API | Criação primária |
| `trafego-insights` | Lê métricas e calcula derivadas | Fonte única de dados das outras |
| `trafego-otimizar` | Diagnóstico em 2 camadas e 6 trilhas | Operação diária |
| `trafego-escalar` | Escala campanhas validadas | Handoff natural do `trafego-otimizar` |
| `trafego-analise` | 9 outputs narrativos VTSD | Ensinar e diagnosticar |
| `trafego-pago` | Base de conhecimento legada | Usada por `copy-anuncio` e `estrategia-lancamento` |
| `criar-aplicativo-analise-ads` | Setup do App no Facebook Developers | Dependência do `trafego-conexao` (modo APP) |
| `gerar-token-permanente-facebook-ads` | Gera token permanente | Dependência do `trafego-conexao` (modo APP) |
| `obter-id-conta-anuncios` | Salva `FB_AD_ACCOUNT_ID` | Dependência do `trafego-conexao` (modo APP) |

### 2.2 Stack que REMOVO (4 skills)

| Skill | Função | Por que removo |
|---|---|---|
| `trafego-pixel` | Diagnóstico aprofundado de pixel | Não uso. O `trafego-analise` output [8] já cobre o essencial |
| `trafego-publicos` | Cria audiences via API | Não uso. Crio audience direto no Gerenciador |
| `trafego-regras` | Cria regras automáticas | Não uso. Crio regras direto no Gerenciador |
| `trafego-testes` | Cria testes A/B disciplinados | Não uso. Duplico entidade direto no Gerenciador |

### 2.3 Sub-skill REMOVIDA

A sub-skill `trafego-otimizar/sub-skills/atalhos-compostos.md` sai junto. Os 4 atalhos compostos (Lookalike para Campanha, Duplicar melhor anúncio, Faxina mais Lookalike, Refresh criativo) dependem das 4 skills removidas. Sem elas, os atalhos quebram. Aceito perder os 4 em troca da stack enxuta.

### 2.4 Não mexo em (ações em lote do `trafego-otimizar`)

A sub-skill `acoes-lote.md` continua de pé. Ações como "pausa tudo com ROAS abaixo de 1 nos últimos 14d" ou "reduz 20% nos adsets com CPA acima de R$ 80" seguem funcionando.

---

## 3. Como re-aplicar a decisão

### 3.1 Caminho rápido (script)

Após `/atualizar-projeto` (ou qualquer `git pull` que reintroduzir as pastas), rodar:

```
python3 scripts/manter-stack-trafego-enxuta.py
```

O script é **idempotente** (pode rodar quantas vezes precisar. Só remove o que ainda existir e só edita o que ainda contiver referência). Output esperado:

```
Pastas removidas: N
Arquivos removidos: N
Arquivos com referencias limpas: N
  - <lista>
```

Em seguida:

```
git add -A
git diff --cached --stat
git commit -m "chore: reaplicar stack de trafego enxuta (PRD)"
```

### 3.2 Caminho manual (caso o script não esteja disponível)

Se o script não existir, é só remover essas 9 entradas e rodar git status.

**Pastas a deletar** (em `.claude/skills/`):
- `trafego-pixel/`
- `trafego-publicos/`
- `trafego-regras/`
- `trafego-testes/`

**Commands a deletar** (em `.claude/commands/`):
- `trafego-pixel.md`
- `trafego-publicos.md`
- `trafego-regras.md`
- `trafego-testes.md`

**Sub-skill a deletar**:
- `.claude/skills/trafego-otimizar/sub-skills/atalhos-compostos.md`

**Referências a limpar** (substituir as menções por caminho manual no Gerenciador):

| Padrão a substituir | Substituir por |
|---|---|
| `/trafego-pixel`, `"trafego-pixel"`, `` `trafego-pixel` ``, `'trafego-pixel'` | `Gerenciador de Eventos` |
| `/trafego-publicos`, `"trafego-publicos"`, `` `trafego-publicos` ``, `'trafego-publicos'` | `Gerenciador de Audiences` |
| `/trafego-regras`, `"trafego-regras"`, `` `trafego-regras` ``, `'trafego-regras'` | `Gerenciador (Regras automáticas)` |
| `/trafego-testes`, `"trafego-testes"`, `` `trafego-testes` ``, `'trafego-testes'` | `Duplicar entidade no Gerenciador (variando 1 dimensão)` |

**Arquivos que costumam ter as referências** (lista pode crescer conforme o projeto evolui. O script grepa em tudo automaticamente):

- `CLAUDE.md`
- `AGENTS.md`
- `README.md`
- `.claude/commands/trafego-analise.md`
- `.claude/commands/gerar-token-permanente-facebook-ads.md`
- `.claude/skills/trafego-otimizar/SKILL.md` (description e seção 16)
- `.claude/skills/trafego-analise/SKILL.md`
- `.claude/skills/trafego-analise/sub-skills/*.md` (1 a 10)
- `.claude/skills/trafego-insights/SKILL.md`
- `.claude/skills/trafego-insights/sub-skills/cache.md`
- `.claude/skills/programar-carrossel/SKILL.md`
- `.claude/skills/programar-carrossel-noticia/SKILL.md`

---

## 4. Validação pós-aplicação

Rodar grep para confirmar que sobrou nada:

```
grep -r "trafego-pixel\|trafego-publicos\|trafego-regras\|trafego-testes" .claude/ CLAUDE.md AGENTS.md README.md
```

Esperado: zero match (ou apenas o próprio script). Se aparecer match em sub-skill nova ou arquivo novo, o script precisa ser estendido. Abrir o script, adicionar o padrão nas listas `SUBSTITUTIONS` ou `SCAN_TARGETS`, rodar de novo.

---

## 5. Quando NÃO aplicar

- Se eu mudar de ideia e quiser voltar a usar audiences via API. Reverter para o repositório oficial (`git checkout origin/main -- .claude/skills/trafego-publicos/ .claude/commands/trafego-publicos.md` e restaurar referências).
- Se eu começar a vender consultoria de tráfego para outras pessoas. Faz sentido manter a stack completa, porque o aluno pode querer as 10 skills.

---

## 6. Histórico

| Data | Quem aplicou | Observação |
|---|---|---|
| 2026-05-29 | gabrieljose-hue | Primeira aplicação. Removeu 4 skills, 4 commands, 1 sub-skill e limpou 17 arquivos |

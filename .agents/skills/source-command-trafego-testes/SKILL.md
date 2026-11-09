---
name: "source-command-trafego-testes"
description: "Cria testes A/B disciplinados e variações estruturadas no Meta Ads, pelo MCP da Meta (padrão) ou pela Marketing API (modo App). Cobre A/B de criativo, headline, audiência, faixa etária, posicionamento, lance, estrutura e CTA, duplicar campanha, conjunto ou anúncio mudando UMA coisa só, e campanha de remarketing completa (público + campanha). Toda criação nasce pausada e documenta a hipótese; no 7º dia, a opção [11] lê o resultado, classifica, registra o aprendizado e sugere o próximo teste. Use quando o aluno pedir \"testar A vs B\", \"duplicar minha melhor campanha mudando a idade\", \"criar campanha de remarketing\", \"Reels vs Feed\", \"broad vs segmentado\", \"como ficou meu teste\"."
---

# source-command-trafego-testes

Use esta skill quando o usuário pedir o comando `/trafego-testes` do workshop (ou `trafego-testes`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/trafego-testes.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Trafego Testes. A/B e Variações Meta Ads

Cria testes A/B com hipótese documentada, mesmo orçamento nos lados e uma única dimensão variando, e devolve a data de leitura do resultado.

A especificação completa está em `.claude/skills/trafego-testes/SKILL.md`. Este command é o orquestrador.

---

## Passo 0. Contexto e validação

### 0.1 Produto ativo
Leia `meus-produtos/.ativo`. Leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme a seção "Contexto Persistente do Negócio" do CLAUDE.md). Do resumo saem o preço e o tipo (mínimo de conversões: 50 por lado em low e middle ticket, 30 em high ticket) e o contexto VTSD para sugerir hipóteses (Quadro, Urgências Ocultas, Decorados, objeções). Não pergunte o que o resumo já tem.

### 0.2 Conexão Meta (gate duro, passo zero obrigatório)
Leia `META_AUTH_MODO` com `grep "^META_AUTH_MODO=" .env | cut -d= -f2-`.

- **Se vazio, ausente ou com valor diferente de `MCP_CONECTOR` e `APP`** (inclusive o legado `HIBRIDO`): acione `/trafego-conexao` e aguarde a conclusão. Não tente adivinhar, não caia em outro caminho e não peça credencial avulsa.
- **Se `MCP_CONECTOR`:** confirme que existe uma tool cujo nome termina em `ads_get_ad_accounts`. Se nenhuma estiver disponível, peça ao aluno para reabrir o Claude Code; se persistir, volte ao `/trafego-conexao`. Se a conta vier como não liberada no MCP, explique e ofereça o modo App pelo `/trafego-conexao`. Confira também que `FB_AD_ACCOUNT_ID` tem valor (`grep -q "^FB_AD_ACCOUNT_ID=." .env`); se faltar, a opção "Validar" do `/trafego-conexao` completa.
- **Se `APP`:** confirme que `FB_ACCESS_TOKEN_PERMANENTE` e `FB_AD_ACCOUNT_ID` têm valor no `.env` (`grep -q "^NOME=." .env`, com o ponto: linha vazia conta como ausente). Se faltar algum, acione `/trafego-conexao`.

A skill nunca prossegue sem essa validação passar.

### 0.3 Seleção de conta de anúncio (multi-conta)
1. Leia `FB_AD_ACCOUNT_IDS` no `.env`. Se não existir ou tiver 1 conta, use `FB_AD_ACCOUNT_ID` sem perguntar.
2. Com 2 ou mais contas, pergunte qual usar, mostrando os nomes (MCP: `ads_get_ad_accounts`; App: `curl -s "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_id,name&limit=100&access_token=***TOKEN_MASCARADO***"`, com o token lido do `.env` na própria chamada).
3. Guarde a conta escolhida só para esta execução.

### 0.4 Ler especificações
- `.claude/skills/trafego-testes/SKILL.md`
- A sub-skill da opção escolhida

---

## Passo 1. Menu

```
🧪 TRÁFEGO TESTES. A/B e Variações Meta Ads

[1]  A/B de criativo                     imagem A vs B, ou imagem vs vídeo
[2]  A/B de headline                     até 3 variações de headline
[3]  A/B de audiência                    broad vs segmentado, ou público X vs Y
[4]  A/B de faixa etária                 ex: 25-34 vs 35-44
[5]  A/B de posicionamento               Reels vs Feed vs Stories
[6]  A/B de lance                        automático vs limite de custo
[7]  A/B de estrutura                    Advantage+ vs ABO manual
[8]  A/B de CTA                          Saiba mais vs Comprar agora vs Cadastre-se
[9]  Duplicar com variação               copia o que já existe mudando 1 coisa
[10] Campanha de remarketing             fluxo composto: público + campanha
[11] Ler resultado de teste              lê no 7º dia, classifica, registra o aprendizado

Digite o número:
```

### Redirecionamentos

Pedido fora do escopo de teste:
- "Pausar todos com CPA > X" → **`/trafego-otimizar`** (ação em lote, não é teste)
- "Aumentar 20% nos 3 melhores" → **`/trafego-escalar`** (escala, não é teste)
- "Criar campanha do zero" → **`/trafego-criar-campanha`**
- "Escrever os anúncios do teste" → **`/copy-anuncio`**, **`/criativo-estatico`** ou **`/mandala-de-anuncios`**

---

## Passo 1.5. Detecção de intenção (sintoma ou teste)

Se o aluno chegou com **sintoma** ("meu CPA subiu", "o criativo cansou", "a página não converte") em vez de **teste** ("quero A/B de criativo"):

```
Parece que você tem um sintoma, não um teste definido.

Para transformar esse sintoma numa hipótese que dá para testar:

1. Rodar /trafego-diagnostico: gera 3 hipóteses com peso
2. Rodar /trafego-criativos: mostra onde o criativo quebra
3. Prefiro montar a hipótese eu mesmo

Digite o número:
```

Se 1 ou 2: encaminhar. Quando o aluno voltar com a hipótese, retomar no Passo 3.
Se 3: seguir para o Passo 3.

---

## Passo 2. Sub-fluxo

| Escolha | Sub-skill |
|---|---|
| [1] a [8] | `sub-skills/ab-generico.md` (com a dimensão da opção) |
| [9] | `sub-skills/duplicar-variando.md` |
| [10] | `sub-skills/campanha-remarketing.md` (junta `/trafego-publicos` e `/trafego-criar-campanha`, no modo lote pré-aprovado) |
| [11] | `sub-skills/leitura-resultado.md` (lê no 7º dia, classifica, registra) |

> **Opção [11]:** pular os Passos 3 a 6. A `leitura-resultado.md` tem o próprio fluxo de 8 passos.

---

## Passo 3. Hipótese

Antes de qualquer dado técnico:
```
Qual a sua hipótese para esse teste?

(ex: "Vídeo converte mais que imagem no público frio de tarot porque mostra a leitura
acontecendo, no ângulo Demonstração da Mandala")

A hipótese fica salva e é usada na leitura do 7º dia.
```

Se o aluno não tiver hipótese clara, sugerir 2 ou 3 a partir do resumo do produto (Urgências Ocultas, objeções, Quadro) e dos tipos da Mandala (`/mandala-de-anuncios`).

---

## Passo 4. Inputs específicos

Cada sub-skill define os inputs. Comum a todas:
- Campanha ou conjunto molde (escolhido por nome ou lista, nunca por ID digitado)
- Orçamento diário (igual nos lados)
- Variações (A vs B, ou A, B e C em headline e CTA)

Headlines, textos e CTAs gerados pela skill passam pela "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md antes de aparecer.

🔍 Próximo passo: montar as entidades do teste, todas pausadas, com a variação aplicada (4 passos). Tempo estimado: cerca de 60 segundos.

(Teste na campanha inteira, com vários conjuntos: 2 a 3 minutos. Campanha de remarketing completa: 2 a 3 minutos.)

---

## Passo 5. Resumo e bloco 🛡️

Resumo em linguagem natural e, depois, bloco 🛡️ do CLAUDE.md com o Preview YAML: nome final (`[WS-AB] {dimensao}-{slug}`), modelo, variações, o que fica igual, orçamento, janela mínima e data de leitura. Um "sim" para o lote inteiro do teste.

---

## Passo 6. Criação

- Cria as entidades PAUSED pelo MCP ou pelo App. Se a cópia pelo MCP falhar, conduz a duplicação guiada no Gerenciador e confere.
- Salva a hipótese e o plano em `meus-produtos/{ativo}/entregas/trafego/testes/{slug}.md` e atualiza o `INDEX.md` da pasta.
- Marca como desatualizado o cache do `/trafego-insights` da conta.
- Informa a data de leitura (7º dia, ou 14º em estrutura).

✅ Concluído: teste A/B criado, pausado. Caminho: `meus-produtos/{ativo}/entregas/trafego/testes/{slug}.md`.

---

## Passo 7. Próximos passos

```
Próximos passos:

1. Revise as entidades no Gerenciador e ative quando quiser (estão pausadas).
   Se preferir, eu ativo por aqui, com confirmação.
2. Aguarde 7 dias com 50 ou mais conversões em cada lado (30 em high ticket).
3. Em {data do 7º dia}, rode /trafego-testes opção [11] "Ler resultado de teste":
   eu classifico, registro o aprendizado e sugiro o próximo teste.
   Para uma leitura VTSD mais ampla dos criativos, use também a /trafego-analise
   (Criativos & Copy) como complemento.

Para desfazer antes do prazo: as entidades já estão pausadas. Se quiser tirá-las da
frente, eu arquivo por aqui (com confirmação), ou você apaga pelo Gerenciador.
```

---

## Princípios

1. **UMA dimensão por teste.** Sem exceção.
2. **Mesmo orçamento** nos lados.
3. **Mínimo de 50 conversões por lado** (30 em high ticket).
4. **Mínimo de 7 dias** de janela.
5. **Hipótese documentada** antes de subir.
6. **Tudo nasce PAUSED.**
7. **Nome com `[WS-AB]`.**
8. **Ler o resultado pela opção [11]** no 7º dia. `/trafego-analise` só como complemento.
9. **Não pausa a perdedora sozinha.** O aluno decide na leitura.
10. **Não escala a vencedora sozinha.** Encaminha para `/trafego-escalar`.
11. **Nunca apaga** e nunca roda `curl -X DELETE`.
12. **Remarketing atravessa skills:** só segue com o plano numerado e um "aprovar tudo" explícito.

# Sub-fluxo. Customer Match (upload de lista de compradores)

Cria Custom Audience tipo `CUSTOM` a partir de uma lista que o aluno **já tem fora do Meta** (CSV de compradores da Hotmart, Eduzz, Kiwify, planilha do CRM, etc.). Aluno sobe o arquivo, skill aplica hash SHA-256 obrigatório (privacy), envia pro Meta. Meta faz match com perfis Facebook/Instagram e cria a audience.

**É o caminho mais potente pra audience de compradores reais.** Sinal direto de "essa pessoa pagou" supera qualquer audience de pixel (que só pega "engajou").

## Por que usar (casos de uso)

- **Excluir compradores das campanhas COLD.** Não desperdiçar verba mostrando anúncio de aquisição pra quem já comprou.
- **Lookalike super qualificada.** LAL gerada da Customer Match de compradores tem qualidade muito superior à LAL de pixel.
- **Remarketing pra base antiga.** Compradores de 6+ meses que sumiram — campanha de upsell ou reativação.
- **Cruzar com outras audiences** (quando o sub-fluxo de combinação de audiences existir): "compradores que NÃO viram meu vídeo X".

## Perguntas que cobre

- "Quero subir minha lista de compradores da Hotmart"
- "Criar audience com a planilha do meu CRM"
- "Excluir quem já comprou das minhas campanhas de aquisição"
- "Lookalike dos meus 5 mil compradores"

## Inputs

| Input | Default | Descrição |
|---|---|---|
| `caminho_csv` | obrigatório | Caminho do CSV no computador do aluno |
| `coluna_match` | obrigatório | Qual coluna do CSV usar (email, telefone, etc.) |
| `nome_audience` | gerado | Sufixo descritivo |
| `descricao` | gerado | O que essa audience representa |

## Pré-requisitos

- **Mínimo 100 registros** no CSV pra Meta aceitar criar a audience.
- **Recomendado 1.000+** pra match razoável (taxa típica de match: 30-60% no Brasil).
- **Política de privacidade na conta de anúncios** declarando que aluno tem permissão de usar a lista (Meta exige aceite — geralmente já está aceito de cadastros anteriores).

## Padrão de coleta de inputs (uma pergunta por mensagem)

Regra dura: **NUNCA agrupar 2+ inputs na mesma mensagem**. Aluno nunca digita hash, nunca digita JSON.

### Ordem fixa

1. **De onde veio essa base?** Pergunta numerada (ajuda skill a sugerir a coluna certa):
   ```
   De onde vem a lista que você quer subir?

   1. Hotmart (export de compradores)
   2. Eduzz / Kiwify / Monetizze / Cakto (export)
   3. ActiveCampaign / Mailchimp / RD Station (export de contatos)
   4. Planilha própria / CRM próprio
   5. Outra fonte (descrever)

   Digite o número:
   ```
   - Sugestão automática de qual coluna usar conforme a fonte (ex: Hotmart usa "Email do Comprador" + "Telefone do Comprador").

2. **Caminho do CSV.** Pergunta aberta:
   ```
   Qual o caminho do arquivo CSV no seu computador?
   (ex: ~/Downloads/compradores-hotmart-2026.csv, ou cola o caminho completo)
   ```
   Skill lê o arquivo, parseia as primeiras 5 linhas, identifica colunas disponíveis.

3. **Coluna(s) pra match.** Pergunta numerada com base no que foi parseado:
   ```
   Achei essas colunas no seu CSV. Qual(is) você quer usar pra match?

   1. Email (coluna "{nome_coluna}", {N} valores válidos)
   2. Telefone (coluna "{nome_coluna}", {N} valores válidos)
   3. Email + Telefone (recomendado pra melhor match)
   4. Outra coluna (cola o nome)

   Digite o número:
   ```
   - **Recomendação automática:** se o CSV tem ambos email e telefone com 100+ válidos cada, sugerir opção 3 (taxa de match dobra quando os 2 são enviados).

4. **Confirmação de privacidade.** Pergunta obrigatória pelo Meta:
   ```
   ⚠️ Antes de subir, preciso confirmar com você:

   - Essa lista foi coletada de forma legítima (aluno opt-in, cadastro de compra, etc.)?
   - Você tem permissão dessas pessoas pra usar o contato em marketing?

   1. Sim, tudo certo (Meta exige esse aceite)
   2. Não tenho certeza (vou parar e verificar)

   Digite o número:
   ```
   Se (2): cancelar e instruir o aluno a verificar LGPD/política da plataforma de origem antes de tentar de novo.

5. **Nome da audience.** Sugerir auto-gerado seguindo `[FC] CustomerMatch-{descricao_curta}-{produto-slug}` (ex: `[FC] CustomerMatch-Compradores-Hotmart-curso-tarot`) e perguntar "uso esse ou prefere outro?".

**Validação automática (transparente pro aluno):**
- Se o CSV tem < 100 registros válidos após parsing: bloquear e avisar.
- Se a coluna escolhida tem > 30% de valores inválidos (não-emails, telefones malformados, etc.): avisar e perguntar se quer prosseguir mesmo assim.

**Proibido:**
- Pedir o hash SHA-256 ao aluno (skill aplica sozinha).
- Pedir `customer_file_source` ou outro campo técnico.
- Agrupar 2+ inputs na mesma mensagem.

## Hash SHA-256 (aplicação obrigatória client-side)

Antes de enviar ao Meta, a skill aplica hash SHA-256 a cada valor da coluna escolhida. Meta **não aceita** PII em claro — só hashes.

Normalização antes do hash (importante pra match alto):
- **Email:** lowercase, trim espaços. Ex: `  RUY@Gmail.com  ` → `ruy@gmail.com` → hash.
- **Telefone:** só dígitos, com código de país. Ex: `(11) 9 8765-4321` → `5511987654321` → hash.

Sem normalização, taxa de match cai drasticamente.

```python
# Pseudocódigo (skill executa internamente, aluno não vê)
import hashlib

def normalize_email(email):
    return email.strip().lower()

def normalize_phone(phone, country_code="55"):
    digits = ''.join(c for c in phone if c.isdigit())
    if not digits.startswith(country_code):
        digits = country_code + digits
    return digits

def hash_value(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()
```

## Endpoints (sequência de 2 chamadas)

### 1. Criar a audience vazia

```
POST /act_<id>/customaudiences
{
  "name": "[FC] CustomerMatch-Compradores-Hotmart-curso-tarot",
  "subtype": "CUSTOM",
  "customer_file_source": "USER_PROVIDED_ONLY",
  "description": "Compradores da Hotmart importados em 2026-05-20 ({N} hashes)."
}
```

`customer_file_source` aceita 3 valores:
- `USER_PROVIDED_ONLY` — aluno coletou direto (cadastro/compra). **Default.**
- `PARTNER_PROVIDED_ONLY` — lista veio de parceiro com permissão. Raro pra infoprodutor.
- `BOTH_USER_AND_PARTNER_PROVIDED` — mix.

### 2. Subir os hashes em lotes

```
POST /<audience_id>/users
{
  "schema": ["EMAIL_SHA256"],
  "data": [
    ["hash_do_email_1"],
    ["hash_do_email_2"],
    ...
  ]
}
```

Schemas comuns:
- `EMAIL_SHA256`
- `PHONE_SHA256`
- `FN_SHA256` (first name), `LN_SHA256` (last name)
- Combinado: `["EMAIL_SHA256", "PHONE_SHA256"]` com data como `[[hash_email, hash_phone], ...]` — **melhor match**.

**Limite por POST:** 10.000 registros. Se a lista tem mais, dividir em lotes.

## Resumo em linguagem natural antes do Preview YAML (obrigatório)

```
📋 Antes de eu subir essa lista pro Meta, deixa eu te resumir:

Vou fazer 2 coisas:

1️⃣ Criar uma audience vazia chamada "{nome}" na sua conta.
2️⃣ Subir {N} {emails|telefones|"emails + telefones"} criptografados (hash SHA-256).

Importante sobre privacidade:
   - Os valores originais (email/telefone) NUNCA são enviados ao Meta — só o hash.
   - Hash é uma "impressão digital" do dado: Meta não consegue ver o valor original,
     só comparar com hashes dos perfis Facebook/Instagram pra achar match.
   - Esse é o mesmo procedimento que ferramentas como Hotmart, Mailchimp e Active fazem
     quando integram com Meta.

Taxa de match esperada: 30 a 60% dos {N} hashes vão bater com perfis ativos.
   - Audience estimada: {N * 0.30} a {N * 0.60} pessoas.
   - Pessoas sem conta Facebook/Instagram ou que cadastraram email diferente NÃO entram.

Tempo: ~24h pra Meta terminar o match. Antes disso, audience aparece como "populando".

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → "[FC] CustomerMatch-..."

Tá certo? (sim cria + sobe, não cancela)
```

**Regras de tradução obrigatórias:**

| Campo técnico | Tradução |
|---|---|
| `EMAIL_SHA256` | "email criptografado" |
| `PHONE_SHA256` | "telefone criptografado" |
| `customer_file_source: USER_PROVIDED_ONLY` | "lista coletada por você (compradores/cadastros)" |
| `subtype: CUSTOM` | "audience customizada por lista" |
| `data: [["hash"]]` (array de arrays) | só mostrar o número de registros, nunca o conteúdo |

**Proibido neste resumo:**
- Mostrar hashes, emails, telefones em claro.
- Usar palavras "SHA-256", "PII", "API" — substituir por "criptografado", "dado pessoal", "Meta".

## Preview YAML

```yaml
sub_fluxo: customer_match
fonte: Hotmart
arquivo: ~/Downloads/compradores-hotmart-2026.csv
total_linhas_csv: 1247
registros_validos: 1198
registros_descartados: 49 (formatos inválidos)
colunas_usadas: [email, telefone]

nome_final: "[FC] CustomerMatch-Compradores-Hotmart-curso-tarot"
subtype: CUSTOM
customer_file_source: USER_PROVIDED_ONLY
schema: ["EMAIL_SHA256", "PHONE_SHA256"]
total_hashes_pra_subir: 1198 (em 1 lote)

audiencia_estimada_apos_match: 360 a 720 pessoas (30-60% de 1198)
tempo_match: ~24h

confirma criar audience + subir hashes? (digite SIM)
```

## Após criar

```
✅ Audience criada: "[FC] CustomerMatch-Compradores-Hotmart-curso-tarot"

✅ Subi {N} hashes em {N_lotes} lote(s).

⏰ Meta vai cruzar os hashes com perfis Facebook/Instagram nas próximas ~24h.
   Audience aparece como "populando" até lá. Tamanho final vai aparecer no Gerenciador.

Onde gerenciar:
   Gerenciador de Anúncios → Públicos → procurar "[FC] CustomerMatch-..."

Próximos passos (depois das 24h):

🎯 Gerar Lookalike super qualificada
   /trafego-publicos → opção Lookalike → escolher essa audience como source.
   LAL gerada de Customer Match supera LAL de pixel em qualidade.

🎯 Excluir compradores das campanhas COLD
   Quando criar campanha de aquisição, adicionar essa audience como
   "audiência a excluir" no targeting. Evita gastar verba mostrando anúncio
   pra quem já comprou.

🎯 Remarketing pra base antiga
   Audience inteira é potencial alvo de upsell (produto novo) ou reativação
   (mesmo produto pra quem sumiu).

📝 Registrado em: meus-produtos/{ativo}/trafego/publicos/{audience_id}.md
   (Hash SHA-256 nunca é registrado em arquivo local — só o ID da audience.)
```

## Limites e pegadinhas confirmadas

- **Mínimo 100 registros** pra Meta aceitar criar.
- **Match típico no Brasil:** 30-60% (depende muito da fonte — base recente de WhatsApp tem match maior, base antiga de email tem match menor).
- **Limite por POST:** 10.000 registros. Listas maiores precisam ser divididas em lotes.
- **Audience expira em 90 dias** se nenhum dado novo for adicionado. Skill avisa quando criar.
- **Compliance LGPD:** aluno é responsável pela coleta legítima. Skill exige aceite no passo 4 da coleta.
- **Não dá pra deletar pessoas individuais** depois de subir. Pra remover, deletar e recriar a audience.
- **Hash é one-way.** Meta não consegue reverter pra ver o email/telefone original — só comparar com hashes dos próprios perfis.

## Próximos passos VTSD

Customer Match casa diretamente com a metodologia VTSD:

- **Quadro do produto** → quem comprou esse Quadro vira a Customer Match base.
- **3 Identidades do Consumidor** → LAL de Customer Match expande pra Identidades adjacentes.
- **Escada de produtos (low/mid/high ticket)** → Customer Match de cada produto vira fonte de upsell pro próximo nível da escada.
- **Mandala de 18 tipos** → campanhas de remarketing (Tipos 7/14/16) usam Customer Match como audience principal.

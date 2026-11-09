# Sub-fluxo. Lista de Clientes (Customer Match)

Cria um público personalizado do tipo `CUSTOM` a partir de uma lista que o aluno **já tem fora da Meta** (CSV de compradores da Hotmart, Eduzz, Kiwify, planilha do CRM etc.). Os dados viram códigos (hash SHA-256) **no computador do aluno**, pelo script local `scripts/preparar_lista_clientes.py`, e só os códigos vão para a Meta. A Meta compara esses códigos com os códigos dos perfis do Facebook e do Instagram e monta o público.

**É o caminho mais forte para público de compradores reais.** O sinal "essa pessoa pagou" vale mais que qualquer público de pixel (que só mostra "engajou").

Passo 0 (produto ativo, conexão, conta) e gate: ver `SKILL.md` desta skill.

## Regras de segurança (valem em todo o fluxo)

1. **A skill nunca abre, lê ou mostra o CSV.** Proibido usar `Read`, `cat`, `head`, `type`, `Get-Content` ou qualquer leitura do arquivo do aluno. Quem lê o arquivo é o script, que só imprime contagens e nomes de colunas.
2. **Nenhum dado pessoal em claro no chat, em log ou em arquivo do projeto.** O registro local guarda só nome do público, ID, contagens e data. No modo conector (MCP), os códigos dos lotes passam pela conversa, e isso é avisado ao aluno no passo 2, antes de ele escolher o caminho.
3. **Os lotes com códigos são temporários** e ficam fora do git (`meus-produtos/` é ignorado). Apagar a pasta dos lotes (`rm -r "meus-produtos/_global/trafego/publicos/lotes-temporarios/<pasta>"`) na hora em **qualquer saída do fluxo depois do passo 4**: depois do envio, no caminho pelo Gerenciador, no bloqueio por menos de 100 válidas, quando o aluno não quiser seguir com mais de 30% de inválidos, quando ele disser "não" no resumo ou no bloco 🛡️, quando desistir no nome, ou quando um envio falhar e ele não quiser continuar. Avisar em 1 linha: `🧹 Apaguei os arquivos temporários com os códigos.`
4. **Sem token no script.** O script não usa internet nem lê o `.env`.

## Por que usar

- **Excluir compradores das campanhas de público frio.** Não gastar verba mostrando anúncio de aquisição para quem já comprou.
- **Semelhante muito qualificado.** Semelhante gerado da lista de compradores supera o semelhante de pixel.
- **Remarketing para a base antiga.** Compradores de 6 meses ou mais que sumiram: upsell ou reativação.

## Perguntas que cobre

- "Quero subir minha lista de compradores da Hotmart"
- "Criar público com a planilha do meu CRM"
- "Excluir quem já comprou das minhas campanhas de aquisição"
- "Lookalike dos meus 5 mil compradores"

## Pré-requisitos

- **Mínimo de 100 registros válidos** para a Meta criar o público.
- **Recomendado 1.000 ou mais** para um cruzamento razoável (no Brasil, costuma bater entre 30% e 60%).
- **Termos de públicos personalizados aceitos na conta de anúncios.** Se a Meta devolver erro de termos não aceitos, o aluno aceita no Gerenciador (Públicos → Criar público → Público personalizado → Lista de clientes, a tela mostra os termos) e volta.
- **Base legal pela LGPD.** O aluno precisa ter base legal para usar esses contatos em anúncio (ex: cliente que comprou e foi informado na política de privacidade, ou consentimento). O código (hash) protege o dado no envio, mas pela LGPD ele continua sendo dado pessoal.

## Coleta de inputs (uma pergunta por mensagem)

Regra dura: **nunca agrupar 2 ou mais inputs na mesma mensagem**. O aluno nunca digita código, JSON ou nome de campo técnico.

### Ordem fixa

1. **Origem da lista.**
   ```
   De onde vem a lista que você quer subir?

   1. Hotmart (exportação de compradores)
   2. Eduzz, Kiwify, Monetizze ou Cakto (exportação)
   3. ActiveCampaign, Mailchimp ou RD Station (exportação de contatos)
   4. Planilha própria ou CRM próprio
   5. Outra fonte (descrever)

   Digite o número:
   ```
   Serve para o nome do público e para orientar a exportação (ex: na Hotmart, exportar a lista de vendas em CSV com e-mail e telefone do comprador).

2. **Explicação curta e base legal.**
   ```
   Antes de subir, dois pontos:

   🔒 Como seus dados ficam protegidos
      Um programa no seu computador transforma cada e-mail e telefone num código
      (hash). É um caminho de mão única: a Meta não consegue voltar do código para o
      e-mail. Ela só compara o código com o código dos perfis dela para achar quem
      é a mesma pessoa. O arquivo original não sai do seu computador e eu não abro
      nem leio o conteúdo dele.
      {Só no modo MCP:} Pelo conector, os códigos (não os e-mails nem os telefones)
      passam pela nossa conversa até a Meta. Se preferir que nem os códigos passem
      por aqui, dá para subir pelo Gerenciador de Anúncios: a Meta faz o código no
      seu navegador. Na próxima pergunta você escolhe o caminho.

   ⚖️ Lei de proteção de dados (LGPD)
      Mesmo em código, a lei trata esses contatos como dado pessoal. Você precisa ter
      base legal para usar essa lista em anúncio: por exemplo, compradores informados
      na sua política de privacidade, ou pessoas que autorizaram receber comunicação.

   Essa lista foi coletada de forma legítima e você pode usá-la em anúncios?

   1. Sim, tenho base legal para usar
   2. Não tenho certeza (vou parar e verificar antes)

   Digite o número:
   ```
   Se (2): cancelar com gentileza e sugerir conferir a política de privacidade e os termos da plataforma de origem antes de voltar.

2b. **Caminho do envio (só no modo MCP, em mensagem própria, para qualquer tamanho de lista).**
   ```
   Por qual caminho você quer subir a lista?

   1. Pelo conector: os códigos passam pela nossa conversa até a Meta
   2. Pelo Gerenciador de Anúncios: você envia o CSV e a Meta faz o código no
      seu navegador (uns 3 minutos, com o meu passo a passo)

   Digite o número:
   ```
   Se (2): perguntar o caminho do CSV (passo 3, só para citar o nome do arquivo no passo a passo) e o nome do público (passo 5), pular o passo 4 (o script não roda e nenhum lote é gerado) e seguir pelo "Caminho pelo Gerenciador".

3. **Caminho do CSV.**
   ```
   Qual o caminho do arquivo CSV no seu computador?
   (ex: C:\Users\aluno\Downloads\compradores-hotmart.csv ou ~/Downloads/compradores-hotmart.csv)
   ```
   Só o caminho. A skill não abre o arquivo.

4. **Preparar os lotes (roda o script).** O script leva poucos segundos, então roda sem anúncio de tempo. O 🔍 com o tempo do envio vem depois do "sim", antes de criar o público (Passo 5 do command, tabela "Anúncio de tempo por sub-fluxo"), e os passos internos do envio são o 1/2 e o 2/2 de "Roteamento por modo".

   Criar uma pasta temporária nova para os lotes, por exemplo `meus-produtos/_global/trafego/publicos/lotes-temporarios/{AAAAMMDD-HHMM}/`, e rodar com o interpretador detectado na sessão (`python3` ou `py -3`, conforme o CLAUDE.md), a partir da raiz do projeto:

   - **Modo App:**
     ```bash
     python3 .claude/skills/trafego-publicos/scripts/preparar_lista_clientes.py "<caminho_do_csv>" "meus-produtos/_global/trafego/publicos/lotes-temporarios/<pasta>"
     ```
   - **Modo MCP (lotes leves, só e-mail e telefone):**
     ```bash
     python3 .claude/skills/trafego-publicos/scripts/preparar_lista_clientes.py "<caminho_do_csv>" "meus-produtos/_global/trafego/publicos/lotes-temporarios/<pasta>" --campos email,telefone --tamanho-lote 200
     ```

   Opções do script: `--ddi 55` (código do país usado quando o telefone não tem; padrão 55), `--tamanho-lote N` (máximo 10.000, limite da Meta), `--campos email,telefone,...` (limita os campos enviados), `--coluna email="Nome da coluna"` (quando o script não reconhecer a coluna sozinho).

   O script mostra **só**: colunas usadas, linhas lidas, válidas, descartadas por campo, duplicadas e lotes gerados. Repassar ao aluno em linguagem simples. Se o script não achar a coluna de e-mail nem a de telefone, perguntar ao aluno o nome do cabeçalho (ex: "Email do Comprador") e rodar de novo com `--coluna`.

   **Validações (pelo que o script imprimiu):**
   - Menos de 100 linhas válidas: bloquear, apagar a pasta dos lotes e avisar (a Meta não cria).
   - Mais de 30% de inválidos num campo de identificação (e-mail ou telefone): avisar e perguntar se quer seguir mesmo assim. Se não quiser, apagar a pasta dos lotes.

5. **Nome do público.** Sugerir `[WS] CustomerMatch-{descricao_curta}-{produto-slug}` (ex: `[WS] CustomerMatch-Compradores-Hotmart-curso-tarot`) e perguntar "uso esse ou prefere outro?".

**Proibido:**
- Abrir, ler ou mostrar o CSV, ou mostrar qualquer linha dele.
- Pedir ao aluno código (hash), JSON, `customer_file_source` ou outro campo técnico.
- Agrupar 2 ou mais inputs na mesma mensagem.

## O que o script faz (referência)

`scripts/preparar_lista_clientes.py` (só biblioteca padrão do Python, sem internet, sem token):

| Campo | Normalização (regras da Meta) | Chave no schema |
|---|---|---|
| E-mail | minúsculo, sem espaços, formato de e-mail válido | `EMAIL` |
| Telefone | só dígitos, sem zeros à esquerda, com código do país (55 quando faltar); junta a coluna DDD se existir | `PHONE` |
| Nome | minúsculo, sem acento, sem pontuação, primeira palavra | `FN` |
| Sobrenome | minúsculo, sem acento, sem pontuação, última palavra (ou tirado do nome completo) | `LN` |
| Cidade | minúsculo, sem acento, sem espaço e sem pontuação | `CT` |
| Estado | minúsculo, sem acento, sem espaço e sem pontuação (ex: `sp`) | `ST` |
| CEP | só letras minúsculas e dígitos, sem espaço e sem traço | `ZIP` |
| País | código de 2 letras em minúsculo (ex: `br`) | `COUNTRY` |

Cada valor passa por SHA-256. Linha sem e-mail nem telefone válidos é descartada. Linhas repetidas são removidas. Cada lote é um arquivo `lote-NNN.json` no formato `payload` da Meta:

```json
{"schema": ["EMAIL", "PHONE", "FN", "LN"], "data": [["<hash>", "<hash>", "<hash>", ""], ...]}
```

Campo sem valor numa linha vai como texto vazio (`""`), como a Meta pede no formato de várias chaves. Máximo de 10.000 linhas por lote (limite da Meta por envio).

## Roteamento por modo

### Modo MCP (`MCP_CONECTOR`)

1. **Criar o público vazio** (`⏳ Passo 1/2: criar o público vazio.`): `ads_create_custom_audience` com `subtype="CUSTOM"`, `ad_account_id` e os campos que o schema pedir (inclusive a origem da lista, `customer_file_source = USER_PROVIDED_ONLY`, quando o schema tiver esse campo).
2. **Enviar os lotes** (`⏳ Passo 2/2: enviar os códigos em {N_lotes} parte(s).`): para cada `lote-NNN.json`, ler o arquivo (só códigos) e chamar `ads_update_custom_audience_users` com o `schema` e o `data` do lote, no formato que o schema da tool pedir.
   - **Antes do primeiro envio, conferir no schema como a tool recebe dado que já está em hash.** A Meta reconhece valores de 64 caracteres hexadecimais como hash. Se o schema indicar que a tool só aceita dado cru (e aplicaria hash de novo), **não usar o MCP para essa lista**: seguir pelo Gerenciador (abaixo) e apagar a pasta dos lotes.
   - Conferir em cada resposta a contagem recebida e a de inválidos; somar e informar no fim.
3. **Tamanho da lista no MCP:** os códigos passam pela conversa, então listas grandes ficam pesadas. Com até 1.000 linhas válidas, seguir pelo MCP em lotes de 200 (só e-mail e telefone). Acima disso, oferecer:
   ```
   Sua lista tem {N} contatos válidos. Pelo conector, eu teria que enviar os códigos
   em {N/200} partes pela conversa, o que fica lento. Como prefere?

   1. Subir pelo Gerenciador de Anúncios (passo a passo abaixo, uns 3 minutos)
   2. Seguir pelo conector mesmo assim, em partes

   Digite o número:
   ```

### Modo App (`APP`)

1. **Criar o público vazio** (`⏳ Passo 1/2: criar o público vazio.`):
   ```
   POST /act_<id>/customaudiences
   {
     "name": "[WS] CustomerMatch-Compradores-Hotmart-curso-tarot",
     "subtype": "CUSTOM",
     "customer_file_source": "USER_PROVIDED_ONLY",
     "description": "Lista de compradores importada em {data} ({N} registros)."
   }
   ```
   `customer_file_source`: `USER_PROVIDED_ONLY` (o aluno coletou direto, padrão), `PARTNER_PROVIDED_ONLY` (veio de parceiro com permissão, raro) ou `BOTH_USER_AND_PARTNER_PROVIDED`.

2. **Enviar cada lote num `curl` próprio** (`⏳ Passo 2/2: enviar os códigos em {N_lotes} parte(s).`), com o arquivo como valor do campo `payload` (o `<` faz o `curl` ler o conteúdo do arquivo, então o comando fica curto) e o token lido do `.env` na própria chamada, conforme a seção "LEITURA SEGURA DO .env" do CLAUDE.md. No chat, o comando aparece só assim:
   ```bash
   curl -s -X POST "https://graph.facebook.com/v25.0/<audience_id>/users?access_token=***TOKEN_MASCARADO***" -F "payload=<meus-produtos/_global/trafego/publicos/lotes-temporarios/<pasta>/lote-001.json"
   ```
   Um `Bash(curl ...)` por lote, nunca um script com vários `curl`. A resposta traz `num_received` e `num_invalid_entries`: somar e informar no fim.

### Caminho pelo Gerenciador (escolha no passo 2b, lista grande no MCP, ou tool que não aceita dado em hash)

```
Você sobe a lista em uns 3 minutos pelo Gerenciador:

📋 Passo 1. Gerenciador de Anúncios → menu "Públicos" → "Criar público" →
           "Público personalizado"
📋 Passo 2. Escolha "Lista de clientes" e clique em "Avançar"
📋 Passo 3. Se aparecerem os termos de públicos personalizados, leia e aceite
📋 Passo 4. Envie o arquivo CSV ({nome do arquivo, sem abrir o conteúdo})
📋 Passo 5. Confira se as colunas foram reconhecidas (e-mail, telefone, nome...)
📋 Passo 6. Nome do público: {nome}
📋 Passo 7. Clique em "Importar e criar"

Segundo a Meta, o Gerenciador transforma os dados em código no seu navegador
antes de enviar.

🛟 Se algum nome de botão estiver diferente, me mande um print.

Me avise com "feito" que eu confiro o público pela listagem.
```

Nesse caminho, se os lotes já tinham sido gerados (escolha depois do passo 4), apagar a pasta de lotes temporários na hora (não serão usados) e avisar em 1 linha. Escolhido no passo 2b, nenhum lote é gerado.

## Resumo em linguagem natural (obrigatório, antes do bloco 🛡️)

```
📋 Antes de eu subir essa lista para a Meta, um resumo:

Vou fazer 2 coisas:

1️⃣ Criar um público vazio chamado "{nome}" na sua conta.
2️⃣ Enviar {N} contatos em código ({emails | telefones | emails e telefones}),
   em {N_lotes} parte(s).

Sobre a proteção dos dados:
   - O e-mail e o telefone originais NÃO são enviados à Meta, só o código.
   - O código é uma "impressão digital" do dado: a Meta não consegue ler o original,
     só comparar com os códigos dos perfis do Facebook e do Instagram.
   - É o mesmo procedimento que Hotmart, Mailchimp e ActiveCampaign usam quando
     integram com a Meta.

Quantos devem bater: de 30% a 60% dos {N} contatos costumam bater com perfis ativos.
   - Público estimado: {N * 0,30} a {N * 0,60} pessoas.
   - Quem não tem Facebook ou Instagram, ou usou outro e-mail lá, não entra.

Tempo: cerca de 24h para a Meta terminar o cruzamento. Até lá, o público aparece
como "populando".

Onde vai aparecer:
   Gerenciador de Anúncios → Públicos → "[WS] CustomerMatch-..."

Está certo? (sim segue para a confirmação final, não cancela)
```

**Tradução obrigatória:**

| Campo técnico | Tradução |
|---|---|
| `EMAIL` | "e-mail em código" |
| `PHONE` | "telefone em código" |
| `customer_file_source: USER_PROVIDED_ONLY` | "lista coletada por você (compradores ou cadastros)" |
| `subtype: CUSTOM` | "público por lista" |
| conteúdo de `data` | só o número de registros, nunca o conteúdo |

**Proibido no resumo:** mostrar códigos, e-mails ou telefones; usar "SHA-256", "PII" ou "API" (dizer "código", "dado pessoal", "Meta").

## Preview YAML (dentro do bloco 🛡️)

```yaml
sub_fluxo: customer_match
modo: MCP_CONECTOR | APP
fonte: Hotmart
total_linhas_csv: 1247
registros_validos: 1198
registros_descartados: 49 (formato inválido ou sem e-mail e telefone)
campos_usados: [email, telefone]

nome_final: "[WS] CustomerMatch-Compradores-Hotmart-curso-tarot"
subtype: CUSTOM
customer_file_source: USER_PROVIDED_ONLY
schema: ["EMAIL", "PHONE"]
lotes: 1 (até 10.000 por lote no App; 200 por lote no MCP)

publico_estimado_apos_cruzamento: 360 a 720 pessoas (30% a 60% de 1198)
tempo_de_cruzamento: cerca de 24h
```

O "sim" vale para criar o público **e** enviar todos os lotes (um lote só). Se um envio falhar no meio, parar, informar quantos lotes foram e perguntar antes de continuar. Se o aluno não quiser continuar, ou disser "não" no resumo ou no bloco 🛡️, apagar a pasta dos lotes na hora e avisar em 1 linha (regra 3 de segurança).

## Depois de criar

1. **Apagar a pasta de lotes temporários** (arquivos gerados pela própria skill; não é dado do aluno):
   ```bash
   rm -r "meus-produtos/_global/trafego/publicos/lotes-temporarios/<pasta>"
   ```
2. Gravar `meus-produtos/_global/trafego/publicos/{audience_id}.md` com nome, ID, contagens, data e origem da lista. **Nunca** gravar código, e-mail ou telefone.
3. Mensagem ao aluno:

```
✅ Público criado: "[WS] CustomerMatch-Compradores-Hotmart-curso-tarot"

✅ Enviei {N} contatos em código em {N_lotes} parte(s).
   A Meta recebeu {num_received} e marcou {num_invalid_entries} como inválidos.

🧹 Os arquivos temporários com os códigos foram apagados do seu computador.

⏰ A Meta vai cruzar os códigos com os perfis do Facebook e do Instagram nas
   próximas 24h. Até lá, o público aparece como "populando".

Onde gerenciar:
   Gerenciador de Anúncios → Públicos → procurar "[WS] CustomerMatch-..."

Próximos passos (depois das 24h):

🎯 Semelhante muito qualificado
   /trafego-publicos → opção 5 → escolher esse público como origem.

🎯 Excluir compradores das campanhas de público frio
   Ao criar a campanha de aquisição (/trafego-criar-campanha), use esse público
   como "público a excluir". Evita gastar verba com quem já comprou.

🎯 Remarketing para a base antiga
   Upsell (produto novo) ou reativação: /trafego-testes opção 10.

📝 Registro em: meus-produtos/_global/trafego/publicos/{audience_id}.md
   (só o nome, as contagens e a data; nenhum dado pessoal)
```

## Limites e pegadinhas

- **Mínimo de 100 registros** para a Meta criar.
- **Cruzamento no Brasil:** de 30% a 60%, dependendo da fonte (base recente de WhatsApp bate mais; base antiga de e-mail bate menos).
- **Limite por envio:** 10.000 registros. Listas maiores viram vários lotes.
- **Público de lista sem atualização** pode ser marcado como desatualizado pela Meta depois de um tempo sem uso. A skill avisa ao criar.
- **Não dá para tirar pessoas uma a uma** pela skill. Para remover, excluir e recriar o público.
- **O código é de mão única.** A Meta não reverte para o e-mail ou telefone original, só compara.

## Ligação com o método VTSD

- **Quadro do produto** → quem comprou esse Quadro vira a lista base.
- **Identidade do Consumidor** → o semelhante da lista amplia para quem tem o mesmo perfil.
- **Escada de produtos** (low, middle, high ticket) → a lista de cada produto é a origem do upsell para o próximo degrau.
- **Mandala da Criatividade** → campanhas com objetivo RMKT usam a lista como público principal (ex: tipos Prova e Oportunidade).

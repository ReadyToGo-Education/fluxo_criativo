# Sub-skill. Leitura de Resultado de Teste

Lê o resultado de um teste A/B que já rodou, classifica, registra o aprendizado e sugere o próximo teste. É a forma padrão de fechar o ciclo de qualquer teste criado pela `/trafego-testes`. A `/trafego-analise` (Criativos & Copy) entra só como complemento, para uma leitura VTSD mais ampla dos criativos.

Passo 0: ver `SKILL.md` desta skill. Só leitura: não passa pelo bloco 🛡️.

## Quando é acionada

- Opção [11] do menu: "Ler resultado de teste"
- Quando o aluno diz "como ficou meu teste?", "lê o resultado do A/B", "o teste terminou"
- Quando passou o 7º dia e o aluno volta

🔍 Anúncio: `🔍 Próximo passo: puxar as métricas das variações e classificar o teste (8 passos). Tempo estimado: cerca de 60 segundos.`

## Fluxo

### Passo 1. Identificar o teste

```
Qual teste você quer ler?

1. {testes com status "rodando" em meus-produtos/{ativo}/entregas/trafego/testes/*.md}
2. Informar o nome do teste

Digite o número ou o nome:
```

Sem testes registrados: "Não encontrei testes registrados. Você criou o teste pela `/trafego-testes`? Se sim, o arquivo deveria estar em `meus-produtos/{ativo}/entregas/trafego/testes/`." Se o teste foi feito como teste A/B oficial da Meta e não tem arquivo, no MCP dá para achá-lo com `ads_experiment_list_tests`.

### Passo 2. Contaminação (antes de julgar)

**Uma pergunta, uma mensagem:**

```
Antes de ler o resultado, preciso saber:

Durante os {X} dias do teste, alguma mudança na conta pode ter afetado o resultado?

1. Não, nada mudou
2. Sim, mudei o orçamento
3. Sim, mudei o público
4. Sim, mexi na página de destino
5. Sim, mudei o criativo ou o texto
6. Sim, outra mudança

Digite o número:
```

| Resposta | Ação |
|---|---|
| 1 (nada mudou) | Leitura normal |
| 2 a 6 (algo mudou) | Classificar como `contaminado`. Explicar: "O resultado pode não refletir o que foi testado porque {mudança} aconteceu durante o teste." Recomendar refazer. Se a mudança foi pequena (ex: 5% no orçamento), considerar `repetir_com_ajuste` em vez de `contaminado`. |

No MCP, para conferir o que mudou, dá para consultar o histórico de alterações da conta com `ads_account_get_activity_logs`.

### Passo 3. Puxar os dados

Ler o `.md` do teste para pegar:
- Entidades das variações A e B (anúncio, conjunto ou campanha)
- Métrica principal e secundárias
- Critérios de vitória, parada e inconclusivo
- Janela e conversões mínimas

Puxar as métricas pela `/trafego-insights`:
- Período: do início do teste até hoje
- Métricas: gasto, impressões, frequência, CTR, CPC, CPA, ROAS, conversões, métricas de vídeo (se for vídeo)

**Teste A/B oficial da Meta** (`modelo: ab_oficial_meta`): no MCP, ler o resultado com `ads_experiment_abtest_get_test` (traz a vencedora e a confiança calculadas pela Meta) e completar com a `/trafego-insights` para as métricas secundárias.

### Passo 4. Classificar

6 classificações:

| Classificação | Critério | Significado |
|---|---|---|
| `validado` | Variação venceu na métrica principal + volume mínimo atingido + diferença acima do limite | Vencedora confirmada. Pode escalar ou aplicar. |
| `invalidado` | Variação perdeu na métrica principal + volume mínimo atingido | Hipótese descartada. Aprendizado: essa abordagem não funciona. |
| `promissor` | Sinais bons, mas volume abaixo do mínimo | Manter rodando. Reavaliar em mais 7 dias. |
| `inconclusivo` | Volume muito baixo ou diferença menor que 5% entre A e B | Dado insuficiente. Estender a janela ou subir o orçamento do teste. |
| `contaminado` | Mudanças durante o teste (Passo 2) | Resultado não confiável. Refazer. |
| `repetir_com_ajuste` | Resultado misto: a principal melhorou, a secundária piorou | Ex: taxa de gancho subiu, mas o CPA piorou. Ajustar o desenho e testar de novo. |

O mínimo de conversões vem do arquivo do teste (50 por lado em low e middle ticket, 30 em high ticket, conforme o tipo no resumo do produto).

### Passo 5. Efeitos colaterais

Mesmo com a principal melhor, conferir se alguma secundária piorou muito:

```
Métrica principal: taxa de gancho A 22% → B 34% (+55%) ✅
Métrica secundária: CTR A 1,8% → B 1,2% (-33%) ⚠️
Métrica secundária: CPA A R$ 120 → B R$ 145 (+21%) ⚠️

Efeito colateral: o gancho novo chama atenção, mas não gera intenção qualificada.
Classificação: repetir_com_ajuste.
```

### Passo 6. Preencher o resultado no arquivo

Atualizar `meus-produtos/{ativo}/entregas/trafego/testes/{slug}.md`:
- Seção "Resultado": classificação, métricas, contaminação
- Seção "Aprendizado": o que funcionou, o que não, repetir, evitar, próximo teste
- Status: de "rodando" para "concluído" ou "inconclusivo"

### Passo 7. Registrar no INDEX

Atualizar a linha do teste em `meus-produtos/{ativo}/entregas/trafego/testes/INDEX.md`.

### Passo 8. Sugerir o próximo teste

| Resultado | Sugestão |
|---|---|
| `validado` | "Escalar a vencedora pela `/trafego-escalar`. Ou testar uma variação da vencedora (novo ângulo do mesmo conceito)." |
| `invalidado` | "Hipótese descartada. Próximo teste: {abordagem alternativa a partir do aprendizado}." |
| `promissor` | "Manter rodando mais 7 dias. Se o volume não subir, aumentar o orçamento do teste em 30%." |
| `inconclusivo` | "Estender a janela ou subir o orçamento. Se depois de 14 dias continuar inconclusivo, refazer o desenho." |
| `contaminado` | "Refazer o teste limpo (uma variável, sem mudanças durante)." |
| `repetir_com_ajuste` | "Ajustar {variável do efeito colateral} e testar de novo." |

Quando o próximo teste pede criativo ou texto novo: `/copy-anuncio`, `/criativo-estatico` ou `/mandala-de-anuncios`. Para ler os criativos pelo método VTSD com mais profundidade: `/trafego-criativos` ou `/trafego-analise` (Criativos & Copy). Pausar a perdedora é decisão do aluno; se ele quiser, é uma escrita com bloco 🛡️ própria (pela `/trafego-otimizar`).

## Explicação obrigatória

Toda classificação vem explicada, em linguagem simples:

```
RESULTADO DO TESTE: "Gancho de vídeo curto vs longo"
Classificação: REPETIR COM AJUSTE ⚠️

O que aconteceu: o gancho curto (B) subiu a taxa de gancho em 55%
(de 22% para 34%). Mais gente parou de rolar a tela.

Porém: o CTR caiu 33% e o CPA subiu 21%. O gancho novo chama atenção,
mas quem para não é quem compra.

Aprendizado: gancho visual forte atrai curioso, não comprador. Para
converter, o gancho precisa qualificar (ex: abrir com um resultado concreto
em vez de uma polêmica).

Próximo teste: mesmo vídeo, com gancho que abre por um número de resultado
real do produto, em vez do visual forte. Manter A como controle.
```

(Se o próximo teste sugerir um gancho ou headline escrita pela skill, o texto passa pela "AUTO-REVISÃO OBRIGATÓRIA DE COPY" do CLAUDE.md antes de aparecer. Número de resultado só se for real, vindo do resumo do produto ou do aluno.)

## Saída YAML

```yaml
leitura_resultado:
  teste_slug: "gancho-video-curto-vs-longo"
  teste_arquivo: "meus-produtos/{ativo}/entregas/trafego/testes/gancho-video-curto-vs-longo.md"
  periodo: { inicio: "2026-05-25", fim: "2026-06-01" }
  modelo: adsets_separados | ads_mesmo_adset | campanhas_separadas | ab_oficial_meta

  variacoes:
    a: { id: "<id>", gasto: 450, conversoes: 28, cpa: 120, metrica_principal: 0.22 }
    b: { id: "<id>", gasto: 430, conversoes: 18, cpa: 145, metrica_principal: 0.34 }

  classificacao: validado | invalidado | promissor | inconclusivo | contaminado | repetir_com_ajuste
  contaminacao: nenhuma | { tipo: "orcamento_alterado", descricao: "..." }

  efeitos_colaterais:
    - metrica: ctr
      a: 0.018
      b: 0.012
      variacao: -0.33
      impacto: negativo

  aprendizado:
    o_que_funcionou: "Gancho curto aumenta a atenção"
    o_que_nao_funcionou: "Atenção não virou intenção qualificada"
    repetir: "Formato curto (15s)"
    evitar: "Gancho visual sem ligação com a oferta"
    proximo_teste: "Gancho com resultado concreto (número real)"

  proximo_teste_sugerido:
    tipo: "gancho"
    hipotese: "Gancho com resultado concreto qualifica melhor"
    prioridade: alta
```

---
name: workshop-marketing:trafego-dashboard
description: Abre, cria ou atualiza o dashboard de tráfego do Meta Ads. Verifica se o aluno já tem um dashboard (artefato do Claude ligado ao conector da Meta) e entrega o link; se não tiver, monta o dashboard a partir do modelo (visão geral com comparação, funil, ritmo do dia, campanhas com anúncios, dia a dia) e salva o link em meus-produtos/dashboard-trafego.md. Para conta que a Meta ainda não liberou no conector, monta o dashboard com dados gravados pelo App (o token fica só no computador do aluno). Com as credenciais da Hotmart ou da Kiwify no .env, inclui as vendas reais com bump, upsell e origem; sem elas, oferece ligar depois. Use quando o aluno pedir "meu dashboard", "painel de anúncios", "dashboard de tráfego", "atualiza as vendas do dashboard" ou quiser ajustar o dashboard. Para mandar o dashboard ao analisador da mentoria, o caminho é o /trafego-dashboard-analisador.
---

# Tráfego Dashboard. Seu Painel do Meta Ads

Entrega ao aluno um dashboard da conta de anúncios, guardado na conta Claude dele, que busca os números novos na Meta com um clique em "Atualizar dados".

A especificação técnica (modelo, scripts, registro, publicação, vendas da Hotmart e da Kiwify, diagnóstico, ajustes e legado) está em `.claude/skills/trafego-dashboard/SKILL.md`. Este command é o roteiro com o aluno.

---

## Passo 0. Procurar um dashboard que já existe

Abrir ou ajustar um dashboard não depende do `.env`: quem busca os dados é o conector da conta Claude do aluno. A exceção é buscar números novos num dashboard com dados gravados, que usa o token do App (Passo 6B).

Seguir a seção 3 da skill (registro em `meus-produtos/dashboard-trafego.md` e, se estiver vazio, a lista de artefatos). Se a lista trouxer candidatos, perguntar (numerado) se algum é o dashboard do aluno, com a opção "Nenhum desses"; o escolhido vai para o registro.

**Se o aluno pediu "atualiza as vendas do dashboard":** ir direto para o Passo 6.

**Se o aluno quer mandar o dashboard para o analisador da mentoria (card do Fluxer):** seguir o `/trafego-dashboard-analisador`. O link deste painel não abre os números para o analisador.

**Se o aluno pediu "atualiza o meu dashboard" e o registro diz `Fonte dos números: App da Meta (dados gravados)`:** ir direto para o Passo 6B. No dashboard ao vivo, lembrar que é só clicar em "Atualizar dados" no painel.

**Se encontrar um dashboard:**

```
Você já tem um dashboard.

📊 {nome do dashboard}
Link: {URL}

O que quer fazer?

1. Só abrir (o link acima já está pronto)
2. Ajustar este dashboard
3. Atualizar as vendas do checkout       ← só se o registro disser que Hotmart ou Kiwify está ligada
4. Buscar os números novos da Meta       ← só se o registro disser "App da Meta (dados gravados)"
5. Criar um dashboard novo
6. Encerrar

Digite o número:
```

Numerar só as opções que aparecem.

- **Só abrir:** repetir o link e lembrar do botão "Atualizar dados". Encerrar.
- **Ajustar:** Passo 5.
- **Vendas do checkout:** Passo 6.
- **Números novos da Meta:** Passo 6B.
- **Dashboard novo:** Passo 1. O novo dashboard precisa de outro nome (pergunta 2.0), senão sobrescreve o que já existe.
- **Encerrar:** encerrar sem perguntar mais nada.

Se houver mais de um dashboard no registro, listar todos numerados e perguntar qual abrir.

**Se não encontrar:** Passo 1.

---

## Passo 1. Ver se dá para fazer o dashboard

Conferir os requisitos da seção 4.1 da skill.

**Ferramenta `Artifact` indisponível:**

```
O dashboard é publicado como uma página na sua conta Claude, e isso só
funciona no Claude Code dentro do app do Claude (Desktop). Por aqui
consigo montar o dashboard estático, uma fotografia dos números de agora.

1. Montar o dashboard estático
2. Encerrar (vou abrir o app do Claude e rodar /trafego-dashboard lá)

Digite o número:
```

- **1:** Passo 7 (legado).

**Conector da Meta:** descobrir o nome conforme a seção 4.2 da skill. Se for preciso perguntar:

```
Qual é o nome do conector da Meta na sua conta do Claude?
(Ele aparece em claude.ai, Configurações, Conectores.)

1. Meta MCP
2. Meta Ads
3. Ainda não adicionei o conector da Meta
4. Outro nome (digite como aparece)

Digite o número:
```

- **3:** se o aluno está no App porque a Meta ainda não liberou a conta dele no conector, adicionar o conector não resolve: ir para o dashboard com dados gravados (abaixo). Senão, seguir o Passo 2A do `/trafego-conexao` (adicionar o conector) e voltar aqui. Se o aluno preferir não conectar, oferecer os dados gravados ou o Passo 7 (legado). **Não trocar `META_AUTH_MODO`** sem o aluno pedir.

**Conta liberada no conector.** Com as ferramentas do conector na conversa, ler `ads_get_ad_accounts` e separar as contas liberadas (`is_ads_mcp_enabled` e `is_queryable` diferentes de `false`) das não liberadas. Seguir a tabela da seção 4.1.1 da skill:

- **Todas as contas que o aluno usa estão liberadas:** dashboard ao vivo (Passo 2).
- **Nenhuma liberada:**

  ```
  A Meta ainda não liberou a sua conta de anúncios no conector do Claude
  (ela libera conta por conta). Por isso o painel ao vivo, que lê a conta
  pelo conector, abriria vazio.

  Dá para ter o mesmo painel com os números buscados pelo App da Meta:
  eu busco os números aqui no seu computador e gravo no painel. A sua
  chave da Meta fica só no seu computador e nunca vai para a página. Os
  números atualizam quando você me pede, ou sozinhos no horário que você
  escolher.

  1. Montar o painel com os números buscados pelo App (recomendado)
  2. Montar a fotografia de uma análise, no seu computador
  3. Encerrar

  Digite o número:
  ```

  - **1:** conferir se `FB_ACCESS_TOKEN_PERMANENTE` tem valor (`grep -q "^FB_ACCESS_TOKEN_PERMANENTE=." .env`). Se tiver, Passo 2 com `fonte: "app"`. Se não tiver, configurar o App pelo `/trafego-conexao` (caminho do App) e voltar aqui, sem trocar `META_AUTH_MODO` sem o aluno pedir.
  - **2:** Passo 7 (legado).
- **Algumas liberadas e outras não:**

  ```
  Algumas das suas contas já estão liberadas no conector da Meta e outras
  ainda não: {lista das não liberadas, com nome e id mascarado}.

  1. Painel ao vivo só com as contas liberadas
  2. Painel com os números buscados pelo App, com todas as contas
  3. Encerrar

  Digite o número:
  ```

Sem as ferramentas do conector na conversa, não dá para conferir a liberação. Se o aluno estiver no App (`META_AUTH_MODO=APP`), perguntar se a conta já foi liberada no conector e, na dúvida, oferecer os dados gravados. Nunca publicar um painel ao vivo sem nenhuma conta liberada.

---

## Passo 2. Perguntas antes de criar

Uma pergunta por vez.

**2.0 Nome (só quando o aluno já tem um dashboard).** Cada dashboard tem a sua pasta; com o mesmo nome, o novo sobrescreveria o antigo.

```
Como quer chamar este novo dashboard?
(ex: "Cliente Papel Semente", "Lançamento de março")
```

O nome vira o título da página e a pasta (`meus-produtos/_dashboard-trafego/{slug do nome}/`). Se o slug já existir, acrescentar `-2`.

**2.1 Contas de anúncios.** Quando as ferramentas do conector da Meta estão na conversa, listar as contas com `ads_get_ad_accounts` (só as liberadas para leitura) e mostrar com número, nome, id mascarado e moeda:

```
Quais contas de anúncios entram no dashboard?

1. Todas as contas abaixo, com seletor no topo
2. Conta Principal (act_1234...7890) · R$
3. Cliente X (act_2345...8901) · R$
4. Conta antiga (act_3456...9012) · US$

Digite um número ou vários separados por vírgula:
```

Sem as ferramentas do conector na conversa, perguntar sem pedir id:

```
Quais contas de anúncios entram no dashboard?

1. Todas as que o conector enxerga, com seletor no topo
2. Só algumas (diga o nome de cada uma como aparece no Gerenciador)

Digite o número:
```

**No painel com dados gravados (`fonte: "app"`),** as contas vêm do `.env` (`FB_AD_ACCOUNT_IDS` ou `FB_AD_ACCOUNT_ID`). Para mostrar o nome de cada uma, rodar `meta-app.py --verificar` (seção 5.1 da skill), que lê as contas sem mostrar o token. Perguntar quais entram como acima e gravar a lista em `contas` no `config.json`.

Contas em moedas diferentes podem entrar juntas: o painel mostra cada conta na moeda dela e, em "Todas as contas", soma só as contas da moeda principal.

**2.2 Vendas do checkout.** Verificar no `.env` só se existem as variáveis da Hotmart (`HOTMART_CLIENT_ID` e `HOTMART_CLIENT_SECRET`) ou da Kiwify (`KIWIFY_CLIENT_ID`, `KIWIFY_CLIENT_SECRET` e `KIWIFY_ACCOUNT_ID`). Nunca exibir valores.

- **Existem as de uma plataforma:** seguir a seção 6.2 da skill (verificar, listar produtos, perguntar produto principal, bumps, upsell e janela, uma pergunta por vez).
- **Existem as das duas:** perguntar qual plataforma vende o produto deste dashboard (1. Hotmart / 2. Kiwify) e seguir a seção 6.2.
- **Não existem:** não perguntar nada sobre checkout agora. A oferta vem depois da entrega (Passo 4).

**2.3 Confirmação.**

```
Resumo do dashboard que vou criar:
- Contas: {todas, com seletor | lista}
- Números da Meta: {ao vivo, pelo conector {nome} | buscados pelo App
  e gravados no painel, atualizados quando você pedir}
- Seções: visão geral com comparação ao período anterior, funil,
  ritmo de hoje por hora, campanhas com anúncios e detalhe, dia a dia
- Vendas: {pelo pixel da Meta | Hotmart ou Kiwify, produto principal
  {nome}, bump {nome}, upsell {nome}}

1. Tudo certo, pode criar
2. Quero ajustar algo

Digite o número:
```

---

## Passo 3. Criar e publicar

```
🔍 Próximo passo: montar e publicar o seu dashboard de tráfego (3 passos). Tempo estimado: cerca de 90 segundos.
```

Com vendas do checkout, o tempo é o de "Montar e publicar o dashboard com vendas do checkout" em `.claude/rules/tempo-estimado.md`.

- `⏳ Passo 1/3: preparar a configuração do dashboard.` (`config.json`, seção 2.1 da skill)
- `⏳ Passo 2/3: montar a página.` (seção 5, item 2)
- `⏳ Passo 3/3: publicar na sua conta Claude e salvar o link.` Com vendas do checkout: `⏳ Passo 3/3: publicar na sua conta Claude, enviar as vendas e salvar o link.` (seção 5, itens 3 a 5)

**Painel com dados gravados** (seção 5.1 da skill): o tempo é o de "Montar e publicar o dashboard com dados gravados (App)" em `.claude/rules/tempo-estimado.md`, e são 4 passos:

- `⏳ Passo 1/4: preparar a configuração do dashboard.`
- `⏳ Passo 2/4: montar a página.`
- `⏳ Passo 3/4: publicar na sua conta Claude.`
- `⏳ Passo 4/4: buscar os números da Meta, gravar no painel e salvar o link.` (com vendas do checkout, enviar as vendas também)

---

## Passo 4. Entrega

```
✅ Concluído: seu dashboard de tráfego está pronto.

Link: {URL}

Na primeira vez que abrir, o Claude pede permissão para o painel ler sua
conta de anúncios pelo conector da Meta. A primeira leitura leva até
1 minuto. Depois disso o painel abre na hora com a última leitura, e o
botão "Atualizar dados" busca os números novos.

O link ficou salvo no projeto. Para ver de novo, é só pedir
"abre meu dashboard".
```

**Painel com dados gravados:**

```
✅ Concluído: seu dashboard de tráfego está pronto.

Link: {URL}

Os números são da Meta, buscados agora há pouco pelo App e gravados no
painel ({dia e hora}). Para números novos, é só me pedir "atualiza o meu
dashboard": eu busco de novo e gravo, sem mudar o link. A sua chave da
Meta não vai para o painel.

Antes de compartilhar o link: quem tiver acesso ao painel vê os números
da sua conta.

O link ficou salvo no projeto. Para ver de novo, é só pedir
"abre meu dashboard".
```

No painel com dados gravados, a primeira pergunta depois da entrega é a atualização automática dos números (seção 5.1 da skill), uma vez. As vendas do checkout e a pergunta de fixar seguem como abaixo.

Terminar a mensagem de entrega pedindo só uma coisa: "Abra o link e me avise quando os números aparecerem." Uma pergunta por vez, nesta ordem, cada uma depois da resposta da anterior:

1. **Quando o aluno avisar que abriu:** ler o diagnóstico (seção 7 da skill), corrigir o que aparecer e confirmar em uma linha o que o painel leu ("4 campanhas e 11 anúncios lidos, sem erro").
2. **Vendas do checkout:**
   - Sem Hotmart nem Kiwify ligada: fazer a oferta da seção 6.4 da skill, uma vez.
   - Com Hotmart ou Kiwify ligada: oferecer a atualização automática das vendas (seção 6.6 da skill), uma vez.
3. **Por último:** "Quer que eu fixe o dashboard na barra lateral do Claude?" Se sim, `Artifact` com `action: "pin"`. Nunca fixar sem o aluno pedir.

---

## Passo 5. Ajustar o dashboard

```
O que quer mudar no dashboard?
(ex: "trocar a conta", "mudar a meta de ROAS para 2", "tirar o ritmo de
hoje", "incluir a coluna de alcance", ou mande um print de um dashboard
que você gosta para eu usar como referência)
```

Mostrar o resumo do ajuste e pedir confirmação (1. Pode aplicar / 2. Quero mudar algo). Seguir a seção 8 da skill, alterando **só** o que foi pedido:

```
🔍 Próximo passo: aplicar o ajuste no seu dashboard. Tempo estimado: cerca de 90 segundos.
```

```
✅ Concluído: dashboard atualizado. O link continua o mesmo: {URL}
```

---

## Passo 6. Atualizar as vendas do checkout

```
🔍 Próximo passo: buscar as vendas novas da {Hotmart | Kiwify} e atualizar o dashboard. Tempo estimado: cerca de 60 segundos.
```

Seguir a seção 6.3 da skill (coletor e envio para o banco do artefato; a página não precisa ser publicada de novo). Antes de gravar, avisar: "Vou gravar as vendas no seu painel. O Claude vai mostrar um pedido de permissão: clique em permitir."

```
✅ Concluído: vendas atualizadas até {hora}. Abra o dashboard e clique em "Atualizar dados".
```

---

## Passo 6B. Buscar os números novos da Meta (painel com dados gravados)

```
🔍 Próximo passo: buscar os números novos da Meta e atualizar o dashboard. Tempo estimado: cerca de 60 segundos.
```

Seguir "Buscar e enviar os números" na seção 5.1 da skill (coletor no computador do aluno e envio para o banco do artefato; a página não precisa ser publicada de novo). Antes de gravar, avisar: "Vou gravar os números da Meta no seu painel. O Claude vai mostrar um pedido de permissão: clique em permitir." Se o coletor devolver `ERRO_TOKEN` ou `ERRO_CREDENCIAIS`, explicar em linguagem simples e levar ao `/trafego-conexao` (caminho do App).

```
✅ Concluído: números da Meta atualizados até {hora}. Abra o dashboard e clique em "Atualizar dados".
```

Se a Meta já tiver liberado a conta no conector, oferecer trocar para o painel ao vivo (fim da seção 5.1 da skill).

---

## Passo 7. Dashboard estático (legado)

Ler `.claude/skills/trafego-dashboard/references/legado-dashboard-estatico.md` e seguir.

---

## Regras

1. **Primeiro procurar, depois criar.**
2. **Só leitura.** O dashboard não pausa, não ativa e não muda orçamento. Para executar ações, `/trafego-otimizar`.
3. **Nunca mostrar código** nem detalhes técnicos ao aluno.
4. **Nunca exibir token nem credencial**, nem do `.env` nem de lugar nenhum. Credenciais da Hotmart ou da Kiwify recebidas no chat vão direto para o `.env`, sem eco.
4a. **O token do App da Meta nunca vai para a página**, para o `config.json`, para o banco do artefato nem para o registro. No painel com dados gravados, ele só é usado pelo coletor, no computador do aluno.
4b. **Nunca publicar um painel ao vivo sem nenhuma conta liberada no conector.**
5. **O link fica em `meus-produtos/dashboard-trafego.md`.** Nunca no `CLAUDE.md`.
6. **Uma pergunta por vez**, sempre com opções numeradas.

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-analise
Com os números na tela, rode a análise narrada pelo método VTSD para
entender o porquê de cada métrica e o que fazer a seguir.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

---
name: "source-command-trafego-dashboard"
description: "Abre ou cria o dashboard de tráfego do Meta Ads ao vivo. Verifica se o aluno já tem um dashboard ativo (artefato do Claude conectado ao MCP da Meta) e entrega o link; se não tiver, cria o dashboard e salva o link em meus-produtos/dashboard-trafego.md. Sem o conector da Meta, oferece conectar ou segue pelo dashboard estático (legado). Use quando o aluno pedir \"meu dashboard\", \"painel de anúncios\", \"dashboard de tráfego\", \"dashboard ao vivo\" ou quiser ajustar o dashboard."
---

# source-command-trafego-dashboard

Use esta skill quando o usuário pedir o comando `/trafego-dashboard` do workshop (ou `trafego-dashboard`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/trafego-dashboard.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Tráfego Dashboard. Seu Painel do Meta Ads ao Vivo

Entrega ao aluno um dashboard da conta de anúncios que busca os números sozinho, toda vez que ele abre o link. É um só dashboard, guardado na conta Claude dele, que pode ser personalizado com o tempo.

A especificação técnica (registro do link, como montar e publicar, métricas, ajustes e legado) está em `.claude/skills/trafego-dashboard/SKILL.md`. Este command é o roteiro com o aluno.

---

## Passo 0. Procurar um dashboard que já existe

Este passo vem antes da conexão com a Meta: abrir ou ajustar um dashboard que já existe não depende do `.env`, porque quem busca os dados é o conector da conta Claude do aluno.

Seguir a seção 2 da skill (registro em `meus-produtos/dashboard-trafego.md` e, se estiver vazio, a lista de artefatos do aluno). Se a lista trouxer candidatos, perguntar (numerado) se algum é o dashboard do aluno, com a opção "Nenhum desses"; o escolhido vai para o registro.

**Se encontrar um dashboard:**

```
Você já tem um dashboard ativo.

📊 {nome do dashboard}
Link: {URL}
Conta: {nome da conta} (act_1234...7890)

O que quer fazer?

1. Só abrir (o link acima já está pronto)
2. Ajustar este dashboard (incluir ou tirar indicadores, gráficos ou filtros)
3. Criar um dashboard novo
4. Encerrar

Digite o número:
```

- **1:** repetir o link e lembrar do botão "Atualizar agora". Encerrar.
- **2:** ir para o Passo 5.
- **3:** ir para o Passo 1.
- **4:** encerrar sem perguntar mais nada.

Se houver mais de um dashboard no registro, listar todos numerados antes e perguntar qual abrir.

**Se não encontrar:** ir para o Passo 1.

---

## Passo 1. Conexão Meta (só para criar)

Ler `META_AUTH_MODO` no `.env`.

- **Vazio ou ausente:** acionar `/trafego-conexao` e voltar aqui quando terminar.
- **`MCP_CONECTOR` ou `APP`:** seguir. Quem decide o caminho do dashboard é o Passo 2.

Não ler nem exibir token nenhum neste command. O dashboard ao vivo não usa o token do `.env`.

---

## Passo 2. Ver se dá para fazer o dashboard ao vivo

Conferir os requisitos da seção 3 da skill e seguir o caso que valer.

**Caso A. Conector da Meta ativo e ferramenta `Artifact` disponível:** ir para o Passo 3.

**Caso B. `META_AUTH_MODO=APP` (App via Facebook Developers):**

```
Seu projeto está conectado à Meta pelo App do Facebook Developers
(token no .env). O dashboard ao vivo funciona pelo conector MCP da
Meta dentro do Claude: é ele que deixa o painel buscar os números
sozinho, toda vez que você abre.

1. Conectar o MCP da Meta agora (recomendado, leva cerca de 1 minuto)
2. Seguir sem o MCP, com o dashboard estático (fotografia que não
   se atualiza)

Digite o número:
```

- **1:** seguir as instruções do Passo 2A do `/trafego-conexao` (adicionar o conector personalizado) e a validação MCP do Passo 3 dele. **Não trocar `META_AUTH_MODO`** sem o aluno pedir: as outras skills de tráfego continuam usando o App. Se as ferramentas do conector ainda não aparecerem na sessão, pedir para reabrir o Claude Code e rodar `/trafego-dashboard` de novo.
- **2:** ir para o Passo 6 (legado).

**Caso C. `META_AUTH_MODO=MCP_CONECTOR`, mas nenhuma ferramenta do conector aparece na sessão:**

```
Não encontrei o conector da Meta nesta conversa. Confirme:

- O conector (ex.: "Meta Ads") aparece como conectado em
  Personalizar > Conectores, no app do Claude?
- Você abriu esta conversa depois de conectar? Conector recém-adicionado
  só aparece em conversas novas.

1. Já conferi, tentar de novo
2. Seguir sem o MCP, com o dashboard estático

Digite o número:
```

**Caso D. A ferramenta `Artifact` não está disponível nesta sessão:**

```
O dashboard ao vivo é publicado como uma página na sua conta Claude,
e isso só funciona no Claude Code dentro do app do Claude (Desktop).
Por aqui consigo montar o dashboard estático, uma fotografia dos
números de agora.

1. Montar o dashboard estático
2. Encerrar (vou abrir o app do Claude e rodar /trafego-dashboard lá)

Digite o número:
```

---

## Passo 3. Perguntas antes de criar

Uma pergunta por vez.

**3.1 Contas de anúncios.** Listar as contas pelo conector (ferramenta de leitura de contas). Se houver só uma, usar ela e pular a pergunta.

```
Quais contas de anúncios entram no dashboard?

1. Só a principal: {nome} (act_1234...7890)
2. Escolher algumas
3. Todas ({N} contas), com seletor no topo

Digite o número:
```

**3.2 Confirmação do conteúdo.**

```
Resumo do dashboard que vou criar:
- Contas: {contas escolhidas}
- Filtros: período (padrão últimos 7 dias, com datas personalizadas) e campanha
- Indicadores: investimento, impressões, alcance, frequência, CPM,
  cliques no link, CTR, CPC, visualizações da página, connect rate,
  resultados (compras ou leads), CPA ou CPL e ROAS
- Gráfico: investimento e resultados por dia
- Tabela: desempenho por campanha
- Botão "Atualizar agora"

1. Tudo certo, pode criar
2. Quero ajustar algo

Digite o número:
```

Se escolher 2, perguntar o que incluir ou tirar e mostrar o resumo de novo.

---

## Passo 4. Criar e publicar

```
🔍 Próximo passo: montar o dashboard ao vivo da sua conta de anúncios (4 passos). Tempo estimado: 3 a 5 minutos.
```

- `⏳ Passo 1/4: preparar a ligação do painel com a Meta.` (seções 4.1 a 4.3 da skill)
- `⏳ Passo 2/4: montar a página do dashboard.` (seções 4.4 a 4.6)
- `⏳ Passo 3/4: publicar o dashboard na sua conta Claude.` (seção 4.7)
- `⏳ Passo 4/4: salvar o link no projeto.` (registro da seção 1)

Entregar com a mensagem da seção 4.8 da skill e oferecer fixar na barra lateral.

Fechar com a dica:

```
Dica: para personalizar com calma, deixe uma conversa só para o
dashboard. Sempre que quiser mudar algo, rode /trafego-dashboard e
escolha "Ajustar este dashboard".
```

---

## Passo 5. Ajustar o dashboard

Perguntar:

```
O que quer mudar no dashboard?
(ex: "tirar o gráfico de frequência", "incluir CTR único", "mostrar só a
campanha de remarketing", ou mande um print de um dashboard que você
gosta para eu usar como referência)
```

Mostrar o resumo do ajuste e pedir confirmação (1. Pode aplicar / 2. Quero mudar algo). Depois anunciar e seguir a seção 5 da skill, alterando **só** o que foi pedido:

```
🔍 Próximo passo: aplicar o ajuste no seu dashboard. Tempo estimado: cerca de 90 segundos.
```

```
✅ Concluído: dashboard atualizado. O link continua o mesmo: {URL}
```

---

## Passo 6. Dashboard estático (legado)

Ler `.claude/skills/trafego-dashboard/references/legado-dashboard-estatico.md` e seguir.

---

## Regras

1. **Primeiro procurar, depois criar.** Nunca criar um dashboard novo sem antes verificar o registro e a lista de artefatos.
2. **Só leitura.** O dashboard não pausa, não ativa e não muda orçamento. Para executar ações, `/trafego-otimizar`.
3. **Nunca mostrar código** nem detalhes técnicos ao aluno. Ele recebe o link e uma explicação curta.
4. **Nunca exibir token**, nem do `.env` nem de lugar nenhum.
5. **O link fica em `meus-produtos/dashboard-trafego.md`.** Nunca no `CLAUDE.md`.
6. **Uma pergunta por vez**, sempre com opções numeradas.

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-analise
Com os números na tela, rode a análise narrada pelo método VTSD para
entender o porquê de cada métrica e o que fazer a seguir.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

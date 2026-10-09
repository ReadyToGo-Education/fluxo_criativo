---
name: "source-command-trafego-dashboard"
description: "Abre, cria ou atualiza o dashboard de tráfego do Meta Ads. Verifica se o aluno já tem um dashboard (artefato do Claude ligado ao conector da Meta) e entrega o link; se não tiver, monta o dashboard a partir do modelo (visão geral com comparação, funil, ritmo do dia, campanhas com anúncios, dia a dia) e salva o link em meus-produtos/dashboard-trafego.md. Com as credenciais da Hotmart ou da Kiwify no .env, inclui as vendas reais com bump, upsell e origem; sem elas, oferece ligar depois. Use quando o aluno pedir \"meu dashboard\", \"painel de anúncios\", \"dashboard de tráfego\", \"atualiza as vendas do dashboard\" ou quiser ajustar o dashboard."
---

# source-command-trafego-dashboard

Use esta skill quando o usuário pedir o comando `/trafego-dashboard` do workshop (ou `trafego-dashboard`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/trafego-dashboard.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Tráfego Dashboard. Seu Painel do Meta Ads

Entrega ao aluno um dashboard da conta de anúncios, guardado na conta Claude dele, que busca os números novos na Meta com um clique em "Atualizar dados".

A especificação técnica (modelo, scripts, registro, publicação, vendas da Hotmart e da Kiwify, diagnóstico, ajustes e legado) está em `.claude/skills/trafego-dashboard/SKILL.md`. Este command é o roteiro com o aluno.

---

## Passo 0. Procurar um dashboard que já existe

Abrir ou ajustar um dashboard não depende do `.env`: quem busca os dados é o conector da conta Claude do aluno.

Seguir a seção 3 da skill (registro em `meus-produtos/dashboard-trafego.md` e, se estiver vazio, a lista de artefatos). Se a lista trouxer candidatos, perguntar (numerado) se algum é o dashboard do aluno, com a opção "Nenhum desses"; o escolhido vai para o registro.

**Se o aluno pediu "atualiza as vendas do dashboard":** ir direto para o Passo 6.

**Se encontrar um dashboard:**

```
Você já tem um dashboard.

📊 {nome do dashboard}
Link: {URL}

O que quer fazer?

1. Só abrir (o link acima já está pronto)
2. Ajustar este dashboard
3. Atualizar as vendas do checkout       ← só se o registro disser que Hotmart ou Kiwify está ligada
4. Criar um dashboard novo
5. Encerrar

Digite o número:
```

- **1:** repetir o link e lembrar do botão "Atualizar dados". Encerrar.
- **2:** Passo 5.
- **3:** Passo 6.
- **4:** Passo 1. O novo dashboard precisa de outro nome (pergunta 2.0), senão sobrescreve o que já existe.
- **5:** encerrar sem perguntar mais nada.

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

- **3:** seguir o Passo 2A do `/trafego-conexao` (adicionar o conector) e voltar aqui. Se o aluno preferir não conectar, Passo 7 (legado). **Não trocar `META_AUTH_MODO`** sem o aluno pedir.

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

Contas em moedas diferentes podem entrar juntas: o painel mostra cada conta na moeda dela e, em "Todas as contas", soma só as contas da moeda principal.

**2.2 Vendas do checkout.** Verificar no `.env` só se existem as variáveis da Hotmart (`HOTMART_CLIENT_ID` e `HOTMART_CLIENT_SECRET`) ou da Kiwify (`KIWIFY_CLIENT_ID`, `KIWIFY_CLIENT_SECRET` e `KIWIFY_ACCOUNT_ID`). Nunca exibir valores.

- **Existem as de uma plataforma:** seguir a seção 6.2 da skill (verificar, listar produtos, perguntar produto principal, bumps, upsell e janela, uma pergunta por vez).
- **Existem as das duas:** perguntar qual plataforma vende o produto deste dashboard (1. Hotmart / 2. Kiwify) e seguir a seção 6.2.
- **Não existem:** não perguntar nada sobre checkout agora. A oferta vem depois da entrega (Passo 4).

**2.3 Confirmação.**

```
Resumo do dashboard que vou criar:
- Contas: {todas, com seletor | lista}
- Conector: {nome}
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

## Passo 7. Dashboard estático (legado)

Ler `.claude/skills/trafego-dashboard/references/legado-dashboard-estatico.md` e seguir.

---

## Regras

1. **Primeiro procurar, depois criar.**
2. **Só leitura.** O dashboard não pausa, não ativa e não muda orçamento. Para executar ações, `/trafego-otimizar`.
3. **Nunca mostrar código** nem detalhes técnicos ao aluno.
4. **Nunca exibir token nem credencial**, nem do `.env` nem de lugar nenhum. Credenciais da Hotmart ou da Kiwify recebidas no chat vão direto para o `.env`, sem eco.
5. **O link fica em `meus-produtos/dashboard-trafego.md`.** Nunca no `CLAUDE.md`.
6. **Uma pergunta por vez**, sempre com opções numeradas.

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 Próximo passo recomendado: /trafego-analise
Com os números na tela, rode a análise narrada pelo método VTSD para
entender o porquê de cada métrica e o que fazer a seguir.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

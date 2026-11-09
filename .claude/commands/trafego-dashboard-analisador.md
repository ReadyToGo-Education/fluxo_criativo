---
name: workshop-marketing:trafego-dashboard-analisador
description: Só para mandar o dashboard de tráfego ao analisador da Mentoria Fluxo. Tira uma fotografia fixa dos números que o dashboard do aluno mostrou na última atualização, publica como uma página que o analisador consegue abrir e devolve o link para colar no card "Planilha ou Dash para acompanhar os dados de tráfego" do Fluxer. Use somente quando o aluno digitar /trafego-dashboard-analisador ou pedir para mandar, entregar ou compartilhar o dashboard com o analisador ou no Fluxer. Para ver, criar, ajustar ou atualizar o próprio dashboard, o caminho é o /trafego-dashboard.
---

# Tráfego Dashboard para o Analisador. Fotografia para o Fluxer

O link do dashboard de tráfego do aluno não serve para o analisador da mentoria: o painel lê a Meta pela conta de quem abre, então o analisador não vê os números do aluno. Este command publica uma **fotografia**: uma página fixa, com os números da última atualização do dashboard, que o analisador abre pelo link colado no Fluxer.

A especificação técnica está na seção 5.2 de `.claude/skills/trafego-dashboard/SKILL.md`. Este command é o roteiro com o aluno.

---

## Passo 0. Ver se dá para publicar

A fotografia é publicada com a ferramenta `Artifact` (aparece na sessão ou com `ToolSearch`). Sem ela:

```
A fotografia para o analisador é publicada na sua conta Claude, e isso só
funciona no Claude Code dentro do app do Claude (Desktop). Abra o Severino
no app do Claude e rode /trafego-dashboard-analisador lá.
```

Encerrar.

---

## Passo 1. Achar o dashboard

Seguir a seção 3 da skill (registro em `meus-produtos/dashboard-trafego.md` e, se estiver vazio, a lista de artefatos).

- **Mais de um dashboard:** listar numerados e perguntar qual vai para o analisador.
- **Nenhum dashboard:**

  ```
  Para mandar ao analisador, primeiro você precisa do dashboard de tráfego.
  Vou criar agora e, no fim, volto para a fotografia.
  ```

  Seguir o `/trafego-dashboard` do Passo 1 ao Passo 4, até o aluno avisar que os números apareceram. Depois, Passo 2 daqui.
- **Dashboard antigo, feito à mão antes do modelo** (só `meus-produtos/_dashboard-trafego/{slug}.html`, sem `config.json`): ele não guarda a fotografia. Explicar em uma frase e seguir o `/trafego-dashboard` para criar um dashboard novo pelo modelo.

---

## Passo 2. Conferir os números guardados

1. **Painel montado antes da fotografia:** procurar `guardarFotografia` no `index.html` da pasta do dashboard. Se não estiver lá, o painel precisa ser montado de novo pelo modelo (seção 5.2 da skill, item 1). Se o registro disser `Personalizado: sim`, perguntar antes:

   ```
   Para mandar ao analisador, o seu dashboard precisa ser montado de novo
   pelo modelo atual. As mudanças de visual que você pediu nele se perdem.

   1. Pode montar de novo
   2. Cancelar

   Digite o número:
   ```

2. **Ler o que o painel guardou:** `ArtifactData` com `action: "get"`, a URL do dashboard, `collection: "fotografia"` e `doc_id: "info"`. Se existir e `numerosEmIso` for de menos de 24 horas, ir para o Passo 3.

3. **Sem números ou números velhos:**
   - Painel com dados gravados (`Fonte dos números: App da Meta` no registro): buscar os números novos antes, pelo Passo 6B do `/trafego-dashboard`.
   - Pedir ao aluno:

     ```
     Abra o seu dashboard e clique em "Atualizar dados":
     {URL do dashboard}

     Quando os números aparecerem, me avise por aqui.
     ```

   - Quando o aluno avisar, ler `info` de novo. Se continuar sem números novos, ler o diagnóstico (seção 7 da skill), procurar erro que começa com `fotografia:` e explicar o problema em linguagem simples. Não montar a fotografia com números velhos.

---

## Passo 3. Tirar e publicar a fotografia

```
🔍 Próximo passo: tirar a fotografia do seu dashboard e publicar o link para o analisador. Tempo estimado: cerca de 60 segundos.
```

Seguir a seção 5.2 da skill, itens 2 a 5 (baixar os números, montar a página, publicar sem conector e gravar o link no registro).

---

## Passo 4. Entrega

**Primeira fotografia:**

```
✅ Concluído: a fotografia do seu dashboard está pronta para o analisador.

Link: {URL da fotografia}
Números da Meta de {atualizadoEm}.

Falta um passo seu: o link começa privado e, assim, o analisador não
consegue abrir.
1. Abra o link.
2. Clique em Compartilhar, no alto da página.
3. Em "Acesso geral", troque "Apenas você" por "Qualquer pessoa com o link".
4. Cole o link no Fluxer, no card "Planilha ou Dash para acompanhar os
   dados de tráfego".

Quem tiver o link vê os números da fotografia: investimento, faturamento e
campanhas. As vendas não levam nome nem e-mail de quem comprou.

A fotografia não muda sozinha. Até 48 horas antes da sua próxima análise,
rode /trafego-dashboard-analisador de novo: os números são atualizados e o
link continua o mesmo.
```

**Fotografia atualizada (o registro já tinha o link):**

```
✅ Concluído: fotografia atualizada com os números da Meta de {atualizadoEm}.

Link: {URL da fotografia}

O link é o mesmo de antes. Se ele já está no card do Fluxer, com o acesso
geral em "Qualquer pessoa com o link", não precisa fazer mais nada.
```

---

## Regras

1. **Só para o analisador.** Para ver, criar, ajustar ou atualizar o próprio dashboard, o caminho é o `/trafego-dashboard`.
2. **Nunca mandar ao analisador o link do dashboard ao vivo.** Ele não mostra os números do aluno para outra pessoa.
3. **A fotografia só leva os números que o painel do aluno guardou.** Nunca montar com a demonstração nem com números escritos ou copiados à mão.
4. **Nunca exibir token nem credencial.** A fotografia não leva nenhum.
5. **O link da fotografia fica no registro**, na linha "Link para o analisador". Nunca no `CLAUDE.md`.
6. **Nunca mostrar código** nem detalhes técnicos ao aluno.
7. **Uma pergunta por vez**, sempre com opções numeradas.

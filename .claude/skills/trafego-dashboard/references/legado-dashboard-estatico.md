# Legado. Dashboard Estático (sem MCP)

Caminho antigo do dashboard de tráfego, mantido para quem não usa o conector MCP da Meta. Ele continua funcionando igual a antes: o dashboard é a **fotografia de uma análise** do `/trafego-analise`, gravada em HTML no computador do aluno.

O `/trafego-dashboard` só chega aqui em dois casos:

1. O aluno usa o App via Facebook Developers (`META_AUTH_MODO=APP`), foi avisado de que o dashboard ao vivo precisa do conector MCP da Meta e **decidiu não conectar**.
2. A sessão não tem a ferramenta `Artifact` (por exemplo, Claude Code rodando só no terminal), então não dá para publicar o dashboard ao vivo.

---

## 1. Avisar o que o aluno vai receber

Antes de gerar, mostrar:

```
Vou montar o dashboard estático. Ele é uma fotografia dos números
de agora: não se atualiza sozinho. Para ver dados novos, é preciso
rodar a análise de novo e salvar outra fotografia.

Se um dia quiser o dashboard ao vivo, rode /trafego-conexao e conecte
o MCP da Meta. Depois é só chamar /trafego-dashboard de novo.
```

---

## 2. Gerar a fotografia

**Se o aluno veio do fim de uma análise do `/trafego-analise`** (a análise já foi entregue nesta conversa): acionar direto `.claude/skills/trafego-analise/sub-skills/_export-html.md` com os dados dessa análise. É exatamente o comportamento antigo da opção "Salvar como dashboard".

**Se o aluno chamou `/trafego-dashboard` sem análise feita:** a fotografia precisa de uma análise. Rodar o fluxo do `/trafego-analise` com o output **[1] Diagnóstico Rápido** (conta de anúncios, status das campanhas, escopo e período, como manda a skill), entregar a análise narrada e, no fim, acionar o `_export-html.md`. Avisar antes:

```
O dashboard estático é montado a partir de uma análise. Vou rodar o
Diagnóstico Rápido da sua conta e, no fim, salvar como dashboard.
```

O `_export-html.md` cuida de tudo o que já fazia: salva em `meus-produtos/{ativo}/trafego/analise/{slug}-{YYYY-MM-DD-HHMM}.html`, atualiza o card no painel de entregas do produto e abre no navegador.

---

## 3. Regras do legado

1. **Nada muda nos arquivos antigos.** O `_export-html.md`, o `painel-trafego.py` e a pasta `trafego/analise/` seguem como estão.
2. **Não gravar nada em `meus-produtos/dashboard-trafego.md`.** Esse registro é só do dashboard ao vivo.
3. **Sempre deixar claro que é fotografia**, com a data e a hora no topo (o `_export-html.md` já faz isso).
4. **Sempre lembrar que existe o ao vivo**, uma única vez por conversa, sem insistir.

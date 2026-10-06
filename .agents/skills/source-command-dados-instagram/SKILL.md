---
name: "source-command-dados-instagram"
description: "Analisar um perfil do Instagram coletando dados públicos (bio, últimos posts, engajamento, temas recorrentes, horários). Gera dashboard HTML com filtros (tipo de post, engajamento, tema) e relatório escrito com insights práticos de conteúdo para o aluno usar."
---

# source-command-dados-instagram

Use esta skill quando o usuário pedir o comando `/dados-instagram` do workshop (ou `dados-instagram`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/dados-instagram.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Dados Instagram. Análise de Perfil com Dashboard

Pega um perfil do Instagram, coleta dados públicos dos posts recentes e entrega um dashboard HTML interativo com filtros + um relatório escrito em markdown com insights acionáveis. Serve para analisar o próprio perfil do aluno ou de um concorrente.

## Usage

```
/dados-instagram @perfil
```

## O Que Fazer

Acione a skill `dados-instagram` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo`. Se não houver produto, oriente a usar `/produto-novo`.
2. Coletar (uma pergunta por vez):
   1. Qual o usuario do perfil no Instagram? (so o nome, sem o arroba — ex: meuperfil)
   2. O objetivo é auditar o próprio perfil ou estudar um concorrente?
   3. Quantos posts recentes analisar? (padrão 30)
3. Fazer uma busca via WebSearch com `site:instagram.com @perfil` e por ferramentas públicas (ex: `inflact.com/@perfil`, `picuki.com/profile/perfil`, `inbeat.co`) para coletar dados públicos básicos. Se não conseguir extração direta, pedir pro aluno exportar dados via uma das ferramentas listadas ou colar manualmente uma planilha com as colunas: data, tipo, tema, legenda, curtidas, comentários, salvamentos (se tiver).
4. Processar os dados calculando:
   - Taxa de engajamento média (curtidas + comentários / seguidores)
   - Melhor horário de postagem
   - Tipo de post que mais engaja (Reels, carrossel, imagem)
   - Temas recorrentes (extrair palavras-chave das legendas)
   - Posts com melhor e pior performance
5. Gerar um arquivo HTML `meus-produtos/{ativo}/entregas/dados/instagram-{perfil}.html` com:
   - Cards de métricas no topo
   - Gráfico simples em Canvas ou SVG puro (barras de engajamento por post)
   - Tabela filtrável por tipo, tema, engajamento (JS vanilla, sem libs externas)
   - Seção de insights (bullets curtos)
6. Gerar também um relatório em `.md` no mesmo diretório com insights escritos em português simples e sugestões de conteúdo baseadas no que já funciona.
7. Sugerir próximo passo: usar os insights em `/copy-carrossel` pra criar conteúdo alinhado ao que funciona.

## Regras Resumidas

- Nunca usar scraping que viole termos de serviço do Instagram. Preferir ferramentas públicas que o aluno já tem acesso ou export manual.
- Dashboard em HTML puro (sem React, sem Chart.js). JS inline, canvas ou SVG para gráficos.
- Filtros funcionam 100% no cliente, sem backend.
- Relatório escrito tem que ter 5 a 10 insights acionáveis, não só descritivos.
- Não usar travessão em nenhum texto exibido.

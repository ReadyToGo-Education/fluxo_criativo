---
name: workshop-marketing:criar-agente
description: Criar o agente de IA do produto para entregar aos alunos como bônus, order bump ou produto. Faz as seis perguntas, gera 10 ideias de agente que entregam algo pronto e escreve as instruções. Dois caminhos. quem vende na Hotmart recebe a ficha e as instruções para colar no Agente de IA da Hotmart; quem vende em outra plataforma (Kiwify, Eduzz, Greenn) recebe o plugin do ChatGPT pronto em .zip, com a aula para a área de membros. Também atualiza um agente já criado e converte um GPT antigo (os GPTs saem do ar em 11/12/2026). Use quando o aluno pedir "criar agente", "agente de IA do meu produto", "bônus com IA", "assistente para os meus alunos", "plugin do ChatGPT", "agente na Hotmart" ou "meu GPT vai sair do ar".
---

# Criar Agente de IA

Cria o agente de IA que o infoprodutor entrega aos alunos dele, pelo caminho que serve para onde ele vende:

1. **Na Hotmart:** Agente de IA da Hotmart, com ficha e instruções para colar no cadastro.
2. **Em outra plataforma:** plugin do ChatGPT, um arquivo .zip que o aluno instala no ChatGPT dele, até na conta gratuita.

Substitui o antigo `/criar-gpt`. Os GPTs personalizados do ChatGPT saem do ar em 11/12/2026.

## Usage

```
/criar-agente
```

## O Que Fazer

Anuncie antes de começar, conforme `.claude/rules/tempo-estimado.md`:

```
🔍 Próximo passo: criar o agente de IA do seu produto (6 passos). Tempo estimado: 3 a 5 minutos.
```

Leia `.claude/skills/agente-ia/SKILL.md` e siga o fluxo:

- **Modo:** criar um agente novo, atualizar um agente já criado ou trazer um GPT antigo.
- **Passo 0:** contexto do produto ativo (`resumo-produto.md`).
- **Passo 1:** as seis perguntas, uma por vez, pulando o que o resumo já responde. A pergunta "Onde você vende hoje?" decide o caminho.
- **Passo 2:** 10 ideias de agente que terminam em algo pronto na mão do aluno, com uma recomendada.
- **Passo 3:** resumo do agente para aprovar.
- **Passo 4:** instruções do agente para aprovar.
- **Passo 5:** Hotmart (ficha, instruções, cadastro e entrega como bônus) ou plugin (`.zip` montado pelo script da skill, instalação, aula da área de membros).
- **Passo 6:** as 8 mensagens de teste.

## Onde salvar

- Com produto ativo: `meus-produtos/{ativo}/entregas/produto/agente-{slug}/`
- Sem produto ativo: `entregas/agente-{slug}/`

## Finalizar

Depois da aprovação, salve, mostre o caminho absoluto de cada arquivo e confirme:

```
✅ Concluído: agente {nome} pronto para {a Hotmart | instalar como plugin}. Caminho: {pasta do agente}.
```

Não sugira melhorias que o aluno não pediu.

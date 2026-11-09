---
name: "source-command-estrategia-lancamento"
description: "Planejar lançamento ou evento completo. cronograma, estrutura de pico de vendas, comunicação pré-evento, pitch e oferta. Baseado nas metodologias VTSD e C10X."
---

# source-command-estrategia-lancamento

Use esta skill quando o usuário pedir o comando `/estrategia-lancamento` do workshop (ou `estrategia-lancamento`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/estrategia-lancamento.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Lançamento. Planejamento Completo de Evento

Planeja lançamento ou evento usando a estrutura C10X (High Ticket via eventos) e Pico de Vendas do VTSD.

## Usage

```
/estrategia-lancamento
```

## O Que Fazer

### 1. Contexto
Leia `meus-produtos/{ativo}/resumo-produto.md` (se não existir, gere conforme o CLAUDE.md).

### 2. Entrevista (UMA pergunta por vez, com progresso visual)

**Bloco 1/4. Tipo de Evento:**
```
Qual tipo de evento?

1. Retiro Online (imersão de 1-3 dias)
2. Webinar/Aula ao vivo (evento único com pitch)
3. Lançamento clássico (CPLs + abertura de carrinho)
4. Desafio (3-7 dias com missões)

Digite o número:
```

```
--- Bloco 1/4 concluído ---
Evento: [tipo escolhido]
Próximo: Data
---
```

**Bloco 2/4. Data:**
```
Qual a data planejada para o evento?
(ex: "15 de abril de 2026", "daqui 30 dias", "ainda não defini")
```

```
--- Bloco 2/4 concluído ---
Evento: [tipo]
Data: [data]
Próximo: Metas
---
```

**Bloco 3/4. Metas:**
```
Qual a meta de participantes e de vendas?
(ex: "500 inscritos, meta de R$50k em vendas")
```

```
--- Bloco 3/4 concluído ---
Evento: [tipo]
Data: [data]
Meta: [participantes] inscritos, R$ [valor] em vendas
Próximo: Orçamento
---
```

**Bloco 4/4. Orçamento:**
```
Qual o orçamento de tráfego para o evento?
(ex: "R$2.000", "R$5.000", "ainda não defini")
```

**Confirmação antes de gerar:**
```
Resumo do lançamento:
- Tipo: [tipo de evento]
- Data: [data]
- Meta: [participantes] inscritos, R$ [valor] vendas
- Orçamento: R$ [valor]

1. Tudo certo, pode gerar
2. Quero ajustar algo
```

### 3. Geração

**Estrutura do Plano:**

1. **Big Idea do Evento (C10X):**
   - Promessa do evento
   - Mote (máx 5 palavras, memorável)
   - Oferta do evento

2. **Cronograma completo:**
   - Comunicação pré-evento (WhatsApp + Email)
   - Agenda do evento
   - Abertura de carrinho
   - Fechamento

3. **Materiais necessários:**
   - Página de inscrição
   - Sequência de emails (convite → lembrete → carrinho)
   - Anúncios de captação
   - Script do pitch
   - Página de vendas

4. **Estrutura de Campanha:**
   - Campanha 1: Aquisição (cadastros)
   - Campanha 2: Remarketing
   - Métricas de acompanhamento

### 4. Salvar
`meus-produtos/{ativo}/entregas/textos-de-venda/lancamento-[evento].md`

### 5. Próximo Passo
"Plano salvo. Comece criando os materiais: `/copy-pagina` para a página do evento e `/copy-anuncio` para os anúncios de aquecimento."

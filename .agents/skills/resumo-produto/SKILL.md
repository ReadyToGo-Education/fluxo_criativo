---
name: resumo-produto
description: >
  Resumo do produto ativo (meus-produtos/{ativo}/resumo-produto.md): um arquivo curto com tudo o
  que as entregas precisam da concepção (Quadro, Furadeira, identidades, público, objeções,
  Urgências Ocultas, Decorados principais e síntese da pesquisa de mercado). É o contexto padrão de
  todas as skills, no lugar de ler perfil.md, idconsumidor.md e pesquisa-mercado.md inteiros.
  Define o modelo do resumo, quando ele é gerado, quando é refeito e onde buscar o detalhe completo.
---

# Resumo do Produto

Os três arquivos da concepção somam perto de 100 KB num produto real (perfil, identidade do consumidor e pesquisa de mercado). Ler tudo antes de cada entrega deixa o Claude lento. O resumo junta, em um arquivo de no máximo 18 KB, o que as entregas usam de verdade.

**Arquivo:** `meus-produtos/{ativo}/resumo-produto.md`
**Quem gera:** o agente `gerador-resumo-produto`, seguindo o modelo da seção 3.

---

## 1. Como usar (regra para todas as skills)

1. **Tentar ler direto** `meus-produtos/{ativo}/resumo-produto.md`. Não conferir antes se existe.
2. **Se não for encontrado:**
   - Se `meus-produtos/{ativo}/perfil.md` tiver o Quadro preenchido: anunciar `⏳ Preparando o resumo do seu produto (só na primeira vez).`, acionar o agente `gerador-resumo-produto` (síncrono) com o slug do produto e ler o resumo que ele gravar. Quem não puder acionar outro agente (ex.: um sub-agente sem a ferramenta de agentes) gera o resumo ele mesmo, seguindo a seção 3, e grava no mesmo caminho.
   - Se o `perfil.md` não existir ou estiver vazio (sem Quadro): orientar `/produto-concepcao`. Não gerar resumo de perfil vazio.
3. **O resumo é o contexto padrão.** Só ler um arquivo original quando a tarefa precisar de um detalhe que o resumo não tem, e mesmo assim **só a seção indicada** na tabela da seção 4.

**Quem continua lendo os originais inteiros:** quem escreve, revisa ou gera a concepção (`/produto-concepcao`, `/gerar-furadeira`, `/furadeira-visual`, `/produto-zerar`, revisores, geradores de Decorados, Urgências e identidade do consumidor, pesquisa de mercado) e os scripts do painel. O resumo é para quem **consome** a concepção.

---

## 2. Quando é gerado e quando é refeito

| Momento | O que acontece |
|---|---|
| Fim do `/produto-concepcao` (produto novo) | Gerado logo depois que a identidade do consumidor é revisada |
| Produto antigo, sem resumo | Gerado na primeira entrega que precisar dele (seção 1, passo 2) |
| O Claude grava `perfil.md`, `idconsumidor.md` ou `pesquisa-mercado.md` | O hook `.claude/hooks/resumo-invalidar.js` apaga o resumo daquele produto. A próxima entrega não encontra o arquivo e o resumo é gerado de novo, já atualizado |

Ninguém edita o resumo à mão. Para mudar algo, muda-se o arquivo original.

---

## 3. Modelo do resumo

Regras de escrita:

- **Literal onde importa:** Quadro, Furadeira (nome do método e etapas), preço e nome do produto entram copiados do original, sem paráfrase. O resumo nunca pode contradizer o que o aluno aprovou.
- **Condensado no resto:** identidades, público e pesquisa viram tópicos curtos com os dados concretos (números, nomes, faixas de preço). Sem frase genérica.
- **Sem inventar:** se uma seção inteira não existir no original (ex.: produto sem pesquisa de mercado), escrever `Não disponível.` na seção. Se só um campo não existir, usar o campo equivalente do original (ex.: "Evitar na comunicação" para "Não gosta") ou omitir a linha. Nunca deduzir um campo a partir de outra informação.
- **Divergência entre os originais:** vale o `perfil.md`, que é o que o aluno aprovou. Registrar a divergência em uma linha (ex.: na síntese da pesquisa: "a pesquisa considerou 21 dias; o formato aprovado é de 14").
- **Sem casos com nome de pessoa:** exemplos com nome próprio nas objeções ou na pesquisa (ex.: "a Fernanda tentou...") ficam de fora. No resumo eles podem virar depoimento inventado numa copy.
- **Tamanho máximo: 18 KB** (1 KB = 1.024 bytes). Se passar, encurtar as seções condensadas, nunca as literais.
- Português do Brasil com acentuação correta. Sem travessão.

```markdown
# Resumo do Produto: {nome do produto}

> Gerado em {AAAA-MM-DD} a partir de perfil.md, idconsumidor.md e pesquisa-mercado.md.
> Contexto padrão das entregas. Não edite: ele é refeito sozinho quando os originais mudam.
> Para o detalhe completo, veja a tabela "Onde está o detalhe completo" no fim.

## Produto
- Nome: {nome}
- Tipo: {Low Ticket | Middle Ticket | High Ticket} (de tipo.md)
- Preço: {preço} (de preco.md ou do perfil)
- Nicho: {nicho}
- Formato: {curso, mentoria, ebook, planilha, quiz...}
- Instagram: {@ do perfil, só se existir no original}
- Cores da marca: {só se existirem no original}

## Quadro
{texto literal do Quadro}

## Furadeira
{nome do método e mecânica, literal}
1. {macroetapa 1, literal}
2. {macroetapa 2, literal}
...

## Identidade do Produto
- Posicionamento: {1 linha}
- Diferencial: {1 a 2 linhas}
- Promessa: {1 linha}

## Identidade do Comunicador
- Nome: {nome}
- Tom: {1 linha}
- Valores: {lista curta}
- Gosta: {lista curta} | Não gosta: {lista curta}
- Mantras e jargões: {lista literal}

## Público (Identidade do Consumidor)
- Perfil: {gênero, idade, profissão, renda, região}
- Sonho: {frase literal}
- Canais: {onde busca informação}
- Frases que diria: {3 a 5 frases literais}
- Como se comunicar: {2 a 3 tópicos}
- Paliativos: {só Middle Ticket; concorrentes que resolvem pela metade}

## Objeções principais
1. {título literal}: {o argumento mais forte, em 1 a 2 frases}
2. ...
(as 5 objeções)

## Argumentos Incontestáveis
- {até 5, os mais fortes, literais}

## Urgências Ocultas
### Dores
- {as 10, uma linha cada, literais}
### Dúvidas
- ...
### Desejos
- ...
### Assuntos Relacionados
- ...
### Urgências Quentes
- ...
### Urgências Frias
- ...
### Urgências Inusitadas
- ...

## Decorados principais
- Financeiro: {2 itens}
- Tempo: {2 itens}
- Autoestima: {2 itens}
- Reputação: {2 itens}
- Crescimento: {2 itens}

## Pesquisa de mercado (síntese)
- Tamanho e crescimento: {números}
- Preço praticado: {faixa}
- Concorrentes principais: {3 a 5, nome + promessa + preço}
- Objeções reais do público: {3, de Reclame Aqui e fóruns}
- Assuntos quentes: {3 ângulos}
- Riscos e cuidados: {1 a 2, regulatórios ou éticos}
- Oportunidade de posicionamento: {1 a 2 linhas da síntese estratégica}

## Onde está o detalhe completo
| Preciso de | Ler só esta parte |
|---|---|
| Os 50 Decorados | `perfil.md`, seção `## Decorados (Benefícios)` |
| Identidades completas | `perfil.md`, seções `## Identidade do Produto` e `## Identidade do Comunicador` |
| Objeções com os 7 argumentos | `idconsumidor.md`, seção `## Objeções de Compra` |
| Baldes "Para quem é" | `idconsumidor.md`, seção `## Baldes de Para Quem É` |
| Concorrentes, YouTube, anúncios, fontes | `pesquisa-mercado.md`, seções 2, 7, 8 e Fontes |
```

As Urgências Ocultas entram inteiras (as 70) porque são a fonte obrigatória de temas de anúncio, bullets, ganchos e emails. Em uma linha cada, cabem no limite.

---

## 4. Onde está o detalhe completo

A mesma tabela do fim do modelo. Exemplos de quando uma skill precisa dela:

| Skill | Lê do original |
|---|---|
| Páginas de vendas (`/copy-pagina`, `paginas`) | Os 50 Decorados para bullets, os baldes "Para quem é" e as objeções com os 7 argumentos para a seção de objeções e o FAQ |
| `/comercial-playbook` | Objeções com os 7 argumentos |
| Pesquisa de concorrentes e referências | Seções específicas da pesquisa de mercado |

Sempre ler o resumo primeiro e só depois a seção específica.

# Referências Visuais. Layouts para a Furadeira

Quinze layouts de referência para representar visualmente um método (Furadeira). Cada layout corresponde a uma estrutura diferente de método. A escolha correta do layout é obrigatória antes de gerar o HTML — o visual deve refletir como o método funciona, não apenas o que o aluno prefere esteticamente.

---

## Tabela de Decisão Rápida

| Estrutura do método | Layout recomendado | Template |
|---|---|---|
| Fases sequenciais, 3-5 etapas | Roadmap Vertical | `02-roadmap-vertical.html` |
| Fases sequenciais, para slides/apresentação | Linear Horizontal | `01-linear-horizontal.html` |
| 3 elementos interdependentes que se encaixam | Puzzle 3 Peças | `06-puzzle-3pecas.html` |
| 4-6 fases progressivas com sub-passos | Hexágonos em Cadeia | `07-hexagonos-cadeia.html` |
| 3-4 perfis ou trilhas paralelas | Grid de Categorias | `08-grid-categorias.html` |
| 4 pilares + núcleo central | Hub Central / Diamante | `04-hub-central.html` |
| Funil ou hierarquia (base → topo) | Pirâmide Invertida | `03-piramide-invertida.html` |
| Caminhos diferentes por perfil do aluno | Fluxograma Condicional | `05-fluxograma-condicional.html` |
| Caminho com zigzag, marco de chegada | Trilha Zigzag | template embutido no SKILL.md |
| 4 quadrantes opostos com elemento central | Quadrantes 2x2 | `09-quadrantes-2x2.html` |
| Roda com N pontos conectados por linhas | Roda com Pontos | `10-roda-eneagrama.html` |
| 8 setores em roda/bússola/octógono | Roda Octogonal | `11-roda-octogonal.html` |
| Anéis concêntricos com seções e subníveis | Mandala Concêntrica | `12-mandala-concentrica.html` |
| Jornada com paradas numeradas e bônus | Trilha Ondulada | `13-trilha-ondulada.html` |
| Níveis de resultado em curva exponencial | Curva Exponencial | `14-curva-exponencial.html` |
| Escala de comportamento com lógica condicional | Régua de Comportamento | `15-regua-comportamento.html` |
| Círculo central com letras + 4 quadrantes numerados ao redor | Hub Numerado com Quadrantes | `16-hub-numerado-quadrantes.html` |

---

## 1. Roadmap Vertical (`02-roadmap-vertical.html`)

**Estrutura:** Milestones empilhados verticalmente com linha central conectando, microetapas como bullets abaixo de cada marco.

**Quando usar:** Método com 3 a 6 fases sequenciais em que cada etapa constrói sobre a anterior. É o layout mais universal para Furadeiras lineares. Formato 1080×1920px (stories/vertical).

**Exemplo real:** Método Fluência 3F (Fonética → Fluência → Fixação), Protocolo Anticoceira.

**Paleta padrão:** Roxo (`#7c3aed`) — adaptável.

---

## 2. Linear Horizontal (`01-linear-horizontal.html`)

**Estrutura:** Cards lado a lado com setas conectando, formato slide/apresentação.

**Quando usar:** Mesmo critério do Roadmap, mas quando o destino é uma apresentação de slides, pitch deck ou tela de computador. Formato 1920×1080px (landscape).

**Exemplo real:** Qualquer método com 3 a 5 fases mostrado em slide de aula.

**Paleta padrão:** Azul (`#2563eb`) — adaptável.

---

## 3. Puzzle 3 Peças (`06-puzzle-3pecas.html`)

**Estrutura:** Três peças de quebra-cabeça encaixadas em diagonal com número (1, 2, 3) e texto descritivo na lateral de cada peça.

**Quando usar:** Método com exatamente 3 fases ou pilares que se encaixam — uma depende da anterior para funcionar. Transmite interdependência. Funciona muito bem para sistemas de aprendizado progressivo, habilidades encadeadas (ex: Números → Ritmo → Notas no Sistema Tríplice da Leitura Musical).

**NÃO usar quando:** O método tem 4 ou mais fases, ou quando as fases são paralelas (independentes).

**Paleta:** Vibrante, peças em cores contrastantes (amarelo, magenta, roxo). Fundo branco.

**Referência visual:** `metodo-puzzle-3pecas.png` na pasta references.

---

## 4. Hexágonos em Cadeia (`07-hexagonos-cadeia.html`)

**Estrutura:** Hexágonos empilhados verticalmente, numerados (1, 2, 3, 4…), cada hexágono com ícone + número. Texto descritivo nas laterais alternando esquerda e direita. Sub-passos separados por seta (→).

**Quando usar:** Método com 4 a 6 fases sequenciais em que cada etapa tem múltiplas sub-tarefas ou conceitos. É mais denso que o Roadmap Vertical — ideal quando precisa mostrar complexidade sem perder clareza visual. Boa opção para métodos com acrônimos (ex: 4 C's da Lapidação: Compreensão → Convicção → Compromisso → Conversão).

**NÃO usar quando:** O método tem apenas 2-3 fases simples sem sub-passos.

**Paleta:** Cores fortes diferentes por etapa (ex: vinho, azul-escuro, verde, vermelho). Fundo branco. Números em branco dentro dos hexágonos.

**Referência visual:** `metodo-hexagonos-4c.png` na pasta references.

---

## 5. Grid de Categorias (`08-grid-categorias.html`)

**Estrutura:** 3 ou 4 colunas lado a lado, cada coluna com: rótulo em destaque acima, bloco de imagem/ícone, lista de atributos/códigos abaixo. Visual limpo e simétrico.

**Quando usar:** Método que começa classificando o aluno em um perfil, trilha ou tipo. O aluno precisa se identificar com uma categoria antes de seguir o protocolo. Exemplos: perfis comportamentais, estilos de aprendizado, tipos de público, diagnóstico inicial (ex: Trilha Vermelha, Azul e Verde do Método PsiMama; tipos de emoção Feliz, Nervoso, Triste, Medo).

**NÃO usar quando:** O método é puramente sequencial sem bifurcação por perfil.

**Paleta:** Fundo branco, tipografia em cor de destaque (turquesa, azul, etc.), imagens com fundo neutro uniforme entre as colunas.

**Referência visual:** `metodo-grid-categorias.png` na pasta references.

---

## 6. Hub Central / Diamante (`04-hub-central.html`)

**Estrutura:** Losango central formado por 4 peças de puzzle, com letras representando cada pilar. Quatro blocos de texto nos cantos externos ligados por linhas.

**Quando usar:** Método com 4 pilares que coexistem e se conectam a um núcleo central. Transmite completude — "todos os 4 são necessários". Ideal para frameworks 360° ou estratégias completas (ex: Matriz do Autor Estratégico com pilares Obra, Autor, Leitor, Mercado).

**Paleta:** Fundo escuro (preto/grafite), peças em cinza, núcleo em dourado. Tipografia bold serifada.

**Referência visual:** `metodo-matriz-puzzle.png` na pasta references.

---

## 7. Pirâmide Invertida (`03-piramide-invertida.html`)

**Estrutura:** Camadas horizontais de largura decrescente de cima para baixo, cada camada com nome e descrição.

**Quando usar:** Método em que o aluno começa amplo (consciência/diagnóstico) e afunila progressivamente até a ação específica. Ou quando há hierarquia clara — a base sustenta o topo. Bom para métodos de diagnóstico → planejamento → execução → resultado.

**Paleta padrão:** Verde (`#16a34a`) — adaptável.

---

## 8. Fluxograma Condicional (`05-fluxograma-condicional.html`)

**Estrutura:** Losangos de decisão (amarelo) conectados por setas a retângulos de ação, com ramificações Sim/Não.

**Quando usar:** Método com caminhos diferentes conforme o perfil ou situação do aluno. A lógica de "se X, faça Y; se não X, faça Z" precisa ficar visível. Ideal para métodos com Mecânica 1 (Lógica Condicional) da Furadeira.

**Paleta padrão:** Vermelho/rosa (`#e11d48`) — adaptável.

**Referência visual:** `metodo-trilhas-regua.png` na pasta references (versão simplificada da lógica condicional).

---

## 9. Trilha Zigzag (template embutido no SKILL.md)

**Estrutura:** Linha central vertical com cards alternando esquerda e direita. Ponto de Partida no início, Quadro conquistado ao final.

**Quando usar:** Método sequencial de 3 a 7 fases quando o destino é visualização standalone (não slide, não post). Transmite jornada e progressão. Formato livre, altura automática.

**Paleta:** 4 opções — Escuro moderno, Claro minimalista, Colorido vibrante, Cor personalizada.

---

## 16. Hub Numerado com Quadrantes (`16-hub-numerado-quadrantes.html`)

**Estrutura:** Círculo central com anéis concêntricos e linhas tracejadas cruzando o centro, dividindo-o em 4 quadrantes com letras. Quatro blocos numerados nos cantos externos, cada um com título bold e lista de sub-itens com seta triangular.

**Quando usar:** Método composto por um núcleo com sigla ou acrônimo (ex: VTSD, DISC, SPIN) e 4 pilares ou dimensões que orbitam esse núcleo, cada um com 2 a 3 ferramentas ou sub-conceitos. Ideal para metodologias que precisam mostrar tanto o sistema central quanto as aplicações práticas de cada pilar. Transmite completude e elegância.

**NÃO usar quando:** As fases são estritamente sequenciais sem núcleo central, ou quando o método tem mais de 4 pilares externos.

**Paleta:** Branco e cinza, monocromático. Os números dos quadrantes ficam em preto. Adaptar apenas a variável `--number-bg` para a cor de destaque do produto.

---

## Como Aplicar

1. Identifique a estrutura real da Furadeira (não o estilo visual preferido)
2. Use a Tabela de Decisão Rápida acima
3. Adapte apenas as cores à paleta do produto — nunca mude a estrutura do template
4. Texto sempre curto: nome da etapa + 1 frase. Proibido parágrafos longos
5. Cores devem dialogar com a paleta da página de vendas do produto

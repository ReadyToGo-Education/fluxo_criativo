# Concorrentes por Nicho (referência)

> Listas de concorrentes conhecidos que historicamente rodam (ou rodaram) anúncios na Biblioteca da Meta, organizados por nicho e mercado.
> Usado pelo `/biblioteca-anuncios` quando o aluno escolhe a opção "Sugerir concorrentes do meu nicho".

---

## Como funciona

Cada nicho tem 3 grupos de concorrentes:

- **BR**: brasileiros (sempre buscar com country=BR)
- **EN**: anglo-saxões (buscar com country=US)
- **ES**: hispano-falantes (buscar com country=MX, AR, CO ou ES, na ordem; se um não tem ads ativos, tentar o próximo)

Marcadores ao lado do nome:
- `*` significa "alta rotação histórica, costuma ter criativos escalados" (prioridade)
- `(PIVOT)` significa "já migrou de nicho, talvez não tenha mais ads relevantes"
- `(baixa escala)` significa "tem ads mas raramente escala um criativo"

A skill deve **filtrar** os marcadores antes de mostrar pro aluno (mostrar só o nome) e **usar** os marcadores internamente pra priorizar ordem de busca e marcar na saída.

---

## Marketing Digital e Infoprodutos

### BR
- Erico Rocha *
- Pedro Sobral *
- Felipe Azevedo *
- Pri Calheiros *
- Conrado Adolpho
- Tiago Tessmann
- Italo Marsili
- Bruno Avila
- Paulo Cuenca
- Rodrigo Vincenzi
- Rafael Rez
- Wendell Carvalho (PIVOT) (pivotou pra mentalidade Protagon)
- Ícaro de Carvalho (PIVOT) (pivotou pra aposentadoria e imóveis)
- Alex Vargas (baixa escala)
- Marcelo Tavara (baixa escala) (alta rotação sem escala vertical)
- Marcelo Braggion (baixa escala)
- Micha Menezes (baixa escala)

### EN
- Alex Hormozi * (Acquisition.com + Skool)
- Sabri Suby * (Sell Like Crazy book funnel)
- Russell Brunson (baixa escala) (ClickFunnels)
- Sam Ovens *
- Tai Lopez
- Frank Kern
- Brendon Burchard
- Pat Flynn
- Iman Gadzhi (PIVOT) (foi pra HILLS Eyewear)

### ES
- Josue Peña * (vendedor digital certificado, US-Hispano)
- Vilma Núñez (baixa escala) (curso $47 marca personal)
- Romuald Fons
- Pau Ninja
- Joan Boluda
- Convertia
- Cristóbal Amatriain
- Juan Diego Gómez
- Carlos Master Muñoz (PIVOT) (foi pra real estate Querétaro/Yucatán)

---

## Fitness e Emagrecimento

### BR
- Caio Bottura
- Leandro Twin
- Jeff Caetano
- Rodrigo Polesso
- Mariana Magnavita
- Dieta do Jejum (Dr. Filippo Pedrinola)
- Sergio Bertolucci
- Dr. Juliano Pimentel
- Felipe Franco

### EN
- Jordan Syatt
- Mike Matthews (Legion Athletics)
- Jeff Cavaliere (Athlean-X)
- Jeff Nippard
- Sal Di Stefano (Mind Pump)
- Greg Doucette
- Joe DeFranco
- Andy Galpin

### ES
- Sergio Peinado
- Marcos Vázquez (Fitness Revolucionario)
- Patry Jordan (Gym Virtual)
- Vikika Costa
- Sergio Espinar
- Yokana Lago

---

## Finanças Pessoais e Investimentos

### BR
- Primo Pobre
- Bruno Perini
- Nathália Arcuri (Me Poupe!)
- Thiago Nigro (Primo Rico)
- Gustavo Cerbasi
- Carol Stange
- Ramiro Gomes Ferreira

### EN
- Graham Stephan
- Andrei Jikh
- Meet Kevin
- Dave Ramsey
- Robert Kiyosaki
- Tony Robbins (PIVOT) (foi pra coaching genérico)
- Patrick Bet-David

### ES
- Sergio Fernández
- Juan Diego Gómez (Invertir Mejor)
- Mariana Avila
- Alejandro Cardona
- Pau Antó

---

## Espiritualidade, Tarô e Autoconhecimento

### BR
- Joana Saint Cyr (Caminho dos Anjos)
- Aline Eckmann
- Magaiver Tarot
- Mary Diniz
- Mundo Astral (Sergio Goes)
- Aline Padilha (Tarot)
- Athyna Fritz

### EN
- Gabby Bernstein
- Vanessa Van Edwards (PIVOT) (foi pra comunicação)
- The Tarot Lady (Theresa Reed)
- Biddy Tarot (Brigit Esselmont)
- Astrology King (Jamie Partridge)

### ES
- Mhoni Vidente
- Soraya Yamín
- Mago Yanbal
- Ainoha Vilches
- Sandra Suh

---

## Beleza, Estética e Maquiagem

### BR
- Boca Rosa (Bianca Andrade) (baixa escala)
- Marina Smith
- Camila Coelho (US-BR)
- Niina Secrets
- Vanessa Lopes
- Lu Ferraes
- Karol Pinheiro

### EN
- Huda Kattan (Huda Beauty)
- Jackie Aina
- Nikkie de Jager (NikkieTutorials)
- James Charles (PIVOT)
- Sephora
- Sigma Beauty

### ES
- Yuya
- Lizy P
- Mariale Marrero
- Jackie Hernandez Maquillaje
- Anaís Marin

---

## Idiomas e Comunicação

### BR
- Cambly BR
- Open English BR
- English in Brazil (Carina Fragozo)
- Mairo Vergara
- Tiago Tessmann (inglês)
- Paulo Barros (PaPaPa English)
- Inglês Winner

### EN
- Lindsay Does Languages
- Steve Kaufmann (LingQ)
- Olly Richards (StoryLearning)
- italki
- Babbel

### ES
- Spanish with Paul
- Dreaming Spanish (Pablo Román)
- Españolistos (Andrea y Nate)
- Why Not Spanish

---

## Alimentação, Receitas e Cozinha

### BR
- Rita Lobo (Panelinha) (baixa escala)
- Receitas Daiana Garbin
- Mil Receitas
- Dani Noce
- Bela Gil
- Carol Fiorentino (Marmita Fit)

### EN
- Tasty (BuzzFeed)
- Bon Appétit
- Joshua Weissman
- Babish Culinary Universe
- The Pioneer Woman

### ES
- Carlos Sin Cazo
- Recetas El Comidista
- Sara La Repostera
- Cocina Compartida

---

## Como expandir esta lista

Quando o aluno tiver um nicho que não está coberto aqui:

1. A skill `/biblioteca-anuncios` oferece a opção "Meu nicho não está aqui" no Passo 2.
2. Nesse caso, o aluno digita 3-6 nomes de concorrentes que ele já conhece (sem precisar buscar fallbacks).
3. A skill segue normalmente, só sem os fallbacks "aleatórios" do nicho.

Se um nicho começar a aparecer com frequência (3+ alunos pedindo), adicione uma nova seção neste arquivo no padrão acima.

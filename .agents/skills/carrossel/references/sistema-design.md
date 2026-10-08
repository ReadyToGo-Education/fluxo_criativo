# Sistema de Design. Carrossel de Instagram (compartilhado)

> Referência usada por TODOS os estilos de `/carrossel` (Nunca, Sempre, Odeio, Erros, Amo, Ninguém Conta, Notícia).
> A skill consulta esta tabela ao montar os prompts de imagem do Passo 3.

---

## Princípios visuais comuns aos 7 estilos

1. **Formato 4:5** (1080x1350 pixels), padrão de carrossel vertical do Instagram.
2. **Dois blocos horizontais por slide**:
   - Bloco superior (~55% da altura): imagem fotográfica realista, sem rosto humano nítido (apenas de costas, perfil ou silhueta).
   - Bloco inferior (~45% da altura): cor sólida que carrega o título + subtítulo do slide.
3. **Tipografia renderizada na arte**, não adesivada por cima. O texto é o elemento gráfico dominante.
4. **Indicador de página** no canto superior direito do bloco inferior (formato `N/6` em uppercase, tracking +100).
5. **Margem de segurança** de 80px nas bordas para o texto.
6. **Realismo fotográfico no bloco superior**. Sem 3D cartoon, sem ilustração, sem estética AI-painterly.

---

## Tabela de tradução do estilo de design visual

Quando o aluno escolhe um dos 7 estilos no Passo 1 da coleta, traduza para a diretriz visual correspondente. **NUNCA cite termos técnicos de tipografia para o aluno** (serifada, condensada, kerning). Use os rótulos da coluna "Estilo".

| Estilo | Tradução visual interna |
|---|---|
| Sofisticado e Elegante | Tipografia serifada, espaçamento generoso, paleta neutra, sem elementos decorativos |
| Editorial e Cinematográfico | Layout de revista, hierarquia tipográfica forte, espaço negativo, sofisticação |
| Despojado e Bem-humorado | Tipografia bold/rounded, cores mais vivas, elementos gráficos lúdicos |
| Energético e Vibrante | Tipografia condensada/impactante, cores fortes, energia gráfica alta |
| Sério e Técnico | Grid rígido, tipografia mono ou sans-serif limpa, dados visuais, ícones funcionais |
| Aconchegante e Humano | Tipografia casual/manuscrita, paleta quente, elementos orgânicos, atmosfera acessível |
| Provocativo e Ousado | Tipografia bold com peso, cores cruas, contraste alto, zero decoração |
| Descrição Livre | Traduzir a descrição do aluno em diretrizes visuais equivalentes |

---

## Defaults de paleta por estilo de carrossel

Cada estilo (Nunca, Sempre, Odeio, etc.) tem paleta default própria, definida em `estilos/{nome}.md`. Esta tabela só lista para referência rápida.

| Carrossel | Paleta default slides 1-5 | Paleta default slide 6 (CTA) | Atmosfera fotográfica |
|---|---|---|---|
| Nunca | Creme bege #F2EAD9 | Verde-sálvia escuro #3D4A3F | Alerta, consequência, naturalista |
| Sempre | Creme bege #F2EAD9 | Verde-sálvia escuro #3D4A3F | Ação positiva, organização, naturalista |
| Odeio | Preto #111111 (texto creme) | Creme #F2EAD9 (texto preto) | Dramático, gravidade, contraste forte |
| Erros | Creme bege #F2EAD9 | Verde-sálvia escuro #3D4A3F | Sutileza do comportamento errado, naturalista |
| Amo | Marfim #F5F0E5 | Verde-sálvia #3D4A3F | Luz dourada quente, presença, íntimo |
| Ninguém Conta | Bege escuro #D9CFB8 (texto verde-musgo) | Verde-musgo #2E3B2C (texto creme) | Bastidor, documental, cru, sem polimento |
| Notícia | Definido pela paleta do criador ou monocromático editorial | Mesmo bloco do slide CTA | Editorial, jornalístico, foto real |

Quando o aluno trouxer paleta da marca dele, sobreponha a paleta default. O slide 6 deve sempre inverter ou contrastar com os slides 1-5 para fechar com peso.

---

## Regra de fotografia (todos os estilos)

- **Sem rosto humano nítido nos slides 1-5.** Apenas de costas, perfil ou silhueta. Isso evita problemas de identidade visual da marca do criador e mantém o foco na tipografia.
- **Slide 6 (CTA) pode ter pessoa**, em pose de fechamento (acenando, virando, terminando uma ação).
- **Atmosfera coerente com o estilo do carrossel** (ver coluna "Atmosfera fotográfica" acima).
- **Sem stock-photo plastification, sem AI-painterly, sem 3D cartoon.** Realismo cinematográfico com leve granulação de filme.

---

## Quando o aluno descreve livremente o estilo

Se o aluno digitar uma descrição em vez de escolher 1-7 (ex: "minimalista escandinavo", "anos 70 brasileiro", "vaporwave"), traduza para diretrizes visuais equivalentes em 3 linhas:
- Tipografia (tipo de fonte e peso)
- Cores (paleta sugerida)
- Atmosfera (luz, textura, mood)

Aplique essas diretrizes no campo `STYLE DIRECTION` do template de prompt de imagem.

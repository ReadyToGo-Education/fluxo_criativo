# Sub-skill. Upsell / Downsell e Take Rate

Lê as páginas de upsell/downsell (oferta pós-compra) e estima o take rate: quantos dos compradores aceitam a segunda oferta. **Particularidade:** essas páginas são pós-compra, só quem comprou as enxerga. Logo, a base é 100% qualificada, não é tráfego frio.

## Quando é acionado

- O aluno informou links de upsell/downsell no Passo 0.97 do SKILL.md.
- O aluno pergunta "quantos dos meus compradores aceitam o upsell?" ou "minha esteira está convertendo?".
- **Nunca roda se o produto não tem upsell/downsell.** Ausência é escolha de modelo, não problema. Pular limpo.

## Cuidado de nomenclatura (o aluno mistura)

| Oferta | Onde aparece | Take rate de mercado | Confiança |
|---|---|---|---|
| Order bump | no checkout, 1 clique | 15–37% (saudável 15–25%) | 🟢 média-alta |
| Upsell pós-compra | página depois de pagar | 3–15% (típico 3–8%; bem otimizado 8–15%) | 🟢 média-alta |
| Downsell | após recusar o upsell | 2–8% (sempre abaixo do upsell) | 🟡 média |

Os links do Passo 0.97 são quase sempre **upsell/downsell pós-compra**, não order bump. Saúde do upsell pós-compra: abaixo de 2% = algo errado, 5–8% = bem otimizado. Fontes: Focus Digital, CartHook, Growth Suite, Hotmart, Ensinio.

## Passo a passo

1. **Ler cada página** na ordem da seção 4.2 do SKILL.md (regra 10 do CLAUDE.md): Claude in Chrome primeiro; se não estiver disponível, WebFetch. Sem editar `settings.local.json` nem lista de permissões.
2. **Se a leitura falhar** (página protegida, só JavaScript), usar a alternativa da seção 4.3 do SKILL.md (texto colado ou descrição).
3. **Ler a oferta** (mesmos elementos do diagnóstico de oferta: promessa, mecanismo, preço, CTA). Avaliar se o upsell **complementa** a oferta principal ou **compete** com ela.

## Estimativa de take rate

- `take_rate = compras_upsell ÷ compras_principal` (quem chega na página de upsell = quem comprou a principal).
- **Só dá para calcular pelo Meta se o upsell tiver evento próprio distinguível:** conversão personalizada separada, ou produto/pixel separado. Procurar em `ads_get_customconversions` (MCP) ou `/act_<id>/customconversions` (App) e no array `actions` (`offsite_conversion.custom.*`).
- **Se o upsell dispara o MESMO evento `purchase` da principal, o Meta NÃO separa as duas compras.** Declarar: "o take rate real só sai do relatório da plataforma (Hotmart/Kiwify); o pixel não distingue." **Nunca inventar o número.**

## Explicação obrigatória

```
ESTEIRA PÓS-COMPRA

Upsell ("{nome}"): take rate {X}% dos compradores
(benchmark de upsell pós-compra: 3% a 15%, típico 3% a 8%; confiança 🟢 média a alta)

O que significa: de cada 100 pessoas que compraram o produto
principal, {X} também levaram o upsell.

Confiança: {alta se evento próprio | baixa se compartilha purchase}.
{Se compartilha: "Esse número é estimativa; o real está na Hotmart."}
```

## Quando não dá pra medir pelo Meta

```
Não consigo isolar a compra do upsell pelo pixel (ele usa o
mesmo evento 'purchase' do produto principal). Posso LER a oferta
da página e dizer se está bem construída, mas o take rate exato
você tira do relatório da Hotmart (vendas do produto de upsell
÷ vendas do produto principal).
```

## Output YAML

```yaml
upsell_downsell:
  tem_esteira: true
  itens:
    - tipo: upsell
      nome: "Mentoria Express"
      url: "https://.../upsell"
      oferta: { promessa: "...", preco: "R$ 497", complementa: true }
      take_rate: 0.11
      fonte_take_rate: "custom_conversion_separada"  # ou "compartilha_purchase_indisponivel"
      confianca: alta
      benchmark: "upsell pós-compra 3–15% (típico 3–8%)"
    - tipo: downsell
      nome: "..."
      take_rate: null
      fonte_take_rate: "compartilha_purchase_indisponivel"
      confianca: indisponivel
  limitacao: "Take rate só sai do Meta se o upsell tiver evento próprio. Senão, vem da plataforma."
```

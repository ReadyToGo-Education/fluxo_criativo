---
name: pagina-checkout
description: >
  Prepara a integração de checkout/presscart em uma página HTML pronta. Conecta
  os botões de CTA ao link de checkout (Hotmart, Kiwify, Eduzz, Cakto, Pepper,
  Stripe ou link próprio), configura parâmetros de tracking (UTM, src),
  instala order bump opcional e injeta evento de InitiateCheckout no Pixel.
  Skill de infraestrutura. Roda depois da página estar pronta.
---

# Página Checkout. Conexão com Plataforma de Pagamento

Pega uma página HTML existente e conecta os botões de compra ao link real do checkout. Sem mexer na copy. Configura UTM, src, evento de pixel e order bump opcional.

## Quando Usar

- Depois de gerar a página com `/copy-pagina` ou `/lt-pagina`.
- Quando o usuário disser "conecta o checkout", "liga essa página na Hotmart", "preciso colocar o link de pagamento", "presscart", "instala o checkout".
- Antes de subir a página pro ar.

## O Que Fazer

### 1. Contexto

Leia `entregas/.ativo` e `entregas/{ativo}/perfil.md`.

Verifique se já existe configuração de checkout salva em `entregas/{ativo}/.checkout`. Se houver, ofereça:
1. Usar a configuração existente
2. Atualizar para uma nova

### 2. Coletar dados (uma pergunta por vez)

**Pergunta 1. Qual página vou modificar?**
1. Última página salva em `entregas/{ativo}/paginas/`
2. Outra (informar caminho)

**Pergunta 2. Qual plataforma de checkout?**
1. Hotmart
2. Kiwify
3. Eduzz
4. Cakto
5. Pepper
6. Stripe Checkout
7. Outro (link direto)

**Pergunta 3. Qual o link do checkout?**
(o usuário cola o link completo, ex: https://pay.hotmart.com/H123456789)

Valide que começa com `https://`. Se não, avise e peça de novo.

**Pergunta 4. Quer rastrear origem com UTM?**
1. Sim (vou anexar utm_source, utm_medium, utm_campaign automaticamente)
2. Não, link puro

Se sim, pergunte:
- `utm_source` (ex: `meta`, `google`, `organic`)
- `utm_medium` (ex: `cpc`, `social`, `email`)
- `utm_campaign` (ex: `lancamento-julho`)

**Pergunta 5. Tem order bump?**
1. Não
2. Sim, é só um checkbox extra na página antes do CTA principal
3. Sim, é um link de checkout diferente quando marcado

Se 2 ou 3, peça o nome, descrição curta e valor do order bump. Se 3, peça o link alternativo.

**Pergunta 6. Quer disparar evento de InitiateCheckout no Pixel?**
1. Sim (recomendado, melhora rastreamento de conversão)
2. Não, já tenho pixel cuidando disso
3. Não tenho pixel ainda, vou rodar `/pagina-pixel` depois

### 3. Modificar o HTML

Edite o arquivo:

**3.1. Localizar botões de CTA**
Procure por:
- `<a>` com classes `cta`, `btn-cta`, `btn-comprar`, `compre`, `quero`, etc.
- `<button>` com texto contendo "comprar", "quero", "garantir", "começar", "inscrever".
- Elementos com `data-cta`.

Liste o que encontrou. Se nada óbvio, mostre os primeiros 3 candidatos e pergunte qual é o CTA principal.

**3.2. Substituir o `href`**
Para cada CTA identificado, substitua o `href` pelo link de checkout, com UTMs apensas se aplicável. Use `target="_blank"` e `rel="noopener"`.

**3.3. Order bump (se houver)**

Tipo 2 (checkbox simples):
Insira logo acima do CTA principal um bloco:
```html
<label class="order-bump">
  <input type="checkbox" id="bump"> Adicionar {nome} por R$ {valor}.
  {descrição curta}
</label>
```
Estilize com inline CSS coerente com a paleta da página (borda destacada, fundo claro, ícone simples).

Tipo 3 (link alternativo):
Adicione um pequeno script que troca o `href` do CTA quando o checkbox marca/desmarca:
```html
<script>
var bump = document.getElementById('bump');
var cta  = document.querySelector('[data-cta-principal]');
var linkA = '{link sem bump}';
var linkB = '{link com bump}';
if (bump && cta) {
  bump.addEventListener('change', function(){
    cta.href = bump.checked ? linkB : linkA;
  });
}
</script>
```
Marque o CTA principal com `data-cta-principal` para o script encontrar.

**3.4. Evento de Pixel (se Pergunta 6 = sim)**
Adicione antes do `</body>`:
```html
<script>
document.querySelectorAll('[data-cta-principal], a.cta, .btn-cta').forEach(function(el){
  el.addEventListener('click', function(){
    if (typeof fbq !== 'undefined') fbq('track', 'InitiateCheckout');
  });
});
</script>
```
Se Pergunta 6 = 3, não adicione nada e avise no resumo final que o usuário deve rodar `/pagina-pixel` depois.

**3.5. Backup**
Antes de salvar, copie o original pra `entregas/{ativo}/paginas/.backup-checkout-{timestamp}.html`.

### 4. Salvar configuração

Salve em `entregas/{ativo}/.checkout`:
```
plataforma={...}
link={...}
utm_source={...}
utm_medium={...}
utm_campaign={...}
order_bump={sim/nao}
order_bump_link={...}
```

### 5. Resumo final

```
Pronto. Checkout conectado.

Página:       entregas/{ativo}/paginas/{nome}.html
Plataforma:   {nome}
Link:         {link com UTMs}
CTAs alterados: {n}
Order bump:   {nao / sim, R$ XX}
Pixel event:  {sim / nao}
Backup:       entregas/{ativo}/paginas/.backup-checkout-{timestamp}.html

Próximos passos sugeridos:
- /pagina-performance (auditar performance antes de subir)
- /pagina-pixel       (instalar pixel se ainda não tem)
- /pagina-lovable     (publicar a página online)
```

## Regras

- Nunca peça email, senha ou dados de login da plataforma de checkout. Só o link de pagamento, que é público.
- Nunca crie conta na Hotmart/Kiwify/Eduzz pelo usuário. Se ele não tiver link, oriente a criar manualmente e voltar.
- Nunca aplique link de checkout em CTA sem ter certeza de que aquilo é um botão de compra. Em caso de dúvida, peça confirmação.
- Sempre gere backup antes de sobrescrever.
- O link de checkout é dado público (link de pagamento), pode ficar salvo no `.checkout`.
- Não use travessão em nenhum texto exibido ao usuário.

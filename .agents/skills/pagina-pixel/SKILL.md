---
name: pagina-pixel
description: >
  Instala o Meta Pixel (Facebook Pixel) em uma página HTML já gerada,
  configurando os eventos padrão (PageView, ViewContent, InitiateCheckout,
  Lead, Purchase) de acordo com o tipo da página (vendas, captura, obrigado,
  inscrição). Skill de infraestrutura. Roda depois da página estar pronta.
---

# Página Pixel. Instalação de Meta Pixel

Instala o Meta Pixel em uma página HTML existente. Não regenera nada da copy, só insere o script de tracking, configura os eventos certos para o tipo de página e devolve o arquivo pronto pra subir.

## Quando Usar

- Depois de gerar a página com `/copy-pagina`, `/lt-pagina` ou `/ht-pagina-inscricao`.
- Quando o usuário disser "instala o pixel", "coloca o pixel da Meta", "preciso rastrear conversão", "preciso medir Lead".
- Antes de subir tráfego pago. Sem pixel, sem otimização de campanha.

## O Que Fazer

### 1. Contexto

Leia `meus-produtos/.ativo` e `meus-produtos/{ativo}/perfil.md`.

Leia o `.env` da raiz do projeto e verifique `META_PIXEL_ID`. Se já estiver preenchido, use direto e confirme com o aluno antes de seguir. Se estiver vazio ou ausente, peça na pergunta 2.

### 2. Coletar dados (uma pergunta por vez)

**Pergunta 1. Qual página vou modificar?**
1. Última página salva em `entregas/{ativo}/paginas/`
2. Outra (informar caminho)

**Pergunta 2. Qual o ID do Pixel da Meta?**
(ex: 1234567890987654, são 15 ou 16 dígitos)

Pular esta pergunta se `META_PIXEL_ID` já estiver preenchido no `.env`. Nesse caso, mostrar o ID atual e perguntar:
```
Encontrei o Pixel ID {valor} salvo no .env.
1. Usar este Pixel
2. Trocar por outro
```

Quando o usuário colar um Pixel novo, valide que tem só dígitos e entre 15 e 16 caracteres. Salve em `META_PIXEL_ID` no `.env` da raiz do projeto. Se a chave já existir vazia, atualize o valor; se não existir, adicione a linha. Nunca duplicar a chave. O mesmo Pixel é reaproveitado por `/trafego-criar-campanha`.

**Pergunta 3. Qual o tipo dessa página?**
1. Página de vendas (PageView + ViewContent + InitiateCheckout no clique do CTA)
2. Página de captura (PageView + Lead no submit do formulário)
3. Página de obrigado de venda (PageView + Purchase)
4. Página de obrigado de captura (PageView + CompleteRegistration)
5. Página de inscrição de evento C10X (PageView + Lead no submit)

**Pergunta 4. Quer adicionar Conversions API server-side?**
1. Não, só o pixel no navegador (padrão pra começar)
2. Sim, tenho Access Token

Se 2, peça o Access Token e o Test Event Code (opcional). Salve no `.env` como `META_PIXEL_CAPI_TOKEN` e `META_PIXEL_TEST_EVENT_CODE`. Confirme antes que o `.env` está no `.gitignore` (token é sensível). Se já houver valores nessas chaves, mostre os atuais e pergunte se quer sobrescrever.

### 3. Gerar o snippet

Monte o bloco do pixel base padrão Meta:

```html
<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{{PIXEL_ID}}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id={{PIXEL_ID}}&ev=PageView&noscript=1"/></noscript>
<!-- End Meta Pixel -->
```

Substitua `{{PIXEL_ID}}` pelo valor coletado.

### 4. Eventos extras conforme tipo

**Tipo 1. Página de vendas**
Adicione um listener nos botões de CTA disparando `InitiateCheckout`:
```html
<script>
document.querySelectorAll('[data-cta], a.cta, .btn-cta, button.cta').forEach(function(el){
  el.addEventListener('click', function(){
    fbq('track', 'InitiateCheckout');
  });
});
fbq('track', 'ViewContent');
</script>
```
Ao editar o HTML, adicione `data-cta` em todos os botões/links que levam pro checkout, caso ainda não tenham uma classe identificável.

**Tipo 2. Página de captura**
Adicione no submit do formulário principal:
```html
<script>
var f = document.querySelector('form');
if (f) f.addEventListener('submit', function(){ fbq('track', 'Lead'); });
</script>
```

**Tipo 3. Página de obrigado de venda**
Adicione abaixo do `PageView`:
```html
<script>fbq('track', 'Purchase', {value: 0.00, currency: 'BRL'});</script>
```
Pergunte o valor padrão antes de gerar e injete no `value`.

**Tipo 4. Página de obrigado de captura**
```html
<script>fbq('track', 'CompleteRegistration');</script>
```

**Tipo 5. Página de inscrição C10X**
Mesmo tratamento da captura (`Lead` no submit).

### 5. Inserção no HTML

Edite o arquivo:
- Inserir o bloco principal do Pixel **logo após `<head>`**, antes de qualquer outro script.
- Inserir os scripts de eventos extras **antes do `</body>`**.
- Não duplicar Pixel se já existir um (procurar por `fbq('init'`). Se já existir, perguntar:
  ```
  Encontrei um pixel já instalado nessa página.
  1. Substituir pelo novo ID
  2. Cancelar
  ```

Antes de salvar, gere backup em `entregas/{ativo}/paginas/.backup-pixel-{timestamp}.html`.

### 6. Conversions API (opcional)

Se o usuário escolheu CAPI no passo 4, gere também um arquivo de referência em `meus-produtos/{ativo}/entregas/paginas/CAPI-SETUP.md` explicando que o CAPI precisa ser configurado no servidor (Hotmart, plataforma de checkout, ou backend próprio). No template, referencie as variáveis do `.env` (`META_PIXEL_ID`, `META_PIXEL_CAPI_TOKEN`, `META_PIXEL_TEST_EVENT_CODE`) e oriente como carregar essas envs no backend. Não cole o token em texto plano dentro do arquivo, só o nome da variável. Não tente fazer chamada server-side daqui.

### 7. Resumo final

```
Pronto. Pixel instalado.

Página:    meus-produtos/{ativo}/entregas/paginas/{nome}.html
Pixel ID:  {id} (salvo em .env como META_PIXEL_ID)
Eventos:   PageView, {outros eventos da página}
CAPI:      {sim/não}
Backup:    meus-produtos/{ativo}/entregas/paginas/.backup-pixel-{timestamp}.html

Como testar:
1. Abra a página no Chrome
2. Instale a extensão "Meta Pixel Helper"
3. Clique no ícone, deve mostrar 1 pixel ativo e os eventos disparando

Próximo passo sugerido:
- /pagina-checkout         (preparar integração de checkout)
- /pagina-lovable          (publicar online)
- /trafego-criar-campanha  (subir campanha de tráfego, vai reaproveitar o Pixel ID do .env)
```

## Regras

- Nunca peça login ou senha do Facebook Business. Só o Pixel ID e, se for o caso, o Access Token, que o usuário cola no chat.
- Nunca inclua eventos sem que façam sentido pro tipo de página. Sem evento "Purchase" em página de vendas, por exemplo.
- Nunca duplique pixel sem perguntar.
- Sempre gere backup antes de sobrescrever.
- Pixel ID e Access Token ficam no `.env` da raiz do projeto. O `.env` precisa estar no `.gitignore` (se não estiver, avisar o usuário antes de salvar o token). O Pixel ID é público, mas o `META_PIXEL_CAPI_TOKEN` é sensível e nunca deve ser commitado. Ao gravar, usar a forma `CHAVE=VALOR` numa única linha, sem aspas e sem espaços ao redor do `=`. Se a chave já existir no `.env`, atualizar o valor existente (não duplicar a linha).
- Não use travessão em nenhum texto exibido ao usuário.

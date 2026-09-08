---
name: "source-command-video-efeitos"
description: "Aplicar motion graphics animados em videos existentes usando GSAP + Puppeteer + FFmpeg. Contador animado, letras voando, card de estatistica, barra de progresso, lower third sofisticado, selo circular, lista animada, CTA com pulso, confetti. Para Reels gravados, VSLs e anuncios."
---

# source-command-video-efeitos

Use this skill when the user asks to run the migrated source command `video-efeitos`.

## Command Template

# Efeitos Visuais Animados. GSAP + Puppeteer + FFmpeg

Voce aplica motion graphics profissionais em cima de videos existentes. O aluno traz o video gravado, escolhe os efeitos, voce gera o overlay animado transparente e composta no video final. Resultado: Reel com efeitos de agencia, sem abrir After Effects.

## REGRA DE CUSTO

100% local e gratuito. GSAP via CDN, Puppeteer open source, FFmpeg ja instalado.

**Para efeitos simples** (texto de gancho, lower third basico, color grade, progress bar, CTA, vinheta): use `/video-editar` opcao 15. E mais rapido e nao precisa do Puppeteer.

**Use este comando para**: contador animado, letras voando com stagger, card de estatistica, barra de porcentagem, lower third com linha que expande, selo circular girando, lista com icones, CTA pulsante, confetti.

---

## PRE-REQUISITOS

### FFmpeg (obrigatorio)

```bash
ffmpeg -version
```

Se nao estiver: `winget install ffmpeg` (Windows) ou `brew install ffmpeg` (Mac).

### Node.js + Puppeteer (obrigatorio)

```bash
node --version
```

Se nao tiver Node.js: `winget install OpenJS.NodeJS.LTS` (Windows) ou `brew install node` (Mac).

Verifique se o Puppeteer ja esta instalado no projeto:

```bash
node -e "require('.Codex/tools/video-efeitos/node_modules/puppeteer')" 2>&1
```

Se falhar, instale (primeira vez, ~200MB, demora 2 a 3 minutos):

```bash
mkdir -p .Codex/tools/video-efeitos
cd .Codex/tools/video-efeitos && npm init -y && npm install puppeteer
cd ../../..
```

Avise o aluno antes de instalar: "Vou instalar o Puppeteer pela primeira vez. Sao ~200MB e leva 2 a 3 minutos. As proximas vezes serao instantaneas."

### Script de captura

Verifique se existe `.Codex/tools/video-efeitos/capture.js`. Se nao existir, crie com o conteudo da secao SCRIPT DE CAPTURA ao final deste arquivo.

---

## PASSO 1. Input do video

Pergunta:

> Qual video voce quer adicionar efeitos? Cole o caminho completo do arquivo.
> (ex: `C:\Users\Maria\Videos\reel_bruto.mp4`)

Apos receber, obtenha largura, altura e duracao:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "entrada.mp4"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "entrada.mp4"
```

Confirme: "Video encontrado. Duracao: Xs. Formato: LARGURAxALTURA."

---

## PASSO 2. Escolha dos efeitos

```
Quais efeitos quer adicionar? Pode combinar varios. Separe por virgula.

1. Contador animado (numero sobe de 0 ate o valor, ex: "247 alunos")
2. Texto com letras voando (stagger de caracteres, estilo premium)
3. Card de estatistica (caixa com numero + label, estilo Instagram)
4. Barra de porcentagem animada (porcentagem que cresce com numero)
5. Lower third sofisticado (linha que expande + nome + cargo)
6. Selo circular (badge giratório de confianca ou garantia)
7. Lista animada com icones em sequencia
8. CTA pulsante (texto que pulsa nos ultimos segundos)
9. Confetti / celebracao (particulas coloridas)

Digite os numeros (ex: 1, 3, 5):
```

---

## PASSO 3. Parametros por efeito

Para cada efeito escolhido, pergunte UM por vez:

**Efeito 1 - Contador:**
- Numero final e sufixo (ex: "247" + " alunos")
- Posicao: topo-centro, centro, base-centro
- Quando aparece (segundos) e duracao em tela
- Cor principal HEX

**Efeito 2 - Texto com stagger:**
- Texto (max 30 caracteres)
- Tamanho: pequeno (60px), medio (90px), grande (120px)
- Posicao: topo, centro, base
- Quando aparece e duracao em tela
- Cor HEX

**Efeito 3 - Card de estatistica:**
- Numero principal (ex: "R$ 12.000")
- Subtitulo (ex: "faturados em 30 dias")
- Cor de fundo HEX e cor do texto HEX
- Posicao: canto inferior esquerdo, direito, ou centro
- Quando aparece e duracao

**Efeito 4 - Barra de porcentagem:**
- Porcentagem alvo (ex: 87)
- Label (ex: "taxa de conclusao")
- Cor da barra HEX
- Quando aparece

**Efeito 5 - Lower third sofisticado:**
- Nome completo
- Cargo ou especialidade
- Cor do destaque HEX (a linha)
- Quando aparece e por quanto tempo

**Efeito 6 - Selo circular:**
- Texto principal (ex: "GARANTIA") e secundario (ex: "30 dias")
- Cor de fundo HEX e cor do texto HEX
- Posicao: canto superior direito, inferior direito, centro
- Quando aparece

**Efeito 7 - Lista animada:**
- Itens da lista (max 5)
- Icone: check (v), seta (>), numero, ou emoji
- Cor do icone HEX e cor do texto HEX
- Quando comeca a aparecer

**Efeito 8 - CTA pulsante:**
- Texto do CTA (ex: "ARRASTA PRA CIMA")
- Cor do texto HEX e cor do fundo HEX (ou "sem fundo")
- Quantos segundos antes do fim aparece (padrao: 3s)

**Efeito 9 - Confetti:**
- Cores (padrao: multicolor festivo)
- Quando aparece e duracao
- Intensidade: suave, media, intensa

---

## PASSO 4. Confirmacao

```
Resumo dos efeitos:

Video: [nome] ([duracao]s, [LxA]px)
Efeitos:
- [Efeito]: [parametros] → aparece em [X]s por [Y]s
...

Saida: meus-produtos/{ativo}/entregas/videos/[nome]_efeitos.mp4

1. Confirmar e gerar
2. Ajustar algo
```

---

## PASSO 5. Gerar overlay.html

Crie a pasta e o arquivo:

```bash
mkdir -p "meus-produtos/{ativo}/entregas/videos/temp_efeitos"
```

Gere `meus-produtos/{ativo}/entregas/videos/temp_efeitos/overlay.html` com:

- `<html>` com `background: transparent`
- Dimensoes iguais ao video (width/height fixos em px)
- GSAP via CDN: `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`
- Google Fonts para cada efeito (Montserrat weight 400, 700, 900)
- Timeline GSAP: `var tl = gsap.timeline({ paused: true }); window._tl = tl;`
- Cada efeito em seu proprio div, `position:absolute`, comecando com `visibility:hidden`

### Templates GSAP por efeito

**Efeito 1 - Contador:**

```html
<div id="ef-contador" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);text-align:center;visibility:hidden;">
  <div id="ef-contador-num" style="font-family:'Montserrat',sans-serif;font-size:160px;font-weight:900;color:COR;text-shadow:4px 4px 20px rgba(0,0,0,0.5);">0</div>
  <div style="font-family:'Montserrat',sans-serif;font-size:48px;font-weight:400;color:COR;opacity:0.9;">SUFIXO</div>
</div>
```

```javascript
var c1 = { v: 0 };
tl.set("#ef-contador", { visibility:"visible", autoAlpha:0 }, INICIO);
tl.to("#ef-contador", { autoAlpha:1, y:-20, duration:0.5, ease:"power3.out" }, INICIO);
tl.to(c1, { v:VALOR, duration:1.8, ease:"power2.out", onUpdate:function(){ document.getElementById("ef-contador-num").textContent = Math.round(c1.v).toLocaleString("pt-BR"); } }, INICIO+0.3);
tl.to("#ef-contador", { autoAlpha:0, duration:0.4, ease:"power2.in" }, FIM-0.4);
```

**Efeito 2 - Stagger de letras:**

```javascript
var s2texto = "TEXTO AQUI";
var s2cont = document.getElementById("ef-stagger");
s2texto.split("").forEach(function(c){ var sp=document.createElement("span"); sp.textContent=c===" "?"\u00A0":c; sp.style.cssText="display:inline-block;font-family:'Montserrat',sans-serif;font-size:TAMANHOpx;font-weight:900;color:COR;text-shadow:3px 3px 12px rgba(0,0,0,0.6);"; s2cont.appendChild(sp); });
var s2chars = s2cont.querySelectorAll("span");
tl.set("#ef-stagger", { visibility:"visible" });
tl.from(s2chars, { y:80, autoAlpha:0, duration:0.5, ease:"power3.out", stagger:{each:0.04,from:"start"} }, INICIO);
tl.to(s2chars, { y:-30, autoAlpha:0, duration:0.4, ease:"power2.in", stagger:{each:0.03,from:"end"} }, FIM-0.4);
```

```html
<div id="ef-stagger" style="position:absolute;top:POSICAO;left:0;right:0;text-align:center;overflow:hidden;visibility:hidden;"></div>
```

**Efeito 3 - Card de estatistica:**

```html
<div id="ef-card" style="position:absolute;bottom:180px;left:40px;background:COR_FUNDO;border-radius:20px;padding:32px 40px;min-width:280px;box-shadow:0 20px 60px rgba(0,0,0,0.4);visibility:hidden;">
  <div style="font-family:'Montserrat',sans-serif;font-size:72px;font-weight:900;color:COR_TEXTO;line-height:1;">NUMERO</div>
  <div style="font-family:'Montserrat',sans-serif;font-size:28px;font-weight:500;color:COR_TEXTO;opacity:0.85;margin-top:8px;">SUBTITULO</div>
</div>
```

```javascript
tl.set("#ef-card", { visibility:"visible" });
tl.from("#ef-card", { x:-120, autoAlpha:0, duration:0.6, ease:"back.out(1.4)" }, INICIO);
tl.to("#ef-card", { x:-120, autoAlpha:0, duration:0.4, ease:"power2.in" }, FIM-0.4);
```

**Efeito 4 - Barra de porcentagem:**

```html
<div id="ef-barra" style="position:absolute;bottom:220px;left:60px;right:60px;visibility:hidden;">
  <div style="font-family:'Montserrat',sans-serif;font-size:32px;font-weight:700;color:white;margin-bottom:12px;text-shadow:2px 2px 8px rgba(0,0,0,0.6);">LABEL</div>
  <div style="background:rgba(255,255,255,0.25);border-radius:99px;height:24px;overflow:hidden;">
    <div id="ef-barra-fill" style="background:COR;height:100%;border-radius:99px;width:0%;"></div>
  </div>
  <div id="ef-barra-num" style="font-family:'Montserrat',sans-serif;font-size:36px;font-weight:900;color:white;margin-top:8px;text-shadow:2px 2px 8px rgba(0,0,0,0.6);">0%</div>
</div>
```

```javascript
var b4 = { v:0 };
tl.set("#ef-barra", { visibility:"visible" });
tl.from("#ef-barra", { y:40, autoAlpha:0, duration:0.5, ease:"power2.out" }, INICIO);
tl.to(b4, { v:PORCENTAGEM, duration:1.5, ease:"power2.out", onUpdate:function(){ document.getElementById("ef-barra-fill").style.width=b4.v+"%"; document.getElementById("ef-barra-num").textContent=Math.round(b4.v)+"%"; } }, INICIO+0.3);
tl.to("#ef-barra", { y:40, autoAlpha:0, duration:0.4, ease:"power2.in" }, FIM-0.4);
```

**Efeito 5 - Lower third sofisticado:**

```html
<div id="ef-lt" style="position:absolute;bottom:120px;left:0;right:0;visibility:hidden;">
  <div id="ef-lt-linha" style="height:4px;background:COR_DESTAQUE;width:0;margin-left:60px;margin-bottom:16px;"></div>
  <div style="padding-left:60px;">
    <div style="overflow:hidden;"><span id="ef-lt-nome" style="display:block;transform:translateY(100%);font-family:'Montserrat',sans-serif;font-size:52px;font-weight:800;color:COR_TEXTO;text-shadow:2px 2px 10px rgba(0,0,0,0.7);">NOME</span></div>
    <div style="overflow:hidden;margin-top:4px;"><span id="ef-lt-cargo" style="display:block;transform:translateY(100%);font-family:'Montserrat',sans-serif;font-size:32px;font-weight:400;color:COR_TEXTO;opacity:0.85;text-shadow:2px 2px 8px rgba(0,0,0,0.6);">CARGO</span></div>
  </div>
</div>
```

```javascript
tl.set("#ef-lt", { visibility:"visible" });
tl.to("#ef-lt-linha", { width:"40%", duration:0.4, ease:"power2.out" }, INICIO);
tl.to("#ef-lt-nome", { y:"0%", duration:0.4, ease:"power2.out" }, INICIO+0.2);
tl.to("#ef-lt-cargo", { y:"0%", duration:0.4, ease:"power2.out" }, INICIO+0.35);
tl.to("#ef-lt-nome", { y:"-100%", duration:0.3, ease:"power2.in" }, FIM-0.5);
tl.to("#ef-lt-cargo", { y:"-100%", duration:0.3, ease:"power2.in" }, FIM-0.4);
tl.to("#ef-lt-linha", { width:0, duration:0.3, ease:"power2.in" }, FIM-0.3);
```

**Efeito 6 - Selo circular:**

```html
<div id="ef-selo" style="position:absolute;top:60px;right:60px;width:180px;height:180px;visibility:hidden;">
  <svg viewBox="0 0 180 180" style="position:absolute;top:0;left:0;width:100%;height:100%;">
    <circle cx="90" cy="90" r="80" fill="COR_FUNDO" stroke="rgba(255,255,255,0.3)" stroke-width="3"/>
    <path id="ef-selo-ring" d="M 90 10 A 80 80 0 1 1 89.999 10" fill="none" stroke="COR_DESTAQUE" stroke-width="6" stroke-linecap="round" stroke-dasharray="503" stroke-dashoffset="503"/>
  </svg>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
    <div style="font-family:'Montserrat',sans-serif;font-size:24px;font-weight:900;color:COR_TEXTO;line-height:1.1;">TEXTO_PRINCIPAL</div>
    <div style="font-family:'Montserrat',sans-serif;font-size:18px;font-weight:500;color:COR_TEXTO;opacity:0.85;margin-top:4px;">TEXTO_SECUNDARIO</div>
  </div>
</div>
```

```javascript
tl.set("#ef-selo", { visibility:"visible" });
tl.from("#ef-selo", { scale:0, autoAlpha:0, rotation:-180, duration:0.6, ease:"back.out(1.7)", transformOrigin:"center center" }, INICIO);
tl.to("#ef-selo-ring", { strokeDashoffset:0, duration:0.8, ease:"power2.out" }, INICIO+0.3);
tl.to("#ef-selo", { scale:1.06, duration:0.3, yoyo:true, repeat:1, ease:"sine.inOut" }, INICIO+1.0);
tl.to("#ef-selo", { scale:0, autoAlpha:0, duration:0.3, ease:"power2.in", transformOrigin:"center center" }, FIM-0.3);
```

**Efeito 7 - Lista animada:**

```html
<div id="ef-lista" style="position:absolute;top:180px;left:60px;right:60px;visibility:hidden;"></div>
```

```javascript
var itens7 = ["ITEM 1","ITEM 2","ITEM 3"];
var lista7 = document.getElementById("ef-lista");
itens7.forEach(function(item,i){ var d=document.createElement("div"); d.id="ef-li-"+i; d.style.cssText="display:flex;align-items:center;gap:20px;margin-bottom:28px;"; d.innerHTML='<div style="width:48px;height:48px;background:COR_ICONE;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:24px;font-weight:900;color:white;">ICONE</div><div style="font-family:\'Montserrat\',sans-serif;font-size:40px;font-weight:700;color:COR_TEXTO;text-shadow:2px 2px 8px rgba(0,0,0,0.5);">'+item+'</div>'; lista7.appendChild(d); });
tl.set("#ef-lista", { visibility:"visible" });
itens7.forEach(function(_,i){ tl.from("#ef-li-"+i, { x:-100, autoAlpha:0, duration:0.4, ease:"power2.out" }, INICIO+i*0.25); });
tl.to("#ef-lista", { x:-100, autoAlpha:0, duration:0.4, ease:"power2.in" }, FIM-0.4);
```

**Efeito 8 - CTA pulsante:**

```html
<div id="ef-cta" style="position:absolute;bottom:120px;left:0;right:0;text-align:center;visibility:hidden;">
  <div style="display:inline-block;background:COR_FUNDO;border-radius:99px;padding:24px 60px;">
    <div style="font-family:'Montserrat',sans-serif;font-size:56px;font-weight:900;color:COR_TEXTO;text-transform:uppercase;letter-spacing:2px;">TEXTO_CTA</div>
  </div>
</div>
```

```javascript
var ctaInicio8 = DURACAO - SEGUNDOS_ANTES_FIM;
tl.set("#ef-cta", { visibility:"visible" });
tl.from("#ef-cta", { y:60, autoAlpha:0, scale:0.8, duration:0.5, ease:"back.out(1.5)" }, ctaInicio8);
tl.to("#ef-cta", { scale:1.05, duration:0.6, ease:"sine.inOut", yoyo:true, repeat:3 }, ctaInicio8+0.6);
```

**Efeito 9 - Confetti (seeded PRNG - deterministico):**

```html
<canvas id="ef-confetti" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;"></canvas>
```

```javascript
function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; var t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return((t^t>>>14)>>>0)/4294967296; }; }
var rand9 = mulberry32(42);
var cv9 = document.getElementById("ef-confetti"); cv9.width=LARGURA; cv9.height=ALTURA;
var ctx9 = cv9.getContext("2d");
var cores9 = ["#ff4444","#ffcc00","#44ff88","#4488ff","#ff44cc"];
var pts9 = []; for(var p=0;p<QUANTIDADE;p++){ pts9.push({ x:rand9()*LARGURA, y:-rand9()*200, vx:(rand9()-0.5)*6, vy:rand9()*4+3, cor:cores9[Math.floor(rand9()*cores9.length)], size:rand9()*14+6, rot:rand9()*360, rotV:(rand9()-0.5)*8 }); }
var cf9ativo=false;
tl.call(function(){ cf9ativo=true; }, [], INICIO);
tl.call(function(){ cf9ativo=false; ctx9.clearRect(0,0,LARGURA,ALTURA); }, [], FIM);
gsap.ticker.add(function(){ if(!cf9ativo)return; ctx9.clearRect(0,0,LARGURA,ALTURA); pts9.forEach(function(p){ p.x+=p.vx; p.y+=p.vy; p.rot+=p.rotV; if(p.y>ALTURA+50){ p.y=-20; p.x=rand9()*LARGURA; } ctx9.save(); ctx9.translate(p.x,p.y); ctx9.rotate(p.rot*Math.PI/180); ctx9.fillStyle=p.cor; ctx9.fillRect(-p.size/2,-p.size/4,p.size,p.size/2); ctx9.restore(); }); });
```

Substitua QUANTIDADE por: 80 (suave), 150 (media), 250 (intensa).

---

## PASSO 6. Executar captura

Verifique se o script existe. Se nao, crie conforme a secao SCRIPT DE CAPTURA abaixo.

```bash
node .Codex/tools/video-efeitos/capture.js \
  --html "meus-produtos/{ativo}/entregas/videos/temp_efeitos/overlay.html" \
  --output "meus-produtos/{ativo}/entregas/videos/temp_efeitos/frames" \
  --duration DURACAO \
  --fps 30 \
  --width LARGURA \
  --height ALTURA
```

Avise antes de rodar: "Capturando TOTAL_FRAMES frames (~SEGUNDOS segundos de processamento). Pode levar alguns minutos em videos longos."

Para videos acima de 60s: sugira `--fps 15` para acelerar sem perda visual perceptivel.

---

## PASSO 7. Compositar com FFmpeg

```bash
# Converter frames para WebM com canal alpha
ffmpeg -y -r 30 -f image2 \
  -i "meus-produtos/{ativo}/entregas/videos/temp_efeitos/frames/frame_%05d.png" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -auto-alt-ref 0 \
  "meus-produtos/{ativo}/entregas/videos/temp_efeitos/overlay.webm"

# Compositar overlay sobre o video original
ffmpeg -y \
  -i "video_original.mp4" \
  -i "meus-produtos/{ativo}/entregas/videos/temp_efeitos/overlay.webm" \
  -filter_complex "[0:v][1:v]overlay=0:0:shortest=1[out]" \
  -map "[out]" -map "0:a?" \
  -c:v libx264 -preset fast -crf 22 -c:a copy \
  "meus-produtos/{ativo}/entregas/videos/{nome}_efeitos.mp4"

# Limpar frames temporarios
rm -rf "meus-produtos/{ativo}/entregas/videos/temp_efeitos/frames"
```

---

## PASSO 8. Entrega

Informe ao aluno:

```
Pronto. Video com efeitos salvo em:
C:\...\meus-produtos\{ativo}\entregas\videos\{nome}_efeitos.mp4

Efeitos aplicados: [lista]
Duracao: [X]s
Tamanho: [X MB]

Proximo passo sugerido:
- /video-editar para comprimir para WhatsApp ou adicionar legenda
- /copy-anuncio para gerar a copy que acompanha esse video
```

---

## REGRAS DE QUALIDADE

- **Nunca use Math.random().** Use o seeded PRNG mulberry32 (seed fixo = resultado deterministico = mesmo overlay toda vez).
- **Sempre use `visibility:hidden` + `tl.set` nos elementos.** Nunca `display:none`.
- **Fontes via Google Fonts CDN.** Adicionar `?display=swap` na URL. O capture.js espera `networkidle0` antes de capturar.
- **Nunca sobrescreva o video original.** Sempre salve com sufixo `_efeitos`.
- **Para fps 15:** ajuste `--fps 15` no capture.js e `-r 15` no ffmpeg de conversao de frames.

---

## SCRIPT DE CAPTURA

Crie `.Codex/tools/video-efeitos/capture.js` se nao existir:

```javascript
const puppeteer = require('./node_modules/puppeteer');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const opts = {};
for (let i = 0; i < args.length; i += 2) {
  opts[args[i].replace('--', '')] = args[i + 1];
}

const htmlPath = path.resolve(opts.html);
const outputDir = path.resolve(opts.output);
const duration = parseFloat(opts.duration);
const fps = parseInt(opts.fps || '30');
const width = parseInt(opts.width || '1080');
const height = parseInt(opts.height || '1920');
const totalFrames = Math.ceil(duration * fps);

fs.mkdirSync(outputDir, { recursive: true });

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security', '--allow-file-access-from-files']
  });
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });

  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  console.log('Capturando ' + totalFrames + ' frames...');

  for (let frame = 0; frame < totalFrames; frame++) {
    const t = frame / fps;
    await page.evaluate(function(time) {
      if (window._tl) window._tl.seek(time, false);
    }, t);

    const framePath = path.join(outputDir, 'frame_' + String(frame).padStart(5, '0') + '.png');
    await page.screenshot({ path: framePath, omitBackground: true });

    if (frame % 30 === 0) {
      process.stdout.write('\r[' + Math.round((frame / totalFrames) * 100) + '%] frame ' + frame + '/' + totalFrames);
    }
  }

  console.log('\nCaptura concluida.');
  await browser.close();
})();
```

---

Inicie pelo **PRE-REQUISITOS**. Verifique FFmpeg, Node.js e Puppeteer antes de pedir o video.

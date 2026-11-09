# Efeitos de Formulários

10+ efeitos para inputs, selects, checkboxes e formulários.

## Índice
floating-label · underline-focus · glow-focus · animated-border-input · validation-flash · password-strength · file-upload-zone · search-expand · checkbox-check · toggle-switch

---

### input-floating-label
**Visual:** Label fica dentro do input; sobe pro topo quando focado ou preenchido.
**Quando usar:** Formulários modernos, padrão Material Design. Economiza espaço.
```html
<div class="input-float">
  <input type="text" id="name" placeholder=" ">
  <label for="name">Seu nome</label>
</div>
```
```css
.input-float { position: relative; margin: 20px 0; }
.input-float input {
  width: 100%;
  padding: 18px 12px 8px;
  border: 1px solid #333;
  background: transparent;
  color: #fff;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}
.input-float label {
  position: absolute;
  top: 50%;
  left: 12px;
  transform: translateY(-50%);
  color: #888;
  pointer-events: none;
  transition: all 0.3s ease;
  background: transparent;
}
.input-float input:focus,
.input-float input:not(:placeholder-shown) {
  border-color: #00f0ff;
}
.input-float input:focus + label,
.input-float input:not(:placeholder-shown) + label {
  top: 8px;
  font-size: 0.75rem;
  color: #00f0ff;
  transform: translateY(0);
}
```

### input-underline-focus
**Visual:** Linha embaixo cresce do centro pras bordas no focus.
**Quando usar:** Formulários minimalistas, sem border-box.
```html
<div class="input-underline">
  <input type="text" placeholder="Digite aqui">
</div>
```
```css
.input-underline { position: relative; margin: 20px 0; }
.input-underline input {
  width: 100%;
  padding: 12px 0;
  border: none;
  border-bottom: 1px solid #333;
  background: transparent;
  color: #fff;
  font-size: 1rem;
  outline: none;
}
.input-underline::after {
  content: "";
  position: absolute;
  bottom: 0; left: 50%;
  width: 0; height: 2px;
  background: linear-gradient(90deg, #ff00cc, #00f0ff);
  transition: all 0.4s ease;
}
.input-underline:focus-within::after {
  left: 0;
  width: 100%;
}
```

### input-glow-focus
**Visual:** Glow ciano envolvendo o input quando focado.
**Quando usar:** Tema dark, formulários premium, dashboards.
```css
.input-glow {
  width: 100%;
  padding: 14px;
  background: #141414;
  border: 1px solid #333;
  border-radius: 8px;
  color: #fff;
  outline: none;
  transition: all 0.3s ease;
}
.input-glow:focus {
  border-color: #00f0ff;
  box-shadow: 0 0 0 4px rgba(0,240,255,0.15), 0 0 20px rgba(0,240,255,0.3);
}
```

### input-animated-border
**Visual:** Borda gradiente animada quando focado.
**Quando usar:** Inputs de destaque (busca principal, código de verificação).
```html
<div class="input-anim-border">
  <input type="text" placeholder="Buscar...">
</div>
```
```css
.input-anim-border {
  position: relative;
  padding: 2px;
  border-radius: 10px;
  background: #141414;
}
.input-anim-border:focus-within {
  background: linear-gradient(45deg, #ff00cc, #00f0ff, #3333ff, #ff00cc);
  background-size: 300% 300%;
  animation: borderInput 3s linear infinite;
}
.input-anim-border input {
  width: 100%;
  padding: 14px;
  background: #141414;
  border: none;
  border-radius: 8px;
  color: #fff;
  outline: none;
}
@keyframes borderInput { to { background-position: 300% 50%; } }
```

### input-validation-flash
**Visual:** Borda fica verde no válido, vermelha no inválido com flash sutil.
**Quando usar:** Validação inline em forms (email, senha, CPF).
```css
.input-valid {
  border: 2px solid #333;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.input-valid.valid {
  border-color: #00ff88;
  animation: validFlash 0.5s ease;
}
.input-valid.invalid {
  border-color: #ff3366;
  animation: invalidShake 0.4s ease;
}
@keyframes validFlash {
  50% { box-shadow: 0 0 20px rgba(0,255,136,0.5); }
}
@keyframes invalidShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
```

### password-strength-meter
**Visual:** Barra abaixo do input mostrando força da senha em tempo real.
**Quando usar:** Cadastro, alteração de senha.
```html
<div class="pw-wrapper">
  <input type="password" id="pw" placeholder="Senha">
  <div class="pw-strength"><div class="pw-bar"></div></div>
</div>
```
```css
.pw-strength {
  margin-top: 6px;
  height: 4px;
  background: #222;
  border-radius: 2px;
  overflow: hidden;
}
.pw-bar {
  height: 100%;
  width: 0%;
  background: #ff3366;
  transition: width 0.3s ease, background 0.3s ease;
}
.pw-bar.weak { width: 33%; background: #ff3366; }
.pw-bar.medium { width: 66%; background: #ffcc00; }
.pw-bar.strong { width: 100%; background: #00ff88; }
```
```js
document.getElementById('pw').addEventListener('input', e => {
  const val = e.target.value;
  const bar = document.querySelector('.pw-bar');
  bar.className = 'pw-bar';
  if (val.length >= 8 && /[A-Z]/.test(val) && /[0-9]/.test(val) && /[^A-Za-z0-9]/.test(val)) bar.classList.add('strong');
  else if (val.length >= 6) bar.classList.add('medium');
  else if (val.length > 0) bar.classList.add('weak');
});
```

### file-upload-zone
**Visual:** Drop zone com borda tracejada, ilumina ao arrastar arquivo.
**Quando usar:** Upload de imagem/arquivo, formulários de envio de documentos.
```html
<label class="upload-zone">
  <input type="file" hidden>
  <div class="upload-icon">📁</div>
  <p>Arraste ou clique para enviar</p>
</label>
```
```css
.upload-zone {
  display: block;
  padding: 40px;
  border: 2px dashed #333;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #141414;
}
.upload-zone:hover, .upload-zone.dragover {
  border-color: #00f0ff;
  background: rgba(0,240,255,0.05);
  box-shadow: 0 0 30px rgba(0,240,255,0.2);
}
.upload-icon {
  font-size: 3rem;
  margin-bottom: 12px;
  transition: transform 0.3s ease;
}
.upload-zone:hover .upload-icon { transform: scale(1.1); }
```
```js
document.querySelectorAll('.upload-zone').forEach(zone => {
  ['dragover', 'dragenter'].forEach(ev => {
    zone.addEventListener(ev, e => { e.preventDefault(); zone.classList.add('dragover'); });
  });
  ['dragleave', 'drop'].forEach(ev => {
    zone.addEventListener(ev, () => zone.classList.remove('dragover'));
  });
});
```

### search-expand
**Visual:** Ícone de busca; clica e expande pra input completo.
**Quando usar:** Headers/navbars com pouco espaço, busca não-prioritária.
```html
<div class="search-expand">
  <input type="text" placeholder="Buscar...">
  <button class="search-btn">🔍</button>
</div>
```
```css
.search-expand {
  display: inline-flex;
  align-items: center;
  background: #141414;
  border-radius: 30px;
  overflow: hidden;
  transition: all 0.4s ease;
}
.search-expand input {
  width: 0;
  padding: 0;
  border: none;
  background: transparent;
  color: #fff;
  outline: none;
  transition: all 0.4s ease;
}
.search-expand:focus-within input,
.search-expand:hover input {
  width: 200px;
  padding: 10px 16px;
}
.search-btn {
  background: transparent;
  border: none;
  color: #fff;
  padding: 10px 14px;
  cursor: pointer;
  font-size: 1.1rem;
}
```

### checkbox-check
**Visual:** Checkbox custom com check animado desenhando.
**Quando usar:** Forms, listas de tarefas, filtros, termos de aceite.
```html
<label class="check">
  <input type="checkbox">
  <span class="check-box"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
  Aceito os termos
</label>
```
```css
.check {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}
.check input { display: none; }
.check-box {
  width: 22px; height: 22px;
  border: 2px solid #333;
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.3s ease;
}
.check-box svg {
  width: 14px; height: 14px;
  fill: none;
  stroke: #fff;
  stroke-width: 3;
  stroke-dasharray: 30;
  stroke-dashoffset: 30;
  transition: stroke-dashoffset 0.4s ease;
}
.check input:checked + .check-box {
  background: #00f0ff;
  border-color: #00f0ff;
}
.check input:checked + .check-box svg {
  stroke-dashoffset: 0;
  stroke: #000;
}
```

### toggle-switch
**Visual:** Switch iOS-style, smooth toggle.
**Quando usar:** Settings, ativar/desativar features, modo escuro/claro.
```html
<label class="toggle">
  <input type="checkbox">
  <span class="toggle-slider"></span>
</label>
```
```css
.toggle { position: relative; display: inline-block; width: 56px; height: 30px; }
.toggle input { display: none; }
.toggle-slider {
  position: absolute; inset: 0;
  background: #333;
  border-radius: 30px;
  cursor: pointer;
  transition: background 0.3s ease;
}
.toggle-slider::before {
  content: "";
  position: absolute;
  width: 24px; height: 24px;
  background: #fff;
  border-radius: 50%;
  top: 3px; left: 3px;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}
.toggle input:checked + .toggle-slider {
  background: linear-gradient(90deg, #ff00cc, #00f0ff);
}
.toggle input:checked + .toggle-slider::before {
  transform: translateX(26px);
}
```

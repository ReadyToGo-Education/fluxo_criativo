# Modais, Tooltips e Popovers

8+ efeitos para overlays e popups.

## Índice
modal-fade-scale · modal-slide-up · modal-blur-backdrop · drawer-side · toast-notification · tooltip-fade · popover-arrow · alert-shake-fade

---

### modal-fade-scale
**Visual:** Modal aparece com fade + scale do centro (zoom-in suave).
**Quando usar:** Padrão pra confirmações, login, forms simples. Mais sutil que slide.
```html
<div class="modal-overlay" id="modal">
  <div class="modal-content">conteúdo</div>
</div>
```
```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 1000;
}
.modal-overlay.active {
  opacity: 1;
  visibility: visible;
}
.modal-content {
  background: #141414;
  padding: 32px;
  border-radius: 16px;
  border: 1px solid #222;
  max-width: 500px;
  width: 90%;
  transform: scale(0.85);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.modal-overlay.active .modal-content { transform: scale(1); }
```

### modal-slide-up
**Visual:** Modal entra deslizando de baixo pra cima.
**Quando usar:** Mobile-first, bottom sheets, ações contextuais.
```css
.modal-slide-up {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}
.modal-slide-up .modal-content {
  background: #141414;
  width: 100%;
  max-width: 600px;
  padding: 32px;
  border-radius: 20px 20px 0 0;
  transform: translateY(100%);
  transition: transform 0.4s cubic-bezier(0.4,0,0.2,1);
}
.modal-slide-up.active { opacity: 1; visibility: visible; }
.modal-slide-up.active .modal-content { transform: translateY(0); }
```

### modal-blur-backdrop
**Visual:** Backdrop com blur (não só dim) destacando o modal.
**Quando usar:** Modais premium, dashboards, sites de design forte.
```css
.modal-blur-bg {
  position: fixed;
  inset: 0;
  background: rgba(10,10,10,0.4);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: all 0.4s ease;
  z-index: 1000;
}
.modal-blur-bg.active { opacity: 1; visibility: visible; }
```

### drawer-side
**Visual:** Painel desliza lateralmente da direita (ou esquerda).
**Quando usar:** Carrinho de compras, filtros, configurações, perfil.
```html
<aside class="drawer" id="drawer">
  <div class="drawer-content">conteúdo</div>
</aside>
```
```css
.drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 400px;
  height: 100vh;
  background: #141414;
  border-left: 1px solid #222;
  transform: translateX(100%);
  transition: transform 0.4s cubic-bezier(0.4,0,0.2,1);
  z-index: 1000;
  overflow-y: auto;
}
.drawer.open { transform: translateX(0); }
@media (max-width: 480px) {
  .drawer { width: 100%; }
}
```

### toast-notification
**Visual:** Caixa de notificação entra do canto e some sozinha.
**Quando usar:** Feedback de ação ("salvo!", "erro!"), notificações não-bloqueantes.
```html
<div class="toast-container" id="toasts"></div>
```
```css
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 9999;
}
.toast {
  background: #141414;
  border: 1px solid #222;
  border-left: 4px solid #00f0ff;
  padding: 14px 20px;
  border-radius: 10px;
  color: #fff;
  min-width: 280px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  transform: translateX(120%);
  animation: toastIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
.toast.success { border-left-color: #00ff88; }
.toast.error { border-left-color: #ff3366; }
.toast.removing { animation: toastOut 0.3s ease forwards; }
@keyframes toastIn { to { transform: translateX(0); } }
@keyframes toastOut {
  to { transform: translateX(120%); opacity: 0; }
}
```
```js
function showToast(msg, type = '') {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = msg;
  document.getElementById('toasts').appendChild(toast);
  setTimeout(() => {
    toast.classList.add('removing');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
// Uso: showToast('Salvo com sucesso!', 'success');
```

### tooltip-fade
**Visual:** Tooltip aparece com fade + slide leve no hover.
**Quando usar:** Ajuda contextual, ícones explicativos, abreviações.
```html
<span class="tooltip" data-tip="Texto explicativo">?</span>
```
```css
.tooltip {
  position: relative;
  display: inline-block;
  cursor: help;
  width: 20px; height: 20px;
  background: #333;
  color: #fff;
  border-radius: 50%;
  text-align: center;
  line-height: 20px;
  font-size: 0.8rem;
}
.tooltip::after {
  content: attr(data-tip);
  position: absolute;
  bottom: 130%;
  left: 50%;
  transform: translateX(-50%) translateY(5px);
  background: #1a1a1a;
  color: #fff;
  padding: 8px 12px;
  border-radius: 6px;
  white-space: nowrap;
  font-size: 0.85rem;
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s ease;
  border: 1px solid #333;
}
.tooltip:hover::after {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
```

### popover-arrow
**Visual:** Caixa de informação com seta apontando pro elemento ativador.
**Quando usar:** Onboarding, dicas inline, info adicional ao clicar.
```html
<button class="pop-trigger">Info</button>
<div class="popover">Conteúdo do popover</div>
```
```css
.popover {
  position: absolute;
  background: #1a1a1a;
  border: 1px solid #333;
  padding: 16px;
  border-radius: 10px;
  max-width: 280px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
}
.popover::before {
  content: "";
  position: absolute;
  top: -6px;
  left: 24px;
  width: 12px; height: 12px;
  background: #1a1a1a;
  border-left: 1px solid #333;
  border-top: 1px solid #333;
  transform: rotate(45deg);
}
.popover.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
```

### alert-shake-fade
**Visual:** Alerta de erro entra balançando levemente, chamando atenção.
**Quando usar:** Erros de validação, ações bloqueadas, avisos críticos.
```css
.alert-error {
  background: rgba(255, 51, 102, 0.1);
  border: 1px solid #ff3366;
  color: #ff3366;
  padding: 14px 20px;
  border-radius: 10px;
  animation: alertIn 0.5s ease;
}
@keyframes alertIn {
  0% { opacity: 0; transform: translateX(-10px); }
  20% { opacity: 1; transform: translateX(8px); }
  40% { transform: translateX(-6px); }
  60% { transform: translateX(4px); }
  80% { transform: translateX(-2px); }
  100% { transform: translateX(0); }
}
```

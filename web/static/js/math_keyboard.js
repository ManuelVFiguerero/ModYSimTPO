/**
 * math_keyboard.js – Teclado matemático interactivo (v2).
 *
 * Mejoras:
 *  – Siempre se reabre al clickear cualquier input[data-keyboard]
 *  – Botón ⌨ inline al costado del input para abrir/cerrar
 *  – Minimizar en vez de ocultar → barra inferior colapsada
 *  – Animación de apertura/cierre
 */

const MathKeyboard = (() => {
    const kb       = document.getElementById('math-keyboard');
    const closeBtn = document.getElementById('kb-close');
    const backBtn  = document.getElementById('kb-backspace');
    const clearBtn = document.getElementById('kb-clear');
    let activeInput = null;
    let isOpen = false;

    // ─── Abrir / Cerrar con animaciones ─────────────────────
    function open(inputEl) {
        activeInput = inputEl;
        kb.classList.add('visible');
        kb.classList.remove('minimized');
        isOpen = true;
        // Highlight del input activo
        document.querySelectorAll('.input-math').forEach(i => i.classList.remove('kb-active'));
        if (inputEl) inputEl.classList.add('kb-active');
    }

    function minimize() {
        kb.classList.remove('visible');
        kb.classList.add('minimized');
        isOpen = false;
        document.querySelectorAll('.input-math').forEach(i => i.classList.remove('kb-active'));
    }

    function close() {
        kb.classList.remove('visible', 'minimized');
        isOpen = false;
        activeInput = null;
        document.querySelectorAll('.input-math').forEach(i => i.classList.remove('kb-active'));
    }

    // Botón ✕ → minimiza (no desaparece totalmente)
    closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        minimize();
    });

    // ─── Insertar texto en la posición del cursor ───────────
    function insertAtCursor(text) {
        if (!activeInput) return;
        activeInput.focus();
        const start = activeInput.selectionStart ?? activeInput.value.length;
        const end   = activeInput.selectionEnd   ?? activeInput.value.length;
        const val   = activeInput.value;
        activeInput.value = val.slice(0, start) + text + val.slice(end);
        const newPos = start + text.length;
        activeInput.setSelectionRange(newPos, newPos);
        activeInput.dispatchEvent(new Event('input'));
    }

    // ─── Botones de inserción ───────────────────────────────
    kb.querySelectorAll('.kb-btn[data-insert]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            insertAtCursor(btn.dataset.insert);
        });
    });

    // ─── Borrar último carácter ─────────────────────────────
    backBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (!activeInput) return;
        activeInput.focus();
        const pos = activeInput.selectionStart ?? activeInput.value.length;
        if (pos > 0) {
            const val = activeInput.value;
            activeInput.value = val.slice(0, pos - 1) + val.slice(pos);
            activeInput.setSelectionRange(pos - 1, pos - 1);
        }
    });

    // ─── Limpiar ────────────────────────────────────────────
    clearBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (!activeInput) return;
        activeInput.value = '';
        activeInput.focus();
    });

    // ─── Inyectar botones ⌨ al lado de cada input-math ─────
    function injectToggleButtons() {
        document.querySelectorAll('input[data-keyboard="true"]').forEach(input => {
            if (input.dataset.kbInjected) return;
            input.dataset.kbInjected = 'true';
            // Skip wrapping for inputs inside point-row (they have own layout)
            if (input.closest('.point-inputs')) return;
            // Envolver en un contenedor
            const wrapper = document.createElement('div');
            wrapper.className = 'input-math-wrapper';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);

            const toggleBtn = document.createElement('button');
            toggleBtn.type = 'button';
            toggleBtn.className = 'kb-toggle-btn';
            toggleBtn.innerHTML = '⌨';
            toggleBtn.title = 'Abrir teclado matemático';
            toggleBtn.setAttribute('aria-label', 'Abrir teclado matemático');
            toggleBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();
                if (isOpen && activeInput === input) {
                    minimize();
                } else {
                    open(input);
                }
            });
            wrapper.appendChild(toggleBtn);
        });
    }

    // ─── Event listeners globales ───────────────────────────

    // Click en input[data-keyboard] → siempre abrir
    document.addEventListener('click', (e) => {
        const input = e.target.closest('input[data-keyboard="true"]');
        if (input) {
            open(input);
            return;
        }
        // Click dentro del teclado → no hacer nada
        if (e.target.closest('#math-keyboard')) return;
        // Click en cualquier otro input numérico → no cerrar
        if (e.target.closest('.input-num, .select-premium')) return;
        // Click fuera de todo → minimizar
        if (isOpen) {
            minimize();
        }
    });

    // Focus en input-math → actualizar activeInput
    document.addEventListener('focusin', (e) => {
        if (e.target.matches('input[data-keyboard="true"]')) {
            activeInput = e.target;
            document.querySelectorAll('.input-math').forEach(i => i.classList.remove('kb-active'));
            e.target.classList.add('kb-active');
            if (!isOpen) open(e.target);
        }
    });

    // Barra minimizada → click para reabrir
    kb.addEventListener('click', (e) => {
        if (kb.classList.contains('minimized') && !e.target.closest('.kb-btn, .kb-close-btn')) {
            if (activeInput) {
                open(activeInput);
            }
        }
    });

    // ─── Init ───────────────────────────────────────────────
    // Ejecutar al cargar
    document.addEventListener('DOMContentLoaded', injectToggleButtons);
    // También ahora por si DOMContentLoaded ya pasó
    if (document.readyState !== 'loading') injectToggleButtons();

    return { open, close, minimize, injectToggleButtons };
})();

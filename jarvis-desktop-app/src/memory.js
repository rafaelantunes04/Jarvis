// ── Auth guard (igual ao chat.js) ──────────────────────────────
const USERNAME = sessionStorage.getItem('jarvis_user');
const PASSWORD = sessionStorage.getItem('jarvis_pass');

if (!USERNAME || !PASSWORD) {
  window.location.href = 'login.html';
}

// ── Init UI ───────────────────────────────────────────────────
document.getElementById('sidebar-username').textContent = USERNAME;
document.getElementById('header-user').textContent      = USERNAME;
document.getElementById('avatar-initials').textContent   = USERNAME.charAt(0).toUpperCase();

// ── Tab switching (placeholder, igual ao chat.html) ────────────
// "Definições" ainda não tem página própria — mantém-se apenas
// como destaque visual, tal como no chat.html.
function switchTab(tab) {
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  event.currentTarget.classList.add('active');
}

// ── Logout ────────────────────────────────────────────────────
function logout() {
  sessionStorage.removeItem('jarvis_user');
  sessionStorage.removeItem('jarvis_pass');
  window.location.href = 'login.html';
}

/**
 * ────────────────────────────────────────────────────────────
 * NOTA IMPORTANTE
 * ────────────────────────────────────────────────────────────
 * Este ficheiro implementa apenas a INTERFACE da página de
 * Memória (layout, estados vazios, placeholders visuais).
 *
 * Ainda NÃO existe qualquer lógica funcional para:
 *   - ler o conv_buffer / token_buffer em tempo real;
 *   - ler a memória de longo prazo (mem0);
 *   - atualizar automaticamente os painéis;
 *   - pesquisar na memória de longo prazo.
 *
 * Os elementos abaixo (contadores, barra de progresso, listas)
 * mantêm-se nos seus estados vazios/"0" definidos no HTML até
 * essa integração ser implementada.
 */

/**
 * Sidebar component
 * --------------------------------------------------
 * Uso em cada página:
 *   1. <aside id="sidebar-mount"></aside>  no HTML (onde a sidebar antiga estava)
 *   2. <link rel="stylesheet" href="sidebar.css">
 *   3. <script src="sidebar.js"></script>  (antes do script da própria página)
 *   4. chamar initSidebar('chat')  -- o id tem de corresponder a um item de SIDEBAR_NAV
 *
 * Para adicionar uma página nova, basta acrescentar uma entrada a SIDEBAR_NAV.
 */
const { invoke } = window.__TAURI__.core;

const SIDEBAR_NAV = [
  {
    id: 'chat',
    label: 'Chat',
    href: 'chat.html',
    icon: `<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>`,
  },
  {
    id: 'memory',
    label: 'Memória',
    href: 'memory.html',
    icon: `<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
           <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
           <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>`,
  },
  {
    id: 'settings',
    label: 'Definições',
    href: 'settings.html',
    icon: `<circle cx="12" cy="12" r="3"></circle>
           <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33
                    1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33
                    l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4
                    h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06
                    A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51
                    a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9
                    a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>`,
  },
];

async function sidebarLogout() {
  try {
    await invoke('logout');
  } catch (e) {
    console.warn('Falha ao terminar sessão no servidor:', e);
  }
  sessionStorage.removeItem('jarvis_user');
  window.location.href = 'login.html';
}

function renderSidebarNav(activePage) {
  return SIDEBAR_NAV.map(item => `
    <div class="nav-item ${item.id === activePage ? 'active' : ''}" onclick="window.location.href='${item.href}'">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
           stroke-linecap="round" stroke-linejoin="round">
        ${item.icon}
      </svg>
      ${item.label}
    </div>
  `).join('');
}

function initSidebar(activePage) {
  const mount = document.getElementById('sidebar-mount');
  if (!mount) return;

  const username = sessionStorage.getItem('jarvis_user') || '—';

  mount.classList.add('sidebar');
  mount.innerHTML = `
    <div class="sidebar-brand">
      <div class="icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
      </div>
      <div class="brand-text">
        <h2>Jarvis</h2>
        <span>assistant</span>
      </div>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-label">Menu</div>
      ${renderSidebarNav(activePage)}
    </nav>

    <div class="sidebar-footer">
      <div class="user-row">
        <div class="user-avatar">${username.charAt(0).toUpperCase()}</div>
        <div class="user-info">
          <div class="user-name">${username}</div>
          <div class="user-status">Online</div>
        </div>
      </div>
      <button class="btn-ghost" onclick="sidebarLogout()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        Sair
      </button>
    </div>
  `;
}
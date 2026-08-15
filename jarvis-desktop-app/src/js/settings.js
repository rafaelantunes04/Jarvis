// Auth guard (igual ao chat.js)
const USERNAME = sessionStorage.getItem('jarvis_user');
const PASSWORD = sessionStorage.getItem('jarvis_pass');

if (!USERNAME || !PASSWORD) {
  window.location.href = 'login.html';
}

initSidebar('settings');

// Lógica específica de definições aqui...

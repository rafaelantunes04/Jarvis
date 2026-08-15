const { invoke } = window.__TAURI__.core;

const inpUser   = document.getElementById('inp-user');
const inpPass   = document.getElementById('inp-pass');
const loginBtn  = document.getElementById('login-btn');
const errBanner = document.getElementById('error-banner');

function showError(msg) {
  errBanner.textContent = msg;
  errBanner.classList.add('show');
}
function hideError() {
  errBanner.classList.remove('show');
}

async function doLogin() {
  const username = inpUser.value.trim();
  const password = inpPass.value;

  if (!username || !password) {
    showError('Preenche o utilizador e a palavra-passe.');
    return;
  }

  hideError();
  loginBtn.disabled  = true;
  loginBtn.textContent = 'A entrar…';

  try {
    // Probe: envia mensagem vazia para validar credenciais
    await invoke('send_message', { username, password, message: '__ping__' });

    // Credenciais válidas — guarda na sessão e navega para o chat
    sessionStorage.setItem('jarvis_user', username);
    sessionStorage.setItem('jarvis_pass', password);
    window.location.href = 'chat.html';

  } catch (e) {
    const err = String(e);
    if (err.includes('401')) {
      showError('Credenciais inválidas. Verifica o utilizador e a palavra-passe.');
    } else if (err.includes('ligação') || err.includes('connect')) {
      showError('Não foi possível ligar ao servidor. Garante que está a correr em localhost:8000.');
    } else {
      showError(`Erro inesperado: ${e}`);
    }
    loginBtn.disabled    = false;
    loginBtn.textContent = 'Entrar';
  }
}

// Enter na password faz login
inpPass.addEventListener('keydown', e => {
  if (e.key === 'Enter') doLogin();
});

// Enter no username passa para a password
inpUser.addEventListener('keydown', e => {
  if (e.key === 'Enter') inpPass.focus();
});

loginBtn.addEventListener('click', doLogin);

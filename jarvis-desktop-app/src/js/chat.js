const USERNAME = sessionStorage.getItem('jarvis_user');

if (!USERNAME) {
  window.location.href = 'login.html';
}

// Init UI
initSidebar('chat');
document.getElementById('header-user').textContent = USERNAME;

// Message helpers
const messagesEl  = document.getElementById('messages');
const emptyState  = document.getElementById('empty-state');
const msgInput    = document.getElementById('msg-input');
const sendBtn     = document.getElementById('send-btn');

function hideEmpty() {
  if (emptyState) emptyState.remove();
}

function escHtml(s) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>');
}

function appendMsg(role, text) {
  hideEmpty();
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerHTML = `
    <div class="msg-tag">${role === 'user' ? USERNAME : 'Jarvis'}</div>
    ${escHtml(text)}
  `;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

function showTyping() {
  hideEmpty();
  const t = document.createElement('div');
  t.className = 'typing';
  t.id = 'typing-indicator';
  t.innerHTML = '<span></span><span></span><span></span>';
  messagesEl.appendChild(t);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function hideTyping() {
  const t = document.getElementById('typing-indicator');
  if (t) t.remove();
}

// Send message
async function sendMessage() {
  const text = msgInput.value.trim();
  if (!text) return;

  msgInput.value = '';
  msgInput.style.height = '42px';
  sendBtn.disabled = true;

  appendMsg('user', text);
  showTyping();

  try {
    const reply = await invoke('chat', { message: text });
    hideTyping();
    appendMsg('bot', reply);
  } catch (e) {
    hideTyping();
    const err = String(e);
    if (err.includes('401')) {
      appendMsg('bot', '⚠️ Sessão inválida. A redirecionar para o login…');
      setTimeout(sidebarLogout, 1500);
    } else {
      appendMsg('bot', `⚠️ Erro: ${e}`);
    }
  }

  sendBtn.disabled = false;
  msgInput.focus();
}

// Input events
msgInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

msgInput.addEventListener('input', function () {
  this.style.height = '42px';
  this.style.height = Math.min(this.scrollHeight, 130) + 'px';
});

sendBtn.addEventListener('click', sendMessage);

// Foco automático ao abrir
msgInput.focus();
const USERNAME = sessionStorage.getItem('jarvis_user');

if (!USERNAME) {
  window.location.href = 'login.html';
}

// Init UI
initSidebar('memory');

const refreshBtn   = document.getElementById('refresh-btn');
const listConv      = document.getElementById('list-conv');
const listToken      = document.getElementById('list-token');
const listLongterm   = document.getElementById('list-longterm');
const countConv      = document.getElementById('count-conv');
const countToken      = document.getElementById('count-token');
const countLongterm   = document.getElementById('count-longterm');

function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>');
}

function setLoading(listEl, countEl) {
  countEl.textContent = '…';
  listEl.innerHTML = '<div class="mem-loading">A carregar…</div>';
}

function setError(listEl, countEl, message) {
  countEl.textContent = '!';
  listEl.innerHTML = `<div class="mem-error">⚠️ ${escHtml(message)}</div>`;
}

function setEmpty(listEl, countEl, message) {
  countEl.textContent = '0';
  listEl.innerHTML = `<div class="mem-empty">${escHtml(message)}</div>`;
}

// --- Renderers -------------------------------------------------------

// conv_buffer / token_buffer: lista de { question, answer }
function renderExchanges(listEl, countEl, exchanges, emptyMsg) {
  if (!exchanges || exchanges.length === 0) {
    setEmpty(listEl, countEl, emptyMsg);
    return;
  }

  countEl.textContent = exchanges.length;
  listEl.innerHTML = exchanges.map(ex => `
    <div class="mem-exchange">
      <div class="mem-row q">
        <span class="mem-role">${escHtml(USERNAME)}</span>
        ${escHtml(ex.question)}
      </div>
      <div class="mem-row a">
        <span class="mem-role">Jarvis</span>
        ${escHtml(ex.answer)}
      </div>
    </div>
  `).join('');
}

// long_term_memory: lista de entradas com forma variável (mem0)
function renderFacts(listEl, countEl, facts) {
  if (!facts || facts.length === 0) {
    setEmpty(listEl, countEl, 'Ainda não há memórias de longo prazo guardadas.');
    return;
  }

  countEl.textContent = facts.length;
  listEl.innerHTML = facts.map(fact => {
    // mem0 costuma devolver objetos com um campo "memory" (texto do facto)
    if (fact && typeof fact === 'object' && typeof fact.memory === 'string') {
      const meta = [];
      if (fact.created_at) meta.push(`criado: ${fact.created_at}`);
      if (fact.score !== undefined) meta.push(`score: ${Number(fact.score).toFixed(3)}`);

      return `
        <div class="mem-fact">
          ${escHtml(fact.memory)}
          ${meta.length ? `<div class="mem-fact-meta">${escHtml(meta.join(' · '))}</div>` : ''}
        </div>
      `;
    }

    // string simples
    if (typeof fact === 'string') {
      return `<div class="mem-fact">${escHtml(fact)}</div>`;
    }

    // fallback: qualquer outra forma, mostra o JSON tal como veio
    return `
      <div class="mem-fact">
        <pre>${escHtml(JSON.stringify(fact, null, 2))}</pre>
      </div>
    `;
  }).join('');
}

// --- Load --------------------------------------------------------------

async function loadMemory() {
  refreshBtn.disabled = true;
  refreshBtn.classList.add('spinning');

  setLoading(listConv, countConv);
  setLoading(listToken, countToken);
  setLoading(listLongterm, countLongterm);

  try {
    const mem = await invoke('memory');

    renderExchanges(listConv, countConv, mem.conv_buffer, 'Buffer de conversa vazio.');
    renderExchanges(listToken, countToken, mem.token_buffer, 'Buffer de tokens vazio.');
    renderFacts(listLongterm, countLongterm, mem.long_term_memory);
  } catch (e) {
    const err = String(e);
    if (err.includes('401')) {
      setError(listConv, countConv, 'Sessão inválida. A redirecionar…');
      setError(listToken, countToken, 'Sessão inválida.');
      setError(listLongterm, countLongterm, 'Sessão inválida.');
      setTimeout(sidebarLogout, 1500);
    } else {
      setError(listConv, countConv, err);
      setError(listToken, countToken, err);
      setError(listLongterm, countLongterm, err);
    }
  }

  refreshBtn.disabled = false;
  refreshBtn.classList.remove('spinning');
}

refreshBtn.addEventListener('click', loadMemory);

loadMemory();
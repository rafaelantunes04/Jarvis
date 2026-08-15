const USERNAME = sessionStorage.getItem('jarvis_user');

if (!USERNAME) {
  window.location.href = 'login.html';
}

initSidebar('settings');

const API_URL = 'http://localhost:8000';
let authToken = null;

document.addEventListener('DOMContentLoaded', async () => {
  authToken = await getStoredToken();
  if (authToken) {
    showCredentialsSection();
    loadCredentials();
  } else {
    showLoginSection();
  }
});

document.getElementById('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const loginError = document.getElementById('login-error');
  
  try {
    showLoading(true);
    loginError.textContent = '';
    
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await fetch(`${API_URL}/token`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error('Invalid credentials');
    }
    
    const data = await response.json();
    authToken = data.access_token;
    await chrome.storage.local.set({ authToken });
    
    showCredentialsSection();
    loadCredentials();
  } catch (error) {
    loginError.textContent = error.message;
  } finally {
    showLoading(false);
  }
});

document.getElementById('logout-btn').addEventListener('click', async () => {
  await chrome.storage.local.remove('authToken');
  authToken = null;
  showLoginSection();
});

async function loadCredentials() {
  try {
    showLoading(true);
    
    const response = await fetch(`${API_URL}/credentials`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    
    if (!response.ok) {
      if (response.status === 401) {
        await chrome.storage.local.remove('authToken');
        authToken = null;
        showLoginSection();
        return;
      }
      throw new Error('Failed to load credentials');
    }
    
    const credentials = await response.json();
    displayCredentials(credentials);
  } catch (error) {
    console.error('Error loading credentials:', error);
  } finally {
    showLoading(false);
  }
}

function displayCredentials(credentials) {
  const credentialsList = document.getElementById('credentials-list');
  credentialsList.innerHTML = '';
  
  if (credentials.length === 0) {
    credentialsList.innerHTML = '<p>No credentials assigned to your account.</p>';
    return;
  }
  
  credentials.forEach(credential => {
    const item = document.createElement('div');
    item.className = 'credential-item';
    item.innerHTML = `
      <div class="credential-info">
        <div class="credential-name">${credential.name}</div>
        <div class="credential-username">${credential.username}</div>
      </div>
      <button class="switch-btn" data-id="${credential.id}">Switch</button>
    `;
    
    item.querySelector('.switch-btn').addEventListener('click', () => {
      switchToAccount(credential.id);
    });
    
    credentialsList.appendChild(item);
  });
}

async function switchToAccount(credentialId) {
  try {
    showLoading(true);
    
    const response = await fetch(`${API_URL}/credentials/${credentialId}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    
    if (!response.ok) {
      throw new Error('Failed to get credential details');
    }
    
    const credential = await response.json();
    
    chrome.runtime.sendMessage({
      action: 'login',
      username: credential.username,
      password: credential.password
    }, (response) => {
      showLoading(false);
      if (response.success) {
        showStatus('Successfully logged in!', 'success');
      } else {
        showStatus('Login failed: ' + response.error, 'error');
      }
    });
  } catch (error) {
    showLoading(false);
    showStatus('Error: ' + error.message, 'error');
  }
}

function showLoginSection() {
  document.getElementById('login-section').classList.remove('hidden');
  document.getElementById('credentials-section').classList.add('hidden');
}

function showCredentialsSection() {
  document.getElementById('login-section').classList.add('hidden');
  document.getElementById('credentials-section').classList.remove('hidden');
}

function showLoading(show) {
  document.getElementById('loading').classList.toggle('hidden', !show);
}

function showStatus(message, type) {
  const existingStatus = document.querySelector('.status');
  if (existingStatus) {
    existingStatus.remove();
  }
  
  const status = document.createElement('div');
  status.className = `status ${type}`;
  status.textContent = message;
  document.querySelector('.container').appendChild(status);
  
  setTimeout(() => {
    status.remove();
  }, 3000);
}

async function getStoredToken() {
  const result = await chrome.storage.local.get('authToken');
  return result.authToken || null;
}
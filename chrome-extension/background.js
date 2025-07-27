chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'login') {
    performLogin(request.username, request.password)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep the message channel open for async response
  }
});

async function performLogin(username, password) {
  try {
    // Clear existing cookies for FanFix
    await clearFanFixCookies();
    
    // Create a new tab with the login page
    const tab = await chrome.tabs.create({
      url: 'https://auth.fanfix.io/login',
      active: true
    });
    
    const tabId = tab.id;
    console.log('Created tab with ID:', tabId);
    
    // Wait for page to be ready
    await new Promise((resolve) => {
      chrome.tabs.onUpdated.addListener(function listener(updatedTabId, changeInfo) {
        if (updatedTabId === tabId && changeInfo.status === 'complete') {
          chrome.tabs.onUpdated.removeListener(listener);
          resolve();
        }
      });
    });
    
    // Small delay to ensure content script is loaded
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Send credentials to content script
    // The content script will intercept the fetch request and inject real credentials
    try {
      await chrome.tabs.sendMessage(tabId, {
        action: 'fillAndSubmit',
        credentials: {
          username: username,
          password: password
        }
      });
    } catch (error) {
      console.error('Failed to send message to content script:', error);
      throw error;
    }
    
    // Wait for redirect to creator dashboard
    return new Promise((resolve) => {
      let checkCount = 0;
      const maxChecks = 20; // 10 seconds total
      
      const checkInterval = setInterval(async () => {
        checkCount++;
        
        try {
          const currentTab = await chrome.tabs.get(tabId);
          
          if (currentTab.url && currentTab.url.includes('creator.fanfix.io')) {
            clearInterval(checkInterval);
            resolve({ success: true });
          } else if (checkCount >= maxChecks) {
            clearInterval(checkInterval);
            resolve({ success: false, error: 'Login timeout - no redirect detected' });
          }
        } catch (e) {
          // Tab might be closed
          clearInterval(checkInterval);
          resolve({ success: false, error: 'Tab was closed' });
        }
      }, 500);
    });
    
  } catch (error) {
    console.error('Login error:', error);
    return { success: false, error: error.message };
  }
}

async function clearFanFixCookies() {
  try {
    // Get all cookies for fanfix.io domains
    const cookies = await chrome.cookies.getAll({ domain: '.fanfix.io' });
    
    for (const cookie of cookies) {
      // Fix the domain - remove leading dot for URL construction
      const domain = cookie.domain.startsWith('.') ? cookie.domain.substring(1) : cookie.domain;
      const url = `https://${domain}${cookie.path}`;
      
      await chrome.cookies.remove({
        url: url,
        name: cookie.name
      });
    }
    
    // Also clear cookies for auth.fanfix.io specifically
    const authCookies = await chrome.cookies.getAll({ domain: 'auth.fanfix.io' });
    for (const cookie of authCookies) {
      await chrome.cookies.remove({
        url: `https://auth.fanfix.io${cookie.path}`,
        name: cookie.name
      });
    }
  } catch (error) {
    console.error('Error clearing cookies:', error);
  }
}
let playwright = null;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'login') {
    performLogin(request.username, request.password)
      .then(() => sendResponse({ success: true }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep the message channel open for async response
  }
});

async function performLogin(username, password) {
  try {
    // Clear existing cookies for FanFix
    await clearFanFixCookies();
    
    // Create a new tab with FanFix login page
    const tab = await chrome.tabs.create({
      url: 'https://auth.fanfix.io/login',
      active: true
    });
    
    // Wait for the page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Inject login script
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: autoLogin,
      args: [username, password]
    });
    
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

async function clearFanFixCookies() {
  const cookies = await chrome.cookies.getAll({ domain: '.fanfix.io' });
  for (const cookie of cookies) {
    await chrome.cookies.remove({
      url: `https://${cookie.domain}${cookie.path}`,
      name: cookie.name
    });
  }
}

// This function will be injected into the FanFix login page
function autoLogin(username, password) {
  const fillAndSubmit = () => {
    // Wait for the form elements to be present
    const emailInput = document.querySelector('input[type="email"], input[name="email"], input[placeholder*="email" i]');
    const passwordInput = document.querySelector('input[type="password"], input[name="password"]');
    const submitButton = document.querySelector('button[type="submit"], button:has-text("Sign in"), button:has-text("Log in")');
    
    if (emailInput && passwordInput) {
      // Fill in the credentials
      emailInput.value = username;
      emailInput.dispatchEvent(new Event('input', { bubbles: true }));
      emailInput.dispatchEvent(new Event('change', { bubbles: true }));
      
      passwordInput.value = password;
      passwordInput.dispatchEvent(new Event('input', { bubbles: true }));
      passwordInput.dispatchEvent(new Event('change', { bubbles: true }));
      
      // Submit the form
      if (submitButton) {
        setTimeout(() => {
          submitButton.click();
        }, 500);
      } else {
        // Try to submit the form directly
        const form = emailInput.closest('form');
        if (form) {
          setTimeout(() => {
            form.submit();
          }, 500);
        }
      }
    } else {
      // Retry if elements not found
      setTimeout(fillAndSubmit, 500);
    }
  };
  
  fillAndSubmit();
}
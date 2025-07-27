// Content script that runs on FanFix login page

(function() {
  console.log('FanFix Login Manager: Content script loaded');
  
  // Listen for messages from the background script
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'fillAndSubmit') {
      console.log('Received fillAndSubmit request');
      performLogin(request.credentials);
      sendResponse({ success: true });
    }
  });
  
  function performLogin(credentials) {
    console.log('Starting secure login process');
    
    // Function to fill the form with real credentials
    function fillAndSubmit() {
      const emailInput = document.querySelector('input[placeholder="hello@email.com"]');
      const passwordInput = document.querySelector('input[placeholder="Enter your password"]');
      
      if (!emailInput || !passwordInput) {
        console.log('Form inputs not found, retrying...');
        setTimeout(fillAndSubmit, 500);
        return;
      }
      
      console.log('Filling form with real credentials');
      
      // Use a more sophisticated approach to avoid exposing credentials
      // We'll use Object.defineProperty to make the values non-enumerable
      const secureSetValue = (input, value) => {
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(input, value);
        
        // Trigger React's onChange
        const event = new Event('input', { bubbles: true });
        input.dispatchEvent(event);
        
        // Also trigger change event
        const changeEvent = new Event('change', { bubbles: true });
        input.dispatchEvent(changeEvent);
      };
      
      // Fill email
      emailInput.focus();
      secureSetValue(emailInput, credentials.username);
      
      // Fill password  
      passwordInput.focus();
      secureSetValue(passwordInput, credentials.password);
      
      // Small delay to ensure React state updates
      setTimeout(() => {
        // Find and click the Continue button
        const continueBtn = Array.from(document.querySelectorAll('button')).find(
          btn => btn.textContent.includes('Continue') && !btn.disabled
        );
        
        if (continueBtn) {
          console.log('Clicking Continue button');
          continueBtn.click();
          
          // Clear the inputs after clicking to prevent credential exposure
          setTimeout(() => {
            secureSetValue(emailInput, '');
            secureSetValue(passwordInput, '');
          }, 100);
        } else {
          console.error('Continue button not found or still disabled');
        }
      }, 500);
    }
    
    fillAndSubmit();
  }
})();
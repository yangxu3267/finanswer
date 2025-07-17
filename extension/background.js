// Background script to handle communication with the Flask server
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'analyzeSentiment') {
    analyzeSentiment(request.text)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ error: error.message }));
    return true; // Keep the message channel open for async response
  }
});

async function analyzeSentiment(text) {
  try {
    // First check if server is running
    const healthCheck = await fetch('http://localhost:5001/health', {
      method: 'GET',
      timeout: 3000 // 3 second timeout
    }).catch(() => null);

    if (!healthCheck || !healthCheck.ok) {
      throw new Error('Server is not running. Please start the Finanswer backend server first.');
    }

    const response = await fetch('http://localhost:5001/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: text })
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Analysis endpoint not found. Please check server configuration.');
      } else if (response.status === 500) {
        throw new Error('Server error occurred. Please try again later.');
      } else if (response.status === 413) {
        throw new Error('Text is too long. Please try with shorter content.');
      } else {
        throw new Error(`Server error (${response.status}). Please try again.`);
      }
    }

    const result = await response.json();
    
    if (result.error) {
      throw new Error(result.error);
    }

    // Validate response structure
    if (!result.label || !result.confidence) {
      throw new Error('Invalid response from server. Please try again.');
    }

    return result;
  } catch (error) {
    console.error('Error calling sentiment analysis API:', error);
    
    // Provide more specific error messages
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Cannot connect to server. Please make sure the Finanswer backend is running on http://localhost:5001');
    } else if (error.message.includes('timeout')) {
      throw new Error('Server is taking too long to respond. Please try again.');
    } else {
      throw new Error(error.message || 'Failed to analyze sentiment. Please try again.');
    }
  }
}

// Check server health on startup
chrome.runtime.onStartup.addListener(async () => {
  try {
    const response = await fetch('http://localhost:5001/health', {
      method: 'GET',
      timeout: 5000
    });
    if (response.ok) {
      console.log('✅ Finanswer server is running');
    } else {
      console.warn('⚠️ Finanswer server responded with error');
    }
  } catch (error) {
    console.warn('⚠️ Finanswer server is not running. Please start the server first.');
  }
});

// Also check when extension is installed/updated
chrome.runtime.onInstalled.addListener(async () => {
  try {
    const response = await fetch('http://localhost:5001/health', {
      method: 'GET',
      timeout: 5000
    });
    if (response.ok) {
      console.log('✅ Finanswer server is running');
    } else {
      console.warn('⚠️ Finanswer server responded with error');
    }
  } catch (error) {
    console.warn('⚠️ Finanswer server is not running. Please start the server first.');
  }
}); 
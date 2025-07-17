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
    const response = await fetch('http://localhost:5001/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: text })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    
    if (result.error) {
      throw new Error(result.error);
    }

    return result;
  } catch (error) {
    console.error('Error calling sentiment analysis API:', error);
    throw new Error('Failed to analyze sentiment. Please make sure the server is running.');
  }
}

// Check server health on startup
chrome.runtime.onStartup.addListener(async () => {
  try {
    const response = await fetch('http://localhost:5001/health');
    if (response.ok) {
      console.log('FinBERT server is running');
    }
  } catch (error) {
    console.warn('FinBERT server is not running. Please start the server first.');
  }
}); 
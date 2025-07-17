// Content script to extract text from the current page
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'extractText') {
    try {
      // Extract text content from the page
      const text = extractFinancialText();
      sendResponse({ text: text });
    } catch (error) {
      console.error('Error extracting text:', error);
      sendResponse({ error: error.message });
    }
    return true; // Keep the message channel open for async response
  }
});

function extractFinancialText() {
  // Priority selectors for financial content
  const selectors = [
    // Article content
    'article',
    '[role="main"]',
    '.article-content',
    '.post-content',
    '.entry-content',
    '.content',
    '.main-content',
    
    // Financial news specific
    '.financial-news',
    '.market-news',
    '.business-news',
    '.stock-news',
    
    // Common content areas
    '.text-content',
    '.body-content',
    '.story-content',
    '.news-content',
    
    // Fallback to main content areas
    'main',
    '#main',
    '#content',
    '.main'
  ];

  let content = '';
  
  // Try to find content using priority selectors
  for (const selector of selectors) {
    const elements = document.querySelectorAll(selector);
    if (elements.length > 0) {
      // Get text from the largest content element
      let maxLength = 0;
      let bestElement = null;
      
      elements.forEach(element => {
        const text = element.textContent.trim();
        if (text.length > maxLength && text.length > 100) { // Minimum 100 chars
          maxLength = text.length;
          bestElement = element;
        }
      });
      
      if (bestElement) {
        content = bestElement.textContent.trim();
        break;
      }
    }
  }
  
  // If no specific content found, try to extract from paragraphs
  if (!content) {
    const paragraphs = document.querySelectorAll('p');
    const texts = [];
    
    paragraphs.forEach(p => {
      const text = p.textContent.trim();
      if (text.length > 50) { // Only paragraphs with substantial content
        texts.push(text);
      }
    });
    
    content = texts.join(' ');
  }
  
  // Clean up the text
  content = cleanText(content);
  
  // If still no content, use body text as fallback
  if (!content || content.length < 100) {
    content = document.body.textContent.trim();
    content = cleanText(content);
  }
  
  return content;
}

function cleanText(text) {
  if (!text) return '';
  
  return text
    // Remove extra whitespace
    .replace(/\s+/g, ' ')
    // Remove common non-content elements
    .replace(/menu|navigation|header|footer|sidebar/gi, '')
    // Remove excessive punctuation
    .replace(/[.!?]{2,}/g, '.')
    // Remove multiple spaces
    .replace(/\s{2,}/g, ' ')
    // Trim
    .trim();
} 
document.addEventListener('DOMContentLoaded', function() {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const loading = document.getElementById('loading');
  const result = document.getElementById('result');
  const meterPointer = document.getElementById('meterPointer');
  const mainScore = document.getElementById('mainScore');
  const newsSummary = document.getElementById('newsSummary');
  const investmentAdvice = document.getElementById('investmentAdvice');
  const feedbackUp = document.getElementById('feedbackUp');
  const feedbackDown = document.getElementById('feedbackDown');
  
  // 存储当前分析结果用于反馈
  let currentAnalysis = null;

  analyzeBtn.addEventListener('click', async function() {
    analyzeBtn.disabled = true;
    loading.style.display = 'block';
    result.style.display = 'none';
<<<<<<< HEAD
    
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (!tab) {
        throw new Error('No active tab found');
      }
      
      const response = await chrome.tabs.sendMessage(tab.id, { action: 'extractText' });
      
      if (!response) {
        throw new Error('Could not communicate with the page. Please refresh and try again.');
      }
      
      if (!response.text || response.text.trim().length === 0) {
        throw new Error('No text content found on this page. Please try on a page with financial news or content.');
      }
      
      if (response.text.length > 10000) {
        throw new Error('Text is too long. Please try on a shorter article or specific section.');
      }
      
      const sentimentResult = await chrome.runtime.sendMessage({
        action: 'analyzeSentiment',
        text: response.text
      });
      
      if (sentimentResult.error) {
        throw new Error(sentimentResult.error);
      }
      
      displayResult(sentimentResult);
      
    } catch (error) {
      console.error('Analysis error:', error);
      
      // Provide user-friendly error messages
      let userMessage = 'Could not analyze this page. ';
      
      if (error.message.includes('Server is not running')) {
        userMessage = 'Backend server is not running. Please start the Finanswer server first.';
      } else if (error.message.includes('Cannot connect')) {
        userMessage = 'Cannot connect to server. Please make sure the backend is running on localhost:5001';
      } else if (error.message.includes('No text content')) {
        userMessage = 'No readable text found on this page. Please try on a financial news article.';
      } else if (error.message.includes('Text is too long')) {
        userMessage = 'The content is too long to analyze. Please try on a shorter article.';
      } else if (error.message.includes('timeout')) {
        userMessage = 'Server is taking too long to respond. Please try again.';
      } else {
        userMessage += 'Please try on a different page or check if the server is running.';
      }
      
      showError(userMessage);
=======
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      const response = await chrome.tabs.sendMessage(tab.id, { action: 'extractText' });
      if (response && response.text) {
        const sentimentResult = await chrome.runtime.sendMessage({
          action: 'analyzeSentiment',
          text: response.text
        });
        displayResult(sentimentResult);
      } else {
        throw new Error('No text content found on this page');
      }
    } catch (error) {
      showError('Could not analyze this page. Please try on a page with financial content.');
>>>>>>> 19f0d3a5886c124d05ccfac9814d3ad81dbe8263
    } finally {
      loading.style.display = 'none';
      analyzeBtn.disabled = false;
    }
  });

  function displayResult(sentimentResult) {
    const { label, confidence, scores, summary, investment_advice } = sentimentResult;
    const labelMap = {
      'LABEL_0': 'Negative',
      'LABEL_1': 'Neutral',
      'LABEL_2': 'Positive'
    };
    const readableLabel = labelMap[label] || label;
    const confidencePercent = (confidence * 100).toFixed(1);
    
    // 存储当前分析结果用于反馈
    currentAnalysis = {
      ...sentimentResult,
      readableLabel,
      confidencePercent,
      timestamp: new Date().toISOString()
    };
    
    // 主分数高亮
    mainScore.textContent = `${readableLabel} (${confidencePercent}%)`;
    mainScore.className = 'main-score ' + readableLabel.toLowerCase();
<<<<<<< HEAD
    
=======
>>>>>>> 19f0d3a5886c124d05ccfac9814d3ad81dbe8263
    // 进度条指针
    let position;
    if (label === 'LABEL_0') {
      position = scores.negative * 33;
    } else if (label === 'LABEL_1') {
      position = 33 + (scores.neutral * 34);
    } else {
      position = 67 + (scores.positive * 33);
    }
    meterPointer.style.left = `${position}%`;
<<<<<<< HEAD
    meterPointer.style.display = 'block'; // Show meter pointer for successful analysis
    
    // 摘要和建议
    newsSummary.textContent = summary || 'No summary available for this content.';
    investmentAdvice.textContent = investment_advice || 'No specific investment advice available for this content.';
    
    result.style.display = 'block';
    
    // 重置反馈按钮状态并显示
    resetFeedbackButtons();
    feedbackUp.style.display = 'block';
    feedbackDown.style.display = 'block';
  }

  function showError(message) {
    mainScore.textContent = 'Analysis Failed';
    mainScore.className = 'main-score negative';
    
    // Clear previous content
    newsSummary.textContent = message;
    investmentAdvice.textContent = 'Please check the following:\n• Backend server is running\n• You are on a financial news page\n• Page has readable text content';
    
    // Hide meter pointer for errors
    meterPointer.style.display = 'none';
    
    result.style.display = 'block';
    
    // Reset feedback buttons for errors
    resetFeedbackButtons();
    feedbackUp.style.display = 'none';
    feedbackDown.style.display = 'none';
=======
    // 摘要和建议
    newsSummary.textContent = summary || '';
    investmentAdvice.textContent = investment_advice || '';
    result.style.display = 'block';
    
    // 重置反馈按钮状态
    resetFeedbackButtons();
  }

  function showError(message) {
    mainScore.textContent = 'Error';
    mainScore.className = 'main-score negative';
    newsSummary.textContent = message;
    investmentAdvice.textContent = 'Unable to provide investment advice due to analysis error.';
    result.style.display = 'block';
>>>>>>> 19f0d3a5886c124d05ccfac9814d3ad81dbe8263
  }
  
  // 反馈按钮事件监听器
  feedbackUp.addEventListener('click', () => submitFeedback('accurate'));
  feedbackDown.addEventListener('click', () => submitFeedback('inaccurate'));
  
  async function submitFeedback(feedbackType) {
    if (!currentAnalysis) return;
    
    // 禁用两个按钮
    feedbackUp.disabled = true;
    feedbackDown.disabled = true;
    
    // 更新按钮样式
    if (feedbackType === 'accurate') {
      feedbackUp.classList.add('submitted');
      feedbackDown.classList.remove('submitted');
    } else {
      feedbackDown.classList.add('submitted');
      feedbackUp.classList.remove('submitted');
    }
    
    // 准备反馈数据
    const feedbackData = {
      text: currentAnalysis.text || '',
      predicted_sentiment: currentAnalysis.label,
      predicted_confidence: currentAnalysis.confidence,
      user_feedback: feedbackType,
      timestamp: currentAnalysis.timestamp,
      page_url: window.location.href,
      model_version: '1.0' // 可以用于追踪模型版本
    };
    
    // 如果没有原始文本，尝试从当前页面获取
    if (!feedbackData.text) {
      try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const response = await chrome.tabs.sendMessage(tab.id, { action: 'extractText' });
        if (response && response.text) {
          feedbackData.text = response.text;
        }
      } catch (error) {
        console.log('Could not extract text for feedback');
      }
    }
    
    // 发送反馈到后端
    sendFeedbackToServer(feedbackData);
  }
  
  function resetFeedbackButtons() {
    feedbackUp.disabled = false;
    feedbackDown.disabled = false;
    feedbackUp.classList.remove('submitted');
    feedbackDown.classList.remove('submitted');
  }
  
  async function sendFeedbackToServer(feedbackData) {
    try {
      const response = await fetch('http://localhost:5001/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData)
      });
      
      if (response.ok) {
        console.log('Feedback submitted successfully');
        // 可以显示一个小的成功提示
        showFeedbackSuccess();
      } else {
        console.error('Failed to submit feedback');
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      // 即使失败也不影响用户体验
    }
  }
  
  function showFeedbackSuccess() {
    // 简单的成功提示
    const feedbackTitle = document.querySelector('.feedback-title');
    const originalText = feedbackTitle.textContent;
    feedbackTitle.textContent = 'Thank you for your feedback!';
    feedbackTitle.style.color = '#4ade80';
    
    setTimeout(() => {
      feedbackTitle.textContent = originalText;
      feedbackTitle.style.color = '#aaa';
    }, 2000);
  }
}); 
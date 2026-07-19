// Chandran's Portfolio Website -- Zero-dependency Visitor Analytics Tracker

(function() {
  const STORAGE_KEY = 'portfolio_analytics_logs';
  let sessionStart = Date.now();
  let accumulatedTime = 0;
  let isActive = true;
  let activeStart = Date.now();

  // Helper to generate a unique session ID
  function generateSessionId() {
    return 'sess_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now();
  }

  // Get current session or create a new one
  let sessionId = sessionStorage.getItem('portfolio_analytics_session_id');
  if (!sessionId) {
    sessionId = generateSessionId();
    sessionStorage.setItem('portfolio_analytics_session_id', sessionId);
  }

  // Extract traffic source / referrer
  function getTrafficSource() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('utm_source')) {
        return urlParams.get('utm_source');
    }
    if (urlParams.has('ref')) {
        return urlParams.get('ref');
    }
    
    const referrer = document.referrer;
    if (referrer) {
      try {
        const url = new URL(referrer);
        if (url.hostname.includes('linkedin.com')) return 'LinkedIn';
        if (url.hostname.includes('github.com')) return 'GitHub';
        if (url.hostname.includes('google.com')) return 'Google Search';
        return url.hostname; // Return main domain name
      } catch (e) {
        return 'Other Referrer';
      }
    }
    return 'Direct Link';
  }

  // Calculate current duration on active page
  function updateTimeSpent() {
    if (isActive) {
      accumulatedTime += (Date.now() - activeStart) / 1000;
      activeStart = Date.now();
    }
  }

  // Log visitor event locally to localStorage
  function saveLog() {
    updateTimeSpent();
    
    const pageTitle = document.title || window.location.pathname;
    const pagePath = window.location.pathname.split('/').pop() || 'index.html';
    const source = getTrafficSource();
    
    // Read existing logs
    let logs = [];
    try {
      logs = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (e) {
      logs = [];
    }
    
    // Check if this session already exists for this page
    let sessionLog = logs.find(l => l.sessionId === sessionId && l.pagePath === pagePath);
    
    if (sessionLog) {
      // Update duration and last active time
      sessionLog.timeSpent = Math.round(accumulatedTime);
      sessionLog.lastActive = new Date().toISOString();
    } else {
      // Create new log entry
      sessionLog = {
        sessionId: sessionId,
        pagePath: pagePath,
        pageTitle: pageTitle,
        source: source,
        timeSpent: Math.round(accumulatedTime),
        startedAt: new Date(sessionStart).toISOString(),
        lastActive: new Date().toISOString(),
        userAgent: navigator.userAgent
      };
      logs.push(sessionLog);
    }
    
    // Prune logs if they exceed 500 records to save memory
    if (logs.length > 500) {
      logs.shift();
    }
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(logs));
    
    // =========================================================================
    // PRODUCTION REMOTES WEBHOOK
    // If you want to view real users' analytics in real-time on a remote server,
    // uncomment and configure the block below to send beacons to your database/webhook:
    /*
    const payload = JSON.stringify(sessionLog);
    if (navigator.sendBeacon) {
      navigator.sendBeacon('https://your-analytics-api-webhook.com/log', payload);
    } else {
      fetch('https://your-analytics-api-webhook.com/log', { method: 'POST', body: payload, keepalive: true });
    }
    */
    // =========================================================================
  }

  // Handle page visibility/focus changes to only track active view time
  window.addEventListener('focus', () => {
    if (!isActive) {
      isActive = true;
      activeStart = Date.now();
    }
  });

  window.addEventListener('blur', () => {
    if (isActive) {
      updateTimeSpent();
      isActive = false;
      saveLog();
    }
  });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      if (isActive) {
        updateTimeSpent();
        isActive = false;
        saveLog();
      }
    } else {
      if (!isActive) {
        isActive = true;
        activeStart = Date.now();
      }
    }
  });

  // Save log on navigation / page close
  window.addEventListener('beforeunload', saveLog);
  window.addEventListener('pagehide', saveLog);

  // Periodically save log every 10 seconds to ensure time is tracked on long sessions
  setInterval(saveLog, 10000);

  // Initial trigger
  saveLog();
})();

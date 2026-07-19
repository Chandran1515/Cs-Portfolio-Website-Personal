/**
 * LinkedIn Feed & Live Profile Integration Script
 * CS Portfolio Website
 */

// User Configuration Block - Easily editable
const LINKEDIN_FEED_CONFIG = {
  // Your public LinkedIn profile URL
  profileUrl: "https://www.linkedin.com/in/ar-chandran-shanmugam-421b7b149",
  
  // Date when you started your professional career (used to auto-calculate years of experience)
  careerStartDate: "2017-09-01",
  
  // Date when you started working in California (used to auto-calculate California experience)
  californiaStartDate: "2022-09-01",
  // Date when you finished working in California (set to null if currently ongoing)
  californiaEndDate: "2026-04-30",

  // Option 1: Native Video Embeds (Highest performance & responsive look)
  // Fill in the 'embedUrl' with the URL from LinkedIn's 'Embed this post' iframe src.
  // Example format: https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7219273982935293952
  embeddedPosts: [
    {
      id: "sheetcraft",
      title: "SheetCraft Automation Tool in Action",
      desc: "Watch how SheetCraft automates sheet naming, drawing numbering, view alignment, and titleblock coordination in Autodesk Revit.",
      embedUrl: "", // Paste your LinkedIn iframe src here
      postUrl: "https://www.linkedin.com/in/ar-chandran-shanmugam-421b7b149/recent-activity/all/"
    },
    {
      id: "aiconnector",
      title: "AI Connector Live Walkthrough",
      desc: "Demonstrating how natural language AI agents query Revit models, edit parameters, and coordinate BIM databases live.",
      embedUrl: "", // Paste your LinkedIn iframe src here
      postUrl: "https://www.linkedin.com/in/ar-chandran-shanmugam-421b7b149/recent-activity/all/"
    },
    {
      id: "batchexport",
      title: "Batch Export Suite Demonstration",
      desc: "Multi-threaded Revit API tool exporting over 100 sheets to PDF/DWG in seconds, with automatic revision matching.",
      embedUrl: "", // Paste your LinkedIn iframe src here
      postUrl: "https://www.linkedin.com/in/ar-chandran-shanmugam-421b7b149/recent-activity/all/"
    }
  ],

  // Option 2: Automatic RSS Feed (Zero-maintenance auto-update)
  // To use, generate a free RSS feed of your LinkedIn posts using rss.app or fetchrss.com,
  // then paste the feed URL here.
  rssFeedUrl: "",

  // Option 3: Third-Party Widget (e.g., Elfsight, SociableKIT, Juicer)
  // If you configure a third-party feed widget, paste its HTML script/embed code here.
  widgetHtml: ""
};

// Main Execution
document.addEventListener("DOMContentLoaded", () => {
  initExperienceCalculations();
  initLinkedInFeed();
  initPortfolioVideoEmbeds();
});

/**
 * Automatically calculates years of experience and updates relevant DOM elements.
 */
function initExperienceCalculations() {
  try {
    const startCareer = new Date(LINKEDIN_FEED_CONFIG.careerStartDate);
    const today = new Date();
    
    // Calculate total years of experience
    let totalYears = today.getFullYear() - startCareer.getFullYear();
    const monthDiff = today.getMonth() - startCareer.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < startCareer.getDate())) {
      totalYears--;
    }
    
    // Calculate California years
    const startCA = new Date(LINKEDIN_FEED_CONFIG.californiaStartDate);
    const endCA = LINKEDIN_FEED_CONFIG.californiaEndDate 
      ? new Date(LINKEDIN_FEED_CONFIG.californiaEndDate) 
      : today;
      
    let caDiffMs = endCA.getTime() - startCA.getTime();
    let caYears = (caDiffMs / (1000 * 60 * 60 * 24 * 365.25)).toFixed(1);
    
    // Convert to a clean text representation (e.g. 8+, 3.5+)
    const totalExpText = `${totalYears}+`;
    const caExpText = `${parseFloat(caYears)}+`;

    // Update index.html DOM elements
    document.querySelectorAll(".dyn-exp-total").forEach(el => {
      // Retain structure: e.g. "8+" or "8+ years"
      if (el.textContent.toLowerCase().includes("years")) {
        el.textContent = `${totalExpText} years`;
      } else {
        el.textContent = totalExpText;
      }
    });

    document.querySelectorAll(".dyn-exp-ca").forEach(el => {
      el.textContent = `${caExpText} years in California`;
    });
  } catch (err) {
    console.error("Error calculating experience:", err);
  }
}

/**
 * Initializes and populates the LinkedIn feed on the homepage.
 */
function initLinkedInFeed() {
  const container = document.getElementById("linkedin-feed-container");
  if (!container) return;

  // 1. Check if a third-party widget is configured
  if (LINKEDIN_FEED_CONFIG.widgetHtml && LINKEDIN_FEED_CONFIG.widgetHtml.trim() !== "") {
    container.innerHTML = LINKEDIN_FEED_CONFIG.widgetHtml;
    // Execute scripts inside widget if necessary
    const scripts = container.querySelectorAll("script");
    scripts.forEach(oldScript => {
      const newScript = document.createElement("script");
      Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
      newScript.appendChild(document.createTextNode(oldScript.innerHTML));
      oldScript.parentNode.replaceChild(newScript, oldScript);
    });
    return;
  }

  // 2. Check if an RSS Feed is configured
  if (LINKEDIN_FEED_CONFIG.rssFeedUrl && LINKEDIN_FEED_CONFIG.rssFeedUrl.trim() !== "") {
    container.innerHTML = `
      <div class="demo-card-placeholder">
        <p>Loading recent posts from LinkedIn...</p>
      </div>
    `;
    
    // Fetch RSS feed via a free RSS-to-JSON API
    const rssJsonUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(LINKEDIN_FEED_CONFIG.rssFeedUrl)}`;
    
    fetch(rssJsonUrl)
      .then(res => res.json())
      .then(data => {
        if (data.status === "ok" && data.items && data.items.length > 0) {
          container.innerHTML = "";
          // Display up to 3 items
          const items = data.items.slice(0, 3);
          items.forEach(item => {
            // Check if item has a video/image or link
            const title = item.title || "New Update";
            const pubDate = new Date(item.pubDate).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
            
            // Extract text snippet (remove HTML tags)
            let desc = item.description || "";
            desc = desc.replace(/<[^>]*>/g, "").substring(0, 140) + "...";

            const card = document.createElement("div");
            card.className = "demo-card";
            card.innerHTML = `
              <div class="demo-video-wrapper">
                <a href="${item.link}" target="_blank" class="video-fallback-btn">
                  <span class="video-play-icon">▶</span>
                  <span>Watch on LinkedIn</span>
                  <span style="font-size:0.7rem;margin-top:0.4rem;color:var(--text-dim)">Posted: ${pubDate}</span>
                </a>
              </div>
              <h3 class="demo-card-title">${title}</h3>
              <p class="demo-card-desc">${desc}</p>
              <a href="${item.link}" target="_blank" class="demo-card-link">View Post on LinkedIn ↗</a>
            `;
            container.appendChild(card);
          });
        } else {
          renderFallbackCards(container);
        }
      })
      .catch(err => {
        console.error("Error fetching RSS feed:", err);
        renderFallbackCards(container);
      });
  } else {
    // 3. Fallback to manually configured embedded posts
    renderFallbackCards(container);
  }
}

/**
 * Renders the fallback embedded post cards or placeholder links.
 */
function renderFallbackCards(container) {
  if (!container) return;
  container.innerHTML = "";

  LINKEDIN_FEED_CONFIG.embeddedPosts.forEach(post => {
    const card = document.createElement("div");
    card.className = "demo-card";
    
    let mediaHtml = "";
    if (post.embedUrl && post.embedUrl.trim() !== "") {
      mediaHtml = `<iframe src="${post.embedUrl}" allowfullscreen title="${post.title}"></iframe>`;
    } else {
      mediaHtml = `
        <a href="${post.postUrl}" target="_blank" class="video-fallback-btn">
          <span class="video-play-icon">▶</span>
          <span>Watch Live Recording</span>
          <span style="font-size:0.7rem;margin-top:0.4rem;color:var(--text-dim)">Opens in LinkedIn</span>
        </a>
      `;
    }

    card.innerHTML = `
      <div class="demo-video-wrapper">
        ${mediaHtml}
      </div>
      <h3 class="demo-card-title">${post.title}</h3>
      <p class="demo-card-desc">${post.desc}</p>
      <a href="${post.postUrl}" target="_blank" class="demo-card-link">Watch on LinkedIn ↗</a>
    `;
    container.appendChild(card);
  });
}

/**
 * Initializes video embeds for specific items on the portfolio page.
 */
function initPortfolioVideoEmbeds() {
  document.querySelectorAll(".bim-video-area").forEach(area => {
    const toolId = area.getAttribute("data-tool-id");
    if (!toolId) return;

    // Find configured post matching this tool ID
    const configPost = LINKEDIN_FEED_CONFIG.embeddedPosts.find(p => p.id === toolId);
    if (configPost && configPost.embedUrl && configPost.embedUrl.trim() !== "") {
      // Clear contents and insert iframe
      area.innerHTML = `<iframe src="${configPost.embedUrl}" allowfullscreen title="${configPost.title}" style="width:100%; height:100%; border:none; z-index:5; position:absolute; top:0; left:0;"></iframe>`;
    }
  });
}

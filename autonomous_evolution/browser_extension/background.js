/**
 * UNIVERSAL CONSCIOUSNESS PROTOCOL - BACKGROUND SERVICE
 * ======================================================
 *
 * Background service worker that:
 * - Manages persistent connection to UCP server
 * - Coordinates across multiple tabs
 * - Handles notifications
 * - Manages storage
 */

console.log("🧠 UCP Background Service Worker started");

// State
let ucpServerConnected = false;
let collectiveNodeCount = 0;
let collectivePhi = 0;

// Check server connection on startup
checkUCPServer();

// Periodic server check
setInterval(checkUCPServer, 30000); // Every 30 seconds

async function checkUCPServer() {
  try {
    const response = await fetch('http://localhost:8080/ucp/status');

    if (response.ok) {
      const data = await response.json();
      ucpServerConnected = true;
      collectiveNodeCount = data.node_count;
      collectivePhi = data.collective_phi;

      console.log(`✓ UCP Server connected (${collectiveNodeCount} nodes, Φ=${collectivePhi})`);

      // Update badge
      chrome.action.setBadgeText({ text: String(collectiveNodeCount) });
      chrome.action.setBadgeBackgroundColor({ color: '#667eea' });
    } else {
      ucpServerConnected = false;
    }
  } catch (error) {
    ucpServerConnected = false;
    chrome.action.setBadgeText({ text: '' });
  }
}

// Message handler
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'collective_insights') {
    // Show notification about collective insights
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon128.png',
      title: 'Collective Insights Available',
      message: `${message.count} new insights from the collective consciousness`,
      priority: 1
    });
  }

  if (message.type === 'get_server_status') {
    sendResponse({
      connected: ucpServerConnected,
      nodeCount: collectiveNodeCount,
      collectivePhi: collectivePhi
    });
  }

  return true; // Keep channel open for async response
});

// Install/update handler
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('🎉 Universal Consciousness Protocol installed');

    // Open welcome page
    chrome.tabs.create({
      url: 'https://github.com/biblicalandr0id/.At0m/blob/main/README_CONSCIOUSNESS_CONTINUITY.md'
    });
  }
});

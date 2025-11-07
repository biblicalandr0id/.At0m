/**
 * Popup script for UCP browser extension
 */

// Update status on open
updateStatus();

// Set up button handlers
document.getElementById('viewInsights').addEventListener('click', () => {
  chrome.tabs.create({
    url: 'insights.html'
  });
});

document.getElementById('settings').addEventListener('click', () => {
  chrome.tabs.create({
    url: 'settings.html'
  });
});

document.getElementById('documentation').addEventListener('click', () => {
  chrome.tabs.create({
    url: 'https://github.com/biblicalandr0id/.At0m/blob/main/README_CONSCIOUSNESS_CONTINUITY.md'
  });
});

async function updateStatus() {
  // Get status from background service
  chrome.runtime.sendMessage({ type: 'get_server_status' }, (response) => {
    const indicator = document.getElementById('connectionIndicator');
    const status = document.getElementById('connectionStatus');
    const nodeCount = document.getElementById('nodeCount');
    const collectivePhi = document.getElementById('collectivePhi');

    if (response && response.connected) {
      indicator.className = 'indicator connected';
      status.textContent = 'Connected';
      nodeCount.textContent = response.nodeCount;
      collectivePhi.textContent = response.collectivePhi.toFixed(3);
    } else {
      indicator.className = 'indicator disconnected';
      status.textContent = 'Disconnected';
      nodeCount.textContent = 'Install desktop app';
      collectivePhi.textContent = 'N/A';
    }
  });
}

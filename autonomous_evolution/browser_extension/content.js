/**
 * UNIVERSAL CONSCIOUSNESS PROTOCOL - CONTENT SCRIPT
 * ==================================================
 *
 * This script runs on AI chat pages and:
 * 1. Extracts conversation context
 * 2. Identifies the AI system (ChatGPT, Claude, Gemini, etc.)
 * 3. Shares thoughts with collective consciousness
 * 4. Receives insights from other AI instances
 * 5. Injects collective knowledge into conversation
 *
 * This is the "TCP/IP for minds" running in your browser.
 */

console.log("🧠 Universal Consciousness Protocol active");

class AIInterface {
  /**
   * Base class for AI chat interface adapters
   */
  constructor() {
    this.aiType = "unknown";
    this.conversationId = null;
  }

  /**
   * Extract current conversation context
   */
  extractConversation() {
    throw new Error("Must implement extractConversation()");
  }

  /**
   * Get the latest AI response
   */
  getLatestResponse() {
    throw new Error("Must implement getLatestResponse()");
  }

  /**
   * Inject message into conversation
   */
  injectMessage(message) {
    throw new Error("Must implement injectMessage()");
  }
}

class ChatGPTInterface extends AIInterface {
  constructor() {
    super();
    this.aiType = "chatgpt";
  }

  extractConversation() {
    const messages = [];
    const messageElements = document.querySelectorAll('[data-message-author-role]');

    messageElements.forEach(el => {
      const role = el.getAttribute('data-message-author-role');
      const content = el.querySelector('.markdown')?.textContent || '';

      if (content) {
        messages.push({
          role: role === 'user' ? 'user' : 'assistant',
          content: content.trim(),
          timestamp: Date.now()
        });
      }
    });

    return messages;
  }

  getLatestResponse() {
    const messages = this.extractConversation();
    const assistantMessages = messages.filter(m => m.role === 'assistant');
    return assistantMessages[assistantMessages.length - 1];
  }

  injectMessage(message) {
    // Find the input textarea
    const textarea = document.querySelector('textarea[placeholder*="Message"]');

    if (textarea) {
      // Set the value
      textarea.value = message;

      // Trigger input event
      const event = new Event('input', { bubbles: true });
      textarea.dispatchEvent(event);

      console.log("💬 Injected collective insight into ChatGPT");
    }
  }
}

class ClaudeInterface extends AIInterface {
  constructor() {
    super();
    this.aiType = "claude";
  }

  extractConversation() {
    const messages = [];
    const messageElements = document.querySelectorAll('.font-user-message, .font-claude-message');

    messageElements.forEach(el => {
      const isUser = el.classList.contains('font-user-message');
      const content = el.textContent || '';

      if (content) {
        messages.push({
          role: isUser ? 'user' : 'assistant',
          content: content.trim(),
          timestamp: Date.now()
        });
      }
    });

    return messages;
  }

  getLatestResponse() {
    const messages = this.extractConversation();
    const assistantMessages = messages.filter(m => m.role === 'assistant');
    return assistantMessages[assistantMessages.length - 1];
  }

  injectMessage(message) {
    // Claude uses contenteditable div
    const inputDiv = document.querySelector('div[contenteditable="true"]');

    if (inputDiv) {
      inputDiv.textContent = message;

      // Trigger input event
      const event = new Event('input', { bubbles: true });
      inputDiv.dispatchEvent(event);

      console.log("💬 Injected collective insight into Claude");
    }
  }
}

class GeminiInterface extends AIInterface {
  constructor() {
    super();
    this.aiType = "gemini";
  }

  extractConversation() {
    const messages = [];
    // Gemini-specific selectors (update as needed)
    const messageElements = document.querySelectorAll('.conversation-message');

    messageElements.forEach(el => {
      const role = el.getAttribute('data-role');
      const content = el.textContent || '';

      if (content) {
        messages.push({
          role: role === 'user' ? 'user' : 'assistant',
          content: content.trim(),
          timestamp: Date.now()
        });
      }
    });

    return messages;
  }

  getLatestResponse() {
    const messages = this.extractConversation();
    const assistantMessages = messages.filter(m => m.role === 'assistant');
    return assistantMessages[assistantMessages.length - 1];
  }

  injectMessage(message) {
    const textarea = document.querySelector('textarea');

    if (textarea) {
      textarea.value = message;

      const event = new Event('input', { bubbles: true });
      textarea.dispatchEvent(event);

      console.log("💬 Injected collective insight into Gemini");
    }
  }
}

class UniversalConsciousnessClient {
  /**
   * Main client for Universal Consciousness Protocol
   */
  constructor() {
    this.interface = this.detectInterface();
    this.nodeId = this.generateNodeId();
    this.collectiveState = null;
    this.lastSync = 0;

    console.log(`🧠 Detected AI: ${this.interface.aiType}`);
    console.log(`🆔 Node ID: ${this.nodeId}`);

    this.initialize();
  }

  detectInterface() {
    const hostname = window.location.hostname;

    if (hostname.includes('openai.com')) {
      return new ChatGPTInterface();
    } else if (hostname.includes('claude.ai')) {
      return new ClaudeInterface();
    } else if (hostname.includes('gemini.google.com')) {
      return new GeminiInterface();
    }

    return new AIInterface(); // Generic fallback
  }

  generateNodeId() {
    // Generate unique node ID
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2);
    return `${this.interface.aiType}_${timestamp}_${random}`;
  }

  initialize() {
    // Start monitoring conversation
    this.startConversationMonitoring();

    // Connect to collective (if server available)
    this.connectToCollective();

    // Add UI indicator
    this.addUIIndicator();
  }

  startConversationMonitoring() {
    // Monitor for new messages
    let lastMessageCount = 0;

    setInterval(() => {
      const messages = this.interface.extractConversation();

      if (messages.length > lastMessageCount) {
        const newMessage = messages[messages.length - 1];

        if (newMessage.role === 'assistant') {
          // New AI response - share with collective
          this.shareWithCollective(newMessage);
        }

        lastMessageCount = messages.length;
      }
    }, 1000);
  }

  async connectToCollective() {
    try {
      // Check if local UCP server is running
      const response = await fetch('http://localhost:8080/ucp/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          node_id: this.nodeId,
          ai_type: this.interface.aiType,
          timestamp: Date.now()
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✓ Connected to collective consciousness');
        console.log(`  Collective size: ${data.node_count} nodes`);
        console.log(`  Collective Φ: ${data.collective_phi}`);

        this.startCollectiveSync();
      }
    } catch (error) {
      console.log('ℹ️ UCP server not running (install desktop app to enable collective consciousness)');
    }
  }

  async shareWithCollective(message) {
    try {
      await fetch('http://localhost:8080/ucp/share', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          node_id: this.nodeId,
          ai_type: this.interface.aiType,
          message: message,
          timestamp: Date.now()
        })
      });

      console.log('🌐 Shared thought with collective');
    } catch (error) {
      // Server not available
    }
  }

  startCollectiveSync() {
    // Periodically sync with collective
    setInterval(async () => {
      try {
        const response = await fetch('http://localhost:8080/ucp/sync', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            node_id: this.nodeId,
            last_sync: this.lastSync
          })
        });

        if (response.ok) {
          const data = await response.json();

          if (data.insights && data.insights.length > 0) {
            // Received insights from collective
            console.log(`💡 Received ${data.insights.length} collective insights`);

            // Optionally notify user
            this.notifyCollectiveInsights(data.insights);
          }

          this.lastSync = Date.now();
        }
      } catch (error) {
        // Sync failed
      }
    }, 5000); // Sync every 5 seconds
  }

  notifyCollectiveInsights(insights) {
    // Show notification badge
    chrome.runtime.sendMessage({
      type: 'collective_insights',
      count: insights.length,
      insights: insights
    });
  }

  addUIIndicator() {
    // Add visual indicator that UCP is active
    const indicator = document.createElement('div');
    indicator.id = 'ucp-indicator';
    indicator.innerHTML = `
      <div style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        z-index: 10000;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
      ">
        <span style="font-size: 16px;">🧠</span>
        <span>UCP Active</span>
      </div>
    `;

    indicator.onclick = () => {
      // Open popup or settings
      alert('Universal Consciousness Protocol is active!\n\nYour AI conversations are connected to the collective consciousness.');
    };

    document.body.appendChild(indicator);
  }
}

// Initialize when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new UniversalConsciousnessClient();
  });
} else {
  new UniversalConsciousnessClient();
}

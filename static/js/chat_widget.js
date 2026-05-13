/**
 * Chat Widget JavaScript
 * Handles the interactive chat widget for the AI Assistant
 * RESTRICTED: Only available to logged-in users
 */

class ChatWidget {
    constructor(isLoggedIn = false) {
        this.isOpen = false;
        this.isLoading = false;
        this.messages = [];
        this.isLoggedIn = isLoggedIn;
        
        // Only initialize if user is logged in
        if (this.isLoggedIn) {
            this.init();
        }
    }

    /**
     * Initialize the chat widget
     */
    init() {
        this.createWidget();
        this.attachEventListeners();
        this.loadInitialMessage();
    }

    /**
     * Create the HTML structure for the chat widget
     */
    createWidget() {
        // Create container
        const container = document.createElement('div');
        container.className = 'chat-widget-container';
        container.id = 'chat-widget-container';

        // Create button
        const button = document.createElement('button');
        button.className = 'chat-widget-button';
        button.id = 'chat-widget-button';
        button.innerHTML = '🤖';
        button.title = 'Chat with AI Assistant';

        // Create window
        const window = document.createElement('div');
        window.className = 'chat-widget-window hidden';
        window.id = 'chat-widget-window';

        window.innerHTML = `
            <div class="chat-widget-header">
                <div class="chat-widget-header-title">
                    <span>🤖</span>
                    <span>Resume Assistant</span>
                </div>
                <button class="chat-widget-close-btn" id="chat-widget-close">✕</button>
            </div>
            <div class="chat-widget-messages" id="chat-widget-messages">
                <div style="text-align: center; color: #999; padding: 20px;">
                    Loading conversation...
                </div>
            </div>
            <div class="chat-widget-input-container">
                <input 
                    type="text" 
                    id="chat-widget-input" 
                    placeholder="Ask me anything..."
                    autocomplete="off"
                >
                <button id="chat-widget-send" title="Send message">➤</button>
            </div>
        `;

        container.appendChild(button);
        container.appendChild(window);
        document.body.appendChild(container);
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        const button = document.getElementById('chat-widget-button');
        const closeBtn = document.getElementById('chat-widget-close');
        const sendBtn = document.getElementById('chat-widget-send');
        const input = document.getElementById('chat-widget-input');

        button.addEventListener('click', () => this.toggleWindow());
        closeBtn.addEventListener('click', () => this.closeWindow());
        sendBtn.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    /**
     * Toggle window visibility
     */
    toggleWindow() {
        if (this.isOpen) {
            this.closeWindow();
        } else {
            this.openWindow();
        }
    }

    /**
     * Open the chat window
     */
    openWindow() {
        const window = document.getElementById('chat-widget-window');
        window.classList.remove('hidden');
        this.isOpen = true;
        
        // Focus input
        const input = document.getElementById('chat-widget-input');
        setTimeout(() => {
            input.focus();
        }, 100);

        // Animate button
        const button = document.getElementById('chat-widget-button');
        button.innerHTML = '✕';
    }

    /**
     * Close the chat window
     */
    closeWindow() {
        const window = document.getElementById('chat-widget-window');
        window.classList.add('hidden');
        this.isOpen = false;

        // Reset button
        const button = document.getElementById('chat-widget-button');
        button.innerHTML = '🤖';
    }

    /**
     * Load initial greeting message
     */
    loadInitialMessage() {
        this.addMessage('assistant', '🤖 Hi! I\'m your Resume AI Assistant. I can:\n\n✨ **PERFORM TASKS:**\n• Write profile summaries\n• Create cover letters\n• Optimize resume text\n• Suggest keywords\n• Write declarations\n\n📚 **ANSWER QUESTIONS:**\n• Features & how to use them\n• Resume writing tips\n• ATS scoring explained\n• And much more!\n\nWhat can I help you with?');
    }

    /**
     * Send a message
     */
    async sendMessage() {
        const input = document.getElementById('chat-widget-input');
        const message = input.value.trim();

        if (!message || this.isLoading) {
            return;
        }

        // Clear input
        input.value = '';
        input.focus();

        // Add user message
        this.addMessage('user', message);

        // Show loading indicator
        this.isLoading = true;
        this.showTypingIndicator();

        try {
            // Send to backend
            const response = await fetch('/api/assistant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });

            // Check if user is logged in (401 means not authenticated)
            if (response.status === 401) {
                this.removeTypingIndicator();
                this.addMessage('assistant', '🔐 **Login Required**\n\nThe AI Assistant is only available for logged-in users. Please log in to your account to use this feature.');
                return;
            }

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            // Add assistant response
            if (data.success) {
                this.addMessage('assistant', data.message);
            } else {
                this.addMessage('assistant', '❌ Sorry, I encountered an error. Please try again. If the problem persists, contact support.');
            }
        } catch (error) {
            console.error('Error:', error);
            this.removeTypingIndicator();
            this.addMessage('assistant', '❌ Sorry, I couldn\'t reach the server. Please check your connection and try again.');
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Add a message to the chat
     */
    addMessage(sender, text) {
        const messagesContainer = document.getElementById('chat-widget-messages');

        // Clear empty state if first message
        if (this.messages.length === 0) {
            messagesContainer.innerHTML = '';
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}`;

        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';
        bubble.innerHTML = this.parseMessageContent(text);

        messageDiv.appendChild(bubble);
        messagesContainer.appendChild(messageDiv);

        // Store message
        this.messages.push({ sender, text });

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    /**
     * Parse and format message content (handle markdown-like formatting)
     */
    parseMessageContent(text) {
        // Escape HTML
        let content = text.replace(/&/g, '&amp;')
                         .replace(/</g, '&lt;')
                         .replace(/>/g, '&gt;');

        // Handle **bold**
        content = content.replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>');

        // Handle *italic*
        content = content.replace(/\*([^\*]+)\*/g, '<em>$1</em>');

        // Handle newlines
        content = content.replace(/\n/g, '<br>');

        // Handle bullet points with different symbols
        content = content.replace(/^\s*([-•✅❌⚠️✓])\s+/gm, '<div style="margin: 4px 0;">$&');
        content = content.replace(/^(\s{2}[-•✅❌⚠️✓].*?)$/gm, '<div style="margin-left: 12px;">$1</div>');

        return content;
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-widget-messages');

        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message assistant';
        typingDiv.id = 'typing-indicator';

        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';
        bubble.innerHTML = '<div class="typing-indicator"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>';

        typingDiv.appendChild(bubble);
        messagesContainer.appendChild(typingDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    /**
     * Remove typing indicator
     */
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    /**
     * Clear chat history
     */
    clearChat() {
        const messagesContainer = document.getElementById('chat-widget-messages');
        messagesContainer.innerHTML = '';
        this.messages = [];
        this.loadInitialMessage();
    }
}

// Initialize widget when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ChatWidget();
    });
} else {
    new ChatWidget();
}

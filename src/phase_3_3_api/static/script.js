const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');
const sendBtn = document.getElementById('send-btn');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = userInput.value.trim();
    if (!query) return;

    // 1. Add user message to UI
    appendMessage('user', query);
    userInput.value = '';
    
    // Disable input while waiting
    userInput.disabled = true;
    sendBtn.disabled = true;

    // 2. Add loading state
    const loadingId = appendMessage('system', 'Searching database...');

    try {
        // 3. Make API Call to FastAPI backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const data = await response.json();
        
        // 4. Update UI with response
        updateMessage(loadingId, data.response);

    } catch (error) {
        console.error("Error fetching data:", error);
        updateMessage(loadingId, "Sorry, I encountered an error while searching the database. Please try again.");
    } finally {
        // Re-enable input
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
});

function appendMessage(sender, text) {
    const id = 'msg-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.id = id;

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'avatar';
    avatarDiv.textContent = sender === 'user' ? 'U' : 'AI';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';
    contentDiv.textContent = text;

    msgDiv.appendChild(avatarDiv);
    msgDiv.appendChild(contentDiv);
    
    chatContainer.appendChild(msgDiv);
    scrollToBottom();
    
    return id;
}

function updateMessage(id, text) {
    const msgDiv = document.getElementById(id);
    if (msgDiv) {
        const contentDiv = msgDiv.querySelector('.content');
        if (contentDiv) {
            contentDiv.textContent = text;
        }
    }
    scrollToBottom();
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

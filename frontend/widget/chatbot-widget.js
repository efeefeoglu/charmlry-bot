(function () {
  const backendUrl = window.SHOPIFY_CHATBOT_BACKEND_URL || 'http://localhost:8000';
  const storageKey = 'shopify-chatbot-history';

  const root = document.createElement('div');
  root.id = 'shopify-chatbot-root';

  const toggle = document.createElement('button');
  toggle.id = 'shopify-chatbot-toggle';
  toggle.textContent = 'Chat';

  const panel = document.createElement('div');
  panel.id = 'shopify-chatbot-panel';

  const messagesEl = document.createElement('div');
  messagesEl.id = 'shopify-chatbot-messages';

  const form = document.createElement('form');
  form.id = 'shopify-chatbot-form';

  const input = document.createElement('input');
  input.id = 'shopify-chatbot-input';
  input.placeholder = 'Ask a question...';
  input.required = true;

  const send = document.createElement('button');
  send.id = 'shopify-chatbot-send';
  send.type = 'submit';
  send.textContent = 'Send';

  form.appendChild(input);
  form.appendChild(send);
  panel.appendChild(messagesEl);
  panel.appendChild(form);
  root.appendChild(toggle);
  root.appendChild(panel);
  document.body.appendChild(root);

  function loadHistory() {
    try {
      return JSON.parse(sessionStorage.getItem(storageKey) || '[]');
    } catch (e) {
      return [];
    }
  }

  function saveHistory(messages) {
    sessionStorage.setItem(storageKey, JSON.stringify(messages));
  }

  let history = loadHistory();

  function renderMessages() {
    messagesEl.innerHTML = '';
    history.forEach((msg) => {
      const div = document.createElement('div');
      div.className = `shopify-chatbot-message ${msg.role}`;
      div.textContent = msg.content;
      messagesEl.appendChild(div);
    });
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  async function sendChat() {
    const response = await fetch(`${backendUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: history,
        page_context: {
          url: window.location.href,
          title: document.title,
        },
      }),
    });

    if (!response.ok) {
      throw new Error('Chat request failed');
    }

    return response.json();
  }

  toggle.addEventListener('click', () => {
    panel.style.display = panel.style.display === 'flex' ? 'none' : 'flex';
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    history.push({ role: 'user', content: text });
    renderMessages();
    saveHistory(history);
    input.value = '';

    try {
      const data = await sendChat();
      history.push({ role: 'assistant', content: data.reply || 'No response.' });
    } catch (err) {
      history.push({ role: 'assistant', content: 'Sorry, something went wrong.' });
    }

    renderMessages();
    saveHistory(history);
  });

  renderMessages();
})();

document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    const API_URL = 'http://localhost:8000/chat'; // URL do nosso backend FastAPI

    const addMessage = (text, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);
        
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Rola para a mensagem mais recente
        return messageDiv;
    };

    const handleSend = async () => {
        const question = userInput.value.trim();
        if (!question) return;

        addMessage(question, 'user');
        userInput.value = '';
        sendBtn.disabled = true;

        const loadingMessage = addMessage('Digitando...', 'bot');
        loadingMessage.classList.add('loading');

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ocorreu um erro na API.');
            }

            const data = await response.json();
            
            // Remove a mensagem de "Digitando..."
            loadingMessage.remove();
            // Adiciona a resposta final do bot
            addMessage(data.answer, 'bot');

        } catch (error) {
            console.error('Erro ao buscar resposta:', error);
            loadingMessage.remove();
            addMessage(`Erro: ${error.message}`, 'bot');
        } finally {
            sendBtn.disabled = false;
            userInput.focus();
        }
    };

    sendBtn.addEventListener('click', handleSend);
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSend();
        }
    });
});
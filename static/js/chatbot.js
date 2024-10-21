// Function to toggle the chat window
function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
        chatWindow.style.display = 'flex';
    } else {
        chatWindow.style.display = 'none';
    }
}

// Function to send a message
function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim().toLowerCase();
    if (userInput === '') return;

    addMessage('You', userInput);
    document.getElementById('user-input').value = '';

    // Fetch chatbot response based on user input
    fetch(chatbotDataUrl)
        .then(response => response.json())
        .then(data => {
            const botResponse = getBotResponse(userInput, data);
            addMessage('Bot', botResponse);
        })
        .catch(error => {
            console.error('Error loading chatbot data:', error);
            addMessage('Bot', 'Sorry, I am unable to process your request at the moment.');
        });
}

// Function to get the bot's response based on the user's input
function getBotResponse(userInput, data) {
    for (const category in data) {
        const questions = data[category].questions;
        for (const question of questions) {
            if (userInput.includes(question)) {
                return data[category].response;
            }
        }
    }
    return data.default.response;
}

// Function to add messages to the chat window
function addMessage(sender, message) {
    const chatContent = document.getElementById('chat-content');
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatContent.appendChild(messageElement);
    chatContent.scrollTop = chatContent.scrollHeight;
}

// Handle "Enter" key press to send message
function checkEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var helpLink = document.getElementById('open-chatbot');
    var chatPopup = document.getElementById('chatbot-popup');
    var closeButton = document.getElementById('close-chatbot');

    helpLink.addEventListener('click', function(e) {
        e.preventDefault();
        chatPopup.style.display = 'block'; // Show the chatbot popup
        if (!localStorage.getItem('chatInitialized')) {
            addInitialChatbotMessage();  // Add initial message when the popup opens
            localStorage.setItem('chatInitialized', 'true'); // Set flag in local storage
        }
    });

    closeButton.addEventListener('click', function() {
        chatPopup.style.display = 'none'; // Hide the chatbot popup
    });

    document.getElementById('send-chatbot-message').addEventListener('click', function() {
        var inputElement = document.getElementById('chatbot-input');
        var userMessage = inputElement.value.trim();
        if (userMessage) {
            addChatMessage('You', userMessage);
            inputElement.value = '';
            fetchChatbotResponse(userMessage);
        }
    });

    // Function to add an initial message from the chatbot
    function addInitialChatbotMessage() {
        addChatMessage('Chatbot', 'Hello! How can I help you today?');
    }

  
});

function addChatMessage(sender, message) {
    var messagesList = document.getElementById('chatbot-messages');
    var newMessage = document.createElement('li');
    newMessage.textContent = `${sender}: ${message}`;
    messagesList.appendChild(newMessage);
    messagesList.scrollTop = messagesList.scrollHeight;
}

function fetchChatbotResponse(message) {
    fetch('/itineraries/chatbot_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Function to get CSRF token from cookies
        },
        body: JSON.stringify({ 'message': message })
        
    })
    .then(response => {
        console.log("Raw response from server:", response);
        return response.json();
    })
    .then(data => {
        console.log("Processed data received from server:", data);
        addChatMessage('Chatbot', data.message);  // Assuming 'message' is the response field
    }).catch(error => {
        console.error('Error:', error);
        addChatMessage('Chatbot', 'Sorry, I am having trouble responding right now.');
    });
}

// Utility function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

console.log("Fetching chatbot response for message:", message);
fetchChatbotResponse(message).then(() => {
    console.log("Response received successfully.");
}).catch(error => {
    console.error("Failed to fetch chatbot response:", error);
});



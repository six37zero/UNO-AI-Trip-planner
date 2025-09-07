// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
}));

// Smooth scrolling for navigation links
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Chat functionality
let chatMessages = [
    {
        sender: 'bot',
        text: "Hello! I'm your AI travel assistant. I can help you plan trips, find destinations, calculate expenses, and much more. What would you like to know?",
        time: 'Just now'
    }
];

function addMessage(sender, text) {
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const message = {
        sender: sender,
        text: text,
        time: timestamp
    };
    
    chatMessages.push(message);
    displayMessages();
    scrollToBottom();
}

function displayMessages() {
    const chatMessagesContainer = document.getElementById('chatMessages');
    chatMessagesContainer.innerHTML = '';
    
    chatMessages.forEach(msg => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${msg.sender}-message`;
        
        const avatar = msg.sender === 'bot' ? 
            '<i class="fas fa-robot"></i>' : 
            '<i class="fas fa-user"></i>';
        
        // If bot, render Markdown to HTML; else escape as plain text
        const contentHtml = msg.sender === 'bot'
            ? (window.marked ? marked.parse(String(msg.text)) : String(msg.text))
            : String(msg.text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                ${avatar}
            </div>
            <div class="message-content">
                <div class="message-body">${contentHtml}</div>
                <span class="message-time">${msg.time}</span>
            </div>
        `;
        
        chatMessagesContainer.appendChild(messageDiv);
    });
}

function scrollToBottom() {
    const chatMessagesContainer = document.getElementById('chatMessages');
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (message) {
        addMessage('user', message);
        input.value = '';
        
        // Show typing indicator
        const typingId = `typing-${Date.now()}`;
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        chatMessages.push({ sender: 'bot', text: 'Typing...', time: timestamp, id: typingId, typing: true });
        displayMessages();
        scrollToBottom();

        // Call backend AI
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        })
        .then(async (res) => {
            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`);
            }
            return res.json();
        })
        .then((data) => {
            // Remove typing indicator
            chatMessages = chatMessages.filter(m => !m.typing);
            const aiText = (data && data.response) ? data.response : generateAIResponse(message);
            addMessage('bot', aiText);
        })
        .catch((err) => {
            console.error('Chat API error:', err);
            // Remove typing indicator and fallback
            chatMessages = chatMessages.filter(m => !m.typing);
            addMessage('bot', generateAIResponse(message));
        });
    }
}

function quickMessage(text) {
    addMessage('user', text);

    // Show typing indicator
    const typingId = `typing-${Date.now()}`;
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    chatMessages.push({ sender: 'bot', text: 'Typing...', time: timestamp, id: typingId, typing: true });
    displayMessages();
    scrollToBottom();

    // Call backend AI
    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
    .then(async (res) => {
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
    })
    .then((data) => {
        chatMessages = chatMessages.filter(m => !m.typing);
        const aiText = (data && data.response) ? data.response : generateAIResponse(text);
        addMessage('bot', aiText);
    })
    .catch((err) => {
        console.error('Chat API error:', err);
        chatMessages = chatMessages.filter(m => !m.typing);
        addMessage('bot', generateAIResponse(text));
    });
}

function generateAIResponse(userMessage) {
    const responses = {
        'paris trip': "Great choice! Paris is beautiful year-round. Here's what I recommend:\n\n• Best time: April-June or September-October\n• Must-see: Eiffel Tower, Louvre, Notre-Dame\n• Budget: $150-300/day for mid-range travel\n• Weather: Check current conditions before booking\n\nWould you like me to help you plan specific details?",
        'calculate travel expenses': "I'd be happy to help you calculate travel expenses! I can assist with:\n\n• Flight costs and booking\n• Accommodation pricing\n• Daily budget planning\n• Currency conversion\n• Expense tracking\n\nWhat type of trip are you planning?",
        'best time to visit japan': "Japan has something to offer every season:\n\n• Spring (March-May): Cherry blossoms, mild weather\n• Summer (June-August): Festivals, but hot and humid\n• Fall (September-November): Beautiful autumn colors\n• Winter (December-February): Snow, hot springs, skiing\n\nWhat interests you most about Japan?"
    };
    
    const lowerMessage = userMessage.toLowerCase();
    
    for (const [key, response] of Object.entries(responses)) {
        if (lowerMessage.includes(key)) {
            return response;
        }
    }
    
    // Default responses based on keywords
    if (lowerMessage.includes('weather') || lowerMessage.includes('climate')) {
        return "I can help you check weather conditions for any destination! Just let me know the city and dates you're interested in.";
    } else if (lowerMessage.includes('budget') || lowerMessage.includes('cost') || lowerMessage.includes('price')) {
        return "I'm great at helping with budget planning! I can calculate expenses, convert currencies, and help you create a detailed travel budget.";
    } else if (lowerMessage.includes('place') || lowerMessage.includes('attraction') || lowerMessage.includes('destination')) {
        return "I can help you discover amazing places and attractions! I have access to information about popular destinations, hidden gems, and local recommendations.";
    } else if (lowerMessage.includes('trip') || lowerMessage.includes('travel') || lowerMessage.includes('vacation')) {
        return "I'd love to help you plan your trip! I can assist with destination selection, itinerary planning, budget calculations, and much more. What specific aspect would you like to focus on?";
    }
    
    return "That's an interesting question! I'm here to help with all aspects of travel planning. Could you tell me more about what you're looking for?";
}

// Enter key to send message
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Tool modal functionality
function openTool(toolType) {
    const modal = document.getElementById('toolModal');
    const modalContent = document.getElementById('modalContent');
    
    let content = '';
    
    switch(toolType) {
        case 'weather':
            content = `
                <h2><i class="fas fa-cloud-sun"></i> Weather Tool</h2>
                <div class="tool-form">
                    <div class="form-group">
                        <label for="weatherCity">City:</label>
                        <input type="text" id="weatherCity" placeholder="Enter city name">
                    </div>
                    <div class="form-group">
                        <label for="weatherCountry">Country:</label>
                        <input type="text" id="weatherCountry" placeholder="Enter country">
                    </div>
                    <button class="btn btn-primary" onclick="checkWeather()">
                        <i class="fas fa-search"></i> Check Weather
                    </button>
                </div>
                <div id="weatherResult" class="tool-result"></div>
            `;
            break;
            
        case 'currency':
            content = `
                <h2><i class="fas fa-exchange-alt"></i> Currency Converter</h2>
                <div class="tool-form">
                    <div class="form-group">
                        <label for="fromCurrency">From:</label>
                        <select id="fromCurrency">
                            <option value="USD">USD - US Dollar</option>
                            <option value="EUR">EUR - Euro</option>
                            <option value="GBP">GBP - British Pound</option>
                            <option value="JPY">JPY - Japanese Yen</option>
                            <option value="CAD">CAD - Canadian Dollar</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="toCurrency">To:</label>
                        <select id="toCurrency">
                            <option value="EUR">EUR - Euro</option>
                            <option value="USD">USD - US Dollar</option>
                            <option value="GBP">GBP - British Pound</option>
                            <option value="JPY">JPY - Japanese Yen</option>
                            <option value="CAD">CAD - Canadian Dollar</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="amount">Amount:</label>
                        <input type="number" id="amount" placeholder="Enter amount" min="0" step="0.01">
                    </div>
                    <button class="btn btn-primary" onclick="convertCurrency()">
                        <i class="fas fa-calculator"></i> Convert
                    </button>
                </div>
                <div id="currencyResult" class="tool-result"></div>
            `;
            break;
            
        case 'calculator':
            content = `
                <h2><i class="fas fa-calculator"></i> Expense Calculator</h2>
                <div class="tool-form">
                    <div class="form-group">
                        <label for="flightCost">Flight Cost:</label>
                        <input type="number" id="flightCost" placeholder="Enter flight cost" min="0" step="0.01">
                    </div>
                    <div class="form-group">
                        <label for="accommodationCost">Accommodation Cost:</label>
                        <input type="number" id="accommodationCost" placeholder="Enter accommodation cost" min="0" step="0.01">
                    </div>
                    <div class="form-group">
                        <label for="dailyBudget">Daily Budget:</label>
                        <input type="number" id="dailyBudget" placeholder="Enter daily budget" min="0" step="0.01">
                    </div>
                    <div class="form-group">
                        <label for="tripDuration">Trip Duration (days):</label>
                        <input type="number" id="tripDuration" placeholder="Enter trip duration" min="1">
                    </div>
                    <button class="btn btn-primary" onclick="calculateExpenses()">
                        <i class="fas fa-calculator"></i> Calculate Total
                    </button>
                </div>
                <div id="calculatorResult" class="tool-result"></div>
            `;
            break;
            
        case 'places':
            content = `
                <h2><i class="fas fa-search-location"></i> Place Search</h2>
                <div class="tool-form">
                    <div class="form-group">
                        <label for="searchQuery">Search for:</label>
                        <input type="text" id="searchQuery" placeholder="Enter place, attraction, or activity">
                    </div>
                    <div class="form-group">
                        <label for="searchLocation">Location:</label>
                        <input type="text" id="searchLocation" placeholder="Enter city or region">
                    </div>
                    <button class="btn btn-primary" onclick="searchPlaces()">
                        <i class="fas fa-search"></i> Search Places
                    </button>
                </div>
                <div id="placesResult" class="tool-result"></div>
            `;
            break;
    }
    
    modalContent.innerHTML = content;
    modal.style.display = 'block';
}

// Close modal when clicking on X or outside
document.querySelector('.close').addEventListener('click', () => {
    document.getElementById('toolModal').style.display = 'none';
});

window.addEventListener('click', (event) => {
    const modal = document.getElementById('toolModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// Tool functions
function checkWeather() {
    const city = document.getElementById('weatherCity').value;
    const country = document.getElementById('weatherCountry').value;
    
    if (!city || !country) {
        document.getElementById('weatherResult').innerHTML = '<p class="error">Please enter both city and country.</p>';
        return;
    }
    
    // Simulate weather API call
    document.getElementById('weatherResult').innerHTML = '<div class="loading"></div> Checking weather...';
    
    setTimeout(() => {
        const weatherData = {
            city: city,
            country: country,
            temperature: Math.floor(Math.random() * 30) + 5,
            condition: ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy'][Math.floor(Math.random() * 4)],
            humidity: Math.floor(Math.random() * 40) + 40,
            windSpeed: Math.floor(Math.random() * 20) + 5
        };
        
        document.getElementById('weatherResult').innerHTML = `
            <div class="weather-info">
                <h3>Weather in ${weatherData.city}, ${weatherData.country}</h3>
                <div class="weather-details">
                    <p><strong>Temperature:</strong> ${weatherData.temperature}°C</p>
                    <p><strong>Condition:</strong> ${weatherData.condition}</p>
                    <p><strong>Humidity:</strong> ${weatherData.humidity}%</p>
                    <p><strong>Wind Speed:</strong> ${weatherData.windSpeed} km/h</p>
                </div>
            </div>
        `;
    }, 2000);
}

function convertCurrency() {
    const fromCurrency = document.getElementById('fromCurrency').value;
    const toCurrency = document.getElementById('toCurrency').value;
    const amount = parseFloat(document.getElementById('amount').value);
    
    if (!amount || amount <= 0) {
        document.getElementById('currencyResult').innerHTML = '<p class="error">Please enter a valid amount.</p>';
        return;
    }
    
    // Simulate currency conversion API call
    document.getElementById('currencyResult').innerHTML = '<div class="loading"></div> Converting...';
    
    setTimeout(() => {
        const exchangeRates = {
            'USD': { 'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0, 'CAD': 1.25 },
            'EUR': { 'USD': 1.18, 'GBP': 0.86, 'JPY': 129.4, 'CAD': 1.47 },
            'GBP': { 'USD': 1.37, 'EUR': 1.16, 'JPY': 150.7, 'CAD': 1.71 },
            'JPY': { 'USD': 0.009, 'EUR': 0.0077, 'GBP': 0.0066, 'CAD': 0.011 },
            'CAD': { 'USD': 0.80, 'EUR': 0.68, 'GBP': 0.58, 'JPY': 88.0 }
        };
        
        const rate = exchangeRates[fromCurrency]?.[toCurrency] || 1;
        const convertedAmount = amount * rate;
        
        document.getElementById('currencyResult').innerHTML = `
            <div class="currency-info">
                <h3>Currency Conversion</h3>
                <div class="conversion-details">
                    <p><strong>${amount} ${fromCurrency}</strong> = <strong>${convertedAmount.toFixed(2)} ${toCurrency}</strong></p>
                    <p><strong>Exchange Rate:</strong> 1 ${fromCurrency} = ${rate.toFixed(4)} ${toCurrency}</p>
                </div>
            </div>
        `;
    }, 1500);
}

function calculateExpenses() {
    const flightCost = parseFloat(document.getElementById('flightCost').value) || 0;
    const accommodationCost = parseFloat(document.getElementById('accommodationCost').value) || 0;
    const dailyBudget = parseFloat(document.getElementById('dailyBudget').value) || 0;
    const tripDuration = parseInt(document.getElementById('tripDuration').value) || 0;
    
    if (tripDuration <= 0) {
        document.getElementById('calculatorResult').innerHTML = '<p class="error">Please enter a valid trip duration.</p>';
        return;
    }
    
    const totalDailyCost = dailyBudget * tripDuration;
    const totalCost = flightCost + accommodationCost + totalDailyCost;
    const averageDailyCost = totalCost / tripDuration;
    
    document.getElementById('calculatorResult').innerHTML = `
        <div class="expense-summary">
            <h3>Travel Expense Summary</h3>
            <div class="expense-breakdown">
                <p><strong>Flight Cost:</strong> $${flightCost.toFixed(2)}</p>
                <p><strong>Accommodation Cost:</strong> $${accommodationCost.toFixed(2)}</p>
                <p><strong>Daily Expenses (${tripDuration} days):</strong> $${totalDailyCost.toFixed(2)}</p>
                <hr>
                <p class="total-cost"><strong>Total Trip Cost:</strong> $${totalCost.toFixed(2)}</p>
                <p><strong>Average Daily Cost:</strong> $${averageDailyCost.toFixed(2)}</p>
            </div>
        </div>
    `;
}

function searchPlaces() {
    const query = document.getElementById('searchQuery').value;
    const location = document.getElementById('searchLocation').value;
    
    if (!query || !location) {
        document.getElementById('placesResult').innerHTML = '<p class="error">Please enter both search query and location.</p>';
        return;
    }
    
    // Simulate places search API call
    document.getElementById('placesResult').innerHTML = '<div class="loading"></div> Searching places...';
    
    setTimeout(() => {
        const places = [
            { name: `${query} in ${location}`, rating: 4.5, type: 'Attraction', description: 'A popular destination that matches your search criteria.' },
            { name: `${query} Experience`, rating: 4.2, type: 'Activity', description: 'An exciting activity that you might enjoy.' },
            { name: `${query} Tour`, rating: 4.7, type: 'Tour', description: 'A guided tour option for your interests.' }
        ];
        
        let placesHTML = '<div class="places-results"><h3>Search Results for "' + query + '" in ' + location + '</h3>';
        
        places.forEach(place => {
            placesHTML += `
                <div class="place-item">
                    <h4>${place.name}</h4>
                    <p><strong>Type:</strong> ${place.type}</p>
                    <p><strong>Rating:</strong> ${'⭐'.repeat(Math.floor(place.rating))} (${place.rating})</p>
                    <p>${place.description}</p>
                </div>
            `;
        });
        
        placesHTML += '</div>';
        document.getElementById('placesResult').innerHTML = placesHTML;
    }, 2000);
}

// Add some CSS for tool results
const toolStyles = `
    <style>
        .tool-form {
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #374151;
        }
        
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #2563eb;
        }
        
        .tool-result {
            margin-top: 20px;
            padding: 20px;
            background: #f8fafc;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
        }
        
        .error {
            color: #ef4444;
            font-weight: 500;
        }
        
        .weather-info h3,
        .currency-info h3,
        .expense-summary h3,
        .places-results h3 {
            color: #1f2937;
            margin-bottom: 15px;
        }
        
        .weather-details p,
        .conversion-details p,
        .expense-breakdown p {
            margin-bottom: 8px;
            color: #6b7280;
        }
        
        .total-cost {
            font-size: 1.2rem;
            color: #2563eb;
            font-weight: 600;
        }
        
        .place-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border: 1px solid #e2e8f0;
        }
        
        .place-item h4 {
            color: #1f2937;
            margin-bottom: 10px;
        }
        
        .place-item p {
            margin-bottom: 5px;
            color: #6b7280;
        }
    </style>
`;

document.head.insertAdjacentHTML('beforeend', toolStyles);

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Add scroll effect to navbar
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 30px rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        }
    });
    
    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all feature cards and tool cards
    document.querySelectorAll('.feature-card, .tool-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
    
    // Display initial chat message
    displayMessages();
});

/**
 * ChatModule is a class that encapsulates all chat-related functionalities.
 */
class ChatModule {
    /**
    * Constructor initializes HTML elements, variables and arrays.
    */
    constructor() {
        this.headerTitle = document.getElementById('header-title');
        this.awaitingResponse = false;
        this.searchResult = [];
        this.chatWindow = document.getElementById('chat-window');
        this.inputMessage = document.getElementById('input-message');
        this.sendButton = document.getElementById('send-button');
        this.awaitingResponseErrorMessage = document.getElementById('awaiting-response');
        this.bubbles = document.getElementById("bubbles")
        this.searchButton = document.getElementById('search-button');
        this.searchInput = document.getElementById('chat-search-input');
        this.backSearchButton = document.getElementById('back-search-button');
        this.nextSearchButton = document.getElementById('next-search-button');
        this.searchResultFraction = document.getElementById('search-results-fraction');
        this.logoutButton = document.getElementById('logout-button')
        this.updateUserDetailsButton = document.getElementById('update-user-details-button')
        this.searchActiveIndex = 0;
        this.iconSavedMessagesButton = document.getElementById('icon-saved-messages-button')
        this.iconUserDetailsButton = document.getElementById('icon-user-details-button')
        this.iconToggleSearchButton = document.getElementById('icon-toggle-search-button')
        this.searchItemsWrapper = document.getElementById('search-items-wrapper')
        this.closeSearchButton = document.getElementById('close-search-button')


        this.searchResults = []; // Will hold IDs of matching messages.
        this.searchIndex = 0; // Current position in search results.
    }

    /**
     * This method hides all elements with the provided class name, if their display property is set to flex.
     * @param {string} className - The class name of the elements to hide.
     */
    hideFlexElements(className) {
        // Select all div elements with the given class
        var elements = document.querySelectorAll('div.' + className);

        // Loop through the elements
        for (var i = 0; i < elements.length; i++) {
            // If the display property is 'flex', change it to 'none'
            if (window.getComputedStyle(elements[i]).display === 'flex') {
                elements[i].style.display = 'none';
            }
        }
    }


    /**
     * This method creates a new message element.
     * @param {string} role - The role of the message (user/bot)
     * @param {string} content - The content of the message
     * @param {string} messageId - The id of the message
     * @returns {Element} - The message element.
     */
    createMessageElement(role, content, messageId) {
        // Create a wrapper div
        const wrapperElement = document.createElement('div');
        wrapperElement.className = `${role}-message-wrapper`;

        const messageElement = document.createElement('div');
        messageElement.className = `${role}-message-element`;
        messageElement.setAttribute('data-message-id', messageId);
        messageElement.innerHTML = `<span class="message-content">${content}</span>`;

        const optionsDiv = document.createElement('div');
        optionsDiv.className = `${role}-options-div options-div`;
        optionsDiv.style.display = 'none';
        const mealPlanButton = this.createButton('🍽️ Meal Plan', 'save-meal-plan-button', messageId);
        const workoutPlanButton = this.createButton('🏋️‍♀️ Workout Plan', 'save-workout-plan-button', messageId);
        const otherButton = this.createButton('✏️ Other', 'save-other-button', messageId);

        optionsDiv.appendChild(mealPlanButton);
        optionsDiv.appendChild(workoutPlanButton);
        optionsDiv.appendChild(otherButton);

        wrapperElement.appendChild(messageElement);
        wrapperElement.appendChild(optionsDiv);

        // Add margin to create a gap between messages
        wrapperElement.style.marginBottom = '10px';


        wrapperElement.addEventListener('click', () => {
            if (optionsDiv.style.display === 'none') {
                this.hideFlexElements('options-div')
                optionsDiv.style.display = 'flex';
            } else {
                optionsDiv.style.display = 'none';
            }

        });

        return wrapperElement;
    }


    /**
     * This is a helper function to create a button.
     * @param {string} text - The text of the button.
     * @param {string} className - The class name for the button.
     * @param {string} messageID - The message id associated with the button.
     * @returns {Element} - The button element.
     */
    createButton(text, className, messageID) {
        const messageSaveTypeDict = { 'save-meal-plan-button': 1, 'save-workout-plan-button': 2, 'save-other-button': 3 }
        let messageSaveType = messageSaveTypeDict[className]
        const button = document.createElement('button');
        button.innerText = text;
        button.className = "save-button-individual-option"; // set class

        // Add event listener
        button.addEventListener('click', function () {
            fetch('/chatbot/api/savemessage', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'messageID': messageID, 'messageSaveType': messageSaveType })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
        });

        return button;
    }

    /**
     * This method searches for a term in the messages.
     * @param {string} term - The term to search for.
     */
    searchMessages(term) {
        // Clear previous search results

        this.searchResults = [];
        this.searchIndex = 0;

        if (this.activeMessage) {
            this.activeMessage.innerHTML = this.activeMessageContent;
        }

        const messages = document.querySelectorAll(".message-content");

        messages.forEach((message, i) => {
            this.regex = new RegExp(`(${term})`, 'gi');

            // Highlight search term
            if (this.regex.test(message.textContent)) {
                // Save the parent message ID
                console.log(message.parentNode)
                const messageId = message.closest("[data-message-id]").getAttribute("data-message-id");
                this.searchResults.push(messageId);
            }
        });

        // Scroll to the first result if any were found
        if (this.searchResults.length > 0) {
            this.activeMessage = document.querySelector(`[data-message-id='${this.searchResults[0]}']`)
            this.activeMessageContent = this.activeMessage.innerHTML
            this.activeMessage.innerHTML = this.activeMessage.innerHTML.replace(this.regex, '<mark>$1</mark>');
            this.activeMessage.scrollIntoView({ block: 'center', inline: 'nearest' });

            // this.searchActiveIndex = this.searchResult.length-1
            this.nextSearchButton.style.display = 'block';
            this.backSearchButton.style.display = 'block';
            this.searchResultFraction.innerHTML = `${1}/${this.searchResults.length}`;
            this.searchResultFraction.style.display = 'block';
        } else {
            // If it is empty, hide the buttons
            this.nextSearchButton.style.display = 'none';
            this.backSearchButton.style.display = 'none';
            this.searchResultFraction.style.display = 'none';
        }

    }

    /**
     * This method scrolls to the next search result.
     */
    nextResult() {
        if (this.searchResults.length > 0) {
            this.activeMessage.innerHTML = this.activeMessageContent;
            // Move to next result or wrap to the start
            this.searchIndex = (this.searchIndex + 1) % this.searchResults.length;
            this.activeMessage = document.querySelector(`[data-message-id='${this.searchResults[this.searchIndex]}']`)
            this.activeMessageContent = this.activeMessage.innerHTML;
            this.activeMessage.innerHTML = this.activeMessage.innerHTML.replace(this.regex, '<mark>$1</mark>');
            this.activeMessage.scrollIntoView({ block: 'center', inline: 'nearest' });

            this.searchResultFraction.innerHTML = `${this.searchIndex + 1}/${this.searchResults.length}`;
        }
    }

    /**
     * This method scrolls to the previous search result.
     */
    prevResult() {
        if (this.searchResults.length > 0) {
            this.activeMessage.innerHTML = this.activeMessageContent;
            // Move to previous result or wrap to the end
            this.searchIndex = (this.searchIndex - 1 + this.searchResults.length) % this.searchResults.length;
            this.activeMessage = document.querySelector(`[data-message-id='${this.searchResults[this.searchIndex]}']`)
            this.activeMessageContent = this.activeMessage.innerHTML;
            this.activeMessage.innerHTML = this.activeMessage.innerHTML.replace(this.regex, '<mark>$1</mark>');
            this.activeMessage.scrollIntoView({ block: 'center', inline: 'nearest' });
            this.searchResultFraction.innerHTML = `${this.searchIndex + 1}/${this.searchResults.length}`;

        }
    }

    /**
     * This method clears the search.
     */
    clearSearch() {
        const highlighted = document.querySelectorAll('mark');

        // Remove highlighting
        highlighted.forEach(mark => {
            const text = document.createTextNode(mark.textContent);
            mark.parentNode.replaceChild(text, mark);
        });

        // Clear search results
        this.searchResults = [];
        this.searchIndex = 0;
    } 

    /**
     * This method creates a div that contains "bubble" elements for a loading animation.
     * @returns {HTMLElement} - The bubble div element.
     */
    bubblesDiv() {
        // Create parent div with id "bubbles"
        var bubblesDiv = document.createElement("div");
        bubblesDiv.id = "bubbles";

        // Create three child divs with class "bubble" and append them to the parent div
        for (var i = 0; i < 3; i++) {
            var bubble = document.createElement("div");
            bubble.className = "bubble";
            bubblesDiv.appendChild(bubble);
        }

        return bubblesDiv;
    }

    /**
     * This method sends a message to the chatbot and handles the response.
     * @param {string} message - The message to send.
     */
    sendMessage(message) {
        if (this.awaitingResponse) {
            this.awaitingResponseErrorMessage.style.display = 'block';
            return;
        }

        if (message) {
            // Create and append the user message
            const userMessageElement = this.createMessageElement('user', message);
            this.chatWindow.appendChild(userMessageElement);
            this.inputMessage.value = '';

            // Show loading animation
            this.awaitingResponse = true;
            const bubblesDiv = this.bubblesDiv();
            this.chatWindow.appendChild(bubblesDiv);
            window.scrollTo(0, document.body.scrollHeight);

            // Send the user message to the chatbot API
            fetch('/chatbot/api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ role: 'user', content: message })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    // Append the chatbot response
                    userMessageElement.setAttribute('data-message-id', data.userMessageID);
                    const fitBotMessageElement = this.createMessageElement('assistant', data.content.replace(/\n/g, '<br>'), data.assistantMessageID);
                    this.chatWindow.appendChild(fitBotMessageElement);
                    window.scrollTo(0, document.body.scrollHeight);

                    // this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
                })
                .catch(error => {
                    // Handle errors
                    console.error('There was a problem with the fetch operation:', error);
                    const fitBotMessageElement = this.createMessageElement('assistant', "Oops! It seems I've pulled a muscle and can't answer your question right now. Please try again later.");
                    this.chatWindow.insertBefore(fitBotMessageElement, this.bubbles);
                    this.chatWindow.appendChild(fitBotMessageElement);
                    window.scrollTo(0, document.body.scrollHeight);
                })
                .finally(() => {
                    // Hide loading animation
                    this.awaitingResponse = false;
                    bubblesDiv.remove();
                    this.awaitingResponseErrorMessage.style.display = 'none';
                });

            this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
        }
    }

    /**
     * This method initializes the chat module.
     */
    initChat() {
        // Load chat history
        for (let i = 0; i < chatHistory.length; i++) {
            const message = chatHistory[i];
            const messageElement = this.createMessageElement(message[0], message[1].replace(/\n/g, '<br>'), message[2]);
            this.chatWindow.appendChild(messageElement);
        }

        this.chatWindow.scrollTop = this.chatWindow.scrollHeight;

        // Add event listeners
        this.headerTitle.addEventListener('click', () => {
            window.location = '/';
        })

        this.sendButton.addEventListener('click', () => {
            const message = this.inputMessage.value.trim();
            this.sendMessage(message);
        });

        this.searchButton.addEventListener('click', () => {
            const searchTerm = this.searchInput.value.trim();
            this.searchMessages(searchTerm);
        });

        this.iconSavedMessagesButton.addEventListener('click', () => {
            window.location = '/saved-messages';
        });

        this.nextSearchButton.addEventListener('click', () => {
            this.nextResult();
        });

        this.backSearchButton.addEventListener('click', () => {
            this.prevResult();
        });

        this.logoutButton.addEventListener('click', () => {
            window.location = '/chatbot/api/logout';
        })


        this.inputMessage.addEventListener('keydown', event => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                const message = this.inputMessage.value.trim();
                this.sendMessage(message);
            }
        });

        this.searchInput.addEventListener('keydown', event => {
            if (event.key === 'Enter') {
                event.preventDefault(); 
                const searchTerm = this.searchInput.value.trim();
                this.searchMessages(searchTerm);
            }
        });

        this.iconUserDetailsButton.addEventListener('click', () => {
            window.location = '/personalinfo';
        })

        this.iconToggleSearchButton.addEventListener('click', () => {
            if (this.searchItemsWrapper.style.display == 'none') {
                this.searchItemsWrapper.style.display = 'flex';
            }
            else {
                this.searchItemsWrapper.style.display = 'none';
            }
        })

        this.closeSearchButton.addEventListener('click', () => {
            this.clearSearch()
            this.searchItemsWrapper.style.display = 'none';
            this.nextSearchButton.style.display = 'none';
            this.backSearchButton.style.display = 'none';
            this.searchResultFraction.style.display = 'none';
        })

    }
}

// Initialize the chat module when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    const chatModule = new ChatModule();
    chatModule.initChat();
});


// This code waits for the page to fully load before running the script
document.addEventListener('DOMContentLoaded', () => {

    // Assign the HTML element with id 'header-title' to headerTitle
    this.headerTitle = document.getElementById('header-title');

    // Add a click event listener to the header title which will navigate to the homepage
    this.headerTitle.addEventListener('click', () => {
        window.location = '/';
    })

    // Get all HTML elements with the class 'toggle-button'
    const toggleButtons = document.querySelectorAll('.toggle-button');
    // Get the HTML element with id 'saved-messages-container'
    const savedMessagesContainer = document.getElementById('saved-messages-container');
    let activeButton = null;

     // Function to create a new message element
     function createMessageElement(content, messageId, date) {
        // Create a new div element
        const messageElement = document.createElement('div');
        // Set the class of the new div element to 'message'
        messageElement.className = 'message';
        // Set a custom data attribute 'data-message-id' with the messageId
        messageElement.setAttribute('data-message-id', messageId);
        // Set the HTML of the new div element
        messageElement.innerHTML = `
          <span class="date">${date}</span>
        `;

        // Create a new paragraph for each line in the content
        const contentLines = content.split('\n');
        contentLines.forEach(line => {
            const paragraph = document.createElement('p');
            paragraph.innerText = line;
            messageElement.appendChild(paragraph);
        });

        // Create a delete button for the message
        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-button';
        deleteButton.setAttribute('data-message-id', messageId);
        deleteButton.innerText = 'Delete';
        messageElement.appendChild(deleteButton);

        return messageElement;
    }


    // Add event listeners to the toggle buttons
    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const option = button.getAttribute('data-option');

            // If there is an active button, remove the 'active' class from it
            if (activeButton) {
                activeButton.classList.remove('active');
            }

            // Highlight the clicked button by adding the 'active' class to it
            button.classList.add('active');
            activeButton = button;

            // Fetch saved messages based on the selected option and user ID
            fetch(`/saved-messages/api?option=${option}`)
                .then(response => response.json())
                .then(data => {
                    // Clear the container
                    savedMessagesContainer.innerHTML = '';

                    // If there are any saved messages, display them
                    if (data && data.messages.length > 0) {
                        data.messages.forEach(message => {
                            const messageElement = createMessageElement(message[1], message[0], message[2]);
                            savedMessagesContainer.appendChild(messageElement);
                        });
                    } else {
                        // If there are no saved messages, display a message stating that
                        const noMessagesElement = document.createElement('div');
                        noMessagesElement.className = 'no-messages';
                        noMessagesElement.innerText = 'No saved messages found.';
                        savedMessagesContainer.appendChild(noMessagesElement);
                    }
                })
                .catch(error => console.error('Error fetching saved messages:', error));
        });
    });


    // Add a click event listener to the saved messages container
    savedMessagesContainer.addEventListener('click', (event) => {
        // If the clicked element is a delete button, delete the associated message
        if (event.target.classList.contains('delete-button')) {
            const messageId = event.target.getAttribute('data-message-id');

            // Send a POST request to delete the saved message
            fetch('/saved-messages/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'message_id': messageId})
            })
                .then(response => response.json())
                .then(data => {
                    // If the message was deleted successfully, remove the message element from the DOM
                    if (data.success) {
                        const messageElement = event.target.closest('.message');
                        messageElement.remove();
                    }
                })
                .catch(error => console.error('Error deleting saved message:', error));
        }
    });
    // Additional code
    const iconUserChatButton = document.getElementById('icon-user-chat-button');
    const logoutButton = document.getElementById('logout-button');

    // Add a click event listener to the chat button which will navigate to the chat page
    iconUserChatButton.addEventListener('click', () => {
        window.location.href = "/chatbot";
    });

    // Add a click event listener to the logout button which will call the logout API
    logoutButton.addEventListener('click', () => {
        window.location = '/chatbot/api/logout';
    });

    // Set the meal plan button as active by default
    const mealPlanButton = document.querySelector('.toggle-button[data-option="1"]');
    mealPlanButton.classList.add('active');
    activeButton = mealPlanButton;

    // Fetch and display saved messages for the meal plan option
    fetch('/saved-messages/api?option=1')
        .then(response => response.json())
        .then(data => {
            // If there are any saved messages, display them
            if (data && data.messages.length > 0) {
                data.messages.forEach(message => {
                    const messageElement = createMessageElement(message[1], message[0], message[2]);
                    savedMessagesContainer.appendChild(messageElement);
                });
            } else {
                // If there are no saved messages, display a message stating that
                const noMessagesElement = document.createElement('div');
                noMessagesElement.className = 'no-messages';
                noMessagesElement.innerText = 'No saved messages found.';
                savedMessagesContainer.appendChild(noMessagesElement);
            }
        })
        .catch(error => console.error('Error fetching saved messages:', error));

});


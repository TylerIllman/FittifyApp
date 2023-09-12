/**
 * Class that encapsulates functionality related to the landing page of the website.
 */class landingPage {
    /**
     * Initializes a new instance of the landingPage class.
     */
    constructor()   {
        this.headerTitle = document.getElementById('header-title');
        this.headerLoginButton = document.getElementById('header-login-button');
        this.headerSignupButton = document.getElementById('header-signup-button');
        this.heroSignupButton = document.getElementById('hero-signup');
        this.helpYouMealButton = document.getElementById('help-you-meal-button');
        this.helpYouExampleMeal = document.getElementById('help-you-example-meal');
        this.helpYouRecoveryButton = document.getElementById('help-you-recovery-button');
        this.helpYouExampleRecovery = document.getElementById('help-you-example-recovery');
        this.helpYouWorkoutButton = document.getElementById('help-you-workout-button');
        this.helpYouExampleWorkout = document.getElementById('help-you-example-workout');
        this.helpYouNutritionButton = document.getElementById('help-you-nutrition-button');
        this.helpYouExampleNutrition = document.getElementById('help-you-example-nutrition');
        this.helpYouStartChattingButton = document.getElementById('help-you-start-chatting-button');
        this.fittifyVsTrainerSignupButton = document.getElementById('fittivy-vs-trainer-signup-button');
    }
        
    /**
     * Clears any existing active example message by removing associated classes.
     */
    clearHelpYouMessages()  {
        // Remove active classes from "help you" buttons and messages.
        this.helpYouMealButton.classList.remove("active-example-button")
        this.helpYouExampleMeal.classList.remove("active-example-message-pair")
        this.helpYouRecoveryButton.classList.remove("active-example-button")
        this.helpYouExampleRecovery.classList.remove("active-example-message-pair")
        this.helpYouWorkoutButton.classList.remove("active-example-button")
        this.helpYouExampleWorkout.classList.remove("active-example-message-pair")
        this.helpYouNutritionButton.classList.remove("active-example-button")
        this.helpYouExampleNutrition.classList.remove("active-example-message-pair")
    }

    /**
     * Changes the active message in the UI.
     */
    changeActiveMessage(messages, buttons, activeIndex, direction) {
        // Loop over the array
        for (let index = 0; index < messages.length; index++) {
            const messageDiv = messages[index];

            // If the message div is the active one
            if (messageDiv.classList.contains('active-example-message-pair')) {
                messageDiv.classList.remove('active-example-message-pair');

                // Determine new index based on direction and whether we are at the end or start of array
                const newIndex = direction === 1 
                    ? (index === messages.length - 1 ? 0 : index + 1) 
                    : (index === 0 ? messages.length - 1 : index - 1);

                // Add active class to the new active element
                messages[newIndex].classList.add('active-example-message-pair');

                // Update button classes
                buttons[activeIndex].classList.remove('active-example-button');
                buttons[newIndex].classList.add('active-example-button');

                // Break out of the loop
                break;
            }
        }
    }

    /**
     * Initializes the landing page with various interactivity.
     */
    initLandingPage()   {
        // Register click events for various elements.
        this.headerTitle.addEventListener('click', () => {
            window.location = '/';
        })
        this.headerLoginButton.addEventListener('click', () => {
            window.location = '/login';
        })
        this.headerSignupButton.addEventListener('click', () => {
            window.location = '/signup';
        })
        this.heroSignupButton.addEventListener('click', () => {
            window.location = '/signup';
        })
        this.helpYouMealButton.addEventListener('click', () => {
            this.clearHelpYouMessages();
            this.helpYouMealButton.classList.add("active-example-button");
            this.helpYouExampleMeal.classList.add("active-example-message-pair");
        })
        this.helpYouRecoveryButton.addEventListener('click', () => {
            this.clearHelpYouMessages();
            this.helpYouRecoveryButton.classList.add("active-example-button");
            this.helpYouExampleRecovery.classList.add("active-example-message-pair");
        })
        this.helpYouWorkoutButton.addEventListener('click', () => {
            this.clearHelpYouMessages();
            this.helpYouWorkoutButton.classList.add("active-example-button");
            this.helpYouExampleWorkout.classList.add("active-example-message-pair");
        })
        this.helpYouNutritionButton.addEventListener('click', () => {
            this.clearHelpYouMessages();
            this.helpYouNutritionButton.classList.add("active-example-button");
            this.helpYouExampleNutrition.classList.add("active-example-message-pair");
        })
        this.helpYouStartChattingButton.addEventListener('click', () => {
            window.location = '/signup';
        })
        this.fittifyVsTrainerSignupButton.addEventListener('click', () => {
            window.location = '/signup';
        })

        // UI related code for enabling left-right swiping of example messages
        let activeButtonIndex = 0;
        const buttons = Array.from(document.querySelectorAll('#help-you-example-buttons-wrapper button'));
        const messages = Array.from(document.querySelectorAll('#help-you-messages-wrapper div'))
        const activeExampleMessage = document.querySelector('#help-you-messages-wrapper .active-example-message-pair');
        const exampleMessages = document.querySelectorAll('#help-you-messages-wrapper > div');
        const exampleMessagesArray = Array.from(exampleMessages);
        // const exampleMessagesIds = exampleMessagesArray.map((messageDiv) => {messageDiv.id})
        // let activeMessageIndex = exampleMessagesArray.indexOf(activeExampleMessage.id)


        /**
         * Click event for the left emoji button.
         */
        document.querySelector('#left-emoji').addEventListener('click', () => {

            // Reverse loop over the array
            for (let index = exampleMessagesArray.length - 1; index >= 0; index--) {
                const messageDiv = exampleMessagesArray[index];
        
                // If the message div is the active one
                if (messageDiv.classList.contains('active-example-message-pair')) {
                    messageDiv.classList.remove('active-example-message-pair');
        
                    // If we're at the start of the array
                    if (index === 0) {
                        exampleMessagesArray[exampleMessagesArray.length - 1].classList.add('active-example-message-pair');
                    } else {
                        exampleMessagesArray[index - 1].classList.add('active-example-message-pair'); 
                    }
        
                    // We've found the active element and moved the active class to the previous one, so we break out of the loop
                    break;
                }
            }
        
            buttons[activeButtonIndex].classList.remove('active-example-button');
            activeButtonIndex = (activeButtonIndex - 1 + buttons.length) % buttons.length;
            buttons[activeButtonIndex].classList.add('active-example-button');
        });



        /**
         * Click event for the right emoji button.
         */
        document.querySelector('#right-emoji').addEventListener('click', () => {
            // Loop over the array
            for (let index = 0; index < exampleMessagesArray.length; index++) {
                const messageDiv = exampleMessagesArray[index];
                
                // If the message div is the active one
                if (messageDiv.classList.contains('active-example-message-pair')) {
                    messageDiv.classList.remove('active-example-message-pair');
                
                    // If we're at the end of the array
                    if (index === exampleMessagesArray.length - 1) {
                        exampleMessagesArray[0].classList.add('active-example-message-pair');
                    } else {
                        exampleMessagesArray[index + 1].classList.add('active-example-message-pair');
                    }
                
                    // We've found the active element and moved the active class to the next one, so we break out of the loop
                    break;
                }
            }
        
            buttons[activeButtonIndex].classList.remove('active-example-button');
            activeButtonIndex = (activeButtonIndex + 1) % buttons.length;
            buttons[activeButtonIndex].classList.add('active-example-button');
        });
        


    }
}



// When document is fully loaded, initialise the landing page
document.addEventListener('DOMContentLoaded', () => {
    const landPageObject = new landingPage();
    landPageObject.initLandingPage();
});
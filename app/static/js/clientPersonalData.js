/**
 * Class that encapsulates functionality related to a client's personal data.
 */
class clientPersonalData {
    /**
     * Initialises a new instance of the clientPersonalData class.
     */
    constructor() {
        // Get references to various elements in the DOM.
        this.headerTitle = document.getElementById('header-title');
        this.iconUserChatButton = document.getElementById('icon-user-chat-button');
        this.logoutButton = document.getElementById('logout-button');
        this.personalDetailsForm = document.getElementById('personal-details-form');
        this.personalDetailsFormTitle = document.getElementById('personal-details-form-title');
        this.fitnessGoalsInput = document.getElementById('fitness-goals');
        this.dietInput = document.getElementById('diet');
        this.workoutDaysInput = document.getElementById('workoutdays');
        this.workoutMinsInput = document.getElementById('workoutmins');
        this.weightInput = document.getElementById('weight');
        this.heightInput = document.getElementById('height');
        this.accessGymSelect = document.getElementById('accessgym');
        this.genderSelect = document.getElementById('gender');
    }

    /**
     * Initialises the user details from the given data.
     */
    initUserDetails() {
        if (data) {
            // Map the user details to the appropriate form fields.
            let userDetails = data
            this.fitnessGoalsInput.value = userDetails[5];
            this.dietInput.value = userDetails[6];
            this.workoutDaysInput.value = userDetails[7];
            this.workoutMinsInput.value = userDetails[8];
            this.weightInput.value = userDetails[3];
            this.heightInput.value = userDetails[4];
            this.accessGymSelect.value = userDetails[9];
            this.genderSelect.value = userDetails[2];
        }

        // Attach event listeners to the buttons.
        this.iconUserChatButton.addEventListener('click', () => {
            window.location.href = "/chatbot";
        });

        this.logoutButton.addEventListener('click', () => {
            window.location = '/chatbot/api/logout';
        });

        this.headerTitle.addEventListener('click', () => {
            window.location = "/";
        });
    }
}

// Instantiate the clientPersonalData class and initialize user details when the document is ready.
document.addEventListener('DOMContentLoaded', () => {
    const clientData = new clientPersonalData();
    clientData.initUserDetails();
});

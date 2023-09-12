// Define a class representing the sign up page
class signUpPage {
    // Constructor initializes the object with elements of the header
    constructor () {
        // Get the title of the header from the DOM
        this.headerTitle = document.getElementById('header-title');
        // Get the login button from the header
        this.headerLoginButton = document.getElementById('header-login-button');
        // Get the signup button from the header
        this.headerSignupButton = document.getElementById('header-signup-button');
    }

    // Initialize the sign up page with event listeners
    initSignUpPage() {
        // When the title of the header is clicked, redirect to home
        this.headerTitle.addEventListener('click', () => {
            window.location = '/';
        })

        // When the login button is clicked, redirect to login page
        this.headerLoginButton.addEventListener('click', () => {
            window.location = '/login';
        })

        // When the sign up button is clicked, redirect to sign up page
        this.headerSignupButton.addEventListener('click', () => {
            window.location = '/signup';
        })

    }

}

// When the document is fully loaded, instantiate the signUpPage object and call the initializer
document.addEventListener('DOMContentLoaded', () => {
    const signUp = new signUpPage();
    signUp.initSignUpPage();
});

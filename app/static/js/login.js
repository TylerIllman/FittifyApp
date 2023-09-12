class loginPage {
    constructor () {
        this.headerTitle = document.getElementById('header-title');
        this.headerLoginButton = document.getElementById('header-login-button');
        this.headerSignupButton = document.getElementById('header-signup-button');
    }

    initSignUpPage() {
        this.headerTitle.addEventListener('click', () => {
            window.location = '/';
        })

        this.headerLoginButton.addEventListener('click', () => {
            window.location = '/login';
        })

        this.headerSignupButton.addEventListener('click', () => {
            window.location = '/signup';
        })

    }

}

document.addEventListener('DOMContentLoaded', () => {
    const login = new loginPage();
    login.initSignUpPage();
});
document.addEventListener('DOMContentLoaded', () => {
    const googleSignup = document.getElementById('googleSignup');
    const facebookSignup = document.getElementById('facebookSignup');
    
    // Add event listeners to prevent default link action
    googleSignup.addEventListener('click', (event) => {
        event.preventDefault();
        alert("Google sign-up is not yet implemented. Please use the email option or other methods.");
    });

    facebookSignup.addEventListener('click', (event) => {
        event.preventDefault();
        alert("Facebook sign-up is not yet implemented. Please use the email option or other methods.");
    });
});

function openModal() {
    document.getElementById('signupModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('signupModal').style.display = 'none';
}

function showEmailSignup() {
    document.getElementById('signupOptions').classList.add('hidden');
    document.getElementById('emailSignup').classList.remove('hidden');
    document.getElementById('modalTitle').innerText = 'Sign Up with Email';
}

function showSignUpOptions() {
    document.getElementById('emailSignup').classList.add('hidden');
    document.getElementById('signupOptions').classList.remove('hidden');
    document.getElementById('modalTitle').innerText = 'Join JournoLab';
}

function handleSignup(event) {
    event.preventDefault(); // Prevent the default form submission

    // Capture the form input values
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Basic validation
    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    // Perform further actions like sending the data to your server here
    // For demonstration, let's just log the data to the console
    console.log({
        firstName,
        lastName,
        username,
        email,
        password,
    });

    // You can also clear the form if needed
    document.getElementById('signupForm').reset();
    showSignUpOptions(); // Optionally return to the sign-up options
}


function showSignIn() {
    document.getElementById('signupOptions').classList.add('hidden');
    document.getElementById('emailSignup').classList.add('hidden');
    document.getElementById('signIn').classList.remove('hidden');
}

function showSignUp() {
    document.getElementById('signupOptions').classList.remove('hidden');
    document.getElementById('emailSignup').classList.add('hidden');
    document.getElementById('signIn').classList.add('hidden');
}

function openSignInModal() {
    document.getElementById('signInModal').style.display = 'flex';
}

function closeSignInModal() {
    document.getElementById('signInModal').style.display = 'none';

}

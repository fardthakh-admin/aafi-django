const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        const token = data.token;
        // const userId = data.user_id;
        
        
        // Save token and userId to localStorage or cookies for later use
        localStorage.setItem('authToken', token);

        // Redirect to the home page
        window.location.href = '/patient/patientHomepage/';
        
    } catch (error) {
        console.error('Error:', error);
    }
});

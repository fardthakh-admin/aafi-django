const loginForm = document.getElementById('login-form');
const logoutBtn = document.getElementById('logout-btn');
let token;


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
        token = data.token;
        const userId = data.user_id;

        // Save token and userId to localStorage or cookies for later use

        // Hide login form, show logout button
        loginForm.style.display = 'none';
        logoutBtn.style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
    }
});

logoutBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/logout/', {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`,
            },
        });
    } catch (error) {
        console.error('Error:', error);
    }
});
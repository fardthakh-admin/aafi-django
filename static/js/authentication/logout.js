const logoutButton = document.getElementById('logout-button');

logoutButton.addEventListener('click', async () => {
    try {
        const token = localStorage.getItem('authToken');
        console.log('Token ' + token)
        const response = await fetch('/api/logout/', {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`,
            },
        });

        localStorage.removeItem('authToken');
        // Redirect to the login page
        window.location.href = '/';

        
    } catch (error) {
        console.error('Error:', error);
    }
});
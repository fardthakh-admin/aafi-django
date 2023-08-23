const login_form = document.getElementById('login-form');
login_form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data)
        localStorage.setItem('authToken', data.jwt);
        window.location.href = '/doctor-homepage/';
        console.log('Logged in successfully!');
    } else {
        console.error('Login failed');
    }
});




// const loginForm = document.getElementById('login-form');

// loginForm.addEventListener('submit', async (e) => {
//     e.preventDefault();

//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;

//     try {
//         const response = await fetch('/api/login/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ username, password }),
//         });
        
//         const data = await response.json();
//         const token = data.token;
//         // const userId = data.user_id;
        
        
//         // Save token and userId to localStorage or cookies for later use
//         localStorage.setItem('authToken', token);

//         // Redirect to the home page
//         window.location.href = '/patient-homepage/';
        
//     } catch (error) {
//         console.error('Error:', error);
//     }
// });

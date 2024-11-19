async function handleLogin() {
    const email = document.querySelector('.email').value
    const password = document.querySelector('.password').value

    const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({'email': email, 'password': password}),
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    })
        .catch(error => console.error('During request: ', error));

    const error_block = document.querySelector('.error-block')

    if (response.ok) {
        const data = await response.json();
        // Optionally process returned data (e.g., user info)
        console.log('Login Successful:', data);
        error_block.textContent = ''
        window.location.href = '/weeks.html';
    } else {
        const error = await response.json();
        console.error('Login Failed:', error);
        error_block.textContent = 'Invalid email or password. Please try again.'
    }
}


// Attach handler to login form
document.querySelector('.auth-form').addEventListener('submit', handleLogin);

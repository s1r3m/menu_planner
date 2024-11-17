async function handleRegistration() {
    const email = document.querySelector('.email').value;
    const username = document.querySelector('.username').value;
    const password = document.querySelector('.password').value;
    const response = await fetch('/api/register', {
        method: 'POST',
        body: JSON.stringify({'email': email, 'username': username, 'password': password}),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    })
        .catch(error => console.error('During request: ', error));

    const error_block = document.querySelector('.error-block')

    if (response.ok) {
        const data = await response.json();
        // Optionally process returned data (e.g., user info)
        console.log('Registration Successful:', data);
        error_block.textContent = ''
        window.location.href = '/weeks.html';
    } else {
        const error = await response.json();
        console.error('Registration Failed:', error);
        error_block.textContent = error.error
    }
}
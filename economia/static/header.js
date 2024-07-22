window.onload = function () {
document.querySelector('.logout').addEventListener('click', function() {
    fetch('/onboarding/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
        },
        body: JSON.stringify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/onboarding';
        } else {
            console.error('Logout failed');
        }
    });
});
}
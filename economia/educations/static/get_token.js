document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('access_token');

    if (token) {
        // 서버에 JWT 토큰 보내기
        fetch('/get_player/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ token: token })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } else {
        console.log('No token found in LocalStorage');
    }
});

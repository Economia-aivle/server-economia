const token = localStorage.getItem('access_token');
fetch('/api/check-token/', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
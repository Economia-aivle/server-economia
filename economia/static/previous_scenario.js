document.addEventListener('DOMContentLoaded', function() {
    const deleteForms = document.querySelectorAll('.deleteForm');

    deleteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const confirmation = confirm('정말 댓글을 삭제하시겠습니까?');

            if (confirmation) {
                form.submit(); // 확인을 클릭하면 폼을 서브밋하여 삭제 요청을 보냄
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const commentId = this.getAttribute('data-comment-id');
            let action = this.getAttribute('data-action');
            
            fetch(`/scenarios/like/comment/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const likeCountElement = document.getElementById(`like-count-${commentId}`);
                    likeCountElement.textContent = data.like_cnt;
                    
                    // 좋아요/좋아요 취소 상태에 따라 버튼의 data-action 값 변경
                    action = data.action; // 서버에서 받은 action 값으로 업데이트
                    
                    // 이미지도 변경할 경우
                    const likeButton = document.getElementById(`like-btn-${commentId}`);
                    if (data.action === 'liked') {
                        likeButton.innerHTML = '<img src="{% static "images/like.png" %}" alt="좋아요" height="40px" width="40px">';
                    } else if (data.action === 'unliked') {
                        likeButton.innerHTML = '<img src="{% static "images/unlike.png" %}" alt="좋아요 취소" height="40px" width="40px">';
                    }
                } else {
                    console.error('Failed to like/unlike comment:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
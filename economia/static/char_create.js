document.addEventListener('DOMContentLoaded', function() {
    let selectedCharId = null;
    let selectedCharUrl = null;
    let characterId = null;
    let playerId = 5; // 실제 로그인한 사용자의 ID로 설정되어야 함

    // 페이지 로드 시 캐릭터 ID 가져오기
    fetch(`/users/get_character/${playerId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            characterId = data.id;
            console.log("Loaded Character ID:", characterId); // 디버깅 로그 추가
        } else {
            console.log("No character found for player.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // 캐릭터 선택 기능
    document.querySelectorAll('.char1, .char2, .char3, .char4, .char5').forEach(char => {
        char.addEventListener('click', function() {
            document.querySelectorAll('.char1, .char2, .char3, .char4, .char5').forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            selectedCharId = parseInt(this.className.replace('char', '').trim());
            selectedCharUrl = getComputedStyle(this).backgroundImage.slice(4, -1).replace(/"/g, "");
            console.log("Selected Character:", {id: selectedCharId, url: selectedCharUrl}); // 디버깅 로그 추가
        });
    });

    // 캐릭터 생성 기능
    document.getElementById('createBtn').addEventListener('click', function() {
        if (!selectedCharId || !selectedCharUrl) {
            alert('먼저 캐릭터를 선택해주세요.');
            return;
        }
        fetch('/users/char_create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                player_id: playerId,
                kind: selectedCharId,
                exp: 400,
                last_quiz: 5,
                kind_url: selectedCharUrl,
                score: 'Score 1'
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
            if (data.id) {
                characterId = data.id;
                console.log("Character ID:", characterId);
                alert('캐릭터가 성공적으로 생성되었습니다!');
            } else {
                alert('캐릭터 생성에 실패했습니다: ' + JSON.stringify(data));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('캐릭터 생성 중 오류가 발생했습니다: ' + error);
        });
    });

    // 캐릭터 변경 기능
    document.getElementById('updateBtn').addEventListener('click', function() {
        if (!characterId || !selectedCharUrl) {
            alert('먼저 캐릭터를 생성하고 변경할 이미지를 선택해주세요.');
            return;
        }
        console.log("Updating Character with ID:", characterId, "and URL:", selectedCharUrl); // 디버깅 로그 추가
        fetch('/users/char_update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                character_id: characterId,
                new_image_url: selectedCharUrl
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
            if (data.message) {
                alert('캐릭터 이미지가 성공적으로 변경되었습니다!');
            } else {
                alert('캐릭터 이미지 변경에 실패했습니다: ' + JSON.stringify(data));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('캐릭터 이미지 변경 중 오류가 발생했습니다: ' + error);
        });
    });

    // CSRF 토큰을 가져오는 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
document.addEventListener('DOMContentLoaded', function() {
    // 유튜브 비디오 ID 추출 함수
    function getYouTubeVideoId(url) {
        const urlObj = new URL(url);
        return urlObj.searchParams.get('v');
    }

    // 페이지 로드 시 유튜브 비디오 정보 가져오기
    fetch('/educations/study_video/?video=true')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.video_url) {
                const videoId = getYouTubeVideoId(data.video_url);
                const videoEmbedUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1`;

                const videoContainer = document.querySelector('#video-container');
                videoContainer.innerHTML = `
                    <iframe width="560" height="315" src="${videoEmbedUrl}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                `;
            } else {
                alert('동영상을 불러오는 데 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('동영상을 불러오는 중 오류가 발생했습니다: ' + error);
        });
});

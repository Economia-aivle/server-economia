
document.addEventListener("DOMContentLoaded", function() {
    loadQuestion();
});

let questionCount = 0;
const maxQuestions = 5;
const usedQuestionIds = [];
let correctCount = 0; // 클라이언트 측에서 맞춘 문제 개수

function loadQuestion() {
    if (questionCount >= maxQuestions) {
        document.getElementById('question-container').innerHTML = '<h1>퀴즈가 완료되었습니다!</h1>';
        return;
    }
    const subjects_id = initialData.subjects_id;
    const chapter = initialData.chapter;
    const characters = initialData.characters;

    fetch(`/educations/tf_quiz/?subjects_id=${subjects_id}&chapter=${chapter}&used_question_ids=${usedQuestionIds.join(',')}`)
        .then(response => response.json())
        .then(data => {
            if (!data.question_id) {
                alert('더 이상 사용할 수 있는 질문이 없습니다.');
                return;
            }

            if (usedQuestionIds.includes(data.question_id)) {
                loadQuestion();
                return;
            }

            document.getElementById('question-text').innerText = data.question_text;
            document.getElementById('question-id').value = data.question_id;
            usedQuestionIds.push(data.question_id);
        })
        .catch(error => console.error('Error:', error));
}


function updateHPBar() {
    const hpBar = document.getElementById('hp-bar');
    const widthDecrease = correctCount * 20;  // correctCount가 1 증가할 때마다 20%씩 감소
    
    hpBar.style.width = `calc(100% - ${widthDecrease}%)`;  // 너비 감소
}

function submitAnswer(answer) {
    const questionId = document.getElementById('question-id').value;
    if (!questionId) {
        alert('질문 ID가 없습니다.');
        return;
    }

    fetch('/educations/tf_quiz/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({
            question_id: questionId,
            submitted_answer: answer
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_correct) {
            alert('정답입니다!');
            correctCount++;
            updateHPBar()
        } else {
            alert('오답입니다. 설명: ' + data.explanation);
        }
        questionCount++;
        updateProgressBar();
        console.log(correctCount)
        if (correctCount === 5) {
            document.querySelector('.wrap-container').style.display = 'none';
            document.querySelector('.wrong-container').style.display = 'block';
            document.getElementById('question-text').style.display = 'none';
            // 모든 문제를 맞췄을 때 Stage 모델 업데이트 요청
            fetch('/educations/update_stage/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: new URLSearchParams({
                    characters: initialData.characters,
                    subjects_id: initialData.subjects_id,
                    chapter: initialData.chapter
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('모든 문제를 맞췄습니다!');
                } else {
                    alert('Stage 업데이트 중 오류가 발생했습니다.');
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            loadQuestion();
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateProgressBar() {
    document.querySelector('.progress-num').innerText = `${questionCount}/${maxQuestions}`;
    const progressSteps = document.querySelectorAll('.progress-step');
    for (let i = 0; i < progressSteps.length; i++) {
        if (i < questionCount) {
            progressSteps[i].classList.add('active');
        } else {
            progressSteps[i].classList.remove('active');
        }
    }
}

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



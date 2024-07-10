document.addEventListener("DOMContentLoaded", function() {
    loadQuestion();
});

let questionCount = 0;
const maxQuestions = 5;
const usedQuestionIds = [];

function loadQuestion() {
    if (questionCount >= maxQuestions) {
        document.getElementById('question-container').innerHTML = '<h1>퀴즈가 완료되었습니다!</h1>';
        return;
    }
    const subjects = initialData.subjects;
    const chapter = initialData.chapter;
    const characters = initialData.characters;

    fetch(`/educations/tf_quiz/?subjects=${subjects}&chapter=${chapter}&used_question_ids=${usedQuestionIds.join(',')}`)
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
        } else {
            alert('오답입니다. 설명: ' + data.explanation);
        }
        questionCount++;
        updateProgressBar();
        loadQuestion();
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
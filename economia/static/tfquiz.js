document.addEventListener("DOMContentLoaded", function() {
  loadQuestion();
});

let questionCount = 0;
const maxQuestions = 5;

function loadQuestion() {
  if (questionCount >= maxQuestions) {
    // 퀴즈를 종료하고 결과를 보여줍니다.
    document.getElementById('question-container').innerHTML = '<h1>퀴즈가 완료되었습니다!</h1>';
    return;
  }

  fetch('/educations/tf_quiz/')
    .then(response => response.json())
    .then(data => {
      document.getElementById('question-text').innerText = data.question_text;
      document.getElementById('question-id').value = data.question_id;
    })
    .catch(error => console.error('Error:', error));
}

function submitAnswer(answer) {
  const questionId = document.getElementById('question-id').value;
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
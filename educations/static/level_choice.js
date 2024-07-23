{% load static %}
document.addEventListener('DOMContentLoaded', (event) => {
    const buttons = document.querySelectorAll('.next-btn');

    buttons.forEach(button => {
        const img = button.querySelector('img');

        if (button.classList.contains('active')) {
            button.disabled = false;
            img.src = "{% static 'images/unlock.png' %}";
        } else {
            button.disabled = true;
            img.src = "{% static 'images/lock.png' %}";
        }
       
    });
});

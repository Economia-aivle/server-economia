       document.addEventListener('DOMContentLoaded', function() {
            const accessToken = localStorage.getItem('access_token');
            console.log(accessToken)
            var createScenarioButton = document.querySelector('.create-scenario-button');
            if (accessToken) {
                fetch("/scenarios/scenario_list", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    body: JSON.stringify({ access_token: accessToken })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    if(data.staff){
                        createScenarioButton.style.display = 'inline-block';
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            }
        });


        
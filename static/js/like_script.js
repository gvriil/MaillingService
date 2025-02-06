document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-button');
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modelType = this.dataset.modelType;
            const modelId = this.dataset.modelId;

            fetch(`/blog/like/${modelType}/${modelId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    this.innerHTML = `<i class="fas fa-heart" style="color: red;"></i> ${data.likes_count}`;
                } else {
                    this.innerHTML = `<i class="far fa-heart"></i> ${data.likes_count}`;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
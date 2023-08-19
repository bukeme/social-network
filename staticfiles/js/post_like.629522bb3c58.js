const likeBtns = document.querySelectorAll('.like-btn');

likeBtns.forEach(function (likeBtn) {
	likeBtn.addEventListener('click', function () {
		fetch(
			`{% url 'post_like' ${this.dataset.post_id} %}`,
			{
				headers: {
					'Content-Type': 'application/json',
			        "X-Requested-With": "XMLHttpRequest",
			        "HTTP_X_REQUESTED_WITH": "XMLHttpRequest",
					'X-CSRFToken': '{{csrf_token}}',
				},
				body: JSON.stringify({csrfmiddlewaretoken: '{{csrf_token}}'})
			}
		)
		.then(response => response.json())
		.then(data => {
			if (data.status === 'not logged in') {
				console.log('You are not logged in');
			} else if (data.status === 'ok') {
				if (data.action === 'like') {
					likeBtn.classList.add('bg-primary text-white');
				} else if (data.action === 'unlike') {
					likeBtn.classList.remove('bg-primary text-white');
				}
				likeBtn.querySelector('.likes-count').innerHTML = data.num_of_likes;
			} else {
				console.log('An error occured');
			}
		});
	});
});
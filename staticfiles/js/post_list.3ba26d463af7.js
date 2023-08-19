const imgModalTrigger = document.querySelectorAll('.img-modal-trigger');

imgModalTrigger.forEach(function(trigger) {
	trigger.addEventListener('click', function() {
		const imgID = trigger.dataset.imgid;
		const img = document.querySelector(imgID);
		const siblings = img.parentElement.querySelectorAll('.carousel-item');
		siblings.forEach(function(item) {
			item.classList.remove('active');
		});
		img.classList.add('active');
	});
});
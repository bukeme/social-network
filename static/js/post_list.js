const imgModals = document.querySelectorAll('.img-modal');


imgModals.forEach(function(imgModal) {
	imgModal.addEventListener('click', function() {
		const imgClass = this.dataset.class;
		const imgIndex = Array.from(document.querySelectorAll(`.${imgClass}`)).indexOf(this);
		console.log(imgIndex);
		let carouselItem = '';
		let i, j;
		for (i = 1; i < 4; i++) {
			if (i == imgIndex + 1) {
				carouselItem += `
				<div class="carousel-item active h-100">
					<img src="../images/0${i}.jpg" class="d-block w-100">
				</div>
				`;
			} else {
				carouselItem += `
				<div class="carousel-item h-100">
					<img src="../images/0${i}.jpg" class="d-block w-100">
				</div>
				`;
			}
		};
		let carouselId = this.dataset.carousel; 
		document.querySelector(`#${carouselId} .carousel-inner`).innerHTML = carouselItem;
	})
});
const profileImg = document.querySelector('.profile-img');
const profileElement = document.querySelector('.profile-element');
const barNav = document.querySelector('.bar-nav');
const mobileNav = document.querySelector('.mobile-nav');

profileImg.addEventListener('click', function() {
	profileElement.classList.toggle('d-none')
});

barNav.addEventListener('click', function() {
	mobileNav.classList.toggle('d-none');
})

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})
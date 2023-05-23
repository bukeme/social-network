const chatHamburgerMenu = document.querySelector('.chat-hamburger-menu');
const chatLeftMobile = document.querySelector('.chat-left-mobile');
const chatOverlayMobile = document.querySelector('.chat-overlay-mobile');
const closeChatLeft = document.querySelector('.close-chat-left');
let toggleEventOn = false;


chatHamburgerMenu.addEventListener('click', function() {
	hideShowItems();
});

closeChatLeft.addEventListener('click', function() {
	hideShowItems();
});

chatOverlayMobile.addEventListener('click', function() {
	hideShowItems();
});

function hideShowItems() {
	if (!toggleEventOn) {
		chatLeftMobile.classList.toggle('active');
		chatOverlayMobile.classList.toggle('active');
		document.body.classList.toggle('stop-scroll');
		toggleEventOn = true;
	}
	setTimeout(function() {
		toggleEventOn = false;
	}, 350);
};

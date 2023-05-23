const postCreateImgInput = document.querySelector('.post-create-img-input');
const postCreateVideoInput = document.querySelector('.post-create-video-input');
const uploadedImgContainer = document.querySelector('.uploaded-img-container');
const uploadedVideoContainer = document.querySelector('.uploaded-video-container');
let imagesArray = [];
let videoFile;

if (postCreateImgInput) {
	postCreateImgInput.addEventListener('change', function(){
		const file = this.files;
		imagesArray = [];
		for (let key in file) {
			imagesArray.push(file[key]);
		};
		imagesArray.splice(imagesArray.length - 2, 2);
		displayUploadedImgs();
	});
}

function displayUploadedImgs() {
	let images = '';
	imagesArray.forEach(function(image, index) {
		images += `<div class="m-1 rounded" style="height: 80px; width: 80px;">
					<img src="${URL.createObjectURL(image)}" alt="image" class="rounded">
				</div>`;
		if (index + 1 == imagesArray.length) {
			images += `<a href="javascript:void()" onclick="clearImgs()" class="btn btn-sm btn-danger f-xl ml-2 px-2"><i class="fa fa-trash"></i></a>`;
		};
	});
	uploadedImgContainer.innerHTML = images;
};

function clearImgs() {
	postCreateImgInput.value = null;
	imagesArray = [];
	displayUploadedImgs();
};

if (postCreateVideoInput) {
	postCreateVideoInput.addEventListener('change', function() {
		videoFile = this.files[0];
		displayUploadedVideo();
	});
}

function displayUploadedVideo() {
	let video = '';
	if (videoFile) {
		video = `<div style="width: 200px;">
					<div class="section d-flex justify-content-center embed-responsive embed-responsive-16by9">
						<video class="embed-responsive-item" controls>
							<source src="${URL.createObjectURL(videoFile)}" type="video/mp4">
						</video>
					</div>
				</div>
				<a href="javascript:void()" class="btn btn-danger f-xl ml-2 px-2" onclick="clearVideo()">
					<i class="fa fa-trash"></i>
				</a>`;
	};
	uploadedVideoContainer.innerHTML = video;
}

function clearVideo() {
	postCreateVideoInput.value = null;
	videoFile = null;
	displayUploadedVideo();
}
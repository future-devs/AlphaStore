function initialize() {
	startSlider('slider-elements');
}

async function addToCart(productID) {
	showLoader();
	const form = new FormData();
	form.append('productID', productID);

	let response = await makeAsyncPostMultiPartRequest('add-to-cart', form);
	let contentType = response.headers['content-type'];
	response = response.data;
	hideLoader();

	if (response['Added'] == 0) document.getElementById('login').click();
	else alert(response['Message']);
}

var api_url = 'http://127.0.0.1:8000/';
// var api_url = 'https://alpha-store-asd.herokuapp.com/';
function makeAsyncGetRequest(path) {
	return new Promise(function (resolve, reject) {
		axios.get(api_url + path).then(
			(response) => {
				var returnObj = response.data;
				console.log('Async Get Request: ' + path);
				resolve(returnObj);
			},
			(error) => {
				reject(error);
			}
		);
	});
}

function makeAsyncPostRequest(path, queryObject) {
	return new Promise(function (resolve, reject) {
		axios.post(api_url + path, queryObject).then(
			(response) => {
				var returnObj = response.data;
				console.log('Async Post Request');
				resolve(returnObj);
			},
			(error) => {
				reject(error);
			}
		);
	});
}

function makeGetRequest(path) {
	axios.get(api_url + path).then(
		(response) => {
			var returnObj = response.data;
			return returnObj;
		},
		(error) => {
			return error;
		}
	);
}

function makePostRequest(path, queryObject) {
	axios.post(api_url + path, queryObject).then(
		(response) => {
			var returnObj = response.data;
			return returnObj;
		},
		(error) => {
			return error;
		}
	);
}

function makeAsyncPostMultiPartRequest(path, queryObject) {
	return new Promise(function (resolve, reject) {
		axios
			.post(api_url + path, queryObject, {
				headers: { 'Content-Type': 'multipart/form-data' },
			})
			.then(
				(response) => {
					var returnObj = response;
					console.log('Async Post Request');
					resolve(returnObj);
				},
				(error) => {
					reject(error);
				}
			);
	});
}

function test() {
	window.alert('Chal Raha hai...');
}

function alert(message) {
	document.getElementById('modal-title').innerHTML = 'Message';
	document.getElementById('modal-body').innerHTML = message;
	document.getElementById('modal-footer').innerHTML = '';

	document.querySelector('#show-modal').click();
}

function validURL(str) {
	var pattern = new RegExp(
		'^(https?:\\/\\/)?' + // protocol
			'((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
			'((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
			'(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
			'(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
			'(\\#[-a-z\\d_]*)?$',
		'i'
	); // fragment locator
	return !!pattern.test(str);
}

function closeModal() {
	document.querySelector('.close').click();
}

function searchQuery() {
	let searchInput = document.getElementById('searchInput').value;
	// console.log(searchInput);
	if (searchInput != '' && searchInput != null) {
		window.location = 'tag?query=' + searchInput;
	}
}

function startSlider(element) {
	$(document).ready(function () {
		$('.' + element).lightSlider({
			autoWidth: true,
			loop: true,
			onSliderLoad: function () {
				$('.' + element).removeClass('cS-hidden');
			},
		});
	});
}

function showModal() {
	document.getElementById('show-modal').click();
}

function hideModal() {
	document.getElementById('main-modal').style.display = 'none';
}

function openLoginModal() {
	document.getElementById('modal-header').innerHTML = document.getElementById(
		'login-modal-header'
	).innerHTML;

	document.getElementById('modal-body').innerHTML = document.getElementById(
		'login-section-body'
	).innerHTML;

	document.getElementById('modal-footer').innerHTML = document.getElementById(
		'login-section-footer'
	).innerHTML;
}

function showLoginSection() {
	document.getElementById('modal-body').innerHTML = document.getElementById(
		'login-section-body'
	).innerHTML;

	document.getElementById('modal-footer').innerHTML = document.getElementById(
		'login-section-footer'
	).innerHTML;
}

function showSignupSection() {
	document.getElementById('modal-body').innerHTML = document.getElementById(
		'signup-section-body'
	).innerHTML;

	document.getElementById('modal-footer').innerHTML = document.getElementById(
		'signup-section-footer'
	).innerHTML;
}

async function performLogin() {
	document.getElementById('login-error').innerHTML = '';

	let useremail = document.getElementById('useremail').value;
	let password = document.getElementById('password').value;

	const form = new FormData();
	form.append('useremail', useremail);
	form.append('password', password);

	let response = await makeAsyncPostMultiPartRequest('login-request', form);
	let contentType = response.headers['content-type'];
	response = response.data;

	if (contentType && contentType.indexOf('application/json') !== -1) {
		document.getElementById('login-error').innerHTML = response['message'];
	} else {
		document.getElementById('header-section').innerHTML = response;
		// console.log(response);
		closeModal();
	}
}

async function performSignup() {
	document.getElementById('signup-error').innerHTML = '';

	let username = document.getElementById('username').value;
	let useremail = document.getElementById('useremail').value;
	let password = document.getElementById('password').value;
	let password2 = document.getElementById('retype-password').value;

	if (password != password2) {
		document.getElementById('signup-error').innerHTML =
			'Passwords Do Not Match';
		return;
	} else {
		const form = new FormData();
		form.append('useremail', useremail);
		form.append('username', username);
		form.append('password', password);

		let response = await makeAsyncPostMultiPartRequest('signup-request', form);
		response = response.data;

		document.getElementById('signup-error').innerHTML = response['message'];
	}
}

async function showCart() {
	showLoader();
	const form = new FormData();

	let response = await makeAsyncPostMultiPartRequest('show-cart', form);
	let contentType = response.headers['content-type'];
	response = response.data;

	if (contentType && contentType.indexOf('application/json') !== -1) {
		document.getElementById('login').click();
	} else {
		document.getElementById('modal-title').innerHTML = 'Cart Summary';
		document.getElementById('modal-body').innerHTML = response;
		document.getElementById('modal-footer').innerHTML = '';
		document.getElementById('show-modal').click();
	}
	hideLoader();
}

async function cartChange(productID, change) {
	showLoader();
	const form = new FormData();
	form.append('change', change);
	form.append('productID', productID);

	let response = await makeAsyncPostMultiPartRequest('change-cart-value', form);

	let contentType = response.headers['content-type'];
	response = response.data;

	if (contentType && contentType.indexOf('application/json') !== -1) {
		document.getElementById('login').click();
	} else {
		document.getElementById('modal-body').innerHTML = response;
		console.log(response);
	}
	hideLoader();
}

async function placeOrder() {
	showLoader();
	document.getElementById('shipping-error').innerHTML = '';

	let name = document.getElementById('shipping-name').value;
	let address = document.getElementById('shipping-address').value;
	let landmark = document.getElementById('shipping-landmark').value;
	let pincode = document.getElementById('shipping-pincode').value;
	let phoneNumber = document.getElementById('shipping-phone-number').value;

	if (
		name == '' ||
		address == '' ||
		landmark == '' ||
		pincode == '' ||
		phoneNumber == ''
	) {
		document.getElementById('shipping-error').innerHTML =
			'Please Enter All Details.';
	} else {
		const form = new FormData();
		form.append('name', name);
		form.append('address', address);
		form.append('landmark', landmark);
		form.append('pincode', pincode);
		form.append('phoneNumber', phoneNumber);

		let response = await makeAsyncPostMultiPartRequest(
			'get-order-summary',
			form
		);

		let contentType = response.headers['content-type'];
		response = response.data;

		if (contentType && contentType.indexOf('application/json') !== -1) {
			document.getElementById('login').click();
		} else {
			document.getElementById('modal-title').innerHTML = 'Order Summary';
			document.getElementById('modal-body').innerHTML = response;
			console.log(response);
		}
	}

	hideLoader();
}

async function logout() {
	showLoader();
	response = await makeAsyncGetRequest('logout-request');
	hideLoader();
	window.location = 'home';
}

async function showProfile() {
	window.location = 'account';
}

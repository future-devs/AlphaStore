function initialize() {}

async function saveAccountChanges() {
	showLoader();
	document.getElementById('account-change-error').innerHTML = '';

	let newUsername = document.getElementById('new-username').value;
	if (newUsername == '') {
		document.getElementById('account-change-error').innerHTML =
			'Name cannot be empty.';
	} else {
		const form = new FormData();
		form.append('newUsername', newUsername);
		let response = await makeAsyncPostMultiPartRequest(
			'save-account-changes',
			form
		);
		response = response.data;
		document.getElementById('account-section').innerHTML = response;
		document.getElementById('account-change-error').innerHTML =
			'Changes Submitted.';
	}
	hideLoader();
}

async function changePassword() {
	showLoader();
	document.getElementById('password-change-error').innerHTML = '';

	let newPassword = document.getElementById('new-password').value;
	let retypeNewPassword = document.getElementById('retype-new-password').value;
	if (newPassword != retypeNewPassword) {
		document.getElementById('password-change-error').innerHTML =
			'New password does not match with the retyped once.';
	} else {
		const form = new FormData();
		form.append('newPassword', newPassword);
		let response = await makeAsyncPostMultiPartRequest('change-password', form);
		response = response.data;
		document.getElementById('account-section').innerHTML = response;
		document.getElementById('password-change-error').innerHTML =
			'Password Change Successful.';
	}
	hideLoader();
}

async function cancelOrder(orderID) {
	showLoader();
	const form = new FormData();
	form.append('orderID', orderID);
	let response = await makeAsyncPostMultiPartRequest('cancel-order', form);
	response = response.data;
	document.getElementById('account-section').innerHTML = response;
	hideLoader();
}

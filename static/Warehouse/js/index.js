function initialize() {
	displayProductSection();
}

function test() {
	window.alert('Chal Raha hai...');
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

function switchActive(doc1, doc2) {
	var attribute = doc1.getAttribute('class');
	attribute = attribute.split(' ');
	new_attribute = '';
	for (x in attribute)
		if (attribute[x] != 'active') new_attribute += attribute[x] + ' ';
	doc1.setAttribute('class', new_attribute);

	var attribute = doc2.getAttribute('class');
	attribute = attribute.split(' ');
	new_attribute = '';
	for (x in attribute)
		if (attribute[x] != 'active') new_attribute += attribute[x] + ' ';
	new_attribute += ' active';
	doc2.setAttribute('class', new_attribute);
}

function displayProductSection() {
	switchActive(
		document.getElementById('details-section-switch'),
		document.getElementById('product-section-switch')
	);
	document.getElementById('product-section').style.display = 'block';
	document.getElementById('details-section').style.display = 'none';
	fetchProducts();
}

function displayDetailsSection() {
	switchActive(
		document.getElementById('product-section-switch'),
		document.getElementById('details-section-switch')
	);

	document.getElementById('product-section').style.display = 'none';
	document.getElementById('details-section').style.display = 'block';

	document.getElementById('save-success').style.display = 'none';
	getDetails();
}

function openAddProductDialog() {
	var title = document.getElementById('open-add-product-dialog-title')
		.innerHTML;
	var body = document.getElementById('open-add-product-dialog-body').innerHTML;
	var footer = document.getElementById('open-add-product-dialog-footer')
		.innerHTML;

	document.getElementById('modal-title').innerHTML = title;
	document.getElementById('modal-body').innerHTML = body;
	document.getElementById('modal-footer').innerHTML = footer;
}

function addNewImageInput(value = 'Paste the GDrive Image URL here...') {
	var div = document.getElementById('imageURLs');
	var text = document.getElementById('imageURL-template').innerHTML;
	text = text.replace('{value}', value);
	div.innerHTML += text;
}

function updateInput(doc, value) {
	doc.setAttribute('value', value);
}

function removeThisInput(doc) {
	doc.remove();
}

async function addProduct() {
	if (document.getElementById('add-pid').value == '-1') {
		var pid = await makeAsyncGetRequest('get-new-pid/');
		pid = pid.result;
		document.getElementById('add-pid').value = pid;
	}

	pid = document.getElementById('add-pid').value;
	queryObj = productQueryObject();

	query = await makeAsyncPostRequest('add-product/', queryObj);
	response = query.result;
	// console.log(response);

	document.getElementById('modal-body').innerHTML =
		'<span class="highlight2">Product ' +
		pid +
		' Added Successfully...!</span>';
	document.getElementById('modal-footer').innerHTML = '';

	await fetchProducts();
}

function productQueryObject() {
	var pid = document.getElementById('add-pid').value;
	var name = document.getElementById('add-name').value;
	var category = document.getElementById('add-category').value;
	var specifications = document.getElementById('add-specifications').value;
	var images = document.getElementsByClassName('imageURL');
	imageURLs = [];
	for (var i = 0; i < images.length; i++)
		if (validURL(images[i].value)) imageURLs.push(images[i].value);
	var tags = document.getElementById('add-tags').value;
	tags = tags.split(',');
	for (var i = 0; i < tags.length; i++) tags[i] = tags[i].toUpperCase().trim();
	var price = document.getElementById('add-price').value;
	var quantity = document.getElementById('add-quantity').value;
	if (document.getElementById('available').checked)
		var availability = 'Available';
	if (document.getElementById('not-available').checked)
		var availability = 'Not Available';

	queryObj = {
		PID: pid,
		Name: name,
		Category: category,
		Specifications: specifications,
		Tags: tags,
		Images: imageURLs,
		Price: price,
		Quantity: quantity,
		Availability: availability,
	};
	// console.log(queryObj);
	// return;
	return queryObj;
}

async function fetchProducts() {
	response = await makeAsyncGetRequest('get-all-products/');
	data = response.result;
	productSection = document.getElementById('product-display');
	var text = '';

	for (x in data.reverse()) {
		var divtext = document.getElementById('product-display-template').innerHTML;
		divtext = divtext.replace('{ProductID}', data[x]['ProductID'].trim());
		divtext = divtext.replace('{Name}', data[x]['Name'].trim());
		divtext = divtext.replace('{Category}', data[x]['Category'].trim());
		imageURLs = '';
		for (i in data[x]['ImageURLs']) {
			imageURLs +=
				'<a href="' +
				data[x]['ImageURLs'][i] +
				'">' +
				data[x]['ImageURLs'][i] +
				'</a><br>';
		}
		divtext = divtext.replace('{ImageURLs}', imageURLs.trim());
		divtext = divtext.replace(
			'\n						{Specifications}\n					',
			data[x]['Specifications'].trim()
		);
		divtext = divtext.replace('{Tags}', data[x]['Tags'].join(', ').trim());
		divtext = divtext.replace('{Availability}', data[x]['Availability'].trim());
		divtext = divtext.replace('{Price}', data[x]['Price']);
		divtext = divtext.replace('{Quantity}', data[x]['Quantity']);
		divtext = divtext.replace('{ProductID}', data[x]['ProductID'].trim());
		divtext = divtext.replace('{ProductID}', data[x]['ProductID'].trim());
		text += divtext;
	}
	// console.log(text);
	productSection.innerHTML = text;
}

function editProduct(doc, Pid) {
	openAddProductDialog();
	document.getElementById('addProductBtn').click();

	parentDiv = doc.parentNode.parentNode;
	// console.log(parentDiv.children[0].innerHTML, Pid);
	document.getElementById('add-pid').value = parentDiv.children[0].innerHTML;
	document.getElementById('add-name').value = parentDiv.children[1].innerHTML;

	if (parentDiv.children[2].innerHTML == 'Clothing')
		document.getElementById('add-category').selectedIndex = '0';
	else if (parentDiv.children[2].innerHTML == 'Products')
		document.getElementById('add-category').selectedIndex = '1';
	else if (parentDiv.children[2].innerHTML == 'Accessories')
		document.getElementById('add-category').selectedIndex = '2';
	else if (parentDiv.children[2].innerHTML == 'Other')
		document.getElementById('add-category').selectedIndex = '3';

	document.getElementById('add-specifications').value =
		parentDiv.children[4].innerHTML;

	var imageURLs = parentDiv.children[3].getElementsByTagName('a');
	for (var i = 0; i < imageURLs.length; i++) {
		// console.log(imageURLs[i].innerText);
		addNewImageInput(imageURLs[i].innerHTML);
	}
	document.getElementById('add-tags').value = parentDiv.children[5].innerHTML;
	if (parentDiv.children[6].innerHTML == 'Available')
		document.getElementById('available').checked = true;
	if (parentDiv.children[6].innerHTML == 'Not Available')
		document.getElementById('not-available').checked = true;
	document.getElementById('add-price').value = parentDiv.children[7].innerHTML;
	document.getElementById('add-quantity').value =
		parentDiv.children[8].innerHTML;
}

async function deleteProduct(doc, Pid) {
	parentDiv = doc.parentNode.parentNode;
	queryObj = { PID: Pid };
	query = await makeAsyncPostRequest('delete-product/', queryObj);
	response = query.result;
	// console.log(response);
	parentDiv.remove(1);
}

async function getDetails() {
	response = await makeAsyncGetRequest('get-details/');
	response = response.result;
	// console.log(response);
	document.getElementById('owner-name').value = response['Name'];
	document.getElementById('owner-address').value = response['Address'];
	document.getElementById('owner-email').value = response['Email'];
	document.getElementById('owner-number').value = response['PhoneNumber'];
}

async function saveDetails() {
	queryObj = {
		Name: document.getElementById('owner-name').value,
		Address: document.getElementById('owner-address').value,
		Email: document.getElementById('owner-email').value,
		PhoneNumber: document.getElementById('owner-number').value,
	};
	response = await makeAsyncPostRequest('save-details/', queryObj);
	// console.log(response.result);
	document.getElementById('save-success').style.display = 'block';
}

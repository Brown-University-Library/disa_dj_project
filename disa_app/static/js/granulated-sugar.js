function create(elementType) {
	let newElement = document.createElement(elementType);
	for (let i = 1; i < arguments.length; i++) {
		let currentArgument = arguments[i];		
		if (typeof(currentArgument) === 'string') {
			newElement.innerHTML += currentArgument;
		} else if (Array.isArray(currentArgument)) {
			for (let j = 0; j < arguments[i].length; j++) {
				if (typeof(arguments[i][j]) === 'string') {
					newElement.innerHTML += currentArgument[j];		
				} else {	
					newElement.appendChild(currentArgument[j]);
				}
			}
		} else if (currentArgument instanceof Element) {
			newElement.appendChild(currentArgument);
		} else {
			Object.getOwnPropertyNames(currentArgument).forEach(
				function (val, idx, array) {
					newElement.setAttribute(val, currentArgument[val]);
				}
			);
		}
	}
	return newElement;
}
function logResponse(responseCode) {
	console.log(responseCode);
}

function getRequest(fileName, onSuccess, onFailure = logResponse, modifyRequest = () => {}) {
	let request = new XMLHttpRequest();
	request.onreadystatechange = function () {
		if (request.readyState == XMLHttpRequest.DONE) {
			if (request.status == 200) {
				onSuccess(request.responseText);
			} else {
				onFailure(request.status);
			}
		}
	};
	request.open("GET", fileName, true);
	request.send();
}

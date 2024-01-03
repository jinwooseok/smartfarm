const $login = document.querySelector("#login");
const $logout = document.querySelector("#logout");

const replaceHref = (event, value='') => {
	event.preventDefault();
	console.log(value);
	if (value !== '') {
		// location.replace(value);
		location.href=value;
		return;
	}

	if (event.target.tagName === 'A') {
		const href = event.target.href;
		location.replace(href);
		return;
	}
}

if ($login) {
	$login.addEventListener("click" , replaceHref);
}
if ($logout) {
	$logout.addEventListener("click" , replaceHref);
}
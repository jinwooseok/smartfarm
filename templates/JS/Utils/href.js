export const replaceHref = (event, value='') => {
	event.preventDefault();
	
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
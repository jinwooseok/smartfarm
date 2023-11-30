function parse_cookies() {
	const cookies = {};
	if (document.cookie && document.cookie !== '') {
			document.cookie.split(';').forEach(function (cookie) {
					let data = cookie.trim().match(/(\w+)=(.*)/);
					if(data !== undefined) {
							cookies[data[1]] = decodeURIComponent(data[2]);
					}
			});
	}
	return cookies;
}

const cookies = parse_cookies();

export default cookies;
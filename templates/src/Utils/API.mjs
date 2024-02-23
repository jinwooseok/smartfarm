import cookies from "/templates/src/Utils/CsrfToken.mjs";

const API = async (url, type, data={}) => {
	console.log("url", url)
	console.log("API_DATA", data);
	try {
		const response = await $.ajax({
			url: url,
			type: type,
			dataType: "json",
			headers: { "X-CSRFToken": cookies['csrftoken'] },
			data: data,
			async: false,
		});
		console.log("response", response);
		return response;

	} catch (error) {
		alert(`ERROR ${error.responseJSON.message}`)
		return error.responseJSON ? error.responseJSON : error.status;
	}
}

export default API;
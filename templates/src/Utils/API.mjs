import cookies from "/templates/src/Utils/CsrfToken.mjs";

const API = async (url, type, data={}) => {
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
		console.log("re",response.status);
		return response.status;

	} catch (error) {
		console.log("error", error.status);
		return error.status;
	}
}

export default API;
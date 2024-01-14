import cookies from "/templates/src/Utils/CsrfToken.mjs";

const API = async (url, type, data) => {
	try {
		const response = await $.ajax({
			url: url,
			type: type,
			dataType: "json",
			headers: { "X-CSRFToken": cookies['csrftoken'] },
			data: data,
			async: false,
		});

		return response;

	} catch (error) {
		return error.status;
	}
}

export default API;
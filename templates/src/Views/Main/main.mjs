import API from "/templates/src/Utils/API.mjs";

const getLoginInfo = async() => {
	const response = await API("get", "/");
	console.log(response);
}

// getLoginInfo()
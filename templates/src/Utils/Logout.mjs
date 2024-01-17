import API from "/templates/src/Utils/API.mjs";

const Logout = async () => {
	const response = await API("/users/sign-out/", "post");

	if (response.status === "success") {
		location.replace("/")
	}
}

export default Logout;
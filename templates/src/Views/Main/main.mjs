import API from "/templates/src/Utils/API.mjs";

const $login = document.querySelector("#login");
const $register = document.querySelector("#register");
const $fileList = document.querySelector("#fileList");

// $login.addEventListener("click", async (event) => {
// 	event.preventDefault();

// 	const response = await API("users/sign-in/", "get");

// 	console.log("response.status", response.status);
// })

// $register.addEventListener("click", async (event) => {
// 	event.preventDefault();

// 	const response = await API("users/sign-up/", "get");

// 	console.log(response);
// })

// $fileList.addEventListener("click", async (event) => {
// 	event.preventDefault();

// 	const response = await API("file-list/", "get");

// 	console.log(response);
// })

import { replaceHref } from "./Utils/href.js";

const $login = document.querySelector("#login");
const $logout = document.querySelector("#logout");

const resetLocalStorage = () =>{
	localStorage.clear();
}

resetLocalStorage();
if ($login) {
	$login.addEventListener("click" , replaceHref);
}
if ($logout) {
	$logout.addEventListener("click" , replaceHref);
}
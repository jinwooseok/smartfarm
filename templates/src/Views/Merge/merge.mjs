import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import setFileListSelectBox from "/templates/src/Utils/FIleList.mjs";

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

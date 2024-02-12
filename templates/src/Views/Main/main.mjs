import API from "/templates/src/Utils/API.mjs";

const $login = document.querySelector("#login");
const $fileList = document.querySelector("#fileList");

const goLogin = async () => {
  const response = await API("/users/sign-in/", "get");
  console.log(response);

  if (response === 200) {
    location.replace("/users/sign-in/");
  }
};

$login.addEventListener("click", goLogin);


const goFileList = async () => {
  // const response = await API("/file-list/", "get");
  // console.log(response);

  // if (response === 200) {
    location.replace("/file-list/");
  // }
};

$fileList.addEventListener("click", goFileList);
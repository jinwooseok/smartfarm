"use strick";
import API from "../../Utils/API.mjs";

const $loginId = document.querySelector("#id");
const $loginPassword = document.querySelector("#password");
const $loginBtn = document.querySelector("#loginButton");

const idPattern = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-za-z0-9\-]+/;

function isValid() {
  // ID를 적고 @가 포함 + 비밀번호는 8자리 이상
  if (idPattern.test($loginId.value) && $loginPassword.value.length >= 8) {
    $loginBtn.style.backgroundColor = "#007A33";
    $loginBtn.disabled = false;
  } else {
    $loginBtn.style.backgroundColor = "#8E8E8E";
    $loginBtn.disabled = true;
  }
}

// 로그인 ajax
const submitLoginInfo = async () =>{
  const data = {
    email: $loginId.value,
    password: $loginPassword.value,
  };

  return API("/users/sign-in/", "post", data);

}

const checkResponse = () => {
  const response = submitLoginInfo();

  if (response.status === "success") {
    location.replace("/file-list/");
  }

  if (response.status === 1001) {
    alert(response.message); //"계정이 존재하지 않습니다.”
  } else if(response.status === 1002) {
    alert(response.message); //"비밀번호가 일치하지 않습니다.”
  }

}

$loginBtn.addEventListener('click', checkResponse());
$loginId.addEventListener("keyup", isValid);
$loginPassword.addEventListener("keyup", isValid);

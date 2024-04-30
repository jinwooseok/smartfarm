"use strick";
import API from "/templates/src/Utils/API.mjs";

const $email = document.querySelector("#email");
const $password = document.querySelector("#password");
const $loginBtn = document.querySelector("#loginButton");
const $showPassword = document.querySelector("#showPassword");
const $showPasswordText = document.querySelector("#showPasswordText");
const $EmailError = document.querySelector("#EmailError");
const $passwordError = document.querySelector("#passwordError");

// test@test.com 형식
const idPattern = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-za-z0-9\-]+/;

// 입력 값 형식 검사
const isValid = () => {
  if (idPattern.test($email.value) && $password.value.length >= 8) {
    $loginBtn.style.backgroundColor = "#007A33";
    $loginBtn.disabled = false;
  } else {
    $loginBtn.style.backgroundColor = "#8E8E8E";
    $loginBtn.disabled = true;
  }
}

// 로그인 검사
const submitLoginInfo = async () =>{
  const data = {
    email: $email.value,
    password: $password.value,
  };
  return await API("/users/sign-in/", "post", data);
}

// 버튼 클릭 결과
const clickResponse = async () => {
  const response = await submitLoginInfo();

  $EmailError.innerHTML = '';
  $passwordError.innerHTML = '';

  if (response.status === "success") {
    location.replace("/file-list/");
  }

  if (response.status === 452) {
    console.log("message", response.message)
    $EmailError.textContent = response.message; //"계정이 존재하지 않습니다."
  } else if(response.status === 453) {
    console.log("message", response.message)
    $passwordError.textContent = response.message; //"비밀번호가 일치하지 않습니다."
  }
}

// 비밀번호 보여주기
const changePassWordStatus = () => {
  if ($showPassword.checked) {
    $password.type = "text";
    $showPasswordText.textContent = "비밀번호 숨기기";
    return;
  }

  $password.type = "password";
  $showPasswordText.textContent = "비밀번호 보기";
  return;
}

$loginBtn.addEventListener('click', clickResponse);
$email.addEventListener("keyup", isValid);
$password.addEventListener("keyup", isValid);
$showPassword.addEventListener("click", changePassWordStatus);
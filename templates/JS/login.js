"use strick";
import { replaceHref } from "./Utils/href.js";

const $loginId = document.querySelector("#id");
const $loginPassword = document.querySelector("#password");
const $loginBtn = document.querySelector("#loginButton");

// const idPattern = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-za-z0-9\-]+/;
const idPattern = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]/;

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

$loginBtn.addEventListener('click', (event) => {
  // replaceHref(event, "/");
  location.replace("/")
});
$loginId.addEventListener("keyup", isValid);
$loginPassword.addEventListener("keyup", isValid);

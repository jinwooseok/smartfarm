"use strick";

const $loginId = document.querySelector('#id');
const $loginPassword = document.querySelector('#password');
const $loginBtn = document.querySelector('#login_btn');

function valid(){
    // ID를 적고 @가 포함 + 비밀번호는 5자리 이상
    if (($loginId.value.length >0 && $loginId.value.indexOf("@") !== -1) && $loginPassword.value.length >= 5){
        $loginBtn.style.backgroundColor = "#007A33";
        $loginBtn.disabled = false;
    } else{
        $loginBtn.style.backgroundColor = "#8E8E8E";
        $loginBtn.disabled = true;
    }
}

// function move_main(){
//     location.href="../";
// }

// $loginBtn.addEventListener('click', move_main);
$loginId.addEventListener('keyup', valid);
$loginPassword.addEventListener('keyup', valid);
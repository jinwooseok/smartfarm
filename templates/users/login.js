"use strick";

const $loginId = document.querySelector('#id'); // 아이디 입력 input
const $loginPassword = document.querySelector('#password'); // 비밀번호 입력 input
const $loginBtn = document.querySelector('#login_btn'); // 로그인 버튼

function isvalid(){
    // ID를 적고 @가 포함 + 비밀번호는 8자리 이상
    if (($loginId.value.length >0 && $loginId.value.indexOf("@") !== -1) && $loginPassword.value.length >= 8){
        $loginBtn.style.backgroundColor = "#007A33";
        $loginBtn.disabled = false;
    } else{
        $loginBtn.style.backgroundColor = "#8E8E8E";
        $loginBtn.disabled = true;
    }
}

function move_main(){
    location.href="../main/main.html";
}

$loginBtn.addEventListener('click', move_main);
$loginId.addEventListener('keyup', isvalid);
$loginPassword.addEventListener('keyup', isvalid);


const $id = document.querySelector('#regi_id');
const $pass = document.querySelector('#regi_pass');
const $check_pass = document.querySelector('#regi_re_pass');
const $name = document.querySelector('#name');
const $phone1 = document.querySelector('#phone1');
const $phone2 = document.querySelector('#phone2');
const $phone3 = document.querySelector('#phone3');
const $regi_btn = document.querySelector('#regi_btn');
const $return = document.querySelector('#return');

let check1 = false;
let check2 = false;
let check3 = false;

// 휴대폰 번호 확인
function check_phone1() {
    if ($phone1.value.length === 3) {
        $phone2.focus();
    }
}
function check_phone2() {
    if ($phone2.value.length === 4) {
        $phone3.focus();
    }
}

// valid_check

// 이메일 검사
$id.onkeyup = function () {
    document.querySelector('#emailError').innerHTML = "이메일이 올바르지 않습니다.";
    if ($id.value.includes('@')) {
        let $id_0 = $id.value.split('@')[0];
        let $id_1 = $id.value.split('@')[1];
        if ($id_0 === '' || $id_1 === '') {
            document.querySelector('#emailError').innerHTML = "이메일이 올바르지 않습니다.";
        } else {
            document.querySelector('#emailError').innerHTML = '';
            check1 =true;
        }
    }
};

// 비밀번호
function strongPassword(str) {
    return /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/.test(str);
}
$pass.onkeyup = function () {
    if ($pass.value === "") {
        document.querySelector('#passwordError').innerHTML = "비밀번호를 입력해주세요.";
    } else if ($pass.value && !strongPassword($pass.value)) {
        document.querySelector('#passwordError').innerHTML = "비밀번호는 8~15자리 숫자/문자/특수문자를 포함해야합니다."
    }
    else {
        document.querySelector('#passwordError').innerHTML = '';
        check2=true;
    }

}

// 비밀번호 확인
$check_pass.onkeyup = function () {
    if (!$pass.value) {
        document.querySelector('#passwordError').innerHTML = "비밀번호를 입력해주세요.";
    } else {
        document.querySelector('#passwordError').innerHTML = "";
        if ($pass.value !== $check_pass.value) {
            document.querySelector('#passwordCheckError').innerHTML = "비밀번호가 동일하지 않습니다.";
        } else {
            document.querySelector('#passwordCheckError').innerHTML = "";
            check3=true;
        }
    }
}

function button() {
    switch (!(check1 && check2 && check3)) {
        case true: $regi_btn.disabled = true; break;
        case false: $regi_btn.disabled = false; break
    }
}

function move_login(){
    location.href="../login";
}

$id.addEventListener('keyup', button);
$pass.addEventListener('keyup', button);
$check_pass.addEventListener('keyup', button);
$regi_btn.addEventListener('click', move_login);
$return.addEventListener('click', move_login);
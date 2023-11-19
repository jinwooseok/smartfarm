const $id = document.querySelector("#registerID");
const $pass = document.querySelector("#registerPassword");
const $checkPassword = document.querySelector("#registerCheckPassword");
const $name = document.querySelector("#name");
const $phoneFront = document.querySelector("#phoneFront");
const $phoneMiddle = document.querySelector("#phoneMiddle");
const $phoneLast = document.querySelector("#phoneLast");

const $registerForm = document.getElementById("registerForm");
const $registerButton = document.querySelector("#registerButton");
const $backToLogin = document.querySelector("#backToLogin");

function isValidEmail(email) {
  const reg = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]/;
  return reg.test(email);
}

function isValidPassword(password) {
  const reg = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
  return reg.test(password);
}

function isValidPhone() {
  return (
    $phoneFront.value.length === 3 &&
    $phoneMiddle.value.length === 4 &&
    $phoneLast.value.length === 4
  );
}

function updateButtonState() {
  const isValid =
    isValidEmail($id.value) &&
    isValidPassword($pass.value) &&
    $pass.value === $checkPassword.value &&
    $name.value.trim() !== "" &&
    isValidPhone();

  $registerButton.disabled = !isValid;
}

function handleKeyUp(event) {
  const id = event.target.id;

  switch (id) {
    case "registerID":
      document.querySelector("#emailError").innerHTML = isValidEmail($id.value)
        ? ""
        : "이메일이 올바르지 않습니다.";
      break;
    case "registerPassword":
      document.querySelector("#passwordError").innerHTML = $pass.value
        ? isValidPassword($pass.value)
          ? ""
          : "비밀번호는 8~15자리 숫자/문자/특수문자를 포함해야합니다."
        : "비밀번호를 입력해주세요.";
      document.querySelector("#passwordCheckError").innerHTML =
        $pass.value !== $checkPassword.value
          ? "비밀번호가 동일하지 않습니다."
          : "";
      break;
    case "registerCheckPassword":
      document.querySelector("#passwordCheckError").innerHTML =
        $pass.value !== $checkPassword.value
          ? "비밀번호가 동일하지 않습니다."
          : "";
      break;
    case "name":
      document.querySelector("#nameError").innerHTML = $name.value.trim()
        ? ""
        : "이름을 입력하세요";
      break;
    default:
      break;
  }

  updateButtonState();
}


function moveLogin() {
  $registerForm.action = "/users/register/";
  $registerForm.method = "POST";
  $registerForm.submit();
}

function moveMain() {
  location.href = "/";
}

$registerForm.addEventListener("keyup", handleKeyUp);
$registerButton.addEventListener("click", moveLogin);
$backToLogin.addEventListener("click", moveMain);

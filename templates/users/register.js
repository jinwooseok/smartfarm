
import cookies from "/templates/JS/csrfToken.js";

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

const $checkEmail = document.querySelector("#checkEmail");
const $checkCertificationNumber = document.querySelector("#checkCertificationNumber");
const $postCertificationNumber = document.querySelector("#postCertificationNumber");

let emailValid;

async function checkDuplicateEmail(email) {
  try {
    const response = await $.ajax({
      url: "./email/",
      type: "post",
      dataType: "json",
      headers: { "X-CSRFToken": cookies['csrftoken'] },
      data: { email },
      async: false,
    });

    return response.data;
  } catch (error) {
    console.error("error: " + error);
    throw error; // rethrow the error for the caller to handle
  }
}

function regEmail() {
  const email=$id.value;
  const reg = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-za-z0-9\-]+/;
  return reg.test(email);
}

async function isValidEmail() {
  const email = $id.value;
  const reg = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-za-z0-9\-]+/;

  if (regEmail()) {
    try {
      const isDuplicate = await checkDuplicateEmail(email);
      if (isDuplicate) {
        alert("중복된 아이디 입니다.");
      } else {
        alert('사용가능한 아이디 입니다.');
      }
      return !isDuplicate;
    } catch (error) {
      alert(error);
      console.log("error: " + await error);
      return false;
    }
  } else {
    alert("올바른 이메일 형식이 아닙니다.");
    return false;
  }
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
    emailValid &&
    isValidPassword($pass.value) &&
    $pass.value === $checkPassword.value &&
    $name.value.trim() !== "" &&
    isValidPhone();

  $registerButton.disabled = !isValid;
}

function showKeyUpError(event) {
  const id = event.target.id;

  switch (id) {
    case "registerID":
      document.querySelector("#emailError").innerHTML = regEmail()
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
  location.replace("/");
}

$checkEmail.addEventListener("click", async () => {
  emailValid = await isValidEmail();
  // Now you can use the 'isValid' variable for further processing
  console.log("Is email valid?", emailValid)
});
$registerForm.addEventListener("keyup", showKeyUpError);
$registerButton.addEventListener("click", moveLogin);
$backToLogin.addEventListener("click", moveMain);

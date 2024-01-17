import API from "/templates/src/Utils/API.mjs";
// import cookies from "/templates/src/Utils/CsrfToken.mjs";

const $id = document.querySelector("#registerID");
const $password = document.querySelector("#registerPassword");
const $checkPassword = document.querySelector("#registerCheckPassword");
const $name = document.querySelector("#name");
const $job = document.querySelector("#registerJob");
const $phoneFront = document.querySelector("#phoneFront");
const $phoneMiddle = document.querySelector("#phoneMiddle");
const $phoneLast = document.querySelector("#phoneLast");
const $timer = document.querySelector("#timer");

const $registerForm = document.getElementById("registerForm");
const $registerButton = document.querySelector("#registerButton");
const $backToLogin = document.querySelector("#backToLogin");

const $checkEmail = document.querySelector("#checkEmail");
const $checkCertificationNumber = document.querySelector("#checkCertificationNumber");
const $postCertificationNumber = document.querySelector("#postCertificationNumber");

let emailValid = false;
let checkCertificationNumber = false;

async function checkDuplicateEmail(email) {
  const data = { email : email };
  const response = await API("./email/", "post", data);
  return response.status;
}

function regEmail() {
  const email=$id.value;
  const reg = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-za-z0-9\-]+/;
  return reg.test(email);
}

async function isValidEmail() {
  const email = $id.value;

  if (regEmail()) {
    try {
      const isDuplicate = await checkDuplicateEmail(email);
      if (isDuplicate === "success") {
        alert('사용가능한 아이디 입니다.');
        document.querySelector('#idDuplicate').innerHTML = '';
        return true;
      } else if (isDuplicate === 452) {
        alert("중복된 아이디 입니다.");
        return false;
      }
    } catch (error) {
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
    isValidPassword($password.value) &&
    $password.value === $checkPassword.value &&
    $name.value.trim() !== "" &&
    isValidPhone() &&
    checkCertificationNumber;

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
      document.querySelector("#passwordError").innerHTML = $password.value
        ? isValidPassword($password.value)
          ? ""
          : "비밀번호는 8~15자리 숫자/문자/특수문자를 포함해야합니다."
        : "비밀번호를 입력해주세요.";
      document.querySelector("#passwordCheckError").innerHTML =
        $password.value !== $checkPassword.value
          ? "비밀번호가 동일하지 않습니다."
          : "";
      break;
    case "registerCheckPassword":
      document.querySelector("#passwordCheckError").innerHTML =
        $password.value !== $checkPassword.value
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

function locationMain() {
  location.replace("/");
}

let timerInterval;

function timer() {
  $checkCertificationNumber.disabled =false;

  const endTime = (+new Date) + 1000 * 181;
  let msLeft = endTime - (+new Date);
  let time = new Date( msLeft );
  let hours = time.getUTCHours();
  let mins = time.getUTCMinutes();

  $postCertificationNumber.disabled = true;

  timerInterval = setInterval( () => {
    const element = $timer;
  
    msLeft = endTime - (+new Date);
    if ( msLeft < 0 ) {
      alert('done');
      $postCertificationNumber.disabled = false;
      clearInterval(timerInterval); 
    } else {
      time = new Date( msLeft );
      hours = time.getUTCHours();
      mins = time.getUTCMinutes();
      element.innerHTML = (hours ? hours + ':' + ('0' + mins).slice(-2) : mins) + ':' + ('0' + time.getUTCSeconds()).slice(-2);
    }
  }, time.getUTCMilliseconds());
};

/* API 미완
async function checkSendCertification() {
  return await API(
    "users/sign-up/phone/send/",
    "post",
    {phone : [$phoneFront.value, $phoneMiddle.value, $phoneLast.value]}
  );
}

async function sendCertification () {
  const isSendNumber = await checkSendCertification();
  console.log(isSendNumber);

  switch(isSendNumber.status) {
    case "success" : 
      alert("인증번호를 전송합니다.");
      timer();
      break;
    case 1001 :
      alert("잘못된 전화번호 형식입니다.");
      break;
    case 1002 :
        alert("존재하지 않는 전화번호입니다.");
        break;
    case 1003 :
      alert("중복된 전화번호입니다.");
      break;
    case 1004 :
      alert("인증번호 전송에 실패했습니다.");
      break;
  };
}
*/

async function submitUserRegisterInfo() {
  const data = {
    email: $id.value,
    password: $password.value,
    name: $name.value,
    job: $job.value,
    phone: JSON.stringify([
      $phoneFront.value.replace(/'/g, ""),
      $phoneMiddle.value.replace(/'/g, ""),
      $phoneLast.value.replace(/'/g, "")
    ]),
  };

  return await API("/users/sign-up/", "post", data);
}

const checkRegisterResponse = async () => {
  const response = await submitUserRegisterInfo();
  console.log("response", response);
  if (response.status === "success") {
    location.replace("/users/sign-in/");
  }

  if (response.status === 1002) {
    // alert("계정이 존재하지 않습니다."); //
  }
}

// $postCertificationNumber.addEventListener('click', sendCertification);
$postCertificationNumber.addEventListener('click', timer);

$checkCertificationNumber.addEventListener('click', () => {
  clearInterval(timerInterval);

  // api로 변경해야 함
  $postCertificationNumber.disabled = false;
  checkCertificationNumber = true;
  updateButtonState();
  // timer();
})

$checkEmail.addEventListener("click", async () => {
  emailValid = await isValidEmail();
  updateButtonState();
});

$registerForm.addEventListener("keyup", showKeyUpError);
$registerButton.addEventListener("click", checkRegisterResponse);
$backToLogin.addEventListener("click", locationMain);

import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";

const $nextBtn = document.querySelector("#next");
const $logoutBtn = document.querySelector("#logoutBtn");
const $buttonDIV = document.querySelector("#buttonDIV");


$logoutBtn.addEventListener("click", Logout);


// 페이지 그리기

const saveFile = () => {
	console.log("Save")
}

// page 변환
const changeWorkDiv = (nowProgress) => {
	switch (nowProgress) {
		case 0 :
			console.log("0");
			break;
		case 1 :
			console.log("1");
			break;
		case 2 :
			console.log("2");
			break;
		case 3 :
			$buttonDIV.innerHTML = '<button class="save" id="save"\>저장</button>';
			const $saveBtn = document.querySelector("#save");
			$saveBtn.addEventListener('click', saveFile);
			break;
	}
}

const changeProgress = () => {
	const $$progress = document.querySelectorAll(".progress");
	const progress = Array.from($$progress);

	let nowIndex = -1;
	for (let i = 0; i < progress.length; i++) {
		if (progress[i].classList.contains('now') && i !== 3){
			progress[i].classList.remove('now');
			nowIndex = i + 1;
			break;
		}
	}

	progress[nowIndex].classList.add('now');
	changeWorkDiv(nowIndex);
}

const clickNextBtn = () => {
	const isNext = confirm("다음 단계로 넘어 갑니다.");

	if (!isNext) {
		return;
	}

	changeProgress();
}

$nextBtn.addEventListener("click" , clickNextBtn);

/*
파일 확인 -> 전처리 -> 기타 설정 -> 변수 설정 -> 저장

1. 전처리 후 데이터 변환
2. 기타 설정 및 변수 목록은 js에서 보관 후 저장할 떄 전송
*/
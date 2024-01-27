import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";

import showFilePage from "./showFilePage.mjs";
import ShowTreatmentPage from "./showTreatmentPage.mjs";

// 순수 페이지 이동만 관리

const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

const $fileListSelectBox = document.querySelector("#fileListSelectBox");

////////////////////// 파일 변경
const fileName = JSON.parse(localStorage.getItem("fileTitle"));
let fileTitleLists; // 파일 목록

const setFileListSelectBox = async ()=> {
	const response = await API("/files/file-name/", "get");
	fileTitleLists = response.data;
	setNowFileTitle(response.data);
}

const setNowFileTitle = (fileTitleLists) => {
  fileTitleLists.map( (title) => {
    if (title.fileName === fileName) {
      $fileListSelectBox.innerHTML += `<Option value= '${title.fileName}' selected>` + title.fileName + `</option>`;
    } else {
      $fileListSelectBox.innerHTML += `<Option value= '${title.fileName}'>` + title.fileName + `</option>`;
    }
  });
};

const moveSelectedFileTitle = () => {
  const selectedFileTitle =  $fileListSelectBox.options[$fileListSelectBox.selectedIndex].value;
  localStorage.setItem("fileTitle", JSON.stringify(selectedFileTitle));
  location.href = `/revise/${selectedFileTitle}/`;
};

$fileListSelectBox.addEventListener("change", moveSelectedFileTitle);

// 시작 설정
(async function () {
	// 파일 목록 보여줌
  await setFileListSelectBox();

	// 파일 데이터 그리기
	showFilePage.setFileTitle(fileName);
	await showFilePage.setFileData();
	showFilePage.showFile($spreadSheetDIV);
}());

///////////////////////// page 변환
const changeProgress = (step) => {
	const $$progress = document.querySelectorAll(".progress");
	const progress = Array.from($$progress);

	let nowIndex = -1;
	for (let i = 0; i < progress.length; i++) {
		if (progress[i].classList.contains('now')){
			nowIndex = i;
			break;
		}
	}

	if (step === "next" && nowIndex !== 3) {
		progress[nowIndex].classList.remove('now');
		progress[nowIndex+1].classList.add('now');
		changeDiv(nowIndex+1);
	} 

	if (step === "prev" && nowIndex !== 0) {
		progress[nowIndex].classList.remove('now');
		progress[nowIndex-1].classList.add('now');
		changeDiv(nowIndex-1);
	}
}

const clickEvent = (id) => {
	switch (id) {
		case "save" :
			alert("파일을 저장합니다.");
			break;
		case "next" :
			confirm(`이동 합니다.`) === true ? changeProgress(id) : null;
			break;
		case "prev" :
			confirm(`이동 합니다.`) === true ? changeProgress(id) : null;
			break;
	}
}

const changeDiv = async (nowProgress) => {
	console.log("현재 페이지", nowProgress);
	const $workDIV = document.querySelector(".workDIV");

	if (nowProgress === 0) {
		$workDIV.innerHTML = showFilePage.templates();

		const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");
		showFilePage.showFile($spreadSheetDIV);
	}

	if (nowProgress === 1) {
		ShowTreatmentPage.setFileTitle(fileName);
		await ShowTreatmentPage.setStaticData();

		$workDIV.innerHTML = ShowTreatmentPage.templates();
	}

	if (nowProgress === 2) {
		
	}

	if (nowProgress === 3) {

	}
	
}

window.addEventListener("click", (event) => {
	const targetId = event.target.id;
	if (targetId !== "") {
		clickEvent(targetId);
	}
})

/*
파일 확인 -> 전처리 -> 기타 설정 -> 변수 설정 -> 저장

1. 전처리 후 데이터 변환
2. 기타 설정 및 변수 목록은 js에서 보관 후 저장할 떄 전송

페이지가 전환되면 전역변수에 설정한 값들은 변경을 안함
함수 내에서 변수를 다시 불러서 해야하는 경우가 많을 것
안되면 변수를 함수 내에서 설정하도록 하자
*/
import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";

import ShowFilePage from "./ShowFilePage.mjs";
import ShowTreatmentPage from "./ShowTreatmentPage.mjs";
import RevisePage from "./RevisePage.mjs";
import Graph from "./Graph.mjs";

// 순수 페이지 이동만 관리
const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

const $fileListSelectBox = document.querySelector("#fileListSelectBox");

////////////////////// 파일 변경
const fileName = JSON.parse(localStorage.getItem("fileTitle"));

const setFileListSelectBox = async ()=> {
	const response = await API("/files/file-name/", "get");
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
	Loading.StartLoading();
	ShowFilePage.setFileTitle(fileName);
	await ShowFilePage.setFileData();
	ShowFilePage.showFile($spreadSheetDIV);
	Loading.CloseLoading();
}());

const submitData = {
	newFileName: '',
	fileType: "", // typeDIv
	startIndex: 1, // startIndex
	dateColumn: 1, // date
	interval: "", //periodDIV
	var: "",
}

const checkRadioValue = (htmlTag) => {
  for (let i = 0; i < htmlTag.length; i++) {
    if (htmlTag[i].checked) {
      if (htmlTag[i].value === "else"){
        return document.getElementById("elsePeriod").value;
      }
      return htmlTag[i].value;
    }
  }
}

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

	if (step === "nextPage" && nowIndex !== 3) {
		progress[nowIndex].classList.remove('now');
		progress[nowIndex+1].classList.add('now');
		changeDiv(nowIndex+1);
	} 

	if (step === "prevPage" && nowIndex !== 0) {
		progress[nowIndex].classList.remove('now');
		progress[nowIndex-1].classList.add('now');
		changeDiv(nowIndex-1);
	}
}

const clickEvent = async (event, id, targetClass) => {

	// 페이지 이동
	if (id === "nextPage" || id === "prevPage") {
		// 데이터 확인
		if(targetClass.contains("setting")) {
			submitData.fileType = checkRadioValue(document.querySelectorAll('input[name="type"]'));
			submitData.startIndex = document.querySelector("#startIndex").value;
			submitData.dateColumn = document.querySelector("#date").value
			submitData.interval =  checkRadioValue(document.querySelectorAll('input[name="period"]'));

			console.log("setting", submitData);
		}

		// 전처리
		if(targetClass.contains("treat")) {
			await ShowTreatmentPage.submit();
		}

		confirm(`이동 합니다.`) === true ? changeProgress(id) : null;
		return;
	}	

	// periodSelectDIV
	if (id === "else") {
		document.querySelector("#elsePeriod").disabled = false;
    return;
	}

	if (id === "weekly" || id === "daily") {
		document.querySelector("#elsePeriod").disabled = true;
    return;
	}

	///////////////////// revise
	if (id === "wordContain") { // 포함된 변수 목록 불러옴
		RevisePage.addWordContainSelectBox(event);
	}

	if (id === "save") { 	// 파일 저장
		submitData.newFileName = document.querySelector('#fileName').value;
		submitData.var = JSON.stringify(RevisePage.getNewData());
		console.log("submitData", submitData);
		return;
	}

	if (id === "resetData") {// 변수 초기화
		RevisePage.resetData();
		document.querySelector("#selectedValueList").innerHTML = '';
		return;
	}

	if (id === "defaultSelect") { // 변수 자동 선택
		RevisePage.createEasyVersionData(event);
		return;
	}

	if (id === "optionDelete") { // 변수 삭제
		RevisePage.varDelete();
		return;
	}

	if (id === "optionADD") { // 변수 추가
		RevisePage.createHardVersionData();
		return;
	}

	if (id === "easy") {
		document.querySelector(".box").innerHTML = RevisePage.templatesEasy();
		return;
	}

	if (id === "hard") {
		document.querySelector(".box").innerHTML = RevisePage.templatesHard();
		return;
	}

	// 그래프
	if (id === "nextGraph") {
		// 그래프 다음 데이터
		return;
	}
	if (id === "prevGraph") {
		// 그래프 이전 데이터
		return;
	}
	if (id === "closeGraph") {
		confirm(`이동 합니다.`) === true ? changeProgress(id) : null;
		return;
	}
}

window.addEventListener("click", (event) => {
	const targetId = event.target.id;
	const targetClass= event.target.classList;
	if (targetId !== "") {
		clickEvent(event, targetId, targetClass);
	}
})

const changeDiv = async (nowProgress) => {
	const $workDIV = document.querySelector(".workDIV");

	if (nowProgress === 0) { // 데이터 그림
		$workDIV.innerHTML = ShowFilePage.templates();

		const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");
		ShowFilePage.showFile($spreadSheetDIV);
	}

	if (nowProgress === 1) { // 전처리
		ShowTreatmentPage.setFileTitle(fileName);

		$workDIV.innerHTML = await ShowTreatmentPage.templates();

		// 그래프 보여주는 부분
		const $$columnName = document.querySelectorAll("#columnName");
		$$columnName.forEach((element) => {
			element.addEventListener('click', (element) => {
				Graph.showGraph(element.innerHTML);
			});
		});
	
	}

	if (nowProgress === 2) { // 파일 수정 데이터 전송
		$workDIV.innerHTML = RevisePage.templates();

		// 데이터 열 불러오기
		ShowFilePage.setColumn(document.querySelector("#dataColumnList"));
		// 이름 자동 지정
		RevisePage.setFileName(fileName);
	}

	if (nowProgress === 3) { // 파일 저장
		$workDIV.innerHTML = `
		<div class="buttonDIV" id="buttonDIV">
			<button class="nextPage" id="nextPage">다음</button>
			<button class="prevPage" id="prevPage">이전</button>
		</div>
		`;
	}
	
}

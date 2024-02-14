import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import { getFileNameList, setFileList } from "/templates/src/Utils/fileNameList.mjs";

import ShowFilePage from "./ShowFilePage.mjs";
import ShowPreprocessPage from "./ShowPreprocessPage.mjs";
import RevisePage from "./RevisePage.mjs";
import Graph from "./Graph.mjs";

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

const $fileListSelectBox = document.querySelector("#fileListSelectBox");

////////////////////// 파일 변경
const fileName = JSON.parse(localStorage.getItem("fileTitle"));

const moveSelectedFileTitle = () => {
  const selectedFileTitle =  $fileListSelectBox.options[$fileListSelectBox.selectedIndex].value;
  localStorage.setItem("fileTitle", JSON.stringify(selectedFileTitle));
  location.href = `/revise/${selectedFileTitle}/`;
};

$fileListSelectBox.addEventListener("change", moveSelectedFileTitle);

const fileList = await getFileNameList();
setFileList($fileListSelectBox, fileList, fileName);

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
	const $$button = document.querySelectorAll('button');
	Array.from($$button).map((button) => {
		button.disabled = true;
	})

	// 페이지 이동
	if (id === "nextPage" || id === "prevPage") {

		const go = confirm(`이동 합니다.`);

		if (go) {
			changeProgress(id);
			// 데이터 확인
			if(targetClass.contains("setting")) {
				submitData.fileType = checkRadioValue(document.querySelectorAll('input[name="type"]'));
				submitData.startIndex = Number(document.querySelector("#startIndex").value);
				submitData.dateColumn = Number(document.querySelector("#date").value);
				submitData.interval =  checkRadioValue(document.querySelectorAll('input[name="period"]'));
			}

			// 전처리
			if(targetClass.contains("treat")) {
				Loading.StartLoading();
				await ShowPreprocessPage.submit();
				Loading.CloseLoading();
			}
		}
	}	

	// periodSelectDIV
	if (id === "else") {
		document.querySelector("#elsePeriod").disabled = false;
	}

	if (id === "weekly" || id === "daily") {
		document.querySelector("#elsePeriod").disabled = true;
	}

	/////
	if (id === "deleteLine") {
		document.querySelector(".SelectDIV").innerHTML = ShowPreprocessPage.templateDelete();
	}

	if (id === "changeValue") {
		document.querySelector(".SelectDIV").innerHTML = ShowPreprocessPage.templatesChange();
	}

	///////////////////// revise
	if (id === "wordContain") { // 포함된 변수 목록 불러옴
		RevisePage.addWordContainSelectBox(event);
	}

	if (id === "save") { 	// 파일 저장
		submitData.newFileName = document.querySelector('#fileName').value;
		submitData.var = JSON.stringify(RevisePage.getNewData());

		Loading.StartLoading();
		await RevisePage.submit(fileName, submitData);
		Loading.CloseLoading();
	}

	if (id === "resetData") {// 변수 초기화
		RevisePage.resetData();
		document.querySelector("#selectedValueList").innerHTML = '';
	}

	if (id === "defaultSelect") { // 변수 자동 선택
		RevisePage.createEasyVersionData(event);
	}

	if (id === "optionDelete") { // 변수 삭제
		RevisePage.varDelete();
	}

	if (id === "optionADD") { // 변수 추가
		RevisePage.createHardVersionData();
	}

	if (id === "easy") {
		document.querySelector(".box").innerHTML = RevisePage.templatesEasy();
	}

	if (id === "hard") {
		document.querySelector(".box").innerHTML = RevisePage.templatesHard();
	}

	/////////////////////// 여기부터 해야함
	// 그래프
	if (id === "nextGraph") {
		// 그래프 다음 데이터
	}
	if (id === "prevGraph") {
		// 그래프 이전 데이터
	}
	if (id === "closeGraph") {
		Graph.closeGraph();
	}
	
	Array.from($$button).map((button) => {
		button.disabled = false;
	})
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

		// 파일 데이터 그리기
		Loading.StartLoading();
		ShowFilePage.setFileTitle(fileName);
		await ShowFilePage.setFileData();
		ShowFilePage.showFile($spreadSheetDIV);
		const $dateBox = document.querySelector("#dateBox");
		const list = ShowFilePage.getFileDate();
		setFileList($dateBox, Object.keys(list[0]));
		Loading.CloseLoading();
	}

	if (nowProgress === 1) { // 전처리
		ShowPreprocessPage.setFileTitle(fileName);

		$workDIV.innerHTML = ShowPreprocessPage.templates();

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

}

changeDiv(0)
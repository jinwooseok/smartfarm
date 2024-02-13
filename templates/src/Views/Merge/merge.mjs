import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import { getFileNameList } from "/templates/src/Utils/fileNameList.mjs";

import MergePage from "./MergePage.mjs";
import VarSelectPage from "./VarSelectPage.mjs";

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

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


	if (id === "nextPage" || id === "prevPage") {
		confirm(`이동 합니다.`) === true ? changeProgress(id) : null;
		
	}	

	if (id === "merge") {
		const $mergeFileName = document.querySelector("#mergeFileName");

		if ($mergeFileName.value === "") {
			alert('파일 이름을 정해주세요')
			return;
		}

		// 병합 데이터 전송
		MergePage.setFileTitle($mergeFileName.value);
		await MergePage.sendMergeInfo();

		// 파일 데이터 그리기
		Loading.StartLoading();
		const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");
		// await MergePage.setFileData();
		// MergePage.showFile($spreadSheetDIV);
		Loading.CloseLoading();
	}

	if (id === "switch") {
		const $confirmDIV = document.querySelector(".confirmDIV");
		$confirmDIV .innerHTML = VarSelectPage.makeCheckedList();
	}

	if (id === '시차'){

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
	const $columnDIV = document.querySelector(".columnDIV");

	if (nowProgress === 0) { // 병합
		$columnDIV.innerHTML = MergePage.templates();
		MergePage.inputSelectBoxValue(await getFileNameList());
		MergePage.setEventListener();
	}

	if (nowProgress === 1) { // 변수 선택
		const $mergeFileName = document.querySelector("#mergeFileName");
		VarSelectPage.setVarList(await MergePage.postFilename($mergeFileName.value));
		$columnDIV.innerHTML = VarSelectPage.templates();
		VarSelectPage.setCheckedVar();
	}

	if (nowProgress === 2) { // 시차 변수
		$columnDIV.innerHTML = `
		2
			<div class="buttonDIV" id="buttonDIV">
				<button class="save" id="save">저장</button>
				<button class="prevPage" id="prevPage">이전</button>
			</div>
		`
	}

	if (nowProgress === 3) { // 파일 저장

	}
}

changeDiv(0);
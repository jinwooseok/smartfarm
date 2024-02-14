import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import { getFileNameList, setFileList } from "/templates/src/Utils/fileNameList.mjs";

import MergePage from "./MergePage.mjs";
import VarSelectPage from "./VarSelectPage.mjs";
import TimeDifferenceDataPage from "./TimeDifferenceDataPage.mjs";

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);
let merged = false;
const 시차데이터 = {
	"feature": [],
	"windowSize": 0,
	"count": 0,
	"dateColumn": 0,
	"newFileName": ""
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


	if (id === "nextPage" || id === "prevPage") {

		if (!merged) {
			alert("병합하기 버튼을 클릭해 병합을 먼저 진행해 주세요");
			return;
		}

		if (targetClass.contains("switchComplete")) {
			const $$text = document.querySelectorAll("p");
			Array.from($$text).map((val) => {
				시차데이터.feature.push(val.innerText);
			});
		}

		confirm(`이동 합니다.`) === true ? changeProgress(id) : null;
		
	}	

	if (id === "merge") {
		const $mergeFileName = document.querySelector("#mergeFileName");

		if ($mergeFileName.value === "") {
			alert('파일 이름을 정해주세요')
			return;
		}

		시차데이터.newFileName = document.querySelector("#mergeFileName").value;

		// 병합 데이터 전송
		await MergePage.mergeData();
		merged = true;

		// 파일 데이터 그리기
		Loading.StartLoading();
		const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");
		MergePage.showFile($spreadSheetDIV);
		Loading.CloseLoading();
	}

	if (id === "switch") {
		const $confirmDIV = document.querySelector(".confirmDIV");
		$confirmDIV.innerHTML = VarSelectPage.makeCheckedListDIV();
	}

	if (id === 'save'){
		시차데이터.windowSize = document.querySelector("#windowSize").value;
		시차데이터.count = document.querySelector("#count").value;
		시차데이터.dateColumn = document.querySelector("#dateBox").options[document.querySelector("#dateBox").selectedIndex]?.value;
		시차데이터.feature = JSON.stringify(시차데이터.feature);
		const timeDiffName = MergePage.getMergeFileName();
		const response = await API(`/files/${timeDiffName}/data/timeseries/`, "post", 시차데이터);

		// if(response.status === "success") {
		// 	location.replace("/file-list/");
		// }
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
		MergePage.inputValueToSelectBox(await getFileNameList());
		MergePage.setEventListener();
	}

	if (nowProgress === 1) { // 변수 선택
		VarSelectPage.setVarList(Object.keys(MergePage.getFileData()[0])); // 87번 줄 엑셀 데이터 Object.keys(MergePage.getFileData()[0]);
		$columnDIV.innerHTML = VarSelectPage.templates();

		const $confirmDIV = document.querySelector(".confirmDIV");
		$confirmDIV.innerHTML = VarSelectPage.makeCheckedListDIV();
	}

	if (nowProgress === 2) { // 시차 변수
		$columnDIV.innerHTML = TimeDifferenceDataPage.templates();

		const $dateBox = document.querySelector("#dateBox");
		setFileList($dateBox, 시차데이터.feature);
	}

}

changeDiv(0);
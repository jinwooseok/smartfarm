import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import { getFileNameList, setFileList } from "/templates/src/Utils/fileNameList.mjs";
import responseMessage from "/templates/src/Constant/responseMessage.mjs";

import MergePage from "./MergePage.mjs";
import VarSelectPage from "../Analyze/VarSelectPage.mjs";

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

const managedData = {
	merged: false,
	useVariable: [],
	fileTitle: "",
	mergedData: '',
	saveData: [],
}

const makeSaveData = (column, data) => {
	const returnData = [];

	data.map((value) => {
		const newObj = {};
		column.map((col) => {
			newObj[col] = value[col];
		})
		returnData.push(newObj);
	});

	return returnData;
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

	if (step === "nextPage" && nowIndex !== 2) {
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
		if (!managedData.merged) {
			alert("병합하기 버튼을 클릭해 병합을 먼저 진행해 주세요");
			return;
		}

		confirm(`이동 합니다.`) === true ? changeProgress(id) : null;		
	}	

	if (id === "merge") {
		const $mergeFileName = document.querySelector("#mergeFileName");

		if ($mergeFileName.value === "") {
			alert('파일 이름을 정해주세요')
			return;
		}

		// 병합 데이터 전송
		await MergePage.mergeData();
		managedData.merged = true;
		managedData.fileTitle = $mergeFileName.value;

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
		const $$text = document.querySelectorAll("p");
		Array.from($$text).map((val) => {
			managedData.useVariable.push(val.innerText);
		});

		managedData.mergedData = MergePage.getFileData();		
		managedData.saveData = makeSaveData(managedData.useVariable, managedData.mergedData);

		const response = await API(`/files/save/`, "post", {
			fileName: managedData.fileTitle,
			fileData: JSON.stringify(managedData.saveData),
		});
		const status = response.status || response;
		responseMessage[status] === "success" ? location.replace("/file-list/") : alert(responseMessage[status]);
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
		VarSelectPage.setVarList(Object.keys(MergePage.getFileData()[0]));
		$columnDIV.innerHTML = VarSelectPage.templates();

		const $confirmDIV = document.querySelector(".confirmDIV");
		$confirmDIV.innerHTML = VarSelectPage.makeCheckedListDIV();
	}

}

changeDiv(0);
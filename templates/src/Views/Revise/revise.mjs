import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import Excel from "/templates/src/Model/Excel.mjs";

const $nextBtn = document.querySelector("#next");
const $prevBtn = document.querySelector("#prev");

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

////////////////////////////////////
////////    파일 변경 끝   //////////
////////////////////////////////////

//////////////////////// 엑셀 그림
let fileData; // 파일 데이터
const setFileData = async () => {
	const response = await API(`/files/${fileName}/data/`, "get");
	const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");
	$spreadSheetDIV.innerHTML = "";
	showFile(response.data, $spreadSheetDIV);
	fileData = response.data;
}

const showFile = (data, element) => {
	new Excel(data, element);
}

////////////////////////////////////
////////    엑셀 그림 끝   //////////
////////////////////////////////////

///////////////////////// 통계치
let staticData;

const setStaticData = async () => {
	const response = await API(`/files/${fileName}/data/summary/`, "get");
	staticData = response.data;
	drawStaticData(staticData);
}

const drawStaticData = (staticData) => {
	const $fileStaticDataDIV = document.querySelector("#fileStaticDataDIV");
	console.log("XXXx", staticData)
	// 여기부터 시작 => 통계치 그리기
	// for(let data of staticData) {
		
	// 	$fileStaticDataDIV.innerHTML += `
	// 		<div class="columnList">
	// 			<div class="columnName" id="columnName">
	// 				rererererererereerr
	// 			</div>
	// 			<div class="nullCount" id="nullCount">
	// 				3
	// 			</div>
	// 			<div class="Q1" id="Q1">
	// 				100
	// 			</div>
	// 			<div class="Q2" id="Q2">
	// 				100
	// 			</div>
	// 			<div class="Q3" id="Q3">
	// 				1000000000
	// 			</div>
	// 			<div class="mean" id="mean">
	// 				1
	// 			</div>
	// 			<div class="min" id="min">
	// 				0
	// 			</div>
	// 			<div class="max" id="max">
	// 				1
	// 			</div>
	// 		</div>
	// 	`
	// }
}

////////////////////////////////////
////////    통계치 끝   //////////
////////////////////////////////////

// 시작 설정
(async function () {
  // 파일 불러오는 API
  await setFileListSelectBox();
	await setFileData();
	await setStaticData();
}());

// 파일 저장
const saveFile = () => {
	console.log("Save")
}

///////////////////////// page 변환
const changeProgress = (step) => {
	const $$progress = document.querySelectorAll(".progress");
	const progress = Array.from($$progress);

	let nowIndex = -1;
	for (let i = 0; i < progress.length; i++) {
		if (progress[i].classList.contains('now')){
			progress[i].classList.remove('now');
			nowIndex = i;
			break;
		}
	}

	if (step === "next") {
		progress[nowIndex+1].classList.add('now');
		changeDiv(nowIndex+1);
	} else {
		progress[nowIndex-1].classList.add('now');
		changeDiv(nowIndex-1);
	}
}

const clickPageMove = (event) => {
	const btnType = event.target.innerHTML;
	const alarm = confirm(`${btnType} 단계로 넘어 갑니다.`);

	if (btnType === "이전" && alarm) {
		changeProgress("prev");
		return;
	}

	if (btnType === "다음" && alarm) {
		changeProgress("next");
		return;
	}
}

const changeDiv = (nowProgress) => {
	console.log("현재 페이지", nowProgress);
	const $workDIV = document.querySelector(".workDIV");

	if (nowProgress === 3) {

		const $buttonDIV = document.querySelector("#buttonDIV");
		$buttonDIV.innerHTML = `
			<button class="save" id="save">다음</button>
			<button class="prev" id="prev">이전</button>
		`;
		const $saveBtn = document.querySelector("#save");
		const $prevBtn = document.querySelector("#prev");
		$saveBtn.addEventListener('click', saveFile);
		$prevBtn.addEventListener("click" , clickPageMove);
		return;
	}

	if (nowProgress === 0) {
		$workDIV.innerHTML = `
			<div class="spreadSheetDIV" id="spreadSheetDIV">
			</div>

			<div class="fileStaticDataDIV" id="fileStaticDataDIV">
				<div class="columnList">
					<div class="columnName" id="columnName">
						열 이름
					</div>
					<div class="nullCount" id="nullCount">
						빈 값
					</div>
					<div class="Q1" id="Q1">
						1사분위 값
					</div>
					<div class="Q2" id="Q2">
						중앙값
					</div>
					<div class="Q3" id="Q3">
						3사분위값
					</div>
					<div class="mean" id="mean">
						평균
					</div>
					<div class="min" id="min">
						최소
					</div>
					<div class="max" id="max">
						최대
					</div>
				</div>
			</div>

			<div class="buttonDIV" id="buttonDIV">
				<button class="next" id="next">다음</button>
				<button class="prev" id="prev">이전</button>
			</div>
		`

		const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");
		showFile(fileData, $spreadSheetDIV);
	}

	if (nowProgress === 1) {
		$workDIV.innerHTML =  `
		<div class="buttonDIV" id="buttonDIV">
			<button class="next" id="next">다음</button>
			<button class="prev" id="prev">이전</button>
		</div>
		`;
	}

	if (nowProgress === 2) {
		
	}

	const $nextBtn = document.querySelector("#next");
	const $prevBtn = document.querySelector("#prev");
	$nextBtn.addEventListener("click" , clickPageMove);
	$prevBtn.addEventListener("click" , clickPageMove);
	
}

$nextBtn.addEventListener("click" , clickPageMove);
$prevBtn.addEventListener("click" , clickPageMove);

/*
파일 확인 -> 전처리 -> 기타 설정 -> 변수 설정 -> 저장

1. 전처리 후 데이터 변환
2. 기타 설정 및 변수 목록은 js에서 보관 후 저장할 떄 전송

페이지가 전환되면 전역변수에 설정한 값들은 변경을 안함
함수 내에서 변수를 다시 불러서 해야하는 경우가 많을 것
안되면 변수를 함수 내에서 설정하도록 하자
*/
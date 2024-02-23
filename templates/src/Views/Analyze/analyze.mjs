import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import downloadToCsv from "/templates/src/Utils/DownloadToCsv.mjs";
import API from "/templates/src/Utils/API.mjs";
import { setFileList } from "/templates/src/Utils/fileNameList.mjs";

import ToolPage from "./ToolPage.mjs";
import VarPage from "./VarPage.mjs";
import SelectPage from "./SelectPage.mjs";
import ResultPage from "./ResultPage.mjs";

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

//////////////////////

const globalData = {
  x: [],
  y: '',
  modelName : "",
}

const fileName = JSON.parse(localStorage.getItem("fileTitle"));

const clickEvent = async (event, id,) => {
  if (id === "nextPage" || id === "prevPage") {
    confirm(`이동 합니다.`) === true ? changeProgress(id) : null;

    if (event.target.classList.contains("analyze")) {
      Loading.StartLoading();
      const data = {
        yValue: globalData.y,
        xValue: JSON.stringify(globalData.x),
        fileData: JSON.stringify(VarPage.getFileData()),
      };
      ResultPage.setModelResult(globalData.modelName, data);
    }

    return;
	}

  if (id === "modelDown") {
    Loading.StartLoading();
    await API(`/analytics/${globalData.modelName}/model/download/`, "get");
    Loading.CloseLoading();
    return;
  }

  if (id === "fileDown") {
    const $mergeFileName = document.querySelector("#mergeFileName");
    if ($mergeFileName.value === "") {
			alert('파일 이름을 정해주세요')
			return;
		}
    downloadToCsv(ResultPage.getFileData(), $mergeFileName.value);
  }

  if (id === "modelSelect") {
    // 기타 설정
    // 모델의 y,x,파일 데이터 이름 등 설정
    /*
      globalData.x: [],
      globalData.y: '',
      modelName : "",
      파일 데이터 = > VarPage.getFileData()
    */
    changeProgress(3, 3);
  }

  if (id === "create") {
    Loading.StartLoading();
    globalData.modelName = document.querySelector(".modelName").value
    const data = {
      modelName: globalData.modelName,
      model: document.querySelector(".technique").options[document.querySelector(".technique").selectedIndex]?.value,
      trainSize: document.querySelector(".trainSize").value,
      yValue: globalData.y,
      xValue: JSON.stringify(globalData.x),
      fileData: JSON.stringify(VarPage.getFileData()),
    };
    const response = await ToolPage.postModelData(fileName, data); // 결과
    const $modelResultDIV = document.querySelector(".modelResultDIV");
    $modelResultDIV.style.display = "flex";
    $modelResultDIV.innerHTML = ToolPage.drawModelResult(response);

    document.querySelector(".analyze").disabled = false;

    return;
  }

  if (
    id === "use" ||
    id === "not"
    ) {
    const $timeDIV = document.querySelector(".timeDIV");
    $timeDIV.innerHTML = VarPage.onClickTimeDIff(id);
    return;
  }

  if (
    id === "classify" ||
    id === "regress"
    ) {
    const $tollDIV = document.querySelector(".tollDIV");
    $tollDIV.innerHTML = ToolPage.onClickTimeDIff(id);
    return;
  }

  if (id === "timeDiffCreate") {
    Loading.StartLoading();
    const data = {
      xValue: JSON.stringify(VarPage.setCheckedVarList()),
      yValue: document.querySelector(".yValue").options[document.querySelector(".yValue").selectedIndex]?.value,
      count: document.querySelector("#count").value,
      fileData: JSON.stringify(VarPage.getFileData()),
    };
    await VarPage.postTimeDiffData(fileName, data);
    const $listDIV = document.querySelector('#listDIV');
    $listDIV.innerHTML = VarPage.makeVarListDIV(VarPage.getFileFeatureInfo());
    return;
  }

  if (id ==="yValue") {
    const $yValue = document.querySelector("#yValue");
    $yValue.addEventListener("change", async(event) => {
      await VarPage.setImportanceOfFeature(fileName, {
        xValue: JSON.stringify(VarPage.getFeatureNameList()),
        yValue: event.target.value,
        fileData: JSON.stringify(VarPage.getFileData()),
      });
      const $listDIV = document.querySelector('#listDIV');
      $listDIV.innerHTML = VarPage.makeVarListDIV(VarPage.getFileFeatureInfo());
    });
  }
}

const changeProgress = (step, index=0) => {
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

  if (index === 3) {
    progress[nowIndex].classList.remove('now');
		progress[3].classList.add('now');
    changeDiv(3)
  }
}

window.addEventListener("click", (event) => {
	const targetId = event.target.id;

	if (targetId !== "") {
		clickEvent(event, targetId);
	}
})

const changeDiv = async (nowProgress) => {
  const $workDIV = document.querySelector(".workDIV");
  if (nowProgress === 0 ){
    $workDIV.innerHTML = SelectPage.templates([]);
  }

	if (nowProgress === 1) { // 모델 설정 - 변수
    if (VarPage.getFileFeatureInfo() === ""){
      await VarPage.setFileData(fileName);
      await VarPage.setFileFeatureInfo(fileName);
    }
    $workDIV.innerHTML = VarPage.templates();
  
    const $listDIV = document.querySelector('#listDIV');
    $listDIV.innerHTML = VarPage.makeVarListDIV(VarPage.getFileFeatureInfo());

    const $yValue = document.querySelector(".yValue");
    $yValue.innerHTML = "";
    setFileList($yValue, VarPage.getFeatureNameList()); 
	}

	if (nowProgress === 2) { // 모델 설정 - 도구
    globalData.x = VarPage.setCheckedVarList();
    globalData.y = document.querySelector(".yValue").options[document.querySelector(".yValue").selectedIndex]?.value

		ToolPage.setSelectedX(globalData.x);
    $workDIV.innerHTML = ToolPage.templates();

    const $yValueInput = document.querySelector(".yValueInput");
    $yValueInput.value = globalData.y;
	}

  if (nowProgress === 3) { // 분석 결과
    const data = {
      yValue: globalData.y,
      xValue: JSON.stringify(globalData.x),
      fileData: JSON.stringify(VarPage.getFileData()),
    };
    await ResultPage.setModelResult(globalData.modelName, data);

    // 분석 결과
    $workDIV.innerHTML = ResultPage.templates();
    // 산점도 그래프
    ResultPage.drawGraph();
    // 엑셀
    const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");
    ResultPage.drawExcel($spreadSheetDIV);
  }
}

window.onload = async () => {
  changeDiv(0);
}
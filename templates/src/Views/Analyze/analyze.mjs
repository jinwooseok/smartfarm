import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
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
    return;
	}	

  if (id === "modelSelect") {
    // 기타 설정
    console.log("X")
    changeDiv(3);
  }

  if (id === "create") {
    globalData.modelName = document.querySelector(".modelName").value
    const data = {
      modelName: globalData.modelName,
      model: document.querySelector(".technique").options[document.querySelector(".technique").selectedIndex]?.value,
      trainSize: document.querySelector(".trainSize").value,
      yValue: globalData.y,
      xValue: JSON.stringify(globalData.x),
      fileData: JSON.stringify(VarPage.getFileData()),
    };
    // const response = await ToolPage.postModelData(fileName, data); // 결과
    const response = {
      "model": "Linear Regression",
      "feature_names": [
          "외부기온",
          "내부습도"
      ],
      "target_names": "내부온도",
      "model_weights": [
          0.4149955508714468,
          0.175607215630296
      ],
      "random_state": 42,
      "mean_squared_error": 19.18719054180353,
      "r2_score": -0.388700425980828,
      "model_name": "linear_env.pkl"
    };
    const $modelResultDIV = document.querySelector(".modelResultDIV");
    $modelResultDIV.style.display = "flex";
    $modelResultDIV.innerHTML = ToolPage.drawModelResult(response);
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
    const data = {
      xValue: JSON.stringify(VarPage.setCheckedVarList()),
      yValue: document.querySelector(".yValue").options[document.querySelector(".yValue").selectedIndex]?.value,
      count: document.querySelector("#count").value,
      fileData: JSON.stringify(VarPage.getFileData()),
    };
    const response = await VarPage.postTimeDiffData(fileName, data);
    console.log("시차 리턴 데이터", response) // 변수 목록 수정 VarPage.makeVarListDIV(list)
    console.log(Object.keys(response[0]));
    // const $listDIV = document.querySelector('#listDIV');
    // $listDIV.innerHTML = VarPage.makeVarListDIV(VarPage.getFileFeatureInfo());
    return;
  }

  if (id ==="yValue") {
    // 변수 중요도
    const data = {
      xValue: JSON.stringify(VarPage.getFeatureNameList()),
      yValue: document.querySelector(".yValue").options[document.querySelector(".yValue").selectedIndex]?.value,
      fileData: JSON.stringify(VarPage.getFileData()),
    }
    console.log("변수 중요도", data);
    await VarPage.setImportanceOfFeature(fileName, data);
    const $listDIV = document.querySelector('#listDIV');
    $listDIV.innerHTML = VarPage.makeVarListDIV(VarPage.getFileFeatureInfo());
  }
}

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
    $workDIV.innerHTML =ToolPage.templates();

    const $yValueInput = document.querySelector(".yValueInput");
    $yValueInput.value = globalData.y;
	}

  if (nowProgress === 3) { // 분석 결과
    // 엑셀, 산점도 그래프, 분석 결과
    $workDIV.innerHTML = ResultPage.templates();
  }
}

window.onload = async () => {
  changeDiv(0);
}
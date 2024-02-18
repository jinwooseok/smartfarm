import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import { setFileList } from "/templates/src/Utils/fileNameList.mjs";

import ToolPage from "./ToolPage.mjs";
import VarPage from "./VarPage.mjs";

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

//////////////////////

const totalData = {
  x: [],
  y: '',
}

const fileName = JSON.parse(localStorage.getItem("fileTitle"));

const clickEvent = async (event, id,) => {

  if (id === "nextPage" || id === "prevPage") {
    confirm(`이동 합니다.`) === true ? changeProgress(id) : null;		
	}	

  if (id === "create") {
    const data = {
      modelName: document.querySelector(".modelName").value,
      model: document.querySelector(".technique").options[document.querySelector(".technique").selectedIndex]?.value,
      trainSize: document.querySelector(".trainSize").value,
      yValue: totalData.y,
      xValue: JSON.stringify(totalData.x),
    };
    console.log("create", data)
    // await ToolPage.postModelData(data);
  }

  if (
    id === "use" ||
    id === "not"
    ) {
    const $timeDIV = document.querySelector(".timeDIV");
    $timeDIV.innerHTML = VarPage.onClickTimeDIff(id);
  }

  if (
    id === "classify" ||
    id === "regress"
    ) {
    const $tollDIV = document.querySelector(".tollDIV");
    $tollDIV.innerHTML = ToolPage.onClickTimeDIff(id);
  }

  if (id === "timeDiffCreate") {
    const data = {
      feature: JSON.stringify(VarPage.setCheckedVarList()),
      windowSize: document.querySelector("#windowSize").value,
      count: document.querySelector("#count").value,
      newFileName: document.querySelector(".modelName").value,
    };
    console.log("timeDiffCreate", data)
    // await VarPage.postTimeDiffData(data);
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

window.addEventListener("click", (event) => {
	const targetId = event.target.id;

	if (targetId !== "") {
		clickEvent(event, targetId);
	}
})

const changeDiv = async (nowProgress) => {
	if (nowProgress === 0) { // 모델 설정 - 변수
    await VarPage.setVarList(fileName);
    const $workDIV = document.querySelector(".workDIV");
    $workDIV.innerHTML = VarPage.templates();
  
    const $yValue = document.querySelector(".yValue");
    setFileList($yValue, VarPage.getFeatureNameList()); 
	}

	if (nowProgress === 1) { // 모델 설정 - 도구
    totalData.x = VarPage.setCheckedVarList();
    totalData.y = document.querySelector(".yValue").options[document.querySelector(".yValue").selectedIndex]?.value

		ToolPage.setSelectedX(VarPage.getXValues());
    const $workDIV = document.querySelector(".workDIV");
    $workDIV.innerHTML =ToolPage.templates();

    const $yValueInput = document.querySelector(".yValueInput");
    $yValueInput.value = totalData.y;
	}

}

window.onload = async () => {
  await VarPage.setVarList(fileName);
  const $workDIV = document.querySelector(".workDIV");
  $workDIV.innerHTML = VarPage.templates();

  const $yValue = document.querySelector(".yValue");
  setFileList($yValue, VarPage.getFeatureNameList()); 
}
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
  fileData: "",
  timeDiffData: "",
  time: false,
}

const fileName = JSON.parse(localStorage.getItem("fileTitle"));

const checkRadioValue = (htmlTag) => {
  for (let i = 0; i < htmlTag.length; i++) {
    if (htmlTag[i].checked) {
      return htmlTag[i].value;
    }
  }
}

const clickEvent = async (event, id,) => {
  if (id === "nextPage" || id === "prevPage") {
    confirm(`이동 합니다.`) === true ? changeProgress(id) : null;
    return;
	}	

  if (id === "create") {
    const data = {
      modelName: document.querySelector(".modelName").value,
      model: document.querySelector(".technique").options[document.querySelector(".technique").selectedIndex]?.value,
      trainSize: document.querySelector(".trainSize").value,
      yValue: totalData.y,
      xValue: JSON.stringify(totalData.x),
      fileData: totalData.time ? JSON.stringify(totalData.timeDiffData) : JSON.stringify(totalData.fileData),
    };
    await ToolPage.postModelData(fileName, data);
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
      windowSize: document.querySelector("#windowSize").value,
      count: document.querySelector("#count").value,
      fileData: JSON.stringify(totalData.fileData),
    };
    totalData.timeDiffData = await VarPage.postTimeDiffData(fileName, data);
    totalData.timeDiffData !== "" ? totalData.time = true : totalData.time = false;
    return;
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
    if (VarPage.getVarList() === ""){
      await VarPage.setVarList(fileName);
    }
    const $workDIV = document.querySelector(".workDIV");
    $workDIV.innerHTML = VarPage.templates();
  
    const $yValue = document.querySelector(".yValue");
    $yValue.innerHTML = "";
    setFileList($yValue, VarPage.getFeatureNameList()); 

    totalData.time = false;
    totalData.timeDiffData = "";
	}

	if (nowProgress === 1) { // 모델 설정 - 도구
    const timeDIffRadio = checkRadioValue(document.querySelectorAll('input[name="time"]'));
    if (totalData.time && timeDIffRadio === "use") {
      totalData.x = Object.keys(totalData.timeDiffData[0]);
    } else {
      totalData.x = VarPage.setCheckedVarList();
    }
    totalData.y = document.querySelector(".yValue").options[document.querySelector(".yValue").selectedIndex]?.value

		ToolPage.setSelectedX(totalData.x);
    const $workDIV = document.querySelector(".workDIV");
    $workDIV.innerHTML =ToolPage.templates();

    const $yValueInput = document.querySelector(".yValueInput");
    $yValueInput.value = totalData.y;
	}
}

window.onload = async () => {
  totalData.fileData = await VarPage.setFileData(fileName);
  changeDiv(0)
}
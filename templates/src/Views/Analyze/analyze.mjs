import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import { setFileList } from "/templates/src/Utils/fileNameList.mjs";

import ToolPage from "./ToolPage.mjs";

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

////////////////////// 파일 변경
const fileName = JSON.parse(localStorage.getItem("fileTitle"));

const clickEvent = async (event, id, disabled) => {
  if (id === "create") {
    const data = {
      modelName: document.querySelector(".modelName").value,
      model: document.querySelector(".technique").options[document.querySelector(".technique").selectedIndex]?.value,
      trainSize: document.querySelector(".trainSize").value,
      yValue: document.querySelector(".yValue").options[document.querySelector(".yValue").selectedIndex]?.value,
      xValue: JSON.stringify(ToolPage.setCheckedVarList()),
    };
    await ToolPage.postModelData(data);
  }

  if (
    id === "use" ||
    id === "not"
    ) {
    const $timeDIV = document.querySelector(".timeDIV");
    $timeDIV.innerHTML = ToolPage.onClickTimeDIff(id);
  }

  if (id === "timeDiffCreate") {
    const data = {
      feature: JSON.stringify(ToolPage.setCheckedVarList()),
      windowSize: document.querySelector("#windowSize").value,
      count: document.querySelector("#count").value,
      newFileName: document.querySelector(".modelName").value,
    };
    await ToolPage.postTimeDiffData(data);
  }
}

window.addEventListener("click", (event) => {
	const targetId = event.target.id;
	const disabled= event.target.disabled;

	if (targetId !== "") {
		clickEvent(event, targetId, disabled);
	}
})

window.onload = async () => {
  await ToolPage.setVarList(fileName);
  const $workDIV = document.querySelector(".workDIV");
  $workDIV.innerHTML = ToolPage.templates();

  const $yValue = document.querySelector(".yValue");
  setFileList($yValue, ToolPage.getFeatureNameList()); 
}
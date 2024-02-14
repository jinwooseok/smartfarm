import Logout from "/templates/src/Utils/Logout.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";
import API from "/templates/src/Utils/API.mjs";
import { getFileNameList, setFileList } from "/templates/src/Utils/fileNameList.mjs";

import ToolPage from "./ToolPage.mjs";

const $logoutBtn = document.querySelector("#logoutBtn");
$logoutBtn.addEventListener("click", Logout);

const $fileListSelectBox = document.querySelector("#fileListSelectBox");
const $uploadDialog = document.querySelector("#uploadDialog");

////////////////////// 파일 변경
const fileName = JSON.parse(localStorage.getItem("fileTitle"));

const moveSelectedFileTitle = () => {
  const selectedFileTitle =  $fileListSelectBox.options[$fileListSelectBox.selectedIndex].value;
  localStorage.setItem("fileTitle", JSON.stringify(selectedFileTitle));
  location.href = `/analytics/${selectedFileTitle}/`;
};

$fileListSelectBox.addEventListener("change", moveSelectedFileTitle);

const fileList = await getFileNameList();
setFileList($fileListSelectBox, fileList, fileName);

const getVarList = async () => {
  const response = await API(`/files/${fileName}/data/feature/`, "get");

  if (response.status === "success") {
    await ToolPage.setVarList(response.data);
  }
}

// 파일 분석 창으로 이동
const handleClickMovePage = async () => {
  await getVarList();
  const $workDIV = document.querySelector(".workDIV");
  $workDIV.innerHTML = ToolPage.templates();

  const $yValue = document.querySelector(".yValue");
  setFileList($yValue, ToolPage.getFeatureNameList()); 
}

const clickEvent = async (event, id, targetClass) => {
  if (id === "create") {
    const data = {
      modelName: document.querySelector(".modelName").value,
      model: document.querySelector(".technique").options[document.querySelector(".technique").selectedIndex]?.value,
      trainSize: document.querySelector(".trainSize").value,
      yValue: document.querySelector(".yValue").options[document.querySelector(".yValue").selectedIndex]?.value,
      xValue: JSON.stringify(ToolPage.setCheckedVarList()),
    }
    console.log(data);
    const response = await API(`/analytics/${fileName}/model/`, "post", data);
  }

  if (
    id === "fileUpload" ||
    id === "movePage"
  ) {
    await handleClickMovePage();
  }

  if (id === "fileUploadBtn") {
    $uploadDialog.style.display = "flex";
    $uploadDialog.showModal();
  }

  if (id === "closeUploadPopup") {
    $uploadDialog.style.display = "none";
    $uploadDialog.close();
  }

}


window.addEventListener("click", (event) => {
	const targetId = event.target.id;
	const targetClass= event.target.classList;

	if (targetId !== "") {
		clickEvent(event, targetId, targetClass);
	}
})
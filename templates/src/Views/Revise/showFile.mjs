import API from "/templates/src/Utils/API.mjs";
import Excel from "/templates/src/Model/Excel.mjs";

const fileName = JSON.parse(localStorage.getItem("fileTitle"));

const setFileData = async () => {
	const response = await API(`/files/${fileName}/data/`, "get");
	const $spreadSheetDIV = document.querySelector("#spreadSheetDIV");
	$spreadSheetDIV.innerHTML = "";
	showFile(response.data, $spreadSheetDIV);
}

const showFile = (data, element) => {
	new Excel(data, element);
}

(async function () {
  // 파일 불러오는 API
	await setFileData();
}());
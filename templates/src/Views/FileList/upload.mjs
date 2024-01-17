import API from "/templates/src/Utils/API.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";

const $uploadContainer = document.querySelector("#uploadContainer");
const $upload = document.querySelector("#upload");
const $fileUpload = document.querySelector("#fileUpload");
const $closeUploadPopup = document.querySelector("#closeUploadPopup");

const $fileUploadDrag = document.querySelector("#fileUploadDrag");
const $fileUploadInput = document.querySelector("#fileUploadInput");
const $fileIcon = document.querySelector("#fileIcon");
const $fileName = document.querySelector("#fileName");

// 파일 업로드 버튼 팝업창 관리 함수
$upload.addEventListener("click", () => {
	$uploadContainer.showModal();
})

$closeUploadPopup.addEventListener("click", () => {
  $uploadContainer.close();
});

let selectedFile;
let sheetData;

const fileSetting = () => {
  $fileIcon.style.display = "none";
  // $fileUploadDrag.style.display = "none";
  $fileName.value = selectedFile.name.replace(/\s/g, "_");
}

const readFileContent = (file) => {
  const reader = new FileReader();
  Loading.StartLoading();

  reader.onload = function (event) {
    const fileContent =  event.target.result;
    const workbook = XLSX.read(fileContent, { type: "binary" });
    sheetData = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[workbook.SheetNames[0]]);
    console.log("sheetData", sheetData);
    Loading.CloseLoading();
  };

  reader.onerror = function (event) {
    console.error(event.target.error);
    Loading.CloseLoading();
  };

  reader.readAsBinaryString(file);
}

$fileUploadInput.addEventListener("change", (event) => {
  selectedFile = event.target.files[0];
  if (!selectedFile) {
    return;
  }
  showFile();
});

$fileUploadDrag.addEventListener("dragenter", (event) => {
  event.preventDefault();
  $fileUploadDrag.style.backgroundColor = "#999";
});

$fileUploadDrag.addEventListener("dragleave", (event) => {
  event.preventDefault();
  $fileUploadDrag.style.backgroundColor = "";
});

$fileUploadDrag.addEventListener("drop", (event) => {
  event.preventDefault();
  selectedFile = event.dataTransfer.files[0];
  showFile();
});

const showFile = () => {
  fileSetting();
  readFileContent(selectedFile);
}

// 파일 업로드
const uploadFile = async () => {
	const data = {
		fileName: $fileName.value,
		fileData: JSON.stringify(sheetData),
	};
	const response = await API("", "" , data);
}

// 업로드 하고 다시 페이지 호출
// $fileUpload.addEventListener("click", uploadFile);


// 파일 업로드 함수
